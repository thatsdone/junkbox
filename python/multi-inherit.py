#
# multi-inherit.py : multple inheritance examples.
# 
# (Case 1)
#
#  A ---+
#       |
#       +--- C
#       |
#  B ---+
#
class A(object):
    val = 'A'
    def __init__(self):
        print 'A.__init__ called'

class B(object):
    val = 'B'
    def __init__(self):
        print 'B.__init__ called'

class C(A, B):
    # if the below 'val' was commented out, val becomes 'A', not 'B'
    # because of the order in class definition: classC(A, B)
    val = 'C'
    def __init__(self):
        print 'C.__init__ called'
        #super(B, self).__init__()
        #super(A, self).__init__()
        print 'super(B, self) = ', super(B, self)
        print 'super(A, self) = ', super(A, self)
#
c = C()
print 'c.val = ', c.val
print 'super(C, c).val = ', super(C, c).val
print 'super(A, c).val = ', super(A, c).val
# the below causes an error because the super class of class B is counted as the generic object class.
#print super(B, c).val
#
# lists of attributes of the class
#
for a in dir(A):
    print '%-20s : %s' % (a, getattr(A, a))
print ''
for a in dir(B):
    print '%-20s : %s' % (a, getattr(B, a))
print ''
for a in dir(C):
    print '%-20s : %s' % (a, getattr(C, a))
print ''
#
# lists of attributes of super
#
for a in dir(super(A, c)):
    print '%-20s : %s' % (a, getattr(super(A, c), a))
print ''
for a in dir(super(B, c)):
    print '%-20s : %s' % (a, getattr(super(B, c), a))
print ''
for a in dir(super(C, c)):
    print '%-20s : %s' % (a, getattr(super(C, c), a))

########################################################################
#
# (Case 2)
#
#  X ---> Y ---> Z
#
class X(object):
    val = 'X'
    def __init__(self):
        print 'X.__init__'

class Y(X):
    val = 'Y'
    def __init__(self):
        print 'Y.__init__'
        super(Y, self).__init__()

class Z(Y):
    val = 'Z'
    def __init__(self):
        print 'Z.__init__'
        super(Z, self).__init__()
        #super(B, self).__init__()
        #super(A, self).__init__()
        print super(Z, self), super(Z, self).val
        print super(Y, self), super(Y, self).val
        print super(X, self)

#
# In this case, __init__ routines of super classes are successively called.
# The very base class is 'class X'
z = Z()
