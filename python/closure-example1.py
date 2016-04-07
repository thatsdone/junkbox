#
# An example script to look into python closure.
#
# http://stackoverflow.com/questions/4020419/closures-in-python
#
# Define a closure function.
# Note that msg is not referenced at all except inside the inner function
# 'printer()'
# 
print 'closure case...'
def make_printer(msg):
    def printer():
        print msg
    return printer

printer = make_printer('Foo!')
printer()
#
# the whole list of attributes of function object.
# Note that '__closure__' and 'func_closure' are NOT None.
# 
print ''
for a in dir(printer):
    print "  ", a, getattr(printer, a)
print ''
#
# Define a non-closure function.
# Note that msg is not referenced as the argument of the inner function
# 'printer(msg=msg)'.
#
print 'non closure case...'
def make_printer1(msg):
    def printer(msg=msg):
        print msg
    return printer

printer1 = make_printer1("Foo!")
# Output is 'Foo!'. This result is the same as closure version.
printer1() 
#
# the whole list of attributes of function object.
# Note that '__closure__' and 'func_closure' are None.
# 
print ''
for a in dir(printer1):
    print "  ", a, getattr(printer1, a)
