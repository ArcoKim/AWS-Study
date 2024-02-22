# Topic
## Create
``` bash
kafka-topics.sh \
--bootstrap-server $MSK_BOOTSTRAP_ADDRESS \
--command-config /tmp/client_iam.properties \
--create --topic workshop-test \
--partitions 5  \
--replication-factor 3
```
## List
``` bash
kafka-topics.sh \
--bootstrap-server $MSK_BOOTSTRAP_ADDRESS \
--command-config /tmp/client_iam.properties \
--list
```
## Describe
``` bash
kafka-topics.sh \
--bootstrap-server $MSK_BOOTSTRAP_ADDRESS \
--command-config /tmp/client_iam.properties \
--describe --topic workshop-test
```
## Producer Test
``` bash
kafka-console-producer.sh \
--bootstrap-server $MSK_BOOTSTRAP_ADDRESS \
--producer.config /tmp/client_iam.properties \
--topic workshop-test
```
## Consumer Test
``` bash
kafka-console-consumer.sh \
--bootstrap-server $MSK_BOOTSTRAP_ADDRESS \
--consumer.config /tmp/client_iam.properties \
--topic workshop-test
```
## Delete
``` bash
kafka-topics.sh \
--bootstrap-server $MSK_BOOTSTRAP_ADDRESS \
--command-config /tmp/client_iam.properties \
--delete --topic workshop-test
```