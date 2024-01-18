# oteltest1

A tiny test/exercise program for OpenTelemetry C++.

## Current Status

This example shows how to use various features of OpenTelemetry C++.

* Basic usage of OpenTelemetry including:
  * Processor
  * Exporter
  * Provider
  * Resource
  * Tracer
* OStream exporter
* OTEL/gRPC exporter
* Span
  * Basic StartSpan() and End()
  * Context Propagation (across function calls within a single process)
  * Set Span attributes
  * AddLink(s) (to other traces)
    * This requires ABI version 2

## Preparation

You need to build OpenTelemetry C++ (opentelemetry-cpp) at first.

https://github.com/open-telemetry/opentelemetry-cpp/

Basically, you can follow the official documentation at:

https://github.com/open-telemetry/opentelemetry-cpp/blob/main/INSTALL.md

But, if you like to build it on Ubuntu 22.04 using cmake,
Ubuntu 22.04 bundle versionlibgrpc-dev has an unresolved issue(*1)
as of Jan. 18, 2024, and this causes build issue.

* (*1) https://bugs.launchpad.net/ubuntu/+source/grpc/+bug/1935709

As of Jan 2024, I'm using Ubuntu 24.04 (beta) for opentelemetry-cpp
package build.
The below is the set of command line that I used to build opentelemetry-cpp
on Ubuntu 24.04. Note that ABI Version 2 is used below because I wanted to
use AddLink(s) to embed remote trace reference information.

1. Generate Makefiles
```
$ mkdir build && cd build && cmake -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DBUILD_SHARED_LIBS=ON -DWITH_OTLP_GRPC=ON -DWITH_ABI_VERSION_2=ON -DBUILD_TESTING:BOOL=OFF -DBUILD_PACKAGE=ON  ..
```
2. Build
```
$ date; time cmake --build . --target all; date
```
3. Create otel-cpp package
```
$ cpack -C debug
```
4. Install the package
```
$ sudo dpkg -i opentelemetry-cpp-1.13.0-ubuntu-24.04-x86_64.deb
```
Note that version number varies depending on the environment.

## Build

Just executre `make` command.


## TODO
* Context Propagation  with remote processes
  * HTTP (including gRPC/HTTP2, HTTP3)
  * Other protocols (MQTT, Kafka...)
* Use cmake (create CMakeList.txt)
* ...
