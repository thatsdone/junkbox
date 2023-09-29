package com.github.thatsdone.junkbox;
    
import java.util.List;
import java.util.Map;
import java.util.Base64;
import java.nio.charset.StandardCharsets;
import java.io.ByteArrayInputStream;
//import java.util.HexFormat; Java17

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Autowired;

import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.ContentType;
import org.apache.hc.core5.http.io.entity.EntityUtils;
import org.apache.hc.core5.http.io.entity.InputStreamEntity;
import org.apache.hc.core5.http.message.StatusLine;

import org.apache.kafka.clients.producer.ProducerRecord;

import com.github.thatsdone.junkbox.SpringTest1Kafka;

@RestController
class SpringTest1Controller {

    @Autowired
    private SpringTest1 springTest1;
    @Autowired
    private SpringTest1Kafka springTest1Kafka;

    
    @GetMapping("/hello")
    String hello() {
        return "Hello, World!";
    }

    @PostMapping("/api/operation")
    String apiPostOperation(@RequestHeader Map<String, String> headers,
                            @RequestBody byte[] data) {

        String forward_url = null;
        for (Map.Entry<String, String> entry : headers.entrySet()) {
            System.out.println(entry.getKey() + " : " + entry.getValue());
            if (entry.getKey().equals("forward_url")) {
                forward_url = entry.getValue();
                System.out.println("Forwarding data to: "  + forward_url);
            }
        }

        //hexdump POST body
        if (data.length == 0) {
            return "POST /api/operation received.";
        }
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < data.length; i++) {
            builder.append(String.format("%02x ", data[i]));
            if ((i + 1) % 16 == 0) {
                System.out.println(builder.toString());
                builder.setLength(0);
            }
        }
        if ((data.length % 16) != 0) {
            System.out.println(builder.toString());
        }

        //forward POST body via Kafka
        if (springTest1Kafka.producer != null && springTest1Kafka.producer_topic != null) {
            System.out.println("Sending data via Kafka: start");
            ProducerRecord<String, byte[]> pr =
                new ProducerRecord<>(springTest1Kafka.producer_topic, data);
            springTest1Kafka.producer.send(pr);
            System.out.println("Sending data via Kafka: end");
        }

        if (forward_url == null) {
            return "POST /api/operation received.";
        }

        //forward POST body via HTTP
        try (CloseableHttpClient httpclient = HttpClients.createDefault()) {
        HttpPost httppost = new HttpPost(forward_url);
        InputStreamEntity reqEntity =
            new InputStreamEntity(new ByteArrayInputStream(data),
                                  data.length,
                                  ContentType.APPLICATION_OCTET_STREAM);
        httppost.setEntity(reqEntity);
        httpclient.execute(httppost, response -> {
                           System.out.println(httppost + " -> " + new StatusLine(response));
                           EntityUtils.consume(response.getEntity());
                           return null;
            });
        } catch (Exception e) {
            e.printStackTrace();
        }

        return "POST /api/operation received.";
    }
}
