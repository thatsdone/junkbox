package com.github.thatsdone.junkbox;
/**
 * AwsTest1SNS : SNS implementation for AwsTest1
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

import software.amazon.awssdk.services.sns.model.SnsException;
import software.amazon.awssdk.services.sns.SnsClient;
import software.amazon.awssdk.services.sns.model.ListTopicsRequest;
import software.amazon.awssdk.services.sns.model.ListTopicsResponse;
import software.amazon.awssdk.services.sns.model.Topic;
//
import org.apache.commons.cli.CommandLine;

public class AwsTest1SNS {

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

        SnsClient sns;
        if (accessKeyId != null) {
            AwsBasicCredentials cred =
                AwsBasicCredentials.create(accessKeyId, secretAccessKey);
            sns = SnsClient.builder()
                .region(region)
                .credentialsProvider(StaticCredentialsProvider.create(cred))
                .build();
        } else if (profile != null) {
            sns = SnsClient.builder()
                .region(region)
                .credentialsProvider(ProfileCredentialsProvider
                                     .create(profile))
                .build();
        } else {
            sns = SnsClient.builder()
                .region(region)
                .credentialsProvider(EnvironmentVariableCredentialsProvider
                                     .create())
                .build();
        }

        try {
            ListTopicsRequest lqreq = ListTopicsRequest.builder().build();
            ListTopicsResponse lqrep = sns.listTopics(lqreq);
            List<Topic> topics = lqrep.topics();
            if (topics.size() > 0) {
                for (Topic topic : topics) {
                    System.out.format("%s\n", topic.topicArn());
                }
            } else {
                System.out.println("No SNS topics found.");
            }

        } catch (SnsException e) {
            System.out.println(e.awsErrorDetails().errorMessage());
        }
    }
}
