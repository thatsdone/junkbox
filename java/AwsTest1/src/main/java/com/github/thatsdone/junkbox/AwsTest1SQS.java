package com.github.thatsdone.junkbox;
/**
 * AwsTest1SQS : SQS implementation for AwsTest1
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

import software.amazon.awssdk.services.sqs.model.SqsException;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.ListQueuesRequest;
import software.amazon.awssdk.services.sqs.model.ListQueuesResponse;
//
import org.apache.commons.cli.CommandLine;

public class AwsTest1SQS {

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

        SqsClient sqs;
        if (accessKeyId != null) {
            AwsBasicCredentials cred =
                AwsBasicCredentials.create(accessKeyId, secretAccessKey);
            sqs = SqsClient.builder()
                .region(region)
                .credentialsProvider(StaticCredentialsProvider.create(cred))
                .build();
        } else if (profile != null) {
            sqs = SqsClient.builder()
                .region(region)
                .credentialsProvider(ProfileCredentialsProvider
                                     .create(profile))
                .build();
        } else {
            sqs = SqsClient.builder()
                .region(region)
                .credentialsProvider(EnvironmentVariableCredentialsProvider
                                     .create())
                .build();
        }

        try {
            ListQueuesRequest lqreq = ListQueuesRequest.builder().build();
            ListQueuesResponse lqrep = sqs.listQueues(lqreq);
            List<String> queues = lqrep.queueUrls();
            if (queues.size() > 0) {
                for (String url : queues) {
                    System.out.format("%s\n", url);
                }
            } else {
                System.out.println("No SQS queues found.");
            }

        } catch (SqsException e) {
            System.out.println(e.awsErrorDetails().errorMessage());
        }
    }
}
