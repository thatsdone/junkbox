#!/usr/bin/env escript
%% -*- erlang -*-
%%! -smp enable -sname fibonacci -mnesia debug verbose
main([String]) ->
    try
        N = list_to_integer(String),
        F = fib(N),
        io:format("fibonacci ~w = ~w\n", [N,F])
    catch
        _:_ ->
            usage()
    end;
main(_) ->
    usage().

usage() ->
    io:format("usage: fibonacci integer\n"),
    halt(1).

fib(0) -> 0;
fib(1) -> 1;
fib(N) -> fib(N-1) + fib(N-2).
