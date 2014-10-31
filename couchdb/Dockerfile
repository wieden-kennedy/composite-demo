# Composite Couchdb
#
# VERSION   0.0.1

FROM        local/base
MAINTAINER  Keith Hamilton <keith.hamilton@wk.com>

RUN apt-get -y install couchdb

ADD default.ini /etc/couchdb/default.ini
ADD local.ini /etc/couchdb/local.ini
ADD run_couchdb /usr/local/bin/run_couchdb
ADD couchdb_setup.py /usr/local/sbin/couchdb_setup.py

RUN mkdir /var/run/couchdb
RUN chown -R couchdb:couchdb /var/run/couchdb
RUN chmod +x /usr/local/bin/run_couchdb

# Expose ssh port and set supervisord to run on container launch
EXPOSE 5984
CMD ["run_couchdb"]
