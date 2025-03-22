# Client VPN
## Download
- AWS Client VPN
    - https://aws.amazon.com/ko/vpn/client-vpn-download/
- EasyRSA
    - https://github.com/OpenVPN/easy-rsa/releases

## Certificate
``` Powershell
.\EasyRSA-Start.bat

./easyrsa init-pki
./easyrsa build-ca nopass
./easyrsa --san=DNS:server build-server-full server.com nopass
./easyrsa build-client-full client1.domain.tld nopass

exit
```

## ACM
``` bash
aws acm import-certificate --certificate fileb://pki/issued/server.com.crt --private-key fileb://pki/private/server.com.key --certificate-chain fileb://pki/ca.crt
aws acm import-certificate --certificate fileb://pki/issued/client1.domain.tld.crt --private-key fileb://pki/private/client1.domain.tld.key --certificate-chain fileb://pki/ca.crt
```