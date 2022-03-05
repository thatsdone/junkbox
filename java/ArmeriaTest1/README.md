# ArmeriaTest1

## Overview

Just a "Hello, world!" program at the moment to learn Armeria.

## Usage


Build is straight foward.

```
$ mvn clean package
```

If you want to see just ArmeriaTest1 log:

```
$ java -Dorg.slf4j.simpleLogger.defaultLogLevel=WARN -Dorg.slf4j.simpleLogger.log.com.github.thatsdone=DEBUG  -jar target/ArmeriaTest1-1.0-SNAPSHOT.jar
```

From another terminal, execute for example:

```
$ curl -v http://localhost:18080/api/operation
$ curl -v -X POST http://localhost:18080/api/operation -d "foo bar"
etc.
```

## References
* https://armeria.dev/
* https://armeria.dev/docs
* https://armeria.dev/docs/server-basics
* https://github.com/line/armeria
* https://www.slf4j.org/api/org/slf4j/impl/SimpleLogger.html

* https://javadoc.io/doc/com.linecorp.armeria/armeria-javadoc/latest/com/linecorp/armeria/server/Server.html
* https://javadoc.io/doc/com.linecorp.armeria/armeria-javadoc/latest/com/linecorp/armeria/server/ServerBuilder.html


