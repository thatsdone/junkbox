package com.github.thatsdone.junkbox;
/**
 * AwsTest1S3 : S3 implementation for AwsTest1
 *
 * License:
 *   Apache License, Version 2.0
 * History:
 *   2022/10/03 v0.1 Initial version
 * Author:
 *   Masanori Itoh <masanori.itoh@gmail.com>
 */

import java.util.List;
//
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.auth.credentials.ProfileCredentialsProvider;

import software.amazon.awssdk.auth.credentials.EnvironmentVariableCredentialsProvider;

import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.ListBucketsRequest;
import software.amazon.awssdk.services.s3.model.ListBucketsResponse;
import software.amazon.awssdk.services.s3.model.S3Exception;
import software.amazon.awssdk.services.s3.model.S3Object;
import software.amazon.awssdk.services.s3.model.Bucket;
import software.amazon.awssdk.services.s3.model.S3Exception;
//
import org.apache.commons.cli.CommandLine;

public class AwsTest1S3 {

    public void run(CommandLine cmd) {
        String accessKeyId = null;
        String secretAccessKey = null;
        Region region = null;
        String profile = null;

        if (cmd.hasOption("a")) {
            accessKeyId = cmd.getOptionValue("a");
        }
        if (cmd.hasOption("s")) {
            secretAccessKey = cmd.getOptionValue("s");
        }
        if (cmd.hasOption("r")) {
            region = Region.of(cmd.getOptionValue("r"));
        }
        if (cmd.hasOption("p")) {
            profile = cmd.getOptionValue("p");
        }
        System.out.println(accessKeyId + " / " + secretAccessKey + " / " +
                           region);

        S3Client s3;
        if (accessKeyId != null) {
            AwsBasicCredentials cred =
                AwsBasicCredentials.create(accessKeyId, secretAccessKey);
            s3 = S3Client.builder()
                .region(region)
                .credentialsProvider(StaticCredentialsProvider.create(cred))
                .build();
        } else if (profile != null) {
            s3 = S3Client.builder()
                .region(region)
                .credentialsProvider(ProfileCredentialsProvider
                                     .create(profile))
                .build();
        } else {
            s3 = S3Client.builder()
                .region(region)
                .credentialsProvider(EnvironmentVariableCredentialsProvider
                                     .create())
                .build();
        }

        try {
            ListBucketsRequest lbreq = ListBucketsRequest.builder().build();
            ListBucketsResponse lbrep = s3.listBuckets(lbreq);
            //System.out.println(lbrep.buckets());
            for (Bucket bucket : lbrep.buckets()) {
                System.out.println(bucket.name());
            }
        } catch (S3Exception e) {
            System.out.println(e.awsErrorDetails().errorMessage());
        }
    }
}
