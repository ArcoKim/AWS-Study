# Dockerfile
## Golang
### Single

- Alpine Linux
``` Dockerfile
FROM public.ecr.aws/docker/library/alpine

WORKDIR /app

COPY main .

RUN apk --no-cache add curl

RUN adduser -D app \
    && chown -R app:app /app \
    && chmod 755 /app
USER app

CMD ["./main"]
```

- Amazon Linux
``` Dockerfile
FROM public.ecr.aws/amazonlinux/amazonlinux:2023

WORKDIR /app

COPY main .

RUN yum install -y shadow-utils

RUN useradd app \
    && chown -R app:app /app \
    && chmod 755 /app
USER app

CMD ["./main"]
```
### Multi
``` Dockerfile
FROM public.ecr.aws/docker/library/golang:alpine AS builder

WORKDIR /build

COPY main.go ./

RUN go mod init main && go mod tidy

RUN go build -o main .

FROM public.ecr.aws/docker/library/alpine

WORKDIR /app

COPY --from=builder /build/main .

RUN apk --no-cache add curl

RUN adduser -D app \
    && chown -R app:app /app \
    && chmod 755 /app
USER app

CMD ["./main"]
```
## Python
``` Dockerfile
FROM public.ecr.aws/docker/library/python:3.9-alpine

WORKDIR /app
COPY app.py requirements.txt ./

RUN apk --no-cache add curl
RUN pip3 install -r requirements.txt

RUN adduser -D app \
    && chown -R app:app /app \
    && chmod 755 /app
USER app

CMD ["python3", "app.py"]
```

## Java
### Single
``` Dockerfile
FROM public.ecr.aws/docker/library/amazoncorretto:17-alpine

WORKDIR /app

RUN apk --no-cache add curl

COPY build/libs/*.jar app.jar

RUN adduser -D app \
    && chown -R app:app /app \
    && chmod 755 /app
USER app

CMD ["java","-jar","./app.jar"]
```
### Multi
``` Dockerfile
FROM public.ecr.aws/docker/library/gradle:jdk17-alpine AS builder

WORKDIR /

COPY *.gradle .
COPY src src

RUN gradle clean build -x test --no-daemon

FROM public.ecr.aws/docker/library/amazoncorretto:17-alpine

WORKDIR /app

RUN apk --no-cache add curl

COPY --from=builder /build/libs/*.jar app.jar

RUN adduser -D app \
    && chown -R app:app /app \
    && chmod 755 /app
USER app

CMD ["java","-jar","./app.jar"]
```