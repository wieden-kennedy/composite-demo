# Composite Server
#
# VERSION   0.0.1

FROM        local/base
MAINTAINER  Keith Hamilton <keith.hamilton@wk.com>

# Install git
RUN apt-get install -y git

# Install Maven
RUN add-apt-repository "deb http://ppa.launchpad.net/natecarlson/maven3/ubuntu precise main"
RUN apt-get update && apt-get -y --force-yes install maven3
RUN ln -s /usr/share/maven3/bin/mvn /usr/bin/mvn

# Install Tomcat
RUN wget -O /tmp/tomcat7.tar.gz http://archive.apache.org/dist/tomcat/tomcat-7/v7.0.54/bin/apache-tomcat-7.0.54.tar.gz
RUN (cd /opt && tar zxf /tmp/tomcat7.tar.gz)
RUN (mv /opt/apache-tomcat* /opt/tomcat)
RUN (rm /opt/tomcat/bin/*.bat)

# Install Oracle Java 7
RUN add-apt-repository ppa:webupd8team/java
RUN apt-get update
RUN echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN apt-get -y install oracle-java7-installer && apt-get clean
RUN update-alternatives --display java
RUN echo "JAVA_HOME=/usr/lib/jvm/java-7-oracle" >> /etc/environment

# Add tomcat start script
ADD run_server /usr/local/bin/run_server
RUN chmod +x /usr/local/bin/run_server

# Update path
RUN echo "PATH=$PATH:/opt/tomcat/bin:/usr/bin" >> /home/vagrant/.bashrc

EXPOSE 22 8080
CMD ["run_server"]

