Example of defer using for tracing taken from: https://golang.org/doc/effective_go.html#defer


```
$ go run defer1.go
in main: calling b()
entering: b
in b: calling a()
entering: a
in a: just returning
leaving: a
leaving: b
```
