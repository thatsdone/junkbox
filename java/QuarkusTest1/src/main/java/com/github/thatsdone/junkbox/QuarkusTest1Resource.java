package com.github.thatsdone.junkbox;

import javax.inject.Inject;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

import org.jboss.resteasy.annotations.jaxrs.PathParam;

@Path("/api")
public class QuarkusTest1Resource {

    @Inject
    QuarkusTest1Service service;

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    @Path("/metrics/{name}")
    public String getMetric(@PathParam String name) {
        return service.metrics(name);
    }
    
    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String metrics() {
        return "Got a 'GET /api/metrics' request'";
    }

    @POST
    @Produces(MediaType.TEXT_PLAIN)
    @Path("/operation")
    public String handlePost() {
        return "POST request received.";
    }

    
}
