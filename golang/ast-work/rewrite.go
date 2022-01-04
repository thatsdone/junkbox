/*
  rewrite.go and target.go

  An example to analyze GO lang AST tree using go/types.
  In the codes below, go/types is not directly used, it's used through
  golang.org/x/tools/go/loader.



  Reference:
  Based on a sample described below.
  https://pod.hatenablog.com/entry/2018/04/08/204907

  Thanks id:podhmo!

  Usage:
    go build rewrite.go
    ./rewrite target.go

  You can specifi a single target file like:
    ./rewrite FOO.go
  But, FOO.go needs to contain 'main' package (at the moment).

*/

package main

import (
  "go/ast"
  "go/parser"
  "go/printer"
  "log"
  "os"
  "fmt"
  "golang.org/x/tools/go/ast/astutil"
  "golang.org/x/tools/go/loader"
)

func main() {
  fmt.Printf("os.Args: %s / %d \n", os.Args, len(os.Args))
  if err := run(); err != nil {
    log.Fatalf("%+v", err)
  }
}

func run() error {
  source := ""

  if len(os.Args) == 1 {
    source = "target.go"
  } else {
    source = os.Args[1]
  }
  
  file, err := os.Open(source)
  if err != nil {
    fmt.Printf("error!\n")
    os.Exit(1)
  }
  defer file.Close()
        
  loader := loader.Config{ParserMode: parser.ParseComments}
  fmt.Printf("DEBUG: calling ParseFile.\n")
  astf, err := loader.ParseFile(source, file)
  if err != nil {
    fmt.Printf("ParseFile returns non nil error.\n")
    return err
  }
  fmt.Printf("DEBUG: calling CreateFromFiles.\n") 
  loader.CreateFromFiles("main", astf)

  fmt.Printf("DEBUG: calling Load.\n") 
  prog, err := loader.Load()
  if err != nil {
    return err
  }
  fmt.Printf("DEBUG: traverse begins...\n")
  
  main := prog.Package("main")
  fmtpkg := prog.Package("fmt").Pkg
  for _, f := range main.Files {
    fmt.Printf("DEBUG1: %s\n", f)   
    ast.Inspect(f, func(node ast.Node) bool {
			if node != nil {
				desc := astutil.NodeDescription(node)
				fmt.Printf("DEBUG1.5: NodeDescription : %s\n", desc)
			} else {
				fmt.Printf("DEBUG1.5: Node is nil\n")
			}
      if t, _ := node.(*ast.SelectorExpr); t != nil {
        fmt.Printf("DEBUG2: %s\n", t)
        fmt.Printf("DEBUG3: %s\n", main.Info.ObjectOf(t.Sel))
				/*
         The below is an example re-writing 'fmt' to 'fmt2' described in the
         URL above. This shows how we can modify parse tree of golang.
         */
        if main.Info.ObjectOf(t.Sel).Pkg() == fmtpkg {
          ast.Inspect(t.X, func(node ast.Node) bool {
            if t, _ := node.(*ast.Ident); t != nil {
              if t.Name == "fmt" && t.Obj == nil {
                t.Name = "fmt2"
              }
              return false
            }
            return true
          })
        }

        return false
      }
      return true
    })
    
    astutil.RewriteImport(prog.Fset, f, "fmt", "fmt2")
    
    pp := &printer.Config{Tabwidth: 8, Mode: printer.UseSpaces | printer.TabIndent}
    pp.Fprint(os.Stdout, prog.Fset, f)
  }
  return nil
}

  
