package com.github.thatsdone.junkbox;


/**
 * Hello world!
 *
 */
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.util.Properties;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringSerializer;
import org.apache.kafka.common.serialization.ByteArraySerializer;

import java.lang.reflect.InvocationTargetException;

@SpringBootApplication
public class SpringTest1 {

    public static String banner = "Shared data!!";
    public static KafkaProducer<String, byte[]> producer = null;
    public static String producer_topic = null;

	public static void main(String... args) {
        //
        String externalClassName = System.getenv("EXTERNAL_CLASS_NAME");
        System.out.println("getenv EXTERNAL_CLASS_NAME: " +  externalClassName);
        String externalClassMethod = System.getenv("EXTERNAL_CLASS_METHOD");
        System.out.println("getenv EXTERNAL_CLASS_MTHOD: " +  externalClassMethod);
        String kafkaServer = System.getenv("KAFKA_SERVER");
        System.out.println("getenv KAFKA_SERVER: " +  kafkaServer);
        producer_topic = System.getenv("KAFKA_PRODUCER_TOPIC");
        System.out.println("getenv KAFKA_PRODUCER_TOPIC: " +  producer_topic);
        //
        if (externalClassName != null && externalClassMethod != null) {
            try {
                Class<?> dyncls = Class.forName(externalClassName);
                Object dynobj = dyncls.newInstance();
                String dyndata = (String)dyncls.getMethod(externalClassMethod).invoke(dynobj);
                System.out.println(dyndata);
            } catch (ClassNotFoundException | InstantiationException |
                     IllegalAccessException | NoSuchMethodException |
                     InvocationTargetException e) {
                e.printStackTrace();
                System.exit(0);
            }
        }
	
        //
        if (kafkaServer != null) {
            Properties prop = new Properties();
            prop.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG,
                             kafkaServer);
            prop.setProperty(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,
                             StringSerializer.class.getName());
            prop.setProperty(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
                             ByteArraySerializer.class.getName());
            //
            //KafkaProducer<String, byte[]> producer = new KafkaProducer<>(prop);
            producer = new KafkaProducer<>(prop);
        }

		SpringApplication.run(SpringTest1.class, args);
	}
}

