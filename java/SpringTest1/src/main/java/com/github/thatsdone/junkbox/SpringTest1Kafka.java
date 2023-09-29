/**
 * SpringTest1Kafka.java: Kafka handler for SpringTest1
 *
 */
package com.github.thatsdone.junkbox;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.util.*;
/**
import java.util.Properties;
import java.util.List;
import java.util.Map;
import java.util.Collections;
import java.util.Properties;
*/
import java.time.Duration;

import java.nio.charset.StandardCharsets;

import org.apache.kafka.common.*;

import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;
import org.apache.kafka.common.serialization.ByteArraySerializer;

import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.ByteArrayDeserializer;

//import java.lang.reflect.InvocationTargetException;

//import org.springframework.web.bind.annotation.Component;
import org.springframework.stereotype.Component;

@Component
public class SpringTest1Kafka extends Thread {

    public static KafkaProducer<String, byte[]> producer = null;
    public static KafkaConsumer<Long, byte[]> consumer = null;
    public static String producer_topic = null;
    public static String consumer_topic = null;
    public static String kafkaServer = null;

    public SpringTest1Kafka() {
        int total_messages = 0;
        
        kafkaServer = System.getenv("KAFKA_SERVER");
        System.out.println("getenv KAFKA_SERVER: " +  kafkaServer);
        producer_topic = System.getenv("KAFKA_PRODUCER_TOPIC");
        System.out.println("getenv KAFKA_PRODUCER_TOPIC: " +  producer_topic);
        consumer_topic = System.getenv("KAFKA_CONSUMER_TOPIC");
        System.out.println("getenv KAFKA_CONSUMER_TOPIC: " +  consumer_topic);

        if (kafkaServer == null) {
            return;
        }

        if (producer_topic != null) {
            Properties prop = new Properties();
            prop.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG,
                             kafkaServer);
            prop.setProperty(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,
                             StringSerializer.class.getName());
            prop.setProperty(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
                             ByteArraySerializer.class.getName());
            producer = new KafkaProducer<>(prop);
        }
        if (consumer_topic != null) {
            Properties props = new Properties();
            props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaServer);
            props.put(ConsumerConfig.GROUP_ID_CONFIG, "SpringTest1");
            props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG,
                      StringDeserializer.class.getName());
            props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,
                      ByteArrayDeserializer.class.getName());

            // Create the consumer using props.
            consumer = new KafkaConsumer<>(props);
            
            // Subscribe to the topic.
            //System.out.printf("DEBUG: calling subscribe() .\n");	
            //consumer.subscribe(Collections.singletonList(consumer_topic));

            /**
            System.out.printf("list of topics:\n");
            for (Map.Entry<String, List<PartitionInfo>> entry : consumer.listTopics().entrySet()) {
                System.out.printf("  %s\n", entry.getKey());
            }
            */

            System.out.printf("partitions for %s: \n",  consumer_topic);
            List<TopicPartition> tps = new LinkedList<TopicPartition>();

            System.out.printf("topic partition leader ealiest latest #msg\n");
            for (PartitionInfo pi: consumer.partitionsFor(consumer_topic)) {
                //System.out.printf("%s %03d %d\n", pi.topic(), pi.partition(), pi.leader().id());
                TopicPartition tp = new TopicPartition(consumer_topic, pi.partition());
                tps.add(tp);
                int earliest = consumer.beginningOffsets(Collections.singletonList(tp)).get(tp).intValue();
                int latest = consumer.endOffsets(Collections.singletonList(tp)).get(tp).intValue();
                System.out.printf("  %s %03d %d %d %d %d\n",
                                  pi.topic(),
                                  pi.partition(),
                                  pi.leader().id(),
                                  earliest,
                                  latest,
                                  latest - earliest
                                  );
                total_messages += (latest - earliest);
            }
            System.out.printf("  Total # of messages in %s %d\n",consumer_topic, total_messages);
            consumer.assign(tps);
            //consumer.seekToBeginning(tps);
        }
    }

    /**
     * Thread for KafkaConsumer
     */
    public void run() {
        
        int poll_count = 60;
        int interval = 60 * 1000;
        final int giveUp = poll_count;
        int noRecordsCount = 0;
        Duration poll_interval = Duration.ofMillis(interval);
	
        System.out.printf("run(): Thread started.\n");

        while (true) {

            System.out.printf("DEBUG: calling KafkaConsumer.poll().\n");

            ConsumerRecords<Long, byte[]> consumerRecords =
                consumer.poll(poll_interval);
            if (consumerRecords.count() == 0) {
                noRecordsCount++;
                if (noRecordsCount > giveUp) {
                    break;
                } else {
                    continue;
                }
            }
            consumerRecords.forEach(record -> {
                    //int length = record.value().position();
                    int length = record.value().length;
                    System.out.printf("Consumer Record:(%d, %d, %d, %d)\n",
                                      record.key(), length,
                                      record.partition(), record.offset());
                    System.out.printf("record.value(): %s %s \n",
                                      record.value(),
                                      new String(record.value(), StandardCharsets.UTF_8)
                                      );
                    // hexdump
                });
            // below necessary?
            //consumer.commitAsync();
        }
        consumer.close();
        System.out.println("DONE");
    }
}
