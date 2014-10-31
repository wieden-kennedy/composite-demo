
FROM        local/base
MAINTAINER  Keith Hamilton <keith.hamilton@wk.com>

# Install Nginx
RUN add-apt-repository -y ppa:nginx/stable
RUN apt-get update
RUN apt-get install -y git nginx

# Upload config file
ADD nginx.conf /etc/nginx/nginx.conf

# Upload run file
ADD run_client /usr/local/bin/run_client
RUN chmod +x /usr/local/bin/run_client

# Define mountable directories.
VOLUME ["/data", "/etc/nginx/sites-enabled", "/var/log/nginx"]

# Define working directory.
WORKDIR /etc/nginx

# Expose ports.
EXPOSE 5000

CMD ["run_client"]
