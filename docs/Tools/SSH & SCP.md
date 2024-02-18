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
## SCP Command Example
``` bash
scp -r -P 4272 -i skills-key.pem stress ec2-user@13.125.158.16:/home/ec2-user/stress
```