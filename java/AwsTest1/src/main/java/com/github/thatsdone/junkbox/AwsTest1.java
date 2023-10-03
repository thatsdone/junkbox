package com.github.thatsdone.junkbox;
/**
 * AwsTest1 : A simple AWS Java SDK v2 example.
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
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.ParseException;
import org.apache.commons.cli.HelpFormatter;

public class AwsTest1 {

    public static void main(String[] args) throws Exception {

        Options options = new Options();
        Option help = new Option("help", "print this message");
        CommandLineParser parser = new DefaultParser();
        CommandLine cmd = null;

        String accessKeyId = null;
        String secretAccessKey = null;
        Region region = null;
        String profile = null;

        options.addOption(help);
        options.addOption("a", true, "accessKey");
        options.addOption("s", true, "secretKey");
        options.addOption("r", true, "region");
        options.addOption("p", true, "profile");

        cmd = parser.parse(options, args);
        if (cmd.hasOption("help")) {
            HelpFormatter formatter = new HelpFormatter();
            formatter.printHelp("AwsTest1", options);
            System.exit(0);
        }
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
