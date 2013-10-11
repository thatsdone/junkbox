/**
 * Jnova.java
 * 
 * A Java version 'nova' command using https://github.com/woorea/openstack-java-sdk.
 * 
 * - Depends on bunch of libraries
 * - Very ugly huge main() method.
 *
 *  Author: Masanori Itoh <masanori.itoh@gmail.com>
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
import com.woorea.openstack.keystone.utils.KeystoneUtils;

import java.lang.System;
import java.io.PrintStream;

import org.codehaus.jackson.map.ObjectMapper;

import java.util.logging.*;
/*
import java.util.Enumeration;
*/
//import org.apache.commons.io.output.NullOutputStream;

public class Jnova {

	public static void printjson(Object o) {
		ObjectMapper mapper = new ObjectMapper();
		try {
			System.out.println(mapper.writeValueAsString(o));
		} catch (Exception e) {
			System.out.println("Exception! :" + e);
		}
	}

	/*
	 * NullFilter for disabling log output
	 */
	public static class NullFilter implements Filter {
		public boolean isLoggable(LogRecord record) {
			//System.out.println("DEBUG: " + record.getLevel());
			return false;
		}
	}


	/**
	 * @param args
	 */
	public static void main(String[] args) {
		
		String os_auth_url = System.getenv("OS_AUTH_URL");
		String os_password = System.getenv("OS_PASSWORD");
		String os_tenant_name = System.getenv("OS_TENANT_NAME");
		String os_username = System.getenv("OS_USERNAME");

		if (os_auth_url == null || os_password == null ||
			os_tenant_name == null || os_username == null)  {
			System.out.println("set OS_* environment variables.");
			System.exit(0);
		}

		// Parse comnand line arguments.
		boolean all_tenants = false;
		boolean debug = false;
		boolean log_message = false;
		for(int i = 1; i < args.length; i++) {
			if (args[i].equals("--all-tenants")) {
				all_tenants = true;
			} else if (args[i].equals("--debug")) {
				debug = true;
			} else if (args[i].equals("--log-message")) {
				 log_message = true;
			}
		}
        // Get account informatoin from environment variables.
		if (debug) {
			System.out.println("OS_AUTH_URL    : " + os_auth_url);
			System.out.println("OS_PASSWORD    : " + os_password);
			System.out.println("OS_TENANT_NAME : " + os_tenant_name);
			System.out.println("OS_USERNAME    : " + os_username);
		}

		// First, create a Keystone cliet class instance.
		Keystone keystoneClient = new Keystone(os_auth_url);
		/*
		  // research purpose
		  LogManager lm  = LogManager.getLogManager();
		  for (Enumeration l = lm.getLoggerNames();l.hasMoreElements();) {
		  String s = (String) l.nextElement();
		  System.out.println(s);
		  }
		*/

		if (log_message == false) {
			/*
			PrintStream devnull = null;
			try {
				devnull = new PrintStream("/dev/null");
			} catch (Exception e) {
				System.out.println("Failed to call PrintStream(/dev/null)");
				System.exit(0);
			}
			Handler nullHandler = new StreamHandler(devnull, new SimpleFormatter());
			*/
			/*
			Handler nullHandler = new StreamHandler(new NullOutputStream(),
													new SimpleFormatter());
			*/
			// openstack-java-sdk creates a logger named "os" internally.
			Logger l = Logger.getLogger("os");
			//l.addHandler(nullHandler);
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
			.authenticate(new UsernamePassword(os_username, os_password))
			.withTenantName(os_tenant_name)
			.execute();
		
		//Set the token now we got for the following requests.
		//keystoneClient.token(access.getToken().getId());

		String nova_endpoint = KeystoneUtils
			.findEndpointURL(access.getServiceCatalog(),
							 "compute", null, "public");
		if (debug) {
			System.out.println("DEBUG:" + nova_endpoint);
		}
		// The above contains TENANT_ID like
		//   http://SERVICE_HOST:PORT/v1.1/TENANT_ID
		// at least version 3.2.2-SNAPSHOT of openstack-java-sdk.
		//
		// Thus, below does not work.
		//		Nova novaClient = new Nova(nova_endpoint.concat("/")
		//								   .concat(access.getToken()
		//										   .getTenant().getId()));

		//		Nova novaClient = new Nova(nova_endpoint.concat("/"));
		Nova novaClient = new Nova(nova_endpoint);

		//Set the token now we got for the following requests.
		//Note that we can use the same token with the above keystone requests
		//unless it's not expired.
		novaClient.token(access.getToken().getId());

		/*
		 * command handlers
		 */
		if (args[0].equals("list")) {
			//servers
			Servers servers;
			if (all_tenants) {
				// nova list --all-tenants
				// get servers of all_tenants.
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
			;

		} else if (args[0].startsWith("host")) {
			// os-hosts : get per-host informatoin using /os-hosts extension
			if (args[0].equals("host-list")) {
				// nova host-list
				Hosts hosts = novaClient.hosts().list().execute();
				//System.out.println(hosts);
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
				Hypervisors hypervisors = novaClient.hypervisors().list().execute();
				if (debug) {
					System.out.println(hypervisors);
				}
				printjson(hypervisors);
				if (debug){
					for(Hypervisor hypervisor : hypervisors) {
						Hypervisor hv = novaClient.hypervisors()
							.show(hypervisor.getId()).execute();
						printjson(hv);
						if (debug) {
							System.out.println(hv);
						}
					}
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

		} else {
			System.out.println("Unknown command :" + args[0]);
		}
	}
}
