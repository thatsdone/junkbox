# PahoTest1

PahoTest1 is an exercise program for Eclipse Paho.

I wrote this in order to know how to use UserProperty of MQTTv5 especially.

## How to build and run

1. Build
    * `mvn clean package`
2. Run
    * Specify 3 environment variables
        1. MQTT_BROKER (ex. tcp://192.168.1.1:1833)
        2. MQTT_PUB_TOPIC (ex. pubtopic1)
        3. MQTT_SUB_TOPIC (ex. subtopic1)
    * `java -cp target/PahoTest1-1.0-SNAPSHOT-jar-with-dependencies.jar com.github.thatsdone.junkbox.PahoTest1`
3. Use other program to subscribe and publish to the above topics (pub/sub)
## TODO
* Add option support using Apache Commons CLI.

## References
* Source code of Paho Java implementation
    * https://github.com/eclipse/paho.mqtt.java
    * Eclipse Paho Java documentation has only MQTTv3 APIs as of now. :(
* https://github.com/jpwsutton/EclipsePahoJavaMQTTv5Example/
