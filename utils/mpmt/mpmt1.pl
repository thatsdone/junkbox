#!/usr/bin/env perl
#
# mpmt1.pl: Perl version of mpmt1.py
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2022/04/16 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TOTO:
#   * Implement multi process model
use strict;
use Getopt::Std;
use Time::HiRes;
use threads;


my $busy_worker = sub
{
    my $idx = shift(@_);
    my $duration = shift(@_);
    printf "busy_worker: %d\n", $idx;
    my $ts_start;
    my $ts_now;
    my $continue = 1;
    $ts_start = Time::HiRes::gettimeofday;
    while ($continue) {
	$ts_now = Time::HiRes::gettimeofday;
	if (($ts_now - $ts_start) > $duration) {
	    printf "busy_worker: exiting... %s\n", $ts_now - $ts_start;
	    $continue = 0;
	}
    }
};
#
# main routine
#
my @th;
my $num_context = 2;
my $duration = 5.0;
my $mode = 'thread';
my %opt;

getopts('n:d:m:', \%opt);
if (exists $opt{n}) {
    $num_context = $opt{n};
}
if (exists $opt{d}) {
    $duration = $opt{d};
}
printf "mpmt1.pl: num_context = %d duration = %f\n", $num_context, $duration;

for (my $i = 0; $i < $num_context; $i++) {
    $th[$i] = threads->new(\&$busy_worker, $i, $duration)
}

for (my $i = 0; $i < $num_context; $i++) {
    $th[$i]->join;
}
