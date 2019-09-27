package main

import fmt "fmt"

func generate() chan int {
    ch := make(chan int)
    go func() {
        for i := 2; ; i++ {
            ch <- i
        }
    }()
    return ch
}


func filter(in chan int, prime int) chan int {
    out := make(chan int)
    // function literal / anonymous function / closure
    go func() {
        for {
            if i := <-in; i%prime != 0 {
                out <- i
            }
        }
    }()
    // As this is a closure, the () above is required to say no argument.
    // If the func takes arguments, need to be specified above.
    return out
}

func sieve() chan int {
    out := make(chan int)
    // function literal / anonymous function / closure
    go func() {
        ch := generate()
        for {
            prime := <-ch
            out <- prime
            ch = filter(ch, prime)
        }
    }()
    // As this is a closure, the () above is required to say no argument.
    // If the func takes arguments, need to be specified above.
    return out
}

func main() {
    primes := sieve()
    for i := 0; i < 100000000; i++ { // show the first 100 prime numbers
	    //fmt.Println(<-primes)
	    j := <-primes
    }
}

