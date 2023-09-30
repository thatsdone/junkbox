# SpringTest2

SpringTest2 is an exercise program for Spring Functions

As of the initial commit, basically it's based on Spring official documentation.

## How to build and run

1. Build
    * `mvn clean package`
3. Run
    * `java -jar target/SpringTest2-0.0.1-SNAPSHOT.jar`
4. Access
    * `curl -v -d "foo" http://localhost:8080/uppercase`
    * `curl -v --data-binary @SOME_FILE -H "Content-Type: application/octet-stream" http://localhost:8080/operation`

## TODO
* Explore the reason why /operation handler says 'GET' for 'POST /operation' with body request.

## References
* https://cloud.spring.io/spring-cloud-function/reference/html/spring-cloud-function.html
* https://stackoverflow.com/questions/57514826/how-to-map-functions-to-rest-compliant-endpoints-with-spring-cloud-function
