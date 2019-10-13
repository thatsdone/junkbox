package main

import "fmt"

type s struct{}

func (s s)Println(x string) {}

func main(){
  fmt.Println("xxx")

  {
      fmt := s{}
      fmt.Println("yyy")
  }

  fmt.Println("xxx")
}
