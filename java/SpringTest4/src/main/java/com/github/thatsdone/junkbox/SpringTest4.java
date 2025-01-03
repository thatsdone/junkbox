/**
 * SpringTest4.java : An excercise program for Spring Framework
 *
 */
package com.github.thatsdone.junkbox;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.util.*;
import java.lang.reflect.InvocationTargetException;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

import com.github.thatsdone.junkbox.SpringTest4Kafka;

@SpringBootApplication
public class SpringTest4 extends Thread {

    private static final Logger logger =
        LoggerFactory.getLogger(SpringTest4.class);
    
    public static BlockingQueue q = null;

    public int getQueueSize() {
        if (q == null) {
            logger.error("q is null\n");
            return 0;
        }
        return q.size();
    }
    public String take() {
        String ret = null;

        if (q == null) {
            logger.error("q is null\n");
            return ret;
        }

        try {
            //NOTE: take() blocks, poll returns null immediately.
            //Also another version of poll() takes timeout.
            //ret = q.take().toString();
            Object result = q.poll();
            if (result != null) {
                ret = result.toString();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return ret;
    }
    
	public static void main(String... args) {
        // Create a BlockingQueue for inter threads communication
        q = new LinkedBlockingQueue();

        logger.info("main() started.");
        
        // Kafka setup
        // NOTE: If we defined a constructor with arguments, Spring Framework
        // complains.
        SpringTest4Kafka t1 = new SpringTest4Kafka();
        t1.setQueue(q);
        t1.start();

        // Run Spring Application
		SpringApplication.run(SpringTest4.class, args);
	}
}

