# AwsTest1

AwsTest1 is an exercise program for AWS Java SDK v2.

As of now, only `aws s3 ls` equievalent is implemented.

## How to build and run

1. Build
    * `mvn clean package`
2. Run
    * Specify AWS credentials using from 3 choices below.variables or options
        1. Explicitly specify access_key_id/secret_access_key(and region)
        2. Specify awscli profile
        3. Specify environment variables
    * `java -jar target/Aws-1.0-SNAPSHOT-jar-with-dependencies.jar`

You can see help messages like below.

```
$ java -jar target/AwsTest1-1.0-SNAPSHOT-jar-with-dependencies.jar  -help
usage: AwsTest1
 -a <arg>   accessKey
 -help      print this message
 -p <arg>   profile
 -r <arg>   region
 -s <arg>   secretKey
```

## TODO
* Dynamodb
* Kinesis
* SQS
* ...

## References
* Official documentation
    * https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/home.html
* Official API References
    * https://sdk.amazonaws.com/java/api/latest/index.html
* Official examples
    * https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/javav2
