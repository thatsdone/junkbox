# QuarkusTest1

An exercise using Quarkus.

Based on:

https://github.com/quarkusio/quarkus-quickstarts/tree/main/getting-started



# How to run

```
$ mvn wrapper:wrapper
$ mvn -N io.takari:maven:wrapper
$ ./mvnw package
$ java jar target/quarkus-app/quarkus-run.jar
$ curl http://localhost:18080/api/metrics/foo
$ curl -X POST http://localhost:18080/api/operation -d "foo"

```

You can change the listening port by modifying `quarkus.http.port=18080`
in `src/main/resources/application.properties`
