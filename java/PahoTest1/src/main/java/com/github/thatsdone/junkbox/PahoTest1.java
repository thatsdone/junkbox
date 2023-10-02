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
import java.nio.charset.StandardCharsets;
//
import org.eclipse.paho.mqttv5.client.IMqttToken;
import org.eclipse.paho.mqttv5.client.IMqttDeliveryToken;
//
import org.eclipse.paho.mqttv5.client.MqttAsyncClient;
import org.eclipse.paho.mqttv5.client.MqttCallback;
import org.eclipse.paho.mqttv5.client.MqttActionListener;

import org.eclipse.paho.mqttv5.client.MqttConnectionOptions;
import org.eclipse.paho.mqttv5.client.MqttConnectionOptionsBuilder;
import org.eclipse.paho.mqttv5.client.MqttDisconnectResponse;
import org.eclipse.paho.mqttv5.client.MqttToken;

import org.eclipse.paho.mqttv5.client.persist.MemoryPersistence;
import org.eclipse.paho.mqttv5.common.MqttException;
import org.eclipse.paho.mqttv5.common.MqttMessage;
import org.eclipse.paho.mqttv5.common.packet.MqttProperties;
import org.eclipse.paho.mqttv5.common.packet.UserProperty;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.ParseException;
import org.apache.commons.cli.HelpFormatter;


public class PahoTest1 implements  MqttCallback {

    public PahoTest1(String broker, String subTopic,
                     String pubTopic) throws InterruptedException {

        String content = "Hello World from PahoTest1";
        String clientId = "PahoTest1";
        int qos = 1;
	
        try {
            MemoryPersistence persistence = new MemoryPersistence();
            MqttAsyncClient client = new MqttAsyncClient(broker,
                                                         clientId,
                                                         persistence);
            MqttConnectionOptionsBuilder connOptsBuilder =
                new MqttConnectionOptionsBuilder();
            MqttConnectionOptions connOpts =
                connOptsBuilder.serverURI(broker)
                .sessionExpiryInterval(60L)
                .automaticReconnect(true)
                .will(pubTopic,
                      new MqttMessage(content.getBytes(), qos, false,
                                      new MqttProperties()))
                .topicAliasMaximum(1000)
                .build();
            connOpts.setCleanStart(true);

            client.setCallback(this);

            System.out.println("Connecting..: " + broker);
            client.connect(connOpts, new MqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    System.out.println("onSuccess() called.");
                    try {
                        IMqttToken token = client.subscribe(subTopic, qos);
                        //
                        token.waitForCompletion();
                        MqttMessage msg = new MqttMessage(content.getBytes());
                        List<UserProperty> prop = new ArrayList<>();
                        prop.add(new UserProperty("traceparent",
                                                  "00-dummy-PahoTest1-01"));
                        msg.setQos(qos);
                        Byte[] vprop = { MqttProperties.USER_DEFINED_PAIR_IDENTIFIER };
                        MqttProperties mprop = new MqttProperties(vprop);
                        mprop.setUserProperties(prop);
                        msg.setProperties(mprop);

                        client.publish(pubTopic, msg);
                        System.out.println("Message published: " + content);
                    } catch (MqttException e) {
                        System.out.println("Exception occured");
                        e.printStackTrace();
                    }
                }
                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable e) {
                    System.out.println("onFailure(): " + e.getMessage());
                }
            });

            int sleep = 60;
            System.out.println("Sleeping " + sleep  + " seconds.");
            Thread.sleep(sleep * 1000);
            client.disconnect(5000);
            System.out.println("disconnect(): returned");
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

    public static void main(String[] args) throws InterruptedException, ParseException {
        Option help = new Option("help", "print this message");
        Options options = new Options();
        options.addOption(help);
        options.addOption("b", true, "MQTT Broker");
        options.addOption("s", true, "Topic to subscribe");
        options.addOption("p", true, "Topic to publish");
        CommandLineParser parser = new DefaultParser();
        CommandLine cmd = parser.parse(options, args);

        String broker = null;
        String subTopic = null;
        String pubTopic = null;

        if (cmd.hasOption("help")) {
            HelpFormatter formatter = new HelpFormatter();
            formatter.printHelp("PahoTest1", options);
            System.exit(0);
        }
        if (cmd.hasOption("b")) {
            broker = cmd.getOptionValue("b");
        } else {
            broker  = System.getenv("MQTT_BROKER");
        }
        if (cmd.hasOption("s")) {
            subTopic = cmd.getOptionValue("s");
        } else {
            subTopic = System.getenv("MQTT_SUB_TOPIC");
        }
        if (cmd.hasOption("p")) {
            pubTopic = cmd.getOptionValue("b");
        } else {
            pubTopic = System.getenv("MQTT_PUB_TOPIC");
        }
        if (broker == null || subTopic == null || pubTopic == null) {
            System.out.println("Specify broker/subTopic/pubTopic");
            System.exit(0);
        }

        new PahoTest1(broker, subTopic, pubTopic);
    }

    @Override
    public void messageArrived(String topic, MqttMessage message)  {
        System.out.println("messageArrvied() called.");
        System.out.println(new String(message.getPayload(), StandardCharsets.UTF_8));
        List<UserProperty> props = message.getProperties().getUserProperties();
        if (props.size() > 0) {
            UserProperty prop = props.get(0);
            System.out.println(prop.getKey() + " : " + prop.getValue());
        }
    }

    @Override
    public void deliveryComplete(IMqttToken token)  {
        System.out.println("deliveryComplete() called.");
    }

    @Override
    public void disconnected(MqttDisconnectResponse disconnectResponse) {
        System.out.println("disconnected() called.");
    }
    @Override
    public void mqttErrorOccurred(MqttException e)  {
        System.out.println("mqttErrorOccured() called.");
    }

    @Override
    public void authPacketArrived(int reasonCode, MqttProperties properties)  {
        System.out.println("authPacketArrvied() called.");
    }
    @Override
    public void connectComplete(boolean reconnect, String serverURI)  {
        System.out.println("connectComplete() called.");
    }
}
