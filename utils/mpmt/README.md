# mpmt : Multi-Process Multi-Thtread examples

This directory contains various (normally) small example programs to see
hehaviour differences of multi-process and multi-thread programming model
frameworks of various languages.

## 1. A simple busy loop workload generator

* Usage

Common across languages.

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
    * In case of golang, 'g' (goroutine).
  * p or P : process model

* Languages
  * Python3: mpmt1.py
    * Uses python threading and multiprocessing.
  * C: mpmt1.c
    * Uses pthread and fork().
    * Build
      * Simplly `make c`, and execute `./mpmt1c`
  * Go: mpmt1.go
      * Uses goroutine. No process model at the moment.
      * Simply `go run mpmt1.go` or`make go`, and `./mpmt1go`
  * Rust: mpmt1.rs
      * Implements thread model only. No process model at the moment.
      * Use nightly tool chain as this uses 'crate'.
      * Simply `make rust `, and `./mpmt1rs`
  * Ruby: mpmt1.rb
      * Implements thread model only. No process model at the moment.
  * Node.js: mpmt1.js
      * Implements thread model only. No process model at the moment.
      * Install 'posix-getopt'
  * Scala: mpmt1.scala
      * Implements thread model only. No process model at the moment.
      * In case of Ubuntu, use scala3.
      * Simply `make scala `, and `scala mpmt1`
  * Lua mpmt1.lua
      * Uses coroutine of Lua. No multi thread nor process at the moment.
      * To be updated to use getopt.
  * Common Lisp mpmt1.lisp
      * Implements thread model only using 'bordeaux-threads'. No multi process at the moment.
      * Runs under sbcl.
      * Still buggy...

* Notes
  * Run the executables on a server at least 2 (v)CPUs.
  * Observe CPU usage by using top command for example. (Better to refresh frequently using '-d 1'.)
  * You would see python threading model can consume only 1 CPU (100%) even if there were multiple CPUs and you specifed more than 2 contexts.
