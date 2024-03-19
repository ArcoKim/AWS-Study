# Memcached
## Install Telnet
``` bash
sudo yum install -y telnet
```
## Connect
``` bash
telnet $ENDPOINT_URL 11211  # without TLS
openssl s_client -quiet -crlf -connect $ENDPOINT_URL:11211  # with TLS
```
## Usage Example
``` bash
set a 0 10 5     # Set key "a" with 10 seconds expiration and 5 byte value
hello            # Set value as "hello"

get a            # Get value for key "a"
```