composite-demo
==============

A tool that can be used to build the [Composite](https://github.com/wieden-kennedy/composite) service as a set of linked Docker containers.

#Contents  
* [License](#license)  
* [Overview](#overview)  
* [Requirements](#requirements)  
   * [Running with composite-vagrant](#running-with-composite-vagrant)  
* [Building & Running Composite on Docker](#building-running-composite-on-docker)  
   * [Defaults](#defaults)  
   * [Optional configuration settings](#optional-configuration-settings)  
* [Port Mirroring](#port-mirroring)  
* [Fabric Commands](#fabric-commands)  
* [FAQ](#faq)

##License
This repository and its code are licensed under the BSD 3-Clause license, which can be found [here](https://github.com/wieden-kennedy/composite-docker/blob/master/LICENSE).

##Overview
Designed to run on an Ubuntu virutal guest, **composite-demo** uses Fabric along with Docker to create three separate, linked, Docker containers to run the Composite service. When building Composite with **composite-demo** you will end up with four Docker containers (where ENV is your desired environment):  
* **ENV/couchdb** - a CouchDB docker container
* **ENV/rabbitmq** - a RabbitMQ docker container
* **ENV/composite** - a Tomcat container running the Composite web application
* **ENV/client** - an NGINX container running the Composite client demo

The four containers will mirror their respective service ports back to the guest on which they are running, so you can then connect to those services from your local machine.  

##Requirements  
* Ubuntu 12.04 Precise virtual guest  
* Linux Kernel 3.8 installed on guest  
* Docker installed on guest  
* pip & fabric installed on guest  

##Documentation
The full documentation on how to get up-and-running with the demo can be found in the [Composite Demo Reference](http://composite-framework.readthedocs.org/en/latest/doc_sections/demo-fabric.html).
