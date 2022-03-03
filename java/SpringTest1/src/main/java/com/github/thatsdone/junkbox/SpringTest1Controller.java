package com.github.thatsdone.junkbox;
    
import java.util.List;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
    
@RestController
class SpringTest1Controller {

    //private final Test1Repository repository;

    //SpringTest1Controller(Test1Repository repository) {
    //    this.repository = repository;
    //}
    
    @GetMapping("/hello")
    String hello() {
        return "Hello, World!";
    }
}
