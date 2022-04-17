#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
#
# mpmt1.rb: A Ruby version of mpmt1.py
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2021/12/29 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TODO:
#   * Implement multi process mode (or more clever thread mode)


def busy_worker(id, num_context, duration)

  printf("thread: %d / n: %d d: %d %s\n", id, num_context, duration, Thread.current)

  tsnow = Time.now
  ts_save = tsnow.to_i * 1000*1000 + tsnow.usec

  loop do
    tsnow = Time.now
    ts = tsnow.to_i * 1000*1000 + tsnow.usec
    if (ts - ts_save) > duration
      printf("thread: %d Expired! %d / %d\n",  id, (ts- ts_save), duration)
      return
    end
  end

end


if $0 == __FILE__

  require 'optparse'

  num_context = 4
  duration = 10 * 1000 * 1000
  mode = 't'

  params = ARGV.getopts("n:", "d:", "m:")

  if params.has_key? 'n'
    num_context = params['n'].to_i
  end
  if params.has_key? 'd'
    duration = params['d'].to_i
    duration = duration * 1000 * 1000
  end
  if params.has_key? 'm'
    mode = params['m']
  end

  printf("num_context: %d duration: %d (us) mode: %s (t: thread)\n", num_context, duration, mode)

  if mode == 't' or mode == 'T'
    threads = []

    num_context.times do |idx|
      threads << Thread.new { busy_worker(idx, num_context, duration) }
    end

    threads.each() { |th|
      p th.join()
    }

  elsif mode == 'p' or mode == 'P'
    printf("multi process mode is not yet implemented: %s\n", mode)
    exit
  else
    printf("Invalide mode: %s\n", mode)
    exit
  end

end
