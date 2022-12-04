# C sharp exercise

This folder contains C# exercise files.

To be updated.

* Environment
    * Ubuntu 22.04
    * mono-complete

* Notes

The initial 'Hello world' is just below.

```
using System;

public class HelloWorld
{
    public static void Main(string[] args)
    {
        Console.WriteLine ("Hello Mono World");
    }
}

```

To build, use mcs.

```
$ ls
hello.cs
$ mcs hello.cs  -out:hello
$ ls
hello  hello.cs
```

mcs generates PE32 executables.
```
$ file hello
hello: PE32 executable (console) Intel 80386 Mono/.Net assembly, for MS Windows
```

To execute, use mono as a wrapper.
``
$ mono hello
Hello Mono World
```
BTW, I didn't know that at least Ubuntu 22.04 can execute PE32. :o
```
$ ./hello
Hello Mono World
```
