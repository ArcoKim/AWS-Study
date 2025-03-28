# Linux Secure
## SSH Connect
- Modify /etc/pam.d/system-auth, /etc/pam.d/password-auth
- Example : After 5 failed attempts, lock for 120 seconds
``` bash
# Add to the "auth" section second line
auth        required      pam_faillock.so preauth silent audit deny=5 unlock_time=120 fail_interval=300

# Add to the "auth" section fourth line
auth        [default=die] pam_faillock.so authfail audit deny=5 unlock_time=120

# Add to the "account" section second line
account     required      pam_faillock.so
```