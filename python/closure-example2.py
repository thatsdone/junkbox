#
# An example script to look into python closure.
#
# http://d.hatena.ne.jp/agw/20080727/1217233163
# http://d.hatena.ne.jp/nishiohirokazu/20080204
#
# Define a closure.
# In this case, 
def make_counter():
    def counter():
        counter.x += 1
        print counter.x
        return counter
    counter.x = 0
    return counter

print 'result of: make_counter()()()()'
make_counter()()()()
#
#
#
print 'result of c = make_counter() and successive c() calls.'
c = make_counter()
c()
c()
c()
#
#
#
print 'list of attributes'
for a in dir(c):
    print '  ', a, getattr(c, a)
