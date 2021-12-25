// mpmt1.go: A stupid simple example of Go language goroutine.
//
// Currently onlly goroutine mode is supported.
//
// License:
//   Apache License, Version 2.0
// History:
//   * 2021/12/24 v0.1 Initial version.
// Author:
//   Masanori Itoh <masanori.itoh@gmail.com>
// TOTO:
//   * blushup
package main

import (
       "fmt"
       "syscall"
       "os"
       "flag"
)

func worker(id int, ch_in <-chan uint64, ch_out chan<- uint64) {

     var tv syscall.Timeval
     var ts, ts_save, ts_diff uint64

     duration := <-ch_in
     fmt.Printf("worker: started. id: %d duration: %d (us)\n", id, duration)

     syscall.Gettimeofday(&tv)
     ts_save = uint64(tv.Sec) * 1000 * 1000 + uint64(tv.Usec)

     for {
          syscall.Gettimeofday(&tv)
          ts = uint64(tv.Sec) * 1000 * 1000 + uint64(tv.Usec)
          ts_diff = ts - ts_save
          if ts_diff >= duration {
             fmt.Printf("Expired! %d / %d(us)\n", ts_diff, duration)
             break
          }
     }
	ch_out <- uint64(id)
     fmt.Println("worker: exiting...")
}

func main() {

     var duration = flag.Int("d", 10, "duration")
     var num_context = flag.Int("n", 4, "number of execution contexts")
     var mode = flag.String("m", "g", "mode: [gG]: goroutine,...")


     flag.Parse()

     fmt.Printf("num_context: %d, duration: %d, mode: %s\n",
                              *num_context, *duration, *mode)

    if *mode != "g" && *mode != "G" {
       fmt.Printf("main: mode: %d not supported\n", *mode)
       os.Exit(1)
    }

    //create channels
     ch_send := make(chan uint64, *num_context)
     ch_recv := make(chan uint64, *num_context)

    //create goroutines
     for i := 0; i < *num_context; i++ {
          go worker(i, ch_send, ch_recv)
     }

    //start goroutine (telling duration by sending a message)
    for i := 0; i < *num_context; i++ {
        ch_send <- uint64(*duration * 1000 * 1000)
    }

    //wait for goroutine completions
    for i := 0; i < *num_context; i++ {
        fmt.Printf("i: %d id: %d\n",  i, <-ch_recv)
    }
    fmt.Println("done")
}
