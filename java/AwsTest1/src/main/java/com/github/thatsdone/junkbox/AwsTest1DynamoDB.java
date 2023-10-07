package com.github.thatsdone.junkbox;
/**
 * AwsTest1DynamoDB : DynamoDB implementation for AwsTest1
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

import software.amazon.awssdk.services.dynamodb.model.DynamoDbException;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.ListTablesRequest;
import software.amazon.awssdk.services.dynamodb.model.ListTablesResponse;
//
import org.apache.commons.cli.CommandLine;

public class AwsTest1DynamoDB {

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

        DynamoDbClient dynamo;
        if (accessKeyId != null) {
            AwsBasicCredentials cred =
                AwsBasicCredentials.create(accessKeyId, secretAccessKey);
            dynamo = DynamoDbClient.builder()
                .region(region)
                .credentialsProvider(StaticCredentialsProvider.create(cred))
                .build();
        } else if (profile != null) {
            dynamo = DynamoDbClient.builder()
                .region(region)
                .credentialsProvider(ProfileCredentialsProvider
                                     .create(profile))
                .build();
        } else {
            dynamo = DynamoDbClient.builder()
                .region(region)
                .credentialsProvider(EnvironmentVariableCredentialsProvider
                                     .create())
                .build();
        }

        try {
            ListTablesRequest ltreq = ListTablesRequest.builder().build();
            ListTablesResponse ltrep = dynamo.listTables(ltreq);
            List<String> tables = ltrep.tableNames();
            if (tables.size() > 0) {
                for (String table : tables) {
                    System.out.format("%s\n", table);
                }
            } else {
                System.out.println("No DynamoDB tables found.");
            }

        } catch (DynamoDbException e) {
            System.out.println(e.awsErrorDetails().errorMessage());
        }
    }
}
