/**
 * SpringTest1.java : An excercise program for Spring Framework
 *
 */
package com.github.thatsdone.junkbox;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.util.*;
import java.lang.reflect.InvocationTargetException;

import com.github.thatsdone.junkbox.SpringTest1Kafka;

@SpringBootApplication
public class SpringTest1 extends Thread {

    public static String banner = "Shared data!!";
    
	public static void main(String... args) {
        //
        String externalClassName = System.getenv("EXTERNAL_CLASS_NAME");
        System.out.println("getenv EXTERNAL_CLASS_NAME: " +  externalClassName);
        String externalClassMethod = System.getenv("EXTERNAL_CLASS_METHOD");
        System.out.println("getenv EXTERNAL_CLASS_MTHOD: " +  externalClassMethod);
        // dynamic class loading test
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
	
        // Kafka setup
        if (System.getenv("KAFKA_SERVER") != null) {
            SpringTest1Kafka t1 = new SpringTest1Kafka();
            if(System.getenv("KAFKA_CONSUMER_TOPIC") != null) {
                t1.start();
                System.out.println("Started a thread for Kafka consumer");
            }
        }

		SpringApplication.run(SpringTest1.class, args);
	}
}

