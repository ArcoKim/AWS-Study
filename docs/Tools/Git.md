# Git
Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.
``` bash
USER_NAME="<user_name>"
USER_EMAIL="<user_email>"

sudo yum install -y git

git config --global credential.helper '!aws codecommit credential-helper $@'
git config --global credential.UseHttpPath true

git config --global user.name $USER_NAME
git config --global user.email $USER_EMAIL
```