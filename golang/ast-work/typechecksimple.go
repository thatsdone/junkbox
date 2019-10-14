/*
Taken from section 4.1 of:
https://motemen.github.io/go-for-go-book/
*/
	
package main

import (
    "fmt"
    "go/ast"
    "go/importer"
    "go/parser"
    "go/token"
    "go/types"
)

func main() {
    fset := token.NewFileSet()
    f, _ := parser.ParseFile(fset, "example.go", src, parser.Mode(0))

    conf := types.Config{Importer: importer.Default()}

    pkg, _ := conf.Check("path/to/pkg", fset, []*ast.File{f}, nil)
    fmt.Println(pkg)
    fmt.Println(pkg.Scope().Lookup("s").Type())
}

var src = `package p

var s = "Hello, world"
`
