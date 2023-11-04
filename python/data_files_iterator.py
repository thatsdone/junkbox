#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# data_files_iterator.py:
#
#   An exercise iterator for processing multiple data files sucessively
#   without taking care of data file switching on the application side.
#
#   Initially, this tool was intended for processing JSON query result files
#   in multiple pages from ElasticSearch/OpenSearch.
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2023/11/04 v0.1 Initial version
#
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
class DataFilesIterator:

    def __init__(self, datafiles=None):
        if not datafiles:
            raise ValueError
        self.datafiles = datafiles
        self._f = 0 # data file index
        self._n = 0 # element (in a data file) index
        self.datafile = self.datafiles.__getitem__(0)
        self.fp = open(self.datafile, 'rt')
        self.data_stream = json.load(self.fp)

    def __iter__(self):
        return self

    def __next__(self):
        # TODO(thatsdone): can be more generic
        if self._n >= self.data_stream['hits']['hits'].__len__():
            self.fp.close()
            self._f += 1
            if self._f >= self.datafiles.__len__():
                raise StopIteration
            else:
                self.datafile = self.datafiles.__getitem__(self._f)
                #print('DEBUG: switching file to : %s' % (self.datafile))
                self.fp = open(self.datafile, 'rt')
                self.data_stream = json.load(self.fp)
                self._n = 0
        # TODO(thatsdone): can be more generic
        elm = self.data_stream['hits']['hits'].__getitem__(self._n)
        if elm:
            self._n += 1
            return elm
        else:
            raise StopIteration

if __name__ == "__main__":
    import sys
    import os
    import glob
    import json
    import argparse
    parser = argparse.ArgumentParser(description='itertest.py')
    parser.add_argument('--data_dir', default=None)
    args = parser.parse_args()
    #
    if not args.data_dir:
        print('Specify the data files directory via --data_dir ')
        sys.exit()

    data_files = glob.glob('%s/*.json' % (args.data_dir))
    # In this example, filename convention below is like 20230123-0123-456.json
    # 3rd comonent means page, and thus used for sort key.
    data_files = [ f for f in sorted(data_files,
                                     key=lambda bn:
                                     int(os.path.basename(bn).split('.')[0].split('-')[2]))]
    #
    dfi = DataFilesIterator(datafiles=data_files)
    #
    count = 0
    for item in dfi:
        count += 1
        # Output current processed element per 10000 records.
        # (10000 comes from ElasticSearch maximum hit counts)
        if count % 10000 == 0:
            print('count = ', count)
        continue

