# Redis
## Install
### Linux
``` bash
sudo yum -y install openssl-devel gcc
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make distclean
make redis-cli BUILD_TLS=yes
sudo install -m 755 src/redis-cli /usr/local/bin/
```

## Connect
Please note that you need to set the ENDPOINT_URL variable.
``` bash
redis-cli -h $ENDPOINT_URL --tls -p 6379
```