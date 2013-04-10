/**
 * Restlet1.java
 *
 * An examination of a small REST server using restlet (http://restlet.org/).
 * Uses:
 *   restlet - A lightweight REST server
 *   slf4j - Symple Logger Framework for Java
 *   commons-cli - Apache Commons CLI
 * 
 *  Author: Masanori Itoh <masanori.itoh@gmail.com>
 */
import org.restlet.*;
import org.restlet.data.*;
import org.restlet.resource.*;
import org.restlet.service.*;

import org.apache.commons.cli.*;

import org.slf4j.bridge.SLF4JBridgeHandler;

import java.util.logging.*;


public class Restlet1 extends ServerResource {  
  
    public static void main(String[] args) throws Exception {  

       /**
	* Parse command line argument and setup various parameters
	*/
	org.apache.commons.cli.Options options = 
	    new org.apache.commons.cli.Options();
	options.addOption("l", true, "logfile");
	options.addOption("p", true, "port");
	CommandLineParser parser = new PosixParser();
	CommandLine cmd = parser.parse(options, args);
	String logfile = cmd.getOptionValue("l");
	String port = cmd.getOptionValue("p");
	if (logfile != null) {
	    System.out.println("logfile is :" + logfile);
	} else {
	    logfile = "restlet1.log";
	}
	if (port == null) {
	    port = "8182";
	}
	
        // The below line must before SL4JBridgeHandler.install()
	Component component = new Component();
	component.getServers().add(Protocol.HTTP, Integer.parseInt(port));
	component.getDefaultHost().attach("/path1", Restlet1.class);
	component.getDefaultHost().attach("/path2", Restlet1.class);
	component.start();  

        /**
	 * Disable standard log facility to supress logs to STDOUT
	 */
	java.util.logging.Logger rootLogger =
	    LogManager.getLogManager().getLogger("");
	Handler[] handlers = rootLogger.getHandlers();
	rootLogger.removeHandler(handlers[0]);
	System.setProperty("org.slf4j.simpleLogger.logFile", logfile);
        /**
	 * Install SLF4J
	 */
	SLF4JBridgeHandler.install();
	
    }
    // @Get is restlet annotation for GET handler
    @Get  
    public String toString() {  
	// Print the requested URI path  
	return
	    "Resource URI  : " + getReference() + '\n' +
	    "Root URI      : " + getRootRef() + '\n' +
	    "Routed part   : " + getReference().getBaseRef() + '\n' + 
	    "Remaining part: " + getReference().getRemainingPart() + '\n' + 
	    "getPath:      : " + getReference().getPath() + '\n' +
	    "identifier:   : " + getReference().getIdentifier() + '\n' +
	    "identifier:   : " + getReference().getSegments() + '\n' +
	    '\n';  
    }   
}  
   

