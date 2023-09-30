/**
 * SpringTest2.java: An exercise of Spring Cloud Functions
 */
package com.github.thatsdone.junkbox.SpringTest2;

import java.util.function.Function;
import java.util.function.Supplier;
import java.nio.charset.StandardCharsets;
//
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.messaging.Message;


@SpringBootApplication
public class SpringTest2 {

    public static void main(String[] args) throws Exception {
	SpringApplication.run(SpringTest2.class, args);
    }

    @Bean
    public Function<String, String> uppercase() {
	System.out.println("uppercase() received.");
	return value -> value.toUpperCase();
    }

    @Bean
    public Function<Message<byte[]>, String> operation() {
	System.out.println("operation() called.");

	return value -> {
	    System.out.println(value.getHeaders());
	    System.out.println(new String(value.getPayload(), StandardCharsets.UTF_8));

	    byte[] data = value.getPayload();//.getBytes();
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
	    return "operation received.";
	};
    }
}
