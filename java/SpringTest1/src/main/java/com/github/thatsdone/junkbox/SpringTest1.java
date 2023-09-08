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

@SpringBootApplication
public class SpringTest1 {

    public static String banner = "Shared data!!";
    public static KafkaProducer<String, byte[]> producer = null;

	public static void main(String... args) {

        //
        Properties prop = new Properties();
        prop.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG,
                         "172.20.105.120:29092");
        prop.setProperty(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,
                         StringSerializer.class.getName());
        prop.setProperty(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
                         ByteArraySerializer.class.getName());
        //
        //KafkaProducer<String, byte[]> producer = new KafkaProducer<>(prop);
        producer = new KafkaProducer<>(prop);

		SpringApplication.run(SpringTest1.class, args);
	}
}

