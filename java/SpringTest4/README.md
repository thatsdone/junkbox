# SpringTest4

This is a simple example (exercise) Spring Boot progoram to show how to:

* Use Kafka Client from a Spring Boot program
* Use BlockingQueue to share a FIFO queue across multiple threads safely
  * LinkedListBlockingQueue is used as the actual implementation

## Usage

0. Prerequisite
   * Install JDK (I used openjdk-21-jdk on Ubuntu 24.04)
   * Install maven
   * Set up a kafka cluster
     * Note that kafka bootstrap server hostname/IP must be resolvable.
1. Build
   * `mvn package`
2. Run
   * Edit environment variables in run.sh
   * `bash run.sh`

Note that this program refers the following environment variables as you can see in run.sh

* KAFKA_SERVER
  * Kafka bootstrap server address, 192.168.0.1:9092 for example.
* KAFKA_TOPIC
  * Kafka topic, test-topic for example.
* KAFKA_GROUP
  * Kafka Consumer group, mygroup for example.

By default, this program listens on tcp 18081.
You can change it by application.properties file.

This program tries to deserialize both key and value of Kafka consumer
records as String. Send some message in string to the kafka topic.

After retrieving messages from the kafka topic, this program push()es
them to a LinkeListBlockingQueue. You can retrieve the message in one by one
manner in FIFO order.

```
$ curl http://YOUR_IP_ADDRESS:18081/check
```

Note that the BlockingQueue is shared between Kafka poller thread and
Spring Boot controller thread.





