# Redis
## Install
### Amazon Linux 2023
``` bash
sudo yum install -y redis6
redis6-cli --version
```
### Amazon Linux 2
``` bash
sudo yum -y install openssl-devel gcc
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make distclean
make redis-cli BUILD_TLS=yes
sudo install -m 755 src/redis-cli /usr/local/bin/
redis-cli --version
```
## Connect
Please note that you need to set the ENDPOINT_URL variable.
``` bash
redis-cli -h $ENDPOINT_URL --tls -p 6379 -c
```
## Usage
``` bash
set a "hello" EX 5
get a
del a
```