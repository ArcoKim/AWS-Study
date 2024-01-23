# Stress Application
## Stress
### Install

- Amazon Linux 2023
``` bash
sudo yum install -y stress
```
- Amazon Linux 2
``` bash
sudo amazon-linux-extras install epel -y
sudo yum install stress -y
```

### Start
``` bash
stress -c 1 # <number of cores>
```

## Locust
### Install
``` bash
pip install locust
```
### Write Python File
``` python title="locustfile.py"
from locust import task, FastHttpUser

class MyUser(FastHttpUser):
    @task
    def index(self):
        self.client.get("/v1/match", params={"token":"cccccccc"})
```
### Start
``` bash
locust -f locustfile.py
```