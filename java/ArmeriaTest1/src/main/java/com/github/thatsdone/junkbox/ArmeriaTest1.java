package com.github.thatsdone.junkbox;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
//
import com.linecorp.armeria.server.Server;
import com.linecorp.armeria.server.ServerPort;
import com.linecorp.armeria.server.ServerBuilder;
import com.linecorp.armeria.server.ServiceRequestContext;
import com.linecorp.armeria.server.AbstractHttpService;
import com.linecorp.armeria.server.logging.LoggingService;
import com.linecorp.armeria.common.HttpRequest;
import com.linecorp.armeria.common.HttpResponse;
import com.linecorp.armeria.common.HttpStatus;
import com.linecorp.armeria.common.MediaType;
import com.linecorp.armeria.common.MediaTypeNames;
import com.linecorp.armeria.common.QueryParams;

import java.util.concurrent.CompletableFuture;
import java.util.*;
import java.net.InetSocketAddress;

class ArmeriaTest1 {

    static private Logger logger = LoggerFactory.getLogger(ArmeriaTest1.class);
	
    public static void main(String[] args) throws Exception {

        System.out.println("Hello, Armeria1!\n");
        logger.info("Hello, Armeria1!(INFO)\n");
        logger.debug("Hello, Armeria1!(DEBUG)\n");

        Server server = newServer(18080);

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                    server.stop().join();
		    System.out.println("Shutfodn hook called.\n");
                    logger.info("Server shutdown.");
        }));
        CompletableFuture<Void> future = server.start();
	/**
        logger.info("Server started at: http://0.0.0.0:{}/",
                    server.activeLocalPort());
	*/
	Map<InetSocketAddress, ServerPort>ports = server.activePorts();
	for (Map.Entry<InetSocketAddress, ServerPort>entry : ports.entrySet()) {
	    logger.info(entry.getKey() + " / " + entry.getValue());
	}
        future.join();
    }

    static Server newServer(int port)  {
        final ServerBuilder sb = Server.builder();
        sb.http(port);
        sb.service("/", (ctx, req) -> HttpResponse.of("Hello, world!"));
        //
        sb.service("/api/{operation}", new AbstractHttpService() {
                @Override
                protected HttpResponse doGet(ServiceRequestContext ctx,
					     HttpRequest creq) {
		    logger.info("doGet called.");
                    String operation = ctx.pathParam("operation");
                    return HttpResponse.of("Got a 'GET /api/%s' request.",
					   operation);
                }
                protected HttpResponse doPost(ServiceRequestContext ctx,
					      HttpRequest creq) {
                    String operation = ctx.pathParam("operation");
		    logger.info("doPost called.");
                    return HttpResponse.of("Got a 'POST /api/%s' request.",
					   operation);
                }
            }.decorate(LoggingService.newDecorator()));
        return sb.build();
    }
}
