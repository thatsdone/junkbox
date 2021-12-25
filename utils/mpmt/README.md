# mpmt : Multi-Process Multi-Thtread examples

This directory contains various (normally) small example programs to see
hehaviour differences of multi-process and multi-thread programming model
frameworks of various languages.

## 1. A simple busy loop workload generator

* Usage

Common across langugages.

```
  $ PROGRAM [-n NUM_CONTEXT] [-d DURATION] [-m MODE]
```

* NUM_CONTEXT
  * number of execution contexts (thread, process or so) default: 4
* DURATION
  * number (in seconds) default: 5 (seconds)
  * duration to generate CPU load
* MODE
  * t or T : thread model (default)
  * p or P : process model

* Languages
  * Python3: mpmt1.py
    * Uses python threading and multiprocessing.
  * C: mpmt1.c
    * Uses pthread and fork().
    * Build
      * `gcc -o mpmt1 mpmt1.c -lpthread`
  * Go: mpmt1.go
  * Uses goroutine. No process model at the moment.
    * Simply `go run mpmt1.go`, or
    * `go build -o mpmt1go mpmt1.go`

* Notes
  * Run the executables on a server at least 2 (v)CPUs.
  * Observe CPU usage by using top command for example. (Better to refresh frequently using '-d 1'.)
  * You would see python threading model can consume only 1 CPU (100%) even if there were multiple CPUs and you specifed more than 2 contexts.
