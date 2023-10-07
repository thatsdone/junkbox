package com.github.thatsdone.junkbox;
/**
 * AwsTest1Kinesis : Kinesis implementation for AwsTest1
 *
 * License:
 *   Apache License, Version 2.0
 * History:
 *   2022/10/07 v0.1 Initial version
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

import software.amazon.awssdk.services.kinesis.model.KinesisException;
import software.amazon.awssdk.services.kinesis.KinesisClient;
import software.amazon.awssdk.services.kinesis.model.ListStreamsRequest;
import software.amazon.awssdk.services.kinesis.model.ListStreamsResponse;
//
import org.apache.commons.cli.CommandLine;

public class AwsTest1Kinesis {

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

        KinesisClient kinesis;
        if (accessKeyId != null) {
            AwsBasicCredentials cred =
                AwsBasicCredentials.create(accessKeyId, secretAccessKey);
            kinesis = KinesisClient.builder()
                .region(region)
                .credentialsProvider(StaticCredentialsProvider.create(cred))
                .build();
        } else if (profile != null) {
            kinesis = KinesisClient.builder()
                .region(region)
                .credentialsProvider(ProfileCredentialsProvider
                                     .create(profile))
                .build();
        } else {
            kinesis = KinesisClient.builder()
                .region(region)
                .credentialsProvider(EnvironmentVariableCredentialsProvider
                                     .create())
                .build();
        }

        try {
            ListStreamsRequest lsreq = ListStreamsRequest.builder().build();
            ListStreamsResponse lsrep = kinesis.listStreams(lsreq);
            List<String> streams = lsrep.streamNames();
            if (streams.size() > 0) {
                for (String name : streams) {
                    System.out.format("%s\n", name);
                }
            } else {
                System.out.println("No Kinesis streams found.");
            }

        } catch (KinesisException e) {
            System.out.println(e.awsErrorDetails().errorMessage());
        }
    }
}
