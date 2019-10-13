# Description

An example to analyze GO lang AST tree using go/types.
In the codes below, go/types is not directly used, it's used through
golang.org/x/tools/go/loader.

Based on a sample described below.

https://pod.hatenablog.com/entry/2018/04/08/204907

Thanks id:podhmo!

# Note

Under heavily development (study?).

# Usage

```
$ go build rewrite.go
$ ./rewrite target.go
```


You can specify a single target file like:

```
$ ./rewrite FOO.go
```

But, FOO.go needs to contain 'main' package (at the moment).


# Example


```
./rewrite  target.go
os.Args: [./rewrite target.go] / 2
DEBUG: calling ParseFile.
DEBUG: calling CreateFromFiles.
DEBUG: calling Load.
DEBUG: traverse begins...
DEBUG1: &{%!s(*ast.CommentGroup=<nil>) %!s(token.Pos=1) main [%!s(*ast.GenDecl=&{<nil> 15 75 0 [0xc000062840] 0}) %!s(*ast.GenDecl=&{<nil> 29 84 0 [0xc000062870] 0}) %!s(*ast.FuncDecl=&{<nil> 0xc000062900 0xc00006c260 0xc00006c2e0 0xc000062990}) %!s(*ast.FuncDecl=&{<nil> <nil> 0xc00006c300 0xc00006c540 0xc000062ae0})] scope 0xc0000603b0 {
        type s
        func main
}
 [%!s(*ast.ImportSpec=&{<nil> <nil> 0xc00006c1a0 <nil> 0})] [string fmt fmt] []}
DEBUG2: &{fmt Println}
DEBUG3: func fmt.Println(a ...interface{}) (n int, err error)
DEBUG2: &{fmt Println}
DEBUG3: func (main.s).Println(x string)
DEBUG2: &{fmt Println}
DEBUG3: func fmt.Println(a ...interface{}) (n int, err error)
package main

import "fmt2"

type s struct{}

func (s s) Println(x string) {}

func main() {
        fmt2.Println("xxx")

        {
                fmt := s{}
                fmt.Println("yyy")
        }

        fmt2.Println("xxx")
}

```
