package com.github.thatsdone.junkbox;
/**
 * ObsTest1 : A simple Huawei Cloud Object Storage Service(OBS) example.
 * 
 * Description: 
 * Author: Masanori Itoh <masanori.itoh@gmail.com>
 */

import java.util.*;
import java.io.*;
import org.apache.commons.io.FileUtils;

import com.obs.services.*;
import com.obs.services.model.*;

public class ObsTest1
{
    public static void main( String[] args ) throws Exception
    {
	String ak = System.getenv("HW_ACCESS_KEY");
	String sk = System.getenv("HW_SECRET_KEY");
	String endPoint = System.getenv("HW_ENDPOINT");
	String location = null;

	/**
	 * Constants
	 *   Chenge the below depending on your environment.
	 */
	String bucketname1 = "testbucket1";
	String objectname1 = "esdk-obs-java-3.21.4.zip";
	String save_objectname1 = "tmp1.zip";

	/**
	 * Check credentials and endpoint information.
	 */
	if (ak == null || sk == null || endPoint == null) {
	    System.out.printf("ERROR: Set HW_ACCESS_KEY and HW_SECRET_KEY and HW_ENDPOINT\n");
	    System.exit(255);
	}

	String[] epa = endPoint.split("\\.");
	System.out.printf("DEBUG: %s / %s\n", endPoint, Arrays.toString(epa));
	if (epa.length >= 3 &&
	    epa[0].equals("https://obs") &&
	    epa[2].equals("myhuaweicloud")) {
	    System.out.printf("DEBUG: region is %s\n", epa[1]);
	    location = epa[1];
	}
	if (location == null) {
	    System.out.printf("ERROR: Failed to extract region(location) from HW_ENDPOINT: %s\n", endPoint);
	    System.exit(255);
	}	    

        System.out.printf( "Huwei Cloud Object Storage (Native API) test.\n");
        System.out.printf( "Using:\n");
        System.out.printf( "    ak: %s\n", ak);
        System.out.printf( "    sk: %s\n", sk);
        System.out.printf( "    endpoint: %s\n", endPoint);
        System.out.printf( "    region: %s\n", location);

	// Here we go.

	// Create an instance of ObsClient.
	ObsClient obsClient = new ObsClient(ak, sk, endPoint);

	// List buckets.
	/** comment out for now
	ListBucketsRequest request = new ListBucketsRequest();
	request.setQueryLocation(true);
	List<ObsBucket> buckets = obsClient.listBuckets(request);
	for(ObsBucket bucket : buckets){
	    System.out.println("BucketName:" + bucket.getBucketName());
	    System.out.println("CreationDate:" + bucket.getCreationDate());
	    System.out.println("Location:" + bucket.getLocation());
	    System.out.printf("\n");
	    ObjectListing objectListing = obsClient.listObjects(bucket.getBucketName());
	    for (ObsObject object : objectListing.getObjects()) {
		System.out.printf("%s / %s / %d\n", object.getObjectKey(), object.getMetadata().getEtag(), object.getMetadata().getContentLength());
		System.out.println(object);
	    }
	    System.out.printf("\n");
	}
	*/

	// create a bucket
	ObsBucket obsBucket = new ObsBucket();
	CreateBucketRequest request = new CreateBucketRequest();
	try {
	    System.out.printf("Creating a bucket %s\n", bucketname1);
	    request.setBucketName(bucketname1);
	    //ACL?
	    //storage class?
	    request.setLocation(location); // region
	    //multi-az bucket?
	    HeaderResponse response = obsClient.createBucket(request);
	    System.out.println(response);
	} catch (Exception e) {
	    e.printStackTrace();
	    obsClient.close();
	    System.exit(255);
	} finally {
	    ;
	}

	//put an object
	try {
	    System.out.printf("Creating an object %s/%s\n",
			      bucketname1, objectname1);
	    ByteArrayInputStream bis1 = new ByteArrayInputStream(FileUtils.readFileToByteArray(new File(objectname1)));
	    HeaderResponse response = obsClient.putObject(bucketname1, objectname1, bis1, null);
	    System.out.println(response);
	} catch (Exception e) {
	    e.printStackTrace();
	    obsClient.close();
	    System.exit(255);
	} finally {
	    ;
	}

	//get the object
	ObsObject obsObject = null;
	try {
	    System.out.printf("Getting an object %s/%s into %s\n",
			      bucketname1, objectname1, save_objectname1);
	    obsObject = obsClient.getObject(bucketname1, objectname1, null);
	    InputStream input = obsObject.getObjectContent();
	    FileUtils.copyInputStreamToFile(input, new File(save_objectname1));
	    
	    System.out.printf("Download and save completed\n");

	} catch (Exception e) {
	    e.printStackTrace();
	    obsClient.close();
	    System.exit(255);
	} finally {
	    ;
	}
	
	//delete the object
	try {
	    System.out.printf("Deleting an object %s/%s\n",
			      bucketname1, objectname1);
	    HeaderResponse response = obsClient.deleteObject(bucketname1, objectname1, null);
	    System.out.println(response);

	} catch (Exception e) {
	    e.printStackTrace();
	    obsClient.close();
	    System.exit(255);
	} finally {
	    ;
	}
	    
	// delete the bucket
	try {
	    System.out.printf("Deleting a bucket %s\n", bucketname1);
	    HeaderResponse response = obsClient.deleteBucket(bucketname1);
	    System.out.println(response);

	} catch (Exception e) {
	    e.printStackTrace();
	    obsClient.close();
	    System.exit(255);
	} finally {
	    ;
	} 

	obsClient.close();
    }
}
