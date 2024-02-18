# Linux Secure
## SSH Connect
1. Modify /etc/pam.d/system-auth, /etc/pam.d/password-auth
2. Example : After 5 failed attempts, lock for 120 seconds
``` bash
# Add each to the second line
auth        required      pam_tally2.so deny=5 unlock_time=120
account     required      pam_tally2.so
```