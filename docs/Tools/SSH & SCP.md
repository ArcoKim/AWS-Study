# SSH & SCP
## Password & Port Change
``` bash
sed -i 's/#Port 22/Port 37722/' /etc/ssh/sshd_config
sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
systemctl restart sshd
echo 'Semye0ng2@23$$$' | passwd --stdin ec2-user
```
## SSH Command Example
``` bash
ssh ec2-user@13.125.158.16 -i skills-key.pem -p 22
```
## SSH Tunneling Example
``` bash
ssh -L 8080:127.0.0.1:8080 ec2-user@43.202.41.246 -i key.pem
```
## SCP Command Example
``` bash
scp -r -P 4272 -i skills-key.pem stress ec2-user@13.125.158.16:/home/ec2-user/stress
```
## VSCode Config
```
Host Bastion
  HostName <PUBLIC_IP>
  User ec2-user
  Port 22
  IdentityFile <KEY_PATH>
```