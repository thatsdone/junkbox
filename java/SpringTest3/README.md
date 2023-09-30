# SpringTest3

SpringTest3 is an exercise program for Spring Framework Native Image.

As of the initial commit, basically it's based on Spring official documentation.

## How to build and run

1. Install GraalVM
    * See https://sdkman.io/ for example.
2. Build
    * `mvn -Pnative native:compile`
    * This can take several minutes.
3. Run
    * `target/SpringTest3`
4. Access
    * `curl -v http://localhost:8080/`

## TODO
* Create native 'image'
    * Currently `mvn -Pnative spring-boot:build-image` does not work.

## References
* https://docs.spring.io/spring-boot/docs/current/reference/html/native-image.html
* https://docs.spring.io/spring-boot/docs/current/reference/html/getting-started.html
* https://sdkman.io/

## Notes
* JVM version
```
$ java -version
openjdk version "17.0.5" 2022-10-18 LTS
OpenJDK Runtime Environment GraalVM 22.3.0 (build 17.0.5+8-LTS)
OpenJDK 64-Bit Server VM GraalVM 22.3.0 (build 17.0.5+8-LTS, mixed mode, sharing)
```
* size differences
```
$ du  target/SpringTest3   target/SpringTest3-0.0.1-SNAPSHOT.jar
73492   target/SpringTest3
19048   target/SpringTest3-0.0.1-SNAPSHOT.jar
```
strip does not have significant effect.
```
$ du  target/SpringTest3  target/SpringTest3.stripped
73492   target/SpringTest3
73344   target/SpringTest3.stripped
```

* invocation time
    * native: 35~50 ms
    * jar: 2~3 seconds
    * Obviously, it depends on local filesystem cache.
* Below section in pom.xml is essential for Native Image.
```
<plugin>
  <groupId>org.graalvm.buildtools</groupId>
  <artifactId>native-maven-plugin</artifactId>
</plugin>
```
* Below section in pom.xml is intended for stand alone

