#
# orm-example1.py : an example of mapping objects and relations
#   specifically preparation for python-mysqlbench sqlalchemy port.
#
"""
python-mysqlbench (based on mysqlbench (originally pgbench))
Database Shema Definitions sample.

mysql> show tables;
+-------------------+
| Tables_in_pgbench |
+-------------------+
| accounts          |
| branches          |
| history           |
| tellers           |
+-------------------+
4 rows in set (0.00 sec)

mysql> describe accounts;
+----------+----------+------+-----+---------+-------+
| Field    | Type     | Null | Key | Default | Extra |
+----------+----------+------+-----+---------+-------+
| aid      | int(11)  | NO   | PRI | NULL    |       |
| bid      | int(11)  | YES  |     | NULL    |       |
| abalance | int(11)  | YES  |     | NULL    |       |
| filler   | char(84) | YES  |     | NULL    |       |
+----------+----------+------+-----+---------+-------+
4 rows in set (0.01 sec)

mysql> describe branches;
+----------+----------+------+-----+---------+-------+
| Field    | Type     | Null | Key | Default | Extra |
+----------+----------+------+-----+---------+-------+
| bid      | int(11)  | NO   | PRI | NULL    |       |
| bbalance | int(11)  | YES  |     | NULL    |       |
| filler   | char(88) | YES  |     | NULL    |       |
+----------+----------+------+-----+---------+-------+
3 rows in set (0.00 sec)

mysql> describe history;
+--------+-----------+------+-----+-------------------+-----------------------------+
| Field  | Type      | Null | Key | Default           | Extra                       |
+--------+-----------+------+-----+-------------------+-----------------------------+
| tid    | int(11)   | YES  |     | NULL              |                             |
| bid    | int(11)   | YES  |     | NULL              |                             |
| aid    | int(11)   | YES  |     | NULL              |                             |
| delta  | int(11)   | YES  |     | NULL              |                             |
| mtime  | timestamp | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
| filler | char(22)  | YES  |     | NULL              |                             |
+--------+-----------+------+-----+-------------------+-----------------------------+
6 rows in set (0.00 sec)

mysql> describe tellers;
+----------+----------+------+-----+---------+-------+
| Field    | Type     | Null | Key | Default | Extra |
+----------+----------+------+-----+---------+-------+
| tid      | int(11)  | NO   | PRI | NULL    |       |
| bid      | int(11)  | YES  |     | NULL    |       |
| tbalance | int(11)  | YES  |     | NULL    |       |
| filler   | char(84) | YES  |     | NULL    |       |
+----------+----------+------+-----+---------+-------+
4 rows in set (0.00 sec)
"""
import sys
from sqlalchemy import *
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
#
# Object-Relation Mappings
#
Base = declarative_base()
#
class Accounts(Base):
    __tablename__ = 'accounts'
    aid = Column(Integer, primary_key=True)
    bid = Column(Integer)
    abalance = Column(Integer)
    filler = Column(String(84))


class Branches(Base):
    __tablename__ = 'branches'
    bid = Column(Integer, primary_key=True)
    bbalance = Column(Integer)
    filler = Column(String(88))


class History(Base):
    __tablename__ = 'history'
    tid = Column(Integer)
    bid = Column(Integer)
    aid = Column(Integer)
    delta = Column(Integer)
    mtime = Column(DATETIME, nullable=False, onupdate=func.current_timestamp, primary_key=True)
    filler = Column(String(22))


class Tellers(Base):
    __tablename__ = 'tellers'
    tid = Column(Integer, primary_key=True)
    bid = Column(Integer)
    tbalance = Column(Integer)
    filler = Column(String(84))
#
# DB Access parameters.
#  
user = 'USERNAME'
password = 'PASSWORD'
host = 'HOSTNAME_OR_IPADDRESS'
dbname = 'DBNAME'
options = '' # begin with '?' such as '?connect_timeout=2'

#
# create a session object
#
uri = 'mysql://%s:%s@%s/%s%s' % (user, password, host, dbname, options)
engine = create_engine(uri)
print 'DEBUG: ', engine

Session = sessionmaker(bind=engine)
print 'DEBUG: ', Session
#  sessionmaker returns a class, not object

session = Session()
print 'DEBUG: ', session
#  the above is an object instance.

#
# issue queries.
# 
# get a single record.
#
myobj = session.query(Accounts).first()
print 'DEBUG: ', myobj
#for a in dir(myobj):
#    print a, ' : ', getattr(myobj, a)
print "aid: %s\nbid: %s\nabalance: %s\nfiller: %s\n" % (myobj.aid, myobj.bid, myobj.abalance, myobj.filler)

#
# get multiple records
#
myobj_multi = session.query(Accounts).limit(3)
for o in myobj_multi:
    print 'DEBUG: ', o.aid, o.bid, o.abalance, o.filler

session.close()


