/**
 * Jnova.java
 * 
 * A Java version 'nova' command using:
 *	  https://github.com/woorea/openstack-java-sdk
 *
 * Note that this program uses some extended features of the java sdk
 * of a forked version available below:
 *	  https://github.com/thatsdone/openstack-java-sdk 
 * 
 * Currently the following sub commands are implemented.
 *	 nova list	--all-tenants
 *	 nova show
 *	 nova host-list
 *	 nova host-describe
 *	 nova hypervisor-list
 *	 nova hypervisor-show
 *	 nova hypervisor-stats
 *	 nova service-list
 *	 nova service-enable
 *	 nova service-disable
 *	 nova usage-list
 *
 * Authentication information must be specified as environment variables
 * such as OS_AUTH_URL etc.
 *
 *	Author: Masanori Itoh <masanori.itoh@gmail.com>
 */
import com.woorea.openstack.keystone.Keystone;
import com.woorea.openstack.keystone.model.Access;
import com.woorea.openstack.keystone.model.authentication.UsernamePassword;
import com.woorea.openstack.nova.Nova;
import com.woorea.openstack.nova.model.Server;
import com.woorea.openstack.nova.model.Servers;
import com.woorea.openstack.nova.model.Host;
import com.woorea.openstack.nova.model.Hosts;
import com.woorea.openstack.nova.model.Service;
import com.woorea.openstack.nova.model.ServiceAction.ServiceUpdateReq;
import com.woorea.openstack.nova.model.Services;
import com.woorea.openstack.nova.model.Hypervisor;
import com.woorea.openstack.nova.model.Hypervisors;
import com.woorea.openstack.nova.model.HypervisorStatistics;
import com.woorea.openstack.nova.model.QuotaSet;
import com.woorea.openstack.nova.model.SimpleTenantUsage;
import com.woorea.openstack.keystone.utils.KeystoneUtils;
import com.woorea.openstack.nova.api.QuotaSetsResource;

import java.lang.System;
import java.io.PrintStream;
import java.lang.Integer;

import java.util.List;
import java.util.Map;
import java.util.HashMap;

import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.type.JavaType;
//import org.codehaus.jackson.impl.DefaultPrettyPrinter;
import java.util.logging.*;
import org.codehaus.jackson.map.annotate.JsonRootName;
import org.codehaus.jackson.annotate.JsonIgnoreProperties;
import org.codehaus.jackson.annotate.JsonProperty;

public class Jnova {

	public static void printjson(Object o) {
		ObjectMapper mapper = new ObjectMapper();
		try {
			//System.out.println(mapper.writeValueAsString(o));
			/*
			  DefaultPrettyPrinter pp = new DefaultPrettyPrinter();
			  pp.indentArrayWith(new Lf2SpacesIndenter());
			  System.out.println(mapper.writer(pp).writeValueAsString(o));
			*/
			System.out.println(mapper.writerWithDefaultPrettyPrinter()
							   .writeValueAsString(o));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/*
	 * NullFilter for disabling log output
	 */
	public static class NullFilter implements Filter {

		// isLoggable says everything is NOT logabble.
		public boolean isLoggable(LogRecord record) {
			//System.out.println("DEBUG: " + record.getLevel());
			return false;
		}
	}


	/**
	 * @param args
	 */
	public static void main(String[] args) {
		
		String osAuthUrl = System.getenv("OS_AUTH_URL");
		String osPassword = System.getenv("OS_PASSWORD");
		String osTenantName = System.getenv("OS_TENANT_NAME");
		String osUsername = System.getenv("OS_USERNAME");

		if (osAuthUrl == null || osPassword == null ||
			osTenantName == null || osUsername == null)	{
			System.out.println("set OS_* environment variables.");
			System.exit(0);
		}

		// Parse comnand line arguments.
		boolean allTenants = false;
		boolean debug = false;
		boolean logMessage = false;
		/*
		 * skip the first argument. ( i = 1, not 0)
		 */
		for(int i = 1; i < args.length; i++) {
			if (args[i].equals("--all-tenants")) {
				allTenants = true;
			} else if (args[i].equals("--debug")) {
				debug = true;
			} else if (args[i].equals("--log-message")) {
				 logMessage = true;
			}
		}
		// Get account informatoin from environment variables.
		if (debug) {
			System.out.println("OS_AUTH_URL	   : " + osAuthUrl);
			System.out.println("OS_PASSWORD	   : " + osPassword);
			System.out.println("OS_TENANT_NAME : " + osTenantName);
			System.out.println("OS_USERNAME	   : " + osUsername);
		}

		// First, create a Keystone cliet class instance.
		Keystone keystoneClient = new Keystone(osAuthUrl);
		/*
		 * research purpose code chunk to see all log handlers in the system.
		 * LogManager lm  = LogManager.getLogManager();
		 * for (Enumeration l = lm.getLoggerNames();l.hasMoreElements();) {
		 *	  String s = (String) l.nextElement();
		 *	  System.out.println(s);
		 * }
		 */
		if (logMessage == false) {
			// openstack-java-sdk creates a logger named "os" internally.
			Logger l = Logger.getLogger("os");
			l.setFilter(new NullFilter());
			if (debug) {
				System.out.println("DEBUG: Filter : " + l.getFilter());
				for (Handler h : l.getHandlers()) {
					System.out.println("DEBUG: Handlers: " + h);
				}
			}

		}

		// Set account information, and issue an authentication request.
		Access access = keystoneClient.tokens()
			.authenticate(new UsernamePassword(osUsername, osPassword))
			.withTenantName(osTenantName)
			.execute();
		
		String novaEndpoint = KeystoneUtils
			.findEndpointURL(access.getServiceCatalog(),
							 "compute", null, "public");
		if (debug) {
			System.out.println("DEBUG: " + novaEndpoint);
		}
		/*
		 * The above contains TENANT_ID like:
		 *	 http://SERVICE_HOST:PORT/v1.1/TENANT_ID
		 * according to endpoints definition in keystone configuration.
		 * It's the same as keystone endpoint-list.
		 *
		 * Note that we don't need to append a '/' to the URL because
		 * openstack-java-sdk library codes add it.
		 *	 Nova novaClient = new Nova(novaEndpoint.concat("/"));
		 */

		// Create a Nova client object.
		Nova novaClient = new Nova(novaEndpoint);

		/*
		 * Set the token now we got for the following requests.
		 * Note that we can use the same token in the above keystone response
		 * unless it's not expired.
		 */
		novaClient.token(access.getToken().getId());

		/*
		 * command handlers
		 */
		if (args[0].equals("list")) {
			//servers :
			Servers servers;
			if (allTenants) {
				// nova list --all-tenants
				// get servers of all tenants.
				// (want to use pagination if possible... ) 
				 servers = novaClient.servers()
					.list(true).queryParam("all_tenants", "1").execute();
			} else {
				// Note that 'true' of list(true) appends 'detail'
				// path element like:  GET /v1.1/TENANT_ID/servers/detail
				// Simple 'nova list' does not use it.
				servers = novaClient.servers().list(true).execute();
			}
			printjson(servers);
			if (debug) {
				for(Server server : servers) {
					System.out.println(server);
				}
			}

		} else if (args[0].equals("show")) {
			if (args.length >= 2) {
				Server server = novaClient.servers().show(args[1]).execute();
				printjson(server);
			} else {
				System.out.println("Specify server id");
			}

		} else if (args[0].startsWith("host")) {
			// os-hosts : get per-host informatoin using /os-hosts extension
			if (args[0].equals("host-list")) {
				// nova host-list
				Hosts hosts = novaClient.hosts().list().execute();
				if (debug) {
					System.out.println(hosts);
				}
				printjson(hosts);
				if (debug) {
					for(Hosts.Host host : hosts) {
						System.out.println(host);
						if (host.getService().equals("compute")) {
							String hostname = host.getHostName();
							//System.out.println(hostname);
							Host h = novaClient.hosts().show(hostname)
								.execute();
							System.out.println(h);
						}
					}
				}

			} else if (args[0].equals("host-describe")) {
				// nova host-describe HOSTNAME
				if (args.length >= 2) {
					Host h = novaClient.hosts().show(args[1]).execute();
					printjson(h);
					if (debug) {
						System.out.println(h);
					}
				} else {
					System.out.println("Specify hostname");
				}
			}

		} else if (args[0].startsWith("hypervisor")) {
			// os-hypervisors :
			if (args[0].equals("hypervisor-list")) {
				// nova hypervisor-list
				Hypervisors hypervisors = novaClient.hypervisors().list()
										  .execute();
				if (debug) {
					System.out.println(hypervisors);
				}
				printjson(hypervisors);

			} else if (args[0].equals("hypervisor-show")) {
				// nova hypervisor-show
				if (args.length < 2) {
					System.out.println("Specify hypervisor id");
					System.exit(0);
				}
				Hypervisor hv = novaClient.hypervisors()
					.show(new Integer(args[1])).execute();
				printjson(hv);
				if (debug) {
					System.out.println(hv);
				}

			} else if (args[0].equals("hypervisor-stats")) {
				// nova hypervisor-stats
				HypervisorStatistics stat = novaClient.hypervisors()
					.showStats().execute();
				printjson(stat);
				if (debug) {
					System.out.println(stat);
				}
			}

		} else if (args[0].startsWith("service")) {
			// os-services
			if (args[0].equals("service-list")) {
				// nova service-list
				Services services = novaClient.services().list().execute();
				printjson(services);
				if (debug) {
					for(Service service : services) {
							System.out.println(service); 
					} 
				}

			} else if (args[0].equals("service-disable")) {
				// nova service-disable HOST SERVIVCE
				ServiceUpdateReq s = new ServiceUpdateReq();
				s.setHost(args[1]);
				s.setBinary(args[2]);
				Service resp = novaClient.services().disableService(s).execute();
				printjson(resp);	
				if (debug) {
					System.out.println(resp);
				}

			} else if (args[0].equals("service-enable")) { 
				// nova service-enable HOST SERVIVCE
				ServiceUpdateReq s = new ServiceUpdateReq();
				s.setHost(args[1]);
				s.setBinary(args[2]);
				Service resp = novaClient.services().enableService(s).execute();
				printjson(resp);
				if (debug) {
					System.out.println(resp);
				}
			}

		} else if (args[0].equals("usage-list")) {
			if (args.length >= 2) {
				SimpleTenantUsage stu = novaClient.quotaSets()
					.showUsage(args[1]).execute();
				printjson(stu);
			} else {
				System.out.println("Specify tenant id");
			}

		} else {
			System.out.println("Unknown command :" + args[0]);
		}
	}
}
