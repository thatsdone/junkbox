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


public class Jnova {

	public static void printjson(Object o) {
		ObjectMapper mapper = new ObjectMapper();
		try {
			System.out.println(mapper.writeValueAsString(o));
		} catch (Exception e) {
			System.out.println("Exception! :" + e);
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
		boolean quiet = true;
		for(int i = 1; i < args.length; i++) {
			if (args[i].equals("--all-tenants")) {
				all_tenants = true;
			} else if (args[i].equals("--debug")) {
				 quiet = false;
			}
		}
		if (quiet == false) {
			System.out.println("OS_AUTH_URL    : " + os_auth_url);
			System.out.println("OS_PASSWORD    : " + os_password);
			System.out.println("OS_TENANT_NAME : " + os_tenant_name);
			System.out.println("OS_USERNAME    : " + os_username);
		}

		// Create a /dev/null PrintStream when quet mode.
		PrintStream devnull = null;
		if (quiet) {
			try {
				devnull = new PrintStream("/dev/null");
			} catch (Exception e) {
				System.out.println("Failed to call PrintStream(/dev/null)");
				System.exit(0);
			}
		}

		// First, create a Keystone cliet class instance.
		Keystone keystoneClient = new Keystone(os_auth_url);
		if (quiet) {
			//original (workaround) extension of openstack-java-sdk.
			keystoneClient.setLogger(devnull);
		}

		// Set account information.
		Access access = keystoneClient.tokens()
			.authenticate(new UsernamePassword(os_username, os_password))
			.withTenantName(os_tenant_name)
			.execute();
		
		//Set the token now we got for the following requests.
		keystoneClient.token(access.getToken().getId());

		String nova_endpoint = KeystoneUtils
			.findEndpointURL(access.getServiceCatalog(),
							 "compute", null, "public");
		if (quiet == false) {
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
		Nova novaClient = new Nova(nova_endpoint.concat("/"));
		if (quiet) {
			//Note that setLogger is not a standard method.
			//Just a workaround extension of openstack-java-sdk.
			novaClient.setLogger(devnull);
		}

		//Set the token now we got for the following requests.
		//Note that we can use the same token with the above keystone requests
		//unless it's expired.
		 novaClient.token(access.getToken().getId());

		/*
		 * command handlers
		 */
		if (args[0].equals("list")) {
			//servers
			Servers servers;
			if (all_tenants) {
				// nova list --all-tenants
				// get servers of all_tenants. (want to user pagination... ) 
				 servers = novaClient.servers()
					.list(true).queryParam("all_tenants", "1").execute();
			} else {
				// Note that 'true' of list(true) appends 'detailed'
				// path element like:  GET /v1.1/TENANT_ID/servers/detail
				// Simple 'nova list' does not use it.
				servers = novaClient.servers().list(true).execute();
			}
			for(Server server : servers) {
				System.out.println(server);
			}

		} else if (args[0].equals("show")) {
			;


		} else if (args[0].startsWith("host")) {
			// os-hosts : get per-host informatoin using /os-hosts extension
			if (args[0].equals("host-list")) {
				// nova host-list
				Hosts hosts = novaClient.hosts().list().execute();
				System.out.println(hosts);
				/*
				for(Hosts.Host host : hosts) {
					System.out.println(host);
					if (host.getService().equals("compute")) {
						String hostname = host.getHostName();
						//System.out.println(hostname);
						Host h = novaClient.hosts().show(hostname).execute();
						System.out.println(h);
					}
				}
				*/

			} else if (args[0].equals("host-describe")) {
				// nova host-describe HOSTNAME
				if (args.length >= 2) {
					Host h = novaClient.hosts().show(args[1]).execute();
					System.out.println(h);
				} else {
					System.out.println("Specify hostname");
				}
			}

		} else if (args[0].startsWith("hypervisor")) {
			// os-hypervisors :
			if (args[0].equals("hypervisor-list")) {
				// nova hypervisor-list
				Hypervisors hypervisors = novaClient.hypervisors().list().execute();
				//System.out.println(hypervisors);
				printjson(hypervisors);
				for(Hypervisor hypervisor : hypervisors) {
					Hypervisor hv = novaClient.hypervisors().show(hypervisor.getId()).execute();
					System.out.println(hv);
					printjson(hv);
				}
			} else if (args[0].equals("hypervisor-stats")) {
				// nova hypervisor-stats
				HypervisorStatistics stat = novaClient.hypervisors().showStats().execute();
				//System.out.println(stat);
				printjson(stat);
			}

		} else if (args[0].startsWith("service")) {
			// os-services
			if (args[0].equals("service-list")) {
				// nova service-list
				Services services = novaClient.services().list().execute();
				for(Service service : services) {
					System.out.println(service);
				} 

			} else if (args[0].equals("service-disable")) {
				// nova service-disable HOST SERVIVCE
				ServiceUpdateReq s = new ServiceUpdateReq();
				s.setHost("ocpswhnc3.ocp-cloud.net"); //1
				s.setBinary("nova-compute"); //2
				Service resp = novaClient.services().disableService(s).execute();
				System.out.println(resp);

			} else if (args[0].equals("service-enable")) { 
				// nova service-enable HOST SERVIVCE
				ServiceUpdateReq s = new ServiceUpdateReq();
				s.setHost("ocpswhnc3.ocp-cloud.net"); //1
				s.setBinary("nova-compute"); //2
				Service resp = novaClient.services().enableService(s).execute();
				System.out.println(resp);
			}

		} else {
			System.out.println("Unknown command :" + args[0]);
		}
	}
}
