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
    public String handlePost(byte[] body) {
        if (body.length == 0) {
            return "POST operation received.";
        }
        System.out.println(String.format("handlePost(): body length: %d", body.length));
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < body.length; i++) {
            builder.append(String.format("%02x ", body[i]));
            if ((i + 1) % 16 == 0) {
                System.out.println(builder.toString());
                builder.setLength(0);
            }
        }
        if ((body.length % 16) != 0) {
            System.out.println(builder.toString());
        }
        return "POST request received.";
    }
}
