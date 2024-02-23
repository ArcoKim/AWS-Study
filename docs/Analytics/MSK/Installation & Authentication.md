# Installation & Authentication
## Install Kafka Client
``` bash
wget https://downloads.apache.org/kafka/3.6.0/kafka_2.12-3.6.0.tgz -O kafka.tgz
tar zxvf kafka.tgz
mv kafka_2.12-3.6.0 kafka
echo 'PATH=$PATH:$HOME/kafka/bin' >> ~/.bash_profile
. ~/.bash_profile

kafka-topics.sh --version
```
## Install UI For Apache Kafka
``` bash
docker run -d \
-p 8080:8080  \
-v /home/ec2-user/environment/ui_for_apach_kafka:/etc/ui_for_apach_kafka  \
-e DYNAMIC_CONFIG_ENABLED=true  \
provectuslabs/kafka-ui
```
## IAM Authentication
1. Set the MSK_BOOTSTRAP_ADDRESS variable.
``` bash
echo "export MSK_BOOTSTRAP_ADDRESS=<MSK_BOOTSTRAP_ADDRESS>" >> ~/.bash_profile
. ~/.bash_profile
```
2. File Settings
``` bash
cd ~/kafka/libs
wget https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.1/aws-msk-iam-auth-1.1.1-all.jar

echo -n "security.protocol=SASL_SSL
sasl.mechanism=AWS_MSK_IAM 
sasl.jaas.config=software.amazon.msk.auth.iam.IAMLoginModule required; 
sasl.client.callback.handler.class=software.amazon.msk.auth.iam.IAMClientCallbackHandler" > /tmp/client_iam.properties
```
3. Example of topic list search.
``` bash
kafka-topics.sh \
--bootstrap-server $MSK_BOOTSTRAP_ADDRESS \
--command-config /tmp/client_iam.properties \
--list
```
## SASL/SCRAM Authentication
1. Creates an “Other type of secret” without using the default KMS key.
``` json title="Key/value Example"
{
  "username": "admin",
  "password": "Admin12#$"
}
```
2. The secret's name must start with "AmazonMSK_".
3. Associate secrets to MSK Cluster.
4. File / Variable Settings
``` bash
echo -n "KafkaClient {
   org.apache.kafka.common.security.scram.ScramLoginModule required
   username=\"admin\"
   password=\"Admin12#$\";
};" > /tmp/users_jaas_admin.conf

export KAFKA_OPTS=-Djava.security.auth.login.config=/tmp/users_jaas_admin.conf
cp /usr/lib/jvm/java-17-amazon-corretto/lib/security/cacerts /tmp/kafka.client.truststore.jks

echo -n "security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512
ssl.truststore.location=/tmp/kafka.client.truststore.jks" > /tmp/client_sasl.properties
```
5. Set the SASL_MSK_BOOTSTRAP_ADDRESS.
``` bash
echo "export SASL_MSK_BOOTSTRAP_ADDRESS=<SASL_MSK_BOOTSTRAP_ADDRESS>" >> ~/.bash_profile
. ~/.bash_profile
```
6. Example of topic list search.
``` bash
kafka-topics.sh \
--bootstrap-server $SASL_MSK_BOOTSTRAP_ADDRESS \
--command-config /tmp/client_sasl.properties \
--list
```
### ACL
- Grant full permissions to cluster, group, and topic to the admin account.
``` bash
kafka-acls.sh  \
--bootstrap-server $SASL_MSK_BOOTSTRAP_ADDRESS \
--command-config /tmp/client_sasl.properties \
--add --allow-principal "User:admin" \
--operation All \
--group=* \
--topic=* \
--cluster=* 
```
- Grant only Read permission to the workshop-acl topic to the test account.
``` bash
kafka-acls.sh  \
--bootstrap-server $SASL_MSK_BOOTSTRAP_ADDRESS \
--command-config /tmp/client_sasl.properties \
--add --allow-principal "User:test" \
--operation Read \
--group=* \
--topic workshop-acl
```
- Current Permission Check
``` bash
kafka-acls.sh \
--bootstrap-server $SASL_MSK_BOOTSTRAP_ADDRESS \
--command-config /tmp/client_sasl.properties \
--list
```