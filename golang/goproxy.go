// goproxy.go: A stupidly  simple HTTP forwarding server
//
// License:
//   Apache License, Version 2.0
// History:
//   * 2023/10/08 v0.1 Initial version.
// Author:
//   Masanori Itoh <masanori.itoh@gmail.com>
package main

import (
	"flag"
	"fmt"
	"net/http"
	"bytes"
	"strings"
)

var forward_to string

func handleRequest(w http.ResponseWriter, req *http.Request) {
	fmt.Printf("%s [%s] %s\n",
		strings.Split(req.RemoteAddr, ":")[0],
		req.Method, req.URL.Path)

	if forward_to == "" {
		return
	}
	if req.Method == "POST" {
		fmt.Println("Forwarding POST message...")
		len := req.ContentLength
		body := make([]byte, len)
		req.Body.Read(body)
		freq, err := http.NewRequest("POST",
			forward_to, bytes.NewBuffer(body))
		if (err != nil) {
			fmt.Println(err)
		}
		//uncomment if you want to forward headers too.
		//for key, elm := range req.Header {
		//	freq.Header.Set(key, elm[0])
		//}
		client := &http.Client{}
		res, err := client.Do(freq)
		if (err != nil) {
			fmt.Println(res, err)
		}
		defer req.Body.Close()
	} else {
		freq, err := http.NewRequest(req.Method, forward_to, nil)
		if (err != nil) {
			fmt.Println(err)
		}
		client := &http.Client{}
		res, err := client.Do(freq)
		if (err != nil) {
			fmt.Println(res, err)
		}
	}
}


func main() {
	var port = flag.Int("b", 8080, "bind port")
	var address = flag.String("a", "0.0.0.0", "bind address")
	var F_flag = flag.String("F", "", "forward to URL")
	flag.Parse()
	
	listen_url := fmt.Sprintf("%s:%d", *address, *port)
	fmt.Printf("Listening on: %s\n", listen_url)
	
	forward_to = *F_flag
	if forward_to != "" && forward_to[len(forward_to)-1:] == "/" {
		forward_to = forward_to[:len(forward_to)-1]
	fmt.Printf("Forwarding evrything to: %s\n", forward_to)
	}

	mux := http.NewServeMux()
	mux.HandleFunc("/api", handleRequest)
	ret := http.ListenAndServe(listen_url, mux)
	fmt.Println(ret)
}
