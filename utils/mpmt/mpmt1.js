/*
# -*- coding: utf-8 -*-
#
# mpmt1.rb: A Node.js version of mpmt1.py
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2021/12/30 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TODO:
#   * Investigate multi-thread feature of Node.js
#   * Add options by using getopt
*/

function busy_worker(timeout) {

    // ts and ts_save are in mili-seconds
    var ts_save = Date.now()
    // duration is in seconds.
    var max = timeout * 1000

    while (true) {
	ts = Date.now()
	if ((ts - ts_save) >= max) {
	    console.log('Expired! ' + (ts - ts_save))
	    break
	}
    }
    process.exit(123)
}


var posix_getopt = require('posix-getopt')
var parser, option

const cluster = require('cluster')

var num_context = 4
var duration = 10
var mode = 'p'

parser = new posix_getopt.BasicParser('n:d:m', process.argv)
while ((option = parser.getopt()) !== undefined) {
    switch (option.option) {
    case 'n':
	num_context = option.optarg
	break;
    case 'd':
	duration = option.optarg
	break;
    case 'm':
	mode = option.optarg
	break;
    }
}


//isPrimary does not work for Node.js v10.19.0?
if (cluster.isMaster) {
    console.log('parent: pid= ' + process.pid)
    console.log('num_context: ' + num_context + ' duration: ' + duration)
    for (var i = 0; i < num_context; i++) {
	cluster.fork()
    }

    cluster.on('exit', (code, signal) => {
	// signal is the value for process.exit()? node code?
	console.log('on exit called. code= ' + code + ' signal= ' + signal)
    });

} else {
    console.log('child: pid=' + process.pid)
    busy_worker(duration)
}

