/**
 * Jnova.java
 * 
 * A Java version 'nova' command using:
 *    https://github.com/woorea/openstack-java-sdk
 *
 * Note that this program uses some extended features of the java sdk
 * of a forked version available below:
 *    https://github.com/thatsdone/openstack-java-sdk 
 * 
 * Currently the following sub command equivalents are implemented.
 *   nova list
 *   nova show
 *   nova host-list
 *   nova host-describe
 *   nova hypervisor-list
 *   nova hypervisor-show
 *   nova hypervisor-stats
 *   nova service-list
 *   nova service-enable
 *   nova service-disable
 *   nova usage-list
 *   nova aggregate-list
 *   nova aggregate-details
 *   nova availability-zone-list
 *   nova flavor-list
 *   nova live-migration
 *   nova availability-zone-list
 *
 * Authentication information must be specified as environment variables
 * such as OS_AUTH_URL etc at the moment.
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
import com.woorea.openstack.nova.model.Services;
import com.woorea.openstack.nova.model.Hypervisor;
import com.woorea.openstack.nova.model.Hypervisors;
import com.woorea.openstack.nova.model.HypervisorStatistics;
import com.woorea.openstack.nova.model.QuotaSet;
import com.woorea.openstack.nova.model.SimpleTenantUsage;
import com.woorea.openstack.nova.model.HostAggregate;
import com.woorea.openstack.nova.model.HostAggregates;
import com.woorea.openstack.nova.model.AvailabilityZoneInfo;
import com.woorea.openstack.nova.model.Flavor;
import com.woorea.openstack.nova.model.Flavors;

import com.woorea.openstack.keystone.utils.KeystoneUtils;
//import com.woorea.openstack.nova.api.QuotaSetsResource;
//import com.woorea.openstack.nova.api.ServersResource;

import java.lang.System;
import java.io.PrintStream;
import java.lang.Integer;

import java.util.List;
import java.util.Arrays;
import java.util.Map;
import java.util.HashMap;
import java.util.LinkedHashMap;

import java.lang.reflect.Method;

import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.type.JavaType;
//import org.codehaus.jackson.impl.DefaultPrettyPrinter;
import java.util.logging.*;
import org.codehaus.jackson.map.annotate.JsonRootName;
import org.codehaus.jackson.annotate.JsonIgnoreProperties;
import org.codehaus.jackson.annotate.JsonProperty;

public class Jnova {

    private static boolean debug = false;
    private static boolean logMessage = false;

    private static String osAuthUrl = System.getenv("OS_AUTH_URL");
    private static String osPassword = System.getenv("OS_PASSWORD");
    private static String osTenantName = System.getenv("OS_TENANT_NAME");
    private static String osUsername = System.getenv("OS_USERNAME");

    public static LinkedHashMap<String, String> cArray = new LinkedHashMap<String, String>();

    static {
        cArray.put("list", "server");
        cArray.put("show", "server");
        cArray.put("host-list", "host");
        cArray.put("host-describe", "host");
        cArray.put("hypervisor-list", "hypervisor");
        cArray.put("hypervisor-show", "hypervisor");
        cArray.put("hypervisor-stats", "hypervisor");
        cArray.put("service-list", "service");
        cArray.put("service-enable", "service");
        cArray.put("service-disable", "service");
        cArray.put("usage-list", "quotaSet");
        cArray.put("aggregate-list", "aggregate");
        cArray.put("aggregate-details", "aggregate");
        cArray.put("flavor-list", "flavor");
        cArray.put("live-migration", "server");
        cArray.put("availability-zone-list", "availabilityZone");
    }

    public static void printJson(Object o) {
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
    private static class NullFilter implements Filter {

        // isLoggable says everything is NOT logabble.
        public boolean isLoggable(LogRecord record) {
            //System.out.println("DEBUG: " + record.getLevel());
            return false;
        }
    }

    private static void setupLog() {

        /*
         * research purpose code chunk to see all log handlers in the system.
         * LogManager lm  = LogManager.getLogManager();
         * for (Enumeration l = lm.getLoggerNames();l.hasMoreElements();) {
         *    String s = (String) l.nextElement();
         *    System.out.println(s);
         * }
         */
        if (!isLogMessage()) {
            // openstack-java-sdk gets/creates a logger named "os" internally.
            Logger l = Logger.getLogger("os");
            l.setFilter(new NullFilter());
            if (isDebug()) {
                System.out.println("DEBUG: Filter : " + l.getFilter());
                for (Handler h : l.getHandlers()) {
                    System.out.println("DEBUG: Handlers: " + h);
                }
            }

        }
    }

    /*
     * skeltons of per resource method for near future use.
     */
    public static void server(String[] args) {
        if(isDebug())
            System.out.println("server() called.");
    }
    public static void host(String[] args) {
        if(isDebug())
            System.out.println("host() called.");
    }
    public static void hypervisor(String[] args) {
        if(isDebug())
            System.out.println("hypervisor() called.");
    }
    public static void service(String[] args) {
        if(isDebug())
            System.out.println("service() called.");
    }
    public static void quotaSet(String[] args) {
        if(isDebug())
            System.out.println("quotaset() called.");
    }
    public static void flavor(String[] args) {
        if(isDebug())
            System.out.println("    flavor() called.");
    }
    public static void aggregate(String[] args) {
        if(isDebug())
            System.out.println("aggregate() called.");
    }
    public static void availabilityZone(String[] args) {
        if(isDebug())
            System.out.println("availabilityZone() called.");
    }

    /**
     * parse() : parse the top level command line arguments.
     *
     * @param   args : the same as args of main()
     * @return  LinkedHashMap of handler method and arguments for that.
     */
    private static Map<Method, String[]> parse(String[] args) {
        String command = args[0];

        int idx;
        for(idx = 0; idx < args.length; idx++) {
            if (args[idx].equals("--debug")) {
                debug = true;
            } else if (args[idx].equals("--log-message")) {
                logMessage = true;
            } else if (!args[idx].startsWith("--")) {
                command = args[idx];
                break;
            }
        }

        if(!cArray.containsKey(command)) {
            System.out.println("Unknown command: " + command);
            printUsage();
            System.exit(0);
        }

        String newargs[] = Arrays.copyOfRange(args, idx + 1, args.length);

        LinkedHashMap<Method, String[]> map =
            new LinkedHashMap<Method, String[]>();
        try {
            map.put(Jnova.class.getMethod(cArray.get(command), String[].class),
                    newargs);
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(0);
            //return null;
        }
        if (isDebug()) {
            System.out.println("DEBUG: command is: " + command);
            System.out.println("DEBUG: hanndler is: " + map);
            for (String s : newargs) {
                System.out.println("DEBUG: newargs: " + s);
            }
        }


        // Get account informatoin from environment variables.
        if (isDebug()) {
            System.out.println("OS_AUTH_URL    : " + osAuthUrl);
            System.out.println("OS_PASSWORD    : " + osPassword);
            System.out.println("OS_TENANT_NAME : " + osTenantName);
            System.out.println("OS_USERNAME    : " + osUsername);
        }
        return map;
    }

    public static boolean isDebug() {
        return debug;
    }

    public static boolean isLogMessage() {
        return logMessage;
    }

    /**
     * getNovaClient() : returns a valid Nova client class instance.
     *
     * @param   osAuthUrl    OS_AUTH_URL
     * @param   osPassword   OS_PASSWORD
     * @param   osTenantName OS_TENANT_NAME
     * @param   osUsername   OS_USERNAME
     * @return  Nova class (of openstack-java-sdk) instance
     */
    public static Nova getNovaClient(String osAuthUrl, String osPassword,
                                      String osTenantName, String osUsername) {
        try {
            // First, create a Keystone cliet class instance.
            Keystone keystoneClient = new Keystone(osAuthUrl);

            setupLog();

            // Set account information, and issue an authentication request.
            Access access = keystoneClient.tokens()
                .authenticate(new UsernamePassword(osUsername, osPassword))
                .withTenantName(osTenantName)
                .execute();
        
            String novaEndpoint = KeystoneUtils
                .findEndpointURL(access.getServiceCatalog(),
                                 "compute", null, "public");
            if (isDebug()) {
                System.out.println("DEBUG: " + novaEndpoint);
            }
            /*  
             * The a    bove contains TENANT_ID like:
             *   http://SERVICE_HOST:PORT/v1.1/TENANT_ID
             * according to endpoints definition in keystone configuration.
             * It's the same as keystone endpoint-list.
             *
             * Note that we don't need to append a '/' to the URL because
             * openstack-java-sdk library codes add it.
             *   Nova novaClient = new Nova(novaEndpoint.concat("/"));
             */

            // Create a Nova client object.
            Nova novaClient = new Nova(novaEndpoint);

            /*
             * Set the token now we got for the following requests.
             * Note that we can use the same token in the above keystone 
             * response unless it's not expired.
             */
            novaClient.token(access.getToken().getId());

            return novaClient;

        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("Failed to create/initialize a Nova client.");
            System.exit(0);
        }
        // never here
        return null;
    }

    private static void printUsage() {
        System.out.println("Usage: ");

        for (Map.Entry<String, String> entry : cArray.entrySet()) {
            System.out.println("    jnova " + entry.getKey());
            
        }
    }

    /**
     * main() : the main routine
     *
     * @param args
     */
    public static void main(String[] args) {
        
        if (args.length == 0) {
            printUsage();
            System.exit(0);
        }

        if (osAuthUrl == null || osPassword == null ||
            osTenantName == null || osUsername == null) {
            System.out.println("set OS_* environment variables.");
            System.exit(0);
        }

        // Parse comnand line arguments.
        boolean allTenants = false;

        /*
         * to be migrated to each handler
         */
        String command = null;
        for(int i = 0; i < args.length; i++) {
            if (args[i].equals("--all-tenants")) {
                allTenants = true;
            } else if ((command == null) && !args[i].startsWith("--")){ 
                command = new String(args[i]);
            }
        }

        Map<Method, String[]> c = parse(args);
        // parse returns only one pair of Map.
        for (Map.Entry<Method, String[]> entry : c.entrySet()) {
            Method m = (Method)entry.getKey();
            String[] cmdargs = (String[])entry.getValue();
            try {
                // Note(thatsdone):
                // Without the cast (Object) below, elements of cmdargs[]
                // will be handled as independent classes and causes an error.
                // Could be a pitfall.
                m.invoke(null, (Object)cmdargs);
            } catch (Exception e) {
                e.printStackTrace();
                System.exit(0);
            }
            break;
        }

        // getNovaClient() succeeds, or aborts the process.
        Nova novaClient = getNovaClient(osAuthUrl, osPassword,
                                        osTenantName, osUsername);

        /*
         * command handlers
         */
        if (command.equals("list")) {
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
            printJson(servers);
            if (isDebug()) {
                for (Server s : servers) {
                    System.out.println("Hypervisor     : "
                                       + s.getHypervisorHostname());
                    System.out.println("VM Name        : "
                                       + s.getInstanceName());
                    System.out.println("Flavor         : " +
                                       s.getFlavor().getId());
                    System.out.println("Instance Id    : " + s.getId());
                    System.out.println("Image Id       : " +
                                       s.getImage().getId());
                    System.out.println("Keypair Name   : " + s.getKeyName());
                    System.out.println("Instance Name  : " + s.getName());
                    System.out.println("Instance Status: " + s.getStatus());
                    System.out.println("Tenant Id      : " + s.getTenantId());
                    System.out.println("User Id        : " + s.getUserId());
                    System.out.println("Task State     : " + s.getTaskState());
                    System.out.println("VM State       : " + s.getVmState());
                    System.out.println("");
                }
            }

            //
            if (isDebug()) {
                for(Server server : servers) {
                    System.out.println(server);
                }
            }

        } else if (command.equals("show")) {
            if (args.length >= 2) {
                Server server = novaClient.servers().show(args[1]).execute();
                printJson(server);
            } else {
                System.out.println("Specify server id");
            }

        } else if (command.startsWith("host")) {
            // os-hosts : get per-host informatoin using /os-hosts extension
            if (command.equals("host-list")) {
                // nova host-list
                Hosts hosts = novaClient.hosts().list().execute();
                if (isDebug()) {
                    System.out.println(hosts);
                }
                printJson(hosts);
                if (isDebug()) {
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

            } else if (command.equals("host-describe")) {
                // nova host-describe HOSTNAME
                if (args.length >= 2) {
                    Host h = novaClient.hosts().show(args[1]).execute();
                    printJson(h);
                    if (isDebug()) {
                        System.out.println(h);
                    }
                } else {
                    System.out.println("Specify hostname");
                }
            }

        } else if (command.startsWith("hypervisor")) {
            // os-hypervisors :
            if (command.equals("hypervisor-list")) {
                // nova hypervisor-list
                Hypervisors hypervisors = novaClient.hypervisors().list()
                                          .execute();
                if (isDebug()) {
                    System.out.println(hypervisors);
                }
                printJson(hypervisors);

            } else if (command.equals("hypervisor-show")) {
                // nova hypervisor-show
                if (args.length < 2) {
                    System.out.println("Specify hypervisor id");
                    System.exit(0);
                }
                Hypervisor hv = novaClient.hypervisors()
                    .show(new Integer(args[1])).execute();
                printJson(hv);
                if (isDebug()) {
                    System.out.println(hv);
                }

            } else if (command.equals("hypervisor-stats")) {
                // nova hypervisor-stats
                HypervisorStatistics stat = novaClient.hypervisors()
                    .showStats().execute();
                printJson(stat);
                if (isDebug()) {
                    System.out.println(stat);
                }
            }

        } else if (command.startsWith("service")) {
            // os-services
            if (command.equals("service-list")) {
                // nova service-list
                Services services = novaClient.services().list().execute();
                printJson(services);
                if (isDebug()) {
                    for(Service service : services) {
                            System.out.println(service); 
                    } 
                }

            } else if (command.equals("service-disable")) {
                // nova service-disable HOST SERVIVCE
                if (args.length >= 3) {
                    Service resp = novaClient.services()
                        .disableService(args[1], args[2]).execute();
                    printJson(resp);    
                    if (isDebug()) {
                        System.out.println(resp);
                    }
                } else {
                    System.out.println("Specify host name and service binary name");
                }

            } else if (command.equals("service-enable")) { 
                // nova service-enable HOST SERVIVCE
                if (args.length >= 3) {
                    Service resp = novaClient.services()
                        .enableService(args[1], args[2]).execute();
                    printJson(resp);
                    if (isDebug()) {
                        System.out.println(resp);
                    }
                } else {
                    System.out.println("Specify host name and service binary name");
                }
            }

        } else if (command.equals("usage-list")) {
            /// os-simple-tenant-usage
            if (args.length >= 2) {
                // nova usage-list
                SimpleTenantUsage stu = novaClient.quotaSets()
                    .showUsage(args[1]).execute();
                printJson(stu);
                if (isDebug()) {
                    System.out.println(stu);
                }
            } else {
                System.out.println("Specify tenant id");
            }

        } else if (command.startsWith("aggregate")) {
            // os-aggregates
            if (command.equals("aggregate-list")) {
                // nova aggregate-list
                HostAggregates ags = novaClient.aggregates().list().execute();
                printJson(ags);
                if (isDebug()) {
                    System.out.println(ags);
                }

            } else if (command.equals("aggregate-details")) {
                // nova aggregate-details AGGREGATE_ID
                // does not work currently because of sdk (probably...)
                if (args.length >= 2) {
                    HostAggregate ag = novaClient.aggregates().
                        showAggregate(args[1]).execute();
                    printJson(ag);
                    if (isDebug()) {
                        System.out.println(ag);
                    }

                } else {
                    System.out.println("Specify tenant id");
                }
            }

        } else if (command.equals("availability-zone-list")) {
            // os-availability-zone
            // nova availability-zone-list
            AvailabilityZoneInfo az = novaClient.availabilityZoneInfo()
                .show(true).execute();
            printJson(az);
            if (isDebug()) {
                System.out.println(az);
            }

        } else if (command.equals("flavor-list")) {
            // flavors
            // nova flavor-list
            Flavors flavors = novaClient.flavors().list(true).execute();
            printJson(flavors);
            if (isDebug()) {
                System.out.println(flavors);
            }

        } else if (command.equals("live-migration")) {
            boolean block = false;
            boolean disk = false;
            if (args.length >= 3) {
                //System.out.println("len: " + args.length);
                for (int i = 3; i < args.length; i++) {
                    if (args[i].equals("--block-migrate")) {
                        block = true;
                    } else if (args[i].equals("--disk-over-commit")) {
                        disk = true;
                    } else {
                        System.out.println("Unknown option: " + args[i]);
                    }
                }
                //System.out.println("block: " + block + ", disk: " + disk);
                //System.exit(0);
                novaClient.servers()
                    .migrateLive(args[1], args[2], block, disk)
                    .execute();

            } else {
                System.out.println("Specify server_id and hostname");
            }

        } else {
            System.out.println("Unknown command :" + command);
        }
    }
}
