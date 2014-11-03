Composite Demo
==============

A tool that can be used to build the [Composite](https://github.com/wieden-kennedy/composite) service as a set of linked Docker containers.

License
-------
This repository and its code are licensed under the BSD 3-Clause license, which can be found `here <https://github.com/wieden-kennedy/composite-docker/blob/master/LICENSE>`_.

Overview
--------
Designed to run on an Ubuntu virutal guest, **composite-demo** uses Fabric along with Docker to create three separate, linked, Docker containers to run the Composite service, and a fourth container that runs the client demo application. When building Composite with **composite-demo** you will end up with four Docker containers (where ENV is your desired environment):

* **ENV/couchdb** - a CouchDB docker container
* **ENV/rabbitmq** - a RabbitMQ docker container
* **ENV/composite** - a Tomcat container running the Composite web application
* **ENV/client** - an NGINX container running the Composite client demo

The four containers will mirror their respective service ports back to the guest on which they are running, so you can then connect to those services from your local machine.

Requirements
------------

* Ubuntu 12.04 Precise virtual guest
* Linux Kernel 3.8 installed on guest
* Docker installed on guest
* pip & fabric installed on guest

Quickstart
----------
The easiest way to check out Composite in action is to download and run our Vagrant demo.
To do this, you will want to have both of the following tools installed:

* `Vagrant <http://www.vagrantup.com>`_
* `Virtual Box <http://www.virtualbox.org>`_

::

    $ wget https://compositeframework.io/static/demo/Vagrantfile
    $ vagrant up && vagrant ssh

This will download the Vagrant box, spin it up, and ssh into it. Once inside, you'll just need to run one more command
to get some docker containers spun up and mapped back to your localhost.

::

    $ sudo composite-demo

This command will import and spin up four Docker containers. While this is working, go grab a beverage of your choice.
The imports can take a few minutes, especially if you're working on a slower connection.

For each container listed, port mapping goes from container to the Vagrant host to your local machine:

+----------------+---------------+-------------+
| Container      | Service       | Mapped port |
+================+===============+=============+
| Composite      | Tomcat        | 8080        |
+----------------+---------------+-------------+
| Database       | CouchDB       | 5984        |
+----------------+---------------+-------------+
| Message Broker | RabbitMQ      | 61613       |
+----------------+---------------+-------------+
| Web Client     | NGINX         | 5000        |
+----------------+---------------+-------------+

Once these containers are up, you should be able to hit your system's address on port 5000 with a mobile device or a
browser in emulation mode to get going. Once you hit localhost:5000 with three devices or browsers in emulation mode, the demo will start.

The demo is our favorite internet cat, Nyancat, streaming across the screens of the paired devices. Dragging
Nyancat will move it up and down across the screens. Totally simple demo, but shows you that the device screens are linked
via Composite messaging.

Documentation
-------------
The full documentation on how to get up-and-running with the demo can be found in the `Composite Demo Reference <http://composite-framework.readthedocs.org/en/latest/doc_sections/demo-fabric.html>`_.
