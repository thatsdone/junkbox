#!/usr/bin/env julia
# -*- coding: utf-8 -*-
#
# mpmt1.jl: Julia version of mpmt1.py
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2022/03/21 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TODO:
#   * Add multiprocessing mode?
#
using Dates
using Printf
using Getopt
using Base.Threads
#using Benchmarktools

function busy_worker(identity, duration)
    msg = @sprintf "busy_worker: %d started" identity
    println(msg)

    ts_start = time()
    while true
        ts_now = time()
	if (ts_now - ts_start) > duration
	   msg = @sprintf "busy_worker: %d duration %d expired" identity duration
	   println(msg)
	   break
	end
    end
end



#
# main routine
#
num_context = 4
duration = 5
use_thread = 1

# https://juliapackages.com/p/getopt
for (opt, arg) in Getopt.getopt(ARGS, "n:d:m:")
    #@printf "%s %s\n" opt arg
    if opt == "-n"
        global num_context = parse(Int, arg)
    end
    if opt == "-d"
        global duration = parse(Int, arg)
    end
    if opt == "-m"
        if arg == "p" || arg == "P"
	    # currently ignored.
            global use_thread = 0
        end
    end
end

@printf "num_context = %d duration = %d\n"  num_context duration
#@printf "DEBUG: nthreads = %d" Threads.nthreads()

if num_context > Threads.nthreads()
    @printf "ERROR: Increase nthrads(%d to %d) via JULIA_NUM_THREADS or -t.\n" Threads.nthreads() num_context
    exit()
end

#@printf "nthreads = %d\n" Threads.nthreads()

@threads for t in 1:num_context
    busy_worker(t, duration)
end


