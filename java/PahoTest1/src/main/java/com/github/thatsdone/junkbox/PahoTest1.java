package com.github.thatsdone.junkbox;
/**
 * PahoTest1 : An Eclipse Paho Java exercise program
 * 
 * History: 2023/09/23 v0.0
 * Author: Masanori Itoh <masanori.itoh@gmail.com>
 * License: Apache License, Version 2.0
 * References:
 *   - https://github.com/eclipse/paho.mqtt.java/blob/master/MQTTv5.md
 */
import java.util.*;
import java.io.*;
import java.io.IOException;
import java.util.concurrent.TimeUnit;
import java.util.logging.Logger;
//
import org.eclipse.paho.mqttv5.client.MqttAsyncClient;
import org.eclipse.paho.mqttv5.client.MqttConnectionOptions;
import org.eclipse.paho.mqttv5.client.IMqttToken;
import org.eclipse.paho.mqttv5.client.persist.MemoryPersistence;
import org.eclipse.paho.mqttv5.common.MqttException;
import org.eclipse.paho.mqttv5.common.MqttMessage;
import org.eclipse.paho.mqttv5.common.packet.MqttProperties;

public class PahoTest1 {
    public static void main(String[] args) {
        String subTopic = System.getenv("MQTT_SUB_TOPIC");
        String pubTopic = System.getenv("MQTT_PUB_TOPIC");
        String broker  = System.getenv("MQTT_BROKER");
	//
        String content = "Hello World from PahoTest1";
        String clientId = "PahoTest1";
        int qos = 2;

	
        MemoryPersistence persistence = new MemoryPersistence();
        try {
            MqttConnectionOptions connOpts = new MqttConnectionOptions();
	    connOpts.setCleanStart(false);
            MqttAsyncClient client = new MqttAsyncClient(broker, clientId, persistence);
	    System.out.println("Connecting...: " + broker);
	    IMqttToken token = client.connect(connOpts);
	    token.waitForCompletion();
	    System.out.println("Connection established:");
            // set callback
            //client.setCallback(new OnMessageCallback());
            // Publish
            System.out.println("Publishing to: " + pubTopic
			       + " with message: " + content);
	    MqttMessage message = new MqttMessage(content.getBytes());
	    message.setQos(qos);
	    token = client.publish(pubTopic, message);
	    token.waitForCompletion();
	    System.out.println("Publish completed:");
	    
            // TODO: Implement Subscribe test 
	    /**
            MqttSubscription sub = new MqttSubscription(subTopic, qos);
            client.subscribe(
                             new MqttSubscription[] { sub },
                             new IMqttMessageListener[] { this });
            Thread.sleep(60 * 1000);
	    */
	    
            client.disconnect(); //TODO: necessary?
            System.out.println("Disconnected");
            client.close();
            System.exit(0);

        } catch (MqttException me) {
            System.out.println("reason " + me.getReasonCode());
            System.out.println("msg " + me.getMessage());
            System.out.println("loc " + me.getLocalizedMessage());
            System.out.println("cause " + me.getCause());
            System.out.println("excep " + me);
            me.printStackTrace();
        }
    }
}
