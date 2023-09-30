package com.github.thatsdone.junkbox;

import org.springframework.boot.SpringApplication;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.boot.autoconfigure.SpringBootApplication;
//import org.springframework.context.annotation.Bean;
//import java.util.function.Function;
//import java.util.function.Supplier;


@RestController
@SpringBootApplication
public class SpringTest3 {

    @RequestMapping("/")
    String home() {
        return "Hello World!";
    }

    public static void main(String[] args) {
        SpringApplication.run(SpringTest3.class, args);
    }
}
