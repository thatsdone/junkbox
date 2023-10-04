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

        cmd = parser.parse(options, args);
        if (cmd.hasOption("help")) {
            HelpFormatter formatter = new HelpFormatter();
            formatter.printHelp("AwsTest1", options);
            System.exit(0);
        }
        AwsTest1S3 s3 = new AwsTest1S3();
        s3.run(cmd);
    }
}
