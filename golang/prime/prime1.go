package main

import fmt "fmt"

func generate(ch chan int) {
    for i := 2; ; i++ {
        ch <- i // send 'i' to channel 'ch'
    }
}

func filter(in, out chan int, prime int) {
    for {
        i := <-in // receive a value into a variable 'i' from channel 'in'
        if i%prime != 0 {
            out <- i // send 'i' to channel 'out'
        }
    }
}

func main() {
    ch := make(chan int)       // create a new channel
    go generate(ch)            // start generate() as a goroutine
    for i := 0; i < 1000000000; i++ { // show the first 100 prime numbers
        prime := <-ch
	//fmt.Println(prime)
        ch1 := make(chan int)
        go filter(ch, ch1, prime)
        ch = ch1
    }
}
