# mpmt : Multi-Process Multi-Thtread examples

This directory contains various (normally) small example programs to see
hehaviour differences of multi-process and multi-thread programming model
frameworks of various languages.

1. A simple busy loop workload generator

* Usage

Common across langugages.

```
  $ PROGRAM [-n NUM_CONTEXT] [-d DURATION]
```

* NUM_CONTEXT
  * number of execution contexts (thread, process or so)
* DURATION
  * number (in seconds)
  * duration to generate CPU load
* MODE
  * t or T : thread model
  * p or P : process model

* Languages
  * Python: mpmt1.py
    * Uses python threading and multiprocessing.
  * C: mpmt1.c
    * Uses pthread and fork.
    * Build
      * `gcc -o mpmt1 mpmt1.c -lpthread`

* Notes
  * Run the executables on a server at least 2 (v)CPUs.
  * Observe CPU usage by using top command for example. (Better to refresh frequently using '-d 1' for example.)
  * You would see python threading model can consume only 1 CPU (100%) even if there were multiple CPUs and you specifed more than 2 contexts.
