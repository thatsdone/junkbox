/**
 * SpringTest4Kafka.java: Kafka handler for SpringTest4
 *
 */
package com.github.thatsdone.junkbox;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

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

    private static final Logger logger =
        LoggerFactory.getLogger(SpringTest4Kafka.class);
    
    public static KafkaConsumer<String, String> consumer = null;

    public static String kafkaServer = null;
    public static String kafkaTopic = null;
    public static String kafkaGroup = null;

    //TODO: Better to refer SpringTest4 using autowired?
    private BlockingQueue queue;

    public SpringTest4Kafka() {
        
        kafkaServer = System.getenv("KAFKA_SERVER");
        logger.debug("getenv KAFKA_SERVER: {}", kafkaServer);
        kafkaTopic = System.getenv("KAFKA_TOPIC");
        logger.debug("getenv KAFKA_TOPIC: {}",  kafkaTopic);
        kafkaGroup = System.getenv("KAFKA_GROUP");
        logger.debug("getenv KAFKA_GROUP: {}", kafkaGroup);

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
	
        logger.debug("run(): Thread started.");

        if (kafkaServer == null || kafkaTopic == null) {
            logger.error("No valid kafka configuration.");
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

            logger.debug("calling KafkaConsumer.poll().");

            ConsumerRecords<String, String> consumerRecords =
                consumer.poll(poll_interval);

            logger.debug("poll() returned. count: {}",
                              consumerRecords.count());

            for (ConsumerRecord<String, String> record:
                     consumerRecords.records(kafkaTopic)) {
                
                logger.debug("ConsumerRecord ({}, {}, {}, {}) {}",
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
                logger.debug("size of queue: {}", queue.size());
            }
        }
    }
}
