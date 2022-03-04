package com.github.thatsdone.junkbox;

import javax.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class QuarkusTest1Service {

    public String metrics(String name) {
        return "GOT a 'GET /api/metrics/" + name + "' request";
    }
}
