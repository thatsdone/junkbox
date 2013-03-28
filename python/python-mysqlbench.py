#!/usr/bin/python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# python-
#
# Description:
#   A simple python port of mysqlbench which is originally pgbench of
#   PostgreSQL.
# 
#   http://www.mysql.gr.jp/frame/modules/bwiki/index.php?plugin=attach&refer=Contrib&openfile=mysqlbench-0.1.tgz
#
# Author: Masanori Itoh <masanori.itoh@gmail.com>
#
"""
/*
mysqlbench
* 2005-12-16
  - padding filler
  - change output format
* 2004-12-26
  - init
*/
/*
 * $PostgreSQL: pgsql/contrib/pgbench/pgbench.c,v 1.35 2004/11/09 06:09:31 neilc Exp $
 *
 * pgbench: a simple TPC-B like benchmark program for PostgreSQL
 * written by Tatsuo Ishii
 *
 * Copyright (c) 2000  Tatsuo Ishii
 *
 * Permission to use, copy, modify, and distribute this software and
 * its documentation for any purpose and without fee is hereby
 * granted, provided that the above copyright notice appear in all
 * copies and that both that copyright notice and this permission
 * notice appear in supporting documentation, and that the name of the
 * author not be used in advertising or publicity pertaining to
 * distribution of the software without specific, written prior
 * permission. The author makes no representations about the
 * suitability of this software for any purpose.  It is provided "as
 * is" without express or implied warranty.
 */
"""
import sys
import getopt
import _mysql as mysql
import threading
import time


class MySQLBench(object):
    nbranches = 1
    ntellers = 10
    naccounts = 100000

    #
    is_init_mode = 0
    mysqlhost = ''
    is_no_vacuum = 0
    is_full_vacuum = 0
    mysqlport = 3306
    debug = 0
    ttype = 0
    nclients = 1
    tps = 1
    nxacts = 1
    login = ''
    password = ''
    engine = 'innodb'
    dbname = 'pgbench'
    #
    threads = []

    def usage(self):
        print 'Usage...'

    def parse_arg(self, argv):
        print 'MySQLBench::parse_arg called.'

        try:
            opts, args = getopt.getopt(argv[1:],
                                   'ih:nvp:dc:t:s:U:P:CSE:D:', [])
        except getopt.GetoptError:
            print sys.exc_info()
            print 'getopt error...'
            sys.exit(2)

        for opt, arg in opts:
            if opt in ('-i'):
                self.is_init_mode += 1
            elif opt in ('-h'):
                self.mysqlhost = arg
            elif opt in ('-n'):
                self.is_no_vacuum += 1
            elif opt in ('-v'):
                self.is_full_vacuum += 1
            elif opt in ('-p'):
                self.mysqlport = arg
            elif opt in ('-d'):
                self.debug += 1
            elif opt in ('-S'):
                self.ttype = 1
            elif opt in ('-c'):
                self.nclients = int(arg)
#            elif opt in ('-C'):
            elif opt in ('-s'):
                self.tps = int(arg)
            elif opt in ('-t'):
                self.nxacts = int(arg)
                if self.nxacts <= 0:
                    print 'wrong number of transactons: %d' % self.nxacts
                    sys.exit(1)
            elif opt in ('-U'):
                self.login = arg
            elif opt in ('-P'):
                self.password= arg
            elif opt in ('-E'):
                self.engine = arg
            elif opt in ('-D'):
                self.dbname = arg
            else:
                usage()
                sys.exit(1)

    def doOne(self, id):
        print 'doOne called. ident: %d id: %d' % (threading.currentThread().ident, id)
        return

    def doClose(self, conn):
        print 'MySQLBench::doClose called.'
        try:
            conn.close()

        except:
            print sys.exc_info()[0]
            print sys.exc_info()[1]
            sys.exit(0)
            

    def doConnect(self):
        print 'MySQLBench::doConnect called.'
        try:
            conn=mysql.connect(host=self.mysqlhost,
                             db=self.dbname,
                             user=self.login,
                             passwd=self.password)
            return conn

        except:
            print sys.exc_info()[0]
            print sys.exc_info()[1]
            sys.exit(0)


    def initialize(self):
        print 'MySQLBench::initialize called.'

        DDLs = [
            "DROP TABLE IF EXISTS branches",
            "CREATE TABLE branches (bid int PRIMARY KEY, bbalance int, filler char(88))",
            "DROP TABLE IF EXISTS tellers",
            "CREATE TABLE tellers (tid int PRIMARY KEY, bid int, tbalance int, filler char(84))",
            "DROP TABLE IF EXISTS accounts",
            "CREATE TABLE accounts (aid int PRIMARY KEY, bid int, abalance int, filler char(84))",
            "DROP TABLE IF EXISTS history",
            "CREATE TABLE history (tid int, bid int, aid int, delta int, mtime timestamp, filler char(22))"
            ]
        self.conn = self.doConnect()
        for stmt in DDLs:
            if stmt.startswith('CREATE'):
                sql ='%s ENGINE=%s' % (stmt, self.engine)
            else:
                sql = '%s' % stmt
            self.conn.query(sql)

        self.conn.query("BEGIN");

        for i in range(0, self.nbranches * self.tps):
            sql = 'INSERT INTO branches (bid, bbalance, filler) VALUES (%d, 0, REPEAT(\'b\',88))' %  (i + 1)
            self.conn.query(sql);

        for i in range(0, self.ntellers * self.tps):
            sql = 'INSERT INTO tellers (tid, bid, tbalance, filler) VALUES (%d, %d, 0, REPEAT(\'t\',84))' % (i + 1, i / self.ntellers + 1)
            self.conn.query(sql);

        print 'Filling tables...'
        for i in range(0, self.naccounts * self.tps):
            j = i + 1
            sql = 'INSERT INTO accounts (aid, bid, abalance, filler) VALUES (%d, %d, %d, REPEAT(\'c\',84))' % (j, j / self.naccounts, 0)
            self.conn.query(sql);

        self.conn.query("COMMIT");
        self.conn.query('OPTIMIZE TABLE branches, tellers, accounts, history')
        #
        self.doClose(self.conn)
        print 'done.'


    def run(self):
        print 'MySQLBench::run called.'

        self.conn = self.doConnect()

        # scaling factor should be the same as count(bid) from branches.
        self.conn.query("SELECT count(bid) FROM branches");
        rows = self.conn.store_result().fetch_row(maxrows=1, how=1)
        self.tps = int(rows[0]['count(bid)'])

        if self.is_no_vacuum is not 0:
            print 'starting vacuum...'
            self.conn.query("OPTIMIZE TABLE branches");
            self.conn.query("OPTIMIZE TABLE tellers");
            self.conn.query("OPTIMIZE TABLE history");
            self.conn.query("OPTIMIZE TABLE branches");

        if self.is_full_vacuum is not 0:
            self.conn.query("OPTIMIZE TABLE accounts");
        # close
        self.doClose(self.conn)

        #create threads
        for i in range(0, self.nclients):
            # print 'i = %d' % i
            t=threading.Thread(target=self.doOne, name='threadb-%d' % i, args=(i,))
            self.threads.append({'id': i, 'state': 'INIT' , 'thread': t, 'conn': None })
            t.start()

        #set random seed
        #get startup time
        #check connections
        print 'go...'
        # start all threads
        time.sleep(3)

#        print self.threads
        for i in range(0, self.nclients):
            print i, self.threads[i]
        for t in self.threads:
            t['thread'].join()
        print 'all threads completed'
        # wait for all threads end up.

if __name__ == '__main__':
    mb = MySQLBench()
    mb.parse_arg(sys.argv)
    if mb.is_init_mode:
        mb.initialize()
    else:
        mb.run()
