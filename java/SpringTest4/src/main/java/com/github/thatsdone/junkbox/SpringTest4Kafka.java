/**
 * SpringTest4Kafka.java: Kafka handler for SpringTest4
 *
 */
package com.github.thatsdone.junkbox;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.util.*;
import java.time.Duration;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

import org.apache.kafka.common.*;
import org.apache.kafka.common.serialization.StringSerializer;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.serialization.StringDeserializer;

import org.springframework.stereotype.Component;

@Component
public class SpringTest4Kafka extends Thread {

    public static KafkaConsumer<String, String> consumer = null;

    public static String kafkaServer = null;
    public static String kafkaTopic = null;
    public static String kafkaGroup = null;

    //TODO: Better to refer SpringTest4 using autowired?
    private BlockingQueue queue;

    public SpringTest4Kafka() {
        
        kafkaServer = System.getenv("KAFKA_SERVER");
        System.out.println("getenv KAFKA_SERVER: " +  kafkaServer);
        kafkaTopic = System.getenv("KAFKA_TOPIC");
        System.out.println("getenv KAFKA_TOPIC: " +  kafkaTopic);
        kafkaGroup = System.getenv("KAFKA_GROUP");
        System.out.println("getenv KAFKA_GROUP: " +  kafkaGroup);

    }

    public void setQueue(BlockingQueue q) {
        queue = q;
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
	
        System.out.printf("DEBUG: run(): Thread started.\n");

        if (kafkaServer == null || kafkaTopic == null) {
            System.out.printf("DEBUG: No valid kafka configuration.\n");
            return;
        }
        
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaServer);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, kafkaGroup);
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG,
                  StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,
                  StringDeserializer.class.getName());

        // Create the consumer using props.
        consumer = new KafkaConsumer<>(props); 
        consumer.subscribe(Arrays.asList(kafkaTopic));
        
        while (true) {

            System.out.printf("DEBUG: calling KafkaConsumer.poll().\n");

            ConsumerRecords<String, String> consumerRecords =
                consumer.poll(poll_interval);

            System.out.printf("DEBUG: poll() returned. count: %d\n",
                              consumerRecords.count());

            for (ConsumerRecord<String, String> record:
                     consumerRecords.records(kafkaTopic)) {
                
                System.out.printf("DEBUG: CR (%d, %d, %d, %d) %s\n",
                                  record.key(),
                                  record.value().length(),
                                  record.partition(),
                                  record.offset(),
                                  record.value());
                //hand the message via BlockingQueue
                try {
                    queue.put(record.value());
                } catch (Exception e) {
                    e.printStackTrace();
                }
                System.out.printf("DEBUG: size of queue: %d\n", queue.size());
            }
        }
    }
}
