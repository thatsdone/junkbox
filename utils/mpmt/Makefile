all: c rust

c:
	gcc -o mpmt1c mpmt1.c -lpthread
python:
	echo 'Execute `python3 mpmt1.py`'
go:
	go build -o mpmt1go mpmt1.go
rust:
	rustc -o mpmt1rs mpmt1.rs

clean:
	/bin/rm -f mpmt1rs mpmt1c mpmt1go *~
