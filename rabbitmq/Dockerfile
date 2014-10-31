# Composite RabbitMQ
#
# VERSION   0.0.1

FROM        local/base
MAINTAINER  Keith Hamilton <keith.hamilton@wk.com>

# ensure vagrant password is set
RUN vagrant:vagrant | chpasswd

# Download Puppet manifest for RabbitMQ
RUN puppet module install puppetlabs-rabbitmq

# Install RabbitMQ
RUN puppet apply -e "class {'rabbitmq': service_manage => false, port => '5672', config_stomp => true, stomp_port => '61613',node_ip_address => '0.0.0.0'}"
RUN rabbitmq-plugins enable rabbitmq_stomp

# Add supervisord configuration
#RUN mkdir -p /var/log/supervisor
#ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD rabbitmq.config /etc/rabbitmq/rabbitmq.config
ADD run_rabbit /usr/local/bin/run_rabbit

RUN chmod +x /usr/local/bin/run_rabbit

# Expose RabbitMQ port and set command to run rabbit on container start
EXPOSE 22 61613 5672
CMD ["run_rabbit"]
