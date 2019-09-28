package main

import fmt "fmt"


func trace(s string) string {
	fmt.Println("entering:", s)
	return s
}

func un(s string) {
	fmt.Println("leaving:", s)
}

func a() {
	defer un(trace("a"))
	fmt.Println("in a: just returning")
}

func b() {
	defer un(trace("b"))
	fmt.Println("in b: calling a()")
	a()
}

func main() {
	fmt.Println("in main: calling b()")
	b()
}

