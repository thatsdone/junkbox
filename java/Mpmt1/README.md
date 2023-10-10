# Java19Test1

At the moment, just an example of Java19 Virtual Thread.

Tested using openjdk-19-jdk on Ubuntu 22.04.

```
$ java -version
openjdk version "19.0.2" 2023-01-17
OpenJDK Runtime Environment (build 19.0.2+7-Ubuntu-0ubuntu322.04)
OpenJDK 64-Bit Server VM (build 19.0.2+7-Ubuntu-0ubuntu322.04, mixed mode, sharing)
```

```
$ java -jar target/Mpmt
1-1.0-SNAPSHOT-jar-with-dependencies.jar  -help
usage: Mpmt1
 -d <arg>   Duration(sec.)
 -help      print this message
 -n <arg>   Number of threads
 -s <arg>   Sleep(sec.)
 -v         Use Java 19 Virtual Thread
```

## Virtual thread mode

As of October 2023, using the above version, specify `--enable-preview` option.
Also, as a Virtual Thread seems to terminate on join() call, we need to
wait enough long time. In the below example, Mpmt1 waits 3 seconds
for 3 seconds busy worker.

Note that only 2 virtual threads actually completed (duration expired).

```
$ java --enable-preview -jar target/Mpmt1-1.0-SNAPSHOT-jar-with-dependencies.jar  -v -d 3 -s 3
main: parallelism: null maxPollSize: null minRunnable: null
main: availableProcessors: 1 maxMemory: 502792192 totalMemory: 32440320 freeMemory: 30345400
main: starting: 0
main: starting: 1
main: starting: 2
main: starting: 3
main: Virtual Thread mode. Sleeping...
worker::run: ts: 1696943213885 index = 0 isVirtual: true
worker::run: ts: 1696943213891 index = 1 isVirtual: true
main: Calling join() to each thread.
main: thread join() returned. 0 Thread[#14,Thread-0,5,main]
main: thread join() returned. 1 Thread[#15,Thread-1,5,main]
main: thread join() returned. 2 Thread[#16,Thread-2,5,main]
main: thread join() returned. 3 Thread[#17,Thread-3,5,main]
$
```

## Normal mode

Note that the first join() was called before the 4th thread (index = 3) starting message,
and they block until worker threads return.

```
$ java --enable-preview -jar target/Mpmt1-1.0-SNAPSHOT-jar-with-dependencies.jar  -d 3
main: parallelism: null maxPollSize: null minRunnable: null
main: availableProcessors: 1 maxMemory: 502792192 totalMemory: 32440320 freeMemory: 30345392
main: starting: 0
main: starting: 1
worker::run: ts: 1696943252555 index = 0 isVirtual: false
main: starting: 2
worker::run: ts: 1696943252561 index = 1 isVirtual: false
main: starting: 3
worker::run: ts: 1696943252563 index = 2 isVirtual: false
main: Calling join() to each thread.
worker::run: ts: 1696943252571 index = 3 isVirtual: false
worker::run: 1 expired. 17538695
worker::run: 0 expired. 17658478
main: thread join() returned. 0 Thread[#14,Thread-0,5,]
main: thread join() returned. 1 Thread[#15,Thread-1,5,]
worker::run: 2 expired. 17592779
main: thread join() returned. 2 Thread[#16,Thread-2,5,]
worker::run: 3 expired. 17722992
main: thread join() returned. 3 Thread[#17,Thread-3,5,]
$
```

## References

* https://openjdk.org/jeps/425
* https://cr.openjdk.org/~rpressler/loom/Loom-Proposal.html
* https://blog.rockthejvm.com/ultimate-guide-to-java-virtual-threads/
* https://blogs.oracle.com/javamagazine/post/going-inside-javas-project-loom-and-virtual-threads
* https://devlog.atlas.jp/2023/03/29/5065 (Japanese)
* https://gihyo.jp/article/2022/08/tfc003-java19 (Japanese)
