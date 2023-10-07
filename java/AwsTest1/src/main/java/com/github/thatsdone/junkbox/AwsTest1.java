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
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.ParseException;
import org.apache.commons.cli.HelpFormatter;

import com.github.thatsdone.junkbox.AwsTest1S3;
import com.github.thatsdone.junkbox.AwsTest1DynamoDB;

public class AwsTest1 {

    public static void main(String[] args) throws Exception {

        Options options = new Options();
        Option help = new Option("help", "print this message");
        CommandLineParser parser = new DefaultParser();
        CommandLine cmd = null;

        options.addOption(help);
        options.addOption("a", true, "accessKey");
        options.addOption("s", true, "secretKey");
        options.addOption("r", true, "region");
        options.addOption("p", true, "profile");
        options.addOption("S", true, "AWS service (default: S3)");

        cmd = parser.parse(options, args);
        if (cmd.hasOption("help")) {
            HelpFormatter formatter = new HelpFormatter();
            formatter.printHelp("AwsTest1", options);
            System.exit(0);
        }
        if (cmd.hasOption("S")) {
            String service = cmd.getOptionValue("S");
            if (service.equals("s3")) {
                AwsTest1S3 s3 = new AwsTest1S3();
                s3.run(cmd);
            } else if (service.equals("dynamo")) {
                AwsTest1DynamoDB dynamo = new AwsTest1DynamoDB();
                dynamo.run(cmd);
            } else if (service.equals("sqs")) {
                AwsTest1SQS sqs = new AwsTest1SQS();
                sqs.run(cmd);
            }
        } else {
            //default
            AwsTest1S3 s3 = new AwsTest1S3();
            s3.run(cmd);
        }
    }
}
