#!/usr/bin/python

from re import search

from fabric.api import env, lcd, local, settings, sudo
from fabric.colors import white as _white

'''
ENV/GLOBALS
'''
env.environment = 'local'
env.user = 'vagrant'
env.password = 'vagrant'

BUILD_CONFIRM = False

'''
CONTAINER DEFS
'''

CONTAINERS = [
    {
        'name': 'base',
        'role': 'base',
        'ports': None,
        'startup_command': None,
        'type': 'base'
    },
    {
        'name': 'couchdb',
        'role': 'database',
        'ports': ['5984'],
        'mirrored_host_volume': '/usr/local/var/lib/couchdb',
        'mirrored_guest_volume': '/usr/local/var/lib/couchdb',
        'startup_command': 'run_couchdb',
        'type': 'service',
        's3_path': 'https://s3.amazonaws.com/compositeframework.io/static/demo/docker_assets/couchdb.tar'
    },
    {
        'name': 'rabbitmq',
        'role': 'broker',
        'ports': ['61613', '5672'],
        'mirrored_host_volume': '/usr/local/var/log/rabbitmq',
        'mirrored_guest_volume': '/usr/local/var/log/rabbitmq',
        'startup_command': 'run_rabbit',
        'type': 'service',
        's3_path': 'https://s3.amazonaws.com/compositeframework.io/static/demo/docker_assets/rabbitmq.tar'
    },
    {
        'name': 'client',
        'role': 'client',
        'ports': ['5000'],
        'mirrored_host_volume': '/var/log/nginx',
        'mirrored_guest_volume': '/var/log/nginx',
        'startup_command': 'run_client',
        'type': 'client',
        's3_path': 'https://s3.amazonaws.com/compositeframework.io/static/demo/docker_assets/client.tar'
    },
    {
        'name': 'composite',
        'role': 'server',
        'ports': ['8080'],
        'mirrored_host_volume': '/opt/tomcat/logs',
        'mirrored_guest_volume': '/opt/tomcat/logs',
        'startup_command': 'run_server',
        'type': 'server',
        's3_path': 'https://s3.amazonaws.com/compositeframework.io/static/demo/docker_assets/composite.tar'
    }
]

'''
CONTAINER CLASS
A class to model the Docker container and provide us with some functionality such as run, commit, kill
'''


class Container:
    def __init__(self, environment, container):
        self.name = container['name']
        self.role = container['role']
        self.container_name = '%s/%s' % (environment.lower(), container['name'])
        self.service_ports = container['ports']
        self.startup_command = container['startup_command']
        self.ssh_command = '/usr/sbin/sshd -D'
        self.linked_containers = []
        self.container_id = None
        self.host_ip = None

        if 'setup_tasks' in container:
            self.setup_tasks = container['setup_tasks']

        if 'mirrored_host_volume' in container:
            self.mirrored_host_volume = container['mirrored_host_volume']

        if 'mirrored_guest_volume' in container:
            self.mirrored_guest_volume = container['mirrored_guest_volume']

        if 's3_path' in container:
            self.s3_path = container['s3_path']

    def build(self):
        """
        builds Docker container for the Container object on the local machine
        using the Dockerfile located at ./self.container_name/Dockerfile
        """
        with lcd('./%s' % self.name):
            local('sudo docker build -q -t %s .' % self.container_name)

    def get_info(self):
        """
        runs the Container in daemon mode with the Container's ssh command so that it can be sshed into.
        using the returned container id from the docker run command, the host_ip address is captured
        and stored in the Container object.

        This is helpful since each time a container is launched it may have a different IP address, so at
        run time we won't need to worry about what the IP is for a Container, we just need to get its info
        """
        self.container_id = local('sudo docker run -d -name %s %s %s' % (self.name,
                                                                         self.container_name,
                                                                         self.ssh_command), capture=True)

        self.host_ip = local("sudo docker inspect -format '{{ .NetworkSettings.IPAddress }}' %s" % self.container_id,
                             capture=True)

    def kill(self):
        """
        kills the Container object's Docker process
        """
        if not self.container_id:
            self.container_id = local("sudo docker ps -a | grep %s | awk '{print $1}'" % self.container_name,
                                      capture=True)
        local('sudo docker kill %s' % self.container_id)
        self.container_id = None

    def commit(self):
        """
        commits the Container object in Docker after the Container has been terminated
        """
        local('sudo docker commit %s %s' % (self.container_id, self.container_name))

    def run(self):
        """
        runs the Container in daemon mode using its startup_command. Also mirrors the Container's service
        port back to the host machine, so that it can be reached
        """
        mirrored_ports = ''
        for port in self.service_ports:
            mirrored_ports += '-p 0.0.0.0:%s:%s ' % (port, port)
        mirrored_ports = mirrored_ports[:-1]

        if 'mirrored_host_volume' in self.__dict__ and 'mirrored_guest_volume' in self.__dict__:
            self.container_id = local('sudo docker run -d --name %s -v %s:%s:rw %s %s %s' %
                                      (self.name,
                                       self.mirrored_guest_volume,
                                       self.mirrored_guest_volume,
                                       mirrored_ports,
                                       self.container_name,
                                       self.startup_command), capture=True)
        else:
            self.container_id = local('sudo docker run -d --name %s %s %s %s' % (self.name,
                                                                                 mirrored_ports,
                                                                                 self.container_name,
                                                                                 self.startup_command), capture=True)

    def run_linked(self):
        """
        runs the Container in linked mode, that is, it executes `docker run` and appends the needed flags
        to link the Containers linked_containers to it when it runs, so those Containers can interact
        with this Container's service
        """
        mirrored_ports = ''
        for port in self.service_ports:
            mirrored_ports += '-p 0.0.0.0:%s:%s ' % (port, port)
        mirrored_ports = mirrored_ports[:-1]

        link_string = ''
        for c in self.linked_containers:
            link_string += '--link %s:%s ' % (c.name, c.role)

        if 'mirrored_host_volume' in self.__dict__ and 'mirrored_guest_volume' in self.__dict__:
            local('sudo docker run -d %s -v %s:%s:rw --name %s %s %s %s' %
                  (link_string[:-1],
                   self.mirrored_host_volume,
                   self.mirrored_guest_volume,
                   self.name, mirrored_ports,
                   self.container_name,
                   self.startup_command))
        else:
            local('sudo docker run -d %s --name %s %s %s %s' %
                  (link_string[:-1], self.name, mirrored_ports, self.container_name, self.startup_command))


'''
ENV/PREFLIGHT
'''


def environ(e):
    """
    defines environment, defaults to local
    :param e: the name of the environment
    """
    if e in ['prod', 'production']:
        env.environment = 'prod'
    elif e in ['test', 'staging']:
        env.environment = 'test'
    elif e in ['dev', 'development']:
        env.environment = 'dev'
    else:
        env.environment = 'local'


'''
BUILD CONTAINERS
'''


def build_container(c, environment=env.environment):
    """
    build_container converts a container dict, c, into a Container object, then executes its build command
    to manufacture the Docker container from the appropriate Dockerfile.

    Additionally, if a set of setup_tasks were defined in the dict, the new Docker container will be
    started in info (sshd) mode and those tasks will be executed.

    :param c: the container object to build
    :param environment: the environment in which to build the container, defaults to 'local'
    """
    container = Container(environment, c)
    container.build()

    # if the container has one or more setup tasks, run the container in ssh mode and execute the setup task
    if 'setup_tasks' in c:
        container.get_info()
        with settings(host_string=container.host_ip, user=env.user, password=env.password):
            local('sleep 5')
            for t in container.setup_tasks:
                sudo(t, pty=False)
        container.kill()
        container.commit()


'''
IMPORT
'''


def import_container(container_name=None):
    """
    import a container by name. If no container name is specified, import all containers
    :param container_name: (optional) the container to import
    """
    import_containers = [x for x in CONTAINERS if x['name'] != 'base']
    
    if container_name:
        import_containers = [x for x in import_containers if x['name'] == container_name]

    for c in import_containers:
        container = Container(env.environment, c)
        print(_white("==> Importing %s container from S3" % container.name))
        local('sudo curl %s | sudo docker import - %s/%s' % (container.s3_path,
                                                             env.environment.lower(),
                                                             container.name))


'''
BUILD & RUN
'''


def build(container_name=None):
    """
    builds all containers sequentially, beginning with the base container,
    from which all other containers derive.

    if container_name is defined, will only build that container
    :param container_name: (optional) container name to build
    """
    killall_containers()

    build_containers = CONTAINERS
    current_images = local('sudo docker images', capture=True)
    base_container_exists = 'base' in current_images
    

    if container_name:
        build_containers = [x for x in build_containers if x['name'] == container_name]
        if container_name != 'base' and not base_container_exists:
            build(container_name='base')

    # build the service and composite containers
    for c in build_containers:
        build_container(c, env.environment)


def run_services():
    """
    runs couchdb and rabbitmq containers to be used as a service for local development purposes.
    """

    killall_containers()
    for c in [x for x in CONTAINERS if x['type'] == 'service']:
        cc = Container(env.environment.lower(), c)
        cc.run()

def run():
    """
    runs all containers, linking the following:
    local/couchdb, local/rabbitmq   -> local/composite
    local/composite                 -> local/client
    """
    killall_containers()

    # create the CompositeContainer object
    composite_container_def = [x for x in CONTAINERS if x['type'] == 'server'][0]
    composite = Container(env.environment.lower(), composite_container_def)
    # create the ClientContainer object
    client_container_def = [x for x in CONTAINERS if x['type'] == 'client'][0]
    client = Container(env.environment.lower(), client_container_def)

    # for the other containers, create Container objects, link them to the CompositeContainer object, and run them
    for c in [x for x in CONTAINERS if x['type'] == 'service']:
        cc = Container(env.environment.lower(), c)
        composite.linked_containers.append(cc)
        cc.run()

    # run the composite container in linked mode (linked to couchdb and rabbitmq)
    composite.run_linked()

    # finally, run the client container in linked mode (linked to composite)
    client.linked_containers.append(composite)
    client.run_linked()

'''
UTIL
'''


def killall_containers():
    """
    kills all running Docker containers
    """
    containers = local("sudo docker ps -a | awk '{print $NF}'", capture=True).replace('\n', ',').split(',')[1:]
    for c in containers:
        # don't try to kill container references that are linked containers
        # example: [foo, foo/bar, bar] <-- we only want to kill foo and bar not foo/bar
        if not search('/', c):
            local("sudo docker kill %s" % c)
            local("sudo docker rm %s" % c)


def delete_image(container_name=None):
    """
    deletes a Docker container by name
    :param container_name: the name of the docker container, e.g., local/couchdb
    """
    if not container_name:
        image_ids = local("sudo docker images | awk '{print $3}'", capture=True).replace('\n', ',').split(',')[1:]
        for image in image_ids:
            local('sudo docker rmi -f %s' % image)
    else:
        image_id = local("sudo docker images | grep %s | awk '{print $3}'" % container_name, capture=True)
        local('sudo docker rmi -f %s' % image_id)
