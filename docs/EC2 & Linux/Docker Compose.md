# Docker Compose

## Install
``` bash
mkdir -p /usr/local/lib/docker/cli-plugins/
curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-$(uname -m)" -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
```

## Template
``` yaml title="compose.yml"
services:
  employee:
    build: employee
    restart: always
    environment:
      MYSQL_USER: admin
      MYSQL_PASSWORD: admin1234!
      MYSQL_HOST: apdev-rds-instance.cacgnhyyutg6.ap-northeast-2.rds.amazonaws.com
      MYSQL_PORT: 3306
      MYSQL_DBNAME: dev
    ports:
      - '8080:8080'
    logging:
      driver: awslogs
      options:
        awslogs-region: ap-northeast-2
        awslogs-group: /app/employee
        awslogs-stream: employee
```