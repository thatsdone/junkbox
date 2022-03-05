/**
 * Jackson1.java : An example of jackson (http://jackson.codehaus.org/)
 * 
 * This is just an (exercise) example to handle layered JSON/object data
 * using a convenient library, 'jackson'.
 */
import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.map.ObjectWriter;
import org.codehaus.jackson.annotate.JsonIgnoreProperties;
import org.codehaus.jackson.annotate.JsonProperty;

import java.io.*;
import java.util.Map;
import java.util.LinkedHashMap;
import java.util.Collection;  
import java.util.List;
import java.util.ArrayList;

public class Jackson1 {

   @JsonIgnoreProperties(ignoreUnknown = true)
    private static class Instance {
	public String id;
	public String status;
    }
    
    @JsonIgnoreProperties(ignoreUnknown = true)
    private static class Node {
	public String name;
	public String status;
	public List<Instance> instances;
    }
    @JsonIgnoreProperties(ignoreUnknown = true)
    private static class Zone {
	public String name;
	public List<Node> nodes;
    }


    public static void main(String[] args) throws Exception {
	ObjectMapper mapper = new ObjectMapper();
        // Not sure if the belo works.
        //OobjectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
	Zone zone = mapper.readValue(new File("jackson1.json"), Zone.class);

	System.out.println("Output a parsed object using readValue() via writeValueAsString()");
	System.out.println(mapper.writeValueAsString(zone));

        //The below causes an warning. Why?
	ObjectWriter writer = mapper.defaultPrettyPrintingWriter();
	System.out.println("\nPrettyPrinting example");
	System.out.println(writer.writeValueAsString(zone));


	System.out.println("\nObject traversal example.");
	System.out.println("zone : " + zone.name);
	Collection<Node> nodes = zone.nodes;
	for (Node n : nodes) {
	    System.out.println("  Node: " + n.name);
	    for (Instance i : n.instances) {
		System.out.println("    id     : " + i.id);
		System.out.println("    status : " + i.status);
	    }
	}

	zone.name = "zone1x";
	System.out.println("\nRewirte parsed object by readValueAsString() example.");
	System.out.println(mapper.writeValueAsString(zone));

/*
	Zone zone2 = new Zone();
	zone2.name = "zone2";
	System.out.println(mapper.writeValueAsString(zone2));

	Node tmpnode = new Node();
	tmpnode.name = "cnw06003";
	//zone2.nodes = new Collection<Node>();
	System.out.println(tmpnode);
		// causes an exception.
	zone2.nodes.add(tmpnode);
	System.out.println(mapper.writeValueAsString(zone2));	
*/
	Map<String, Object> o = createExample();
	System.out.println("\nOutput internally constructed object by writeValueAsString() example.");
	System.out.println(mapper.writeValueAsString(o));

    }

    private static Map<String, Object> createExample() {
	// LinkedHashMap honors the order of objects pushed.
	Map<String, Object> map = new LinkedHashMap<String, Object>();
	map.put("name", "zone3");

	List<Node> nodes = new ArrayList<Node>();
	map.put("nodes", nodes);
	Node node1 = new Node();

	nodes.add(node1);
	node1.name = "opsthv01";
	node1.status = "POWER_ON";
	
	List<Instance> instances = new ArrayList<Instance>();
	node1.instances = instances;

	Instance i1 = new Instance();
	i1.id = "5c41f3da-a9e1-46e7-b53c-7f05a11f622d";
	Instance i2 = new Instance();
	i2.id = "f3da5c41-e1a9-e746-3cb5-7f05a11f622d";
	node1.instances.add(i1);
	node1.instances.add(i2);
	//map.add("nodes", node1);
	//Class<ArrayList<Node>>ns = (Class<ArrayList<Node>>)nodes.getClass();


	return map;
    }
}


/**
 jacson1.json sample

{
	"name": "zone1",
	"nodes": [
		 {
	            "name": "opsthv01",
	            "status": "POWER_ON",
	            "hypervisor": "kvm",
	            "instances": [
	                {"id": "5c41f3da-a9e1-46e7-b53c-7f05a11f622d" },
	                {"id": "5c41f3da-a9e1-46e7-b53c-7f05a11fxxxx" }
			]
		},
	        {
	            "name": "opstsvc02",
	            "status": "POWER_ON",
	            "instances": [
	                {"id": "279fe06d-76dd-4383-9768-46f8339a0889",
			 "status": "ACTIVE" },
	                {"id": "81f61b67-1fb8-4923-9f44-9f4090aaec02",
			  "status": "MIGRATING" }
	            ]
	        }
	]
}
*/
    
