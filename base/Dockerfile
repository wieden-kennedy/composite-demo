# Composite Base
#
# VERSION   0.0.1

FROM        ubuntu:14.04
MAINTAINER  Keith Hamilton <keith.hamilton@wk.com>

RUN apt-get update
RUN apt-get clean

# Install base tools
RUN apt-get -y install vim curl wget openssh-server python-pip python-dev build-essential openssl software-properties-common python-software-properties

# Ensure SSHD running
RUN mkdir /var/run/sshd

# create admin user
RUN /usr/sbin/useradd vagrant
RUN echo vagrant:vagrant | chpasswd
RUN touch /etc/sudoers.tmp
RUN echo "vagrant ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN rm /etc/sudoers.tmp
RUN mkdir /home/vagrant

# Install puppet
RUN wget https://apt.puppetlabs.com/puppetlabs-release-precise.deb -O /tmp/puppet-labs-release-precise.deb
RUN dpkg -i /tmp/puppet-labs-release-precise.deb
RUN apt-get -y update && apt-get -y install puppet

# Install pip
RUN pip install --upgrade pip
RUN PATH=$PATH:/usr/local/bin

# Install fabric
RUN pip install fabric

# Update and Upgrade system
RUN apt-get update && apt-get -y upgrade

