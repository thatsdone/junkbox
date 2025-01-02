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

import com.github.thatsdone.junkbox.SpringTest4Kafka;

@RestController
class SpringTest4Controller {

    @Autowired
    private SpringTest4 springTest4;

    
    @GetMapping("/check")
    String check() {
        System.out.printf("DEBUG: before poll()/take(): size: %d\n", springTest4.getQueueSize());
        String msg = springTest4.take();
        System.out.printf("DEBUG: after poll()/take(): size: %d\n", springTest4.getQueueSize());
        return msg;
    }

    @PostMapping("/api/operation")
    String apiPostOperation(@RequestHeader Map<String, String> headers,
                            @RequestBody byte[] data) {

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

        return "POST /api/operation received.";
    }
}
