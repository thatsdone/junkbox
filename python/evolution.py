#
# evolution.py
# 
# A simple(/stupid) and straight forward port of an example
# from 'Land of Lisp'  http://landoflisp.com/evolution.lisp
#
# Note1:
#   Still buggy and ugly... :o
#
# Note2:
# In the original program, 'genes' of an animal is referenced only
# by 'turn'. This means genes have effects only on making a decision of 
# choosing direction to move to in the current step.
# In a sense, that's why there are 8 elements in 'genes', I think.
# First, 'turn' function sums up all 8 elements of the given genes,
# generate a random number between 0(inclusive) and the sum (exclusive)
# and stores it into 'x'.
# Second, 'turn' calls 'angle' sub-function.
# 'angle' takes a list(genes) and the random number 'x' as parameters, and
# it calculates 'x - (car genes)' and stores it into 'xnu'.
# If xnu is negative, 'angle' returns 0 immediately.
# If not, 'angle' calls itself recursively using '(cdr genes)' and 'xnu'
# instead of the given genes and x. On return, the result is incremented.
# Thus, dir(ection) from 0 to 7 will be choosed according to 8 values 
# contained in the given genes.
#
# dir(ection) is like the following.
#  'o' is the current position.
# +-------->X-axis
# |0  1  2
# |7  o  3
# |6  5  4
# v
# Y-axis
#
# Author: Masanori Itoh <masanori.itoh@gmail.com>
#
import os,sys,random

def draw_world():
    global counter, killed_animal
#    print 'draw_world called.'
    print '(width, height) = (%d, %d), update= %d, #animals = %d (%d killed), #plants = %d' % (width, height, counter, len(animals), killed_animal, len(plants))

#    print 'width = %d, height = %d' % (width, height)
    aa = []
    for a in animals:
        aa.append([a['x'], a['y']])
#    print aa

    for y in range(0, height):
        str = ''
        for x in range(0, width):
            if [x, y] in aa:
                str = str + 'A'
            elif {'x': x, 'y': y} in plants:
                str = str + 'T'
            else:
                str = str + '-'
        print '%s%s%s' % ('|', str, '|')

    return

def fresh_line():
    print 'fresh_line called.'
    return

def move(animal):
#    print 'move called.'
    dir = animal['dir']
    x = animal['x']
    y = animal['y']

    def movex(dir):
        if (dir >= 2 and dir <= 4):
            return 1
        elif (dir == 1 or dir == 5):
            return 0
        else:
            return -1

    def movey(dir):
        if (dir >= 0 and dir <= 2):
            return -1
        elif (dir >= 4 and dir <= 6):
            return 1
        else:
            return 0

    animal['x'] = (x + movex(dir)) % width
# oops... here was a critical bug. the below 'y' was 'x'...orz
    animal['y'] = (y + movey(dir)) % height
    animal['energy'] -= 1
    return

def turn(animal):
#    print 'turn called.'
    global debug
    x = random.randint(0, sum(animal['genes']))
#    print 'DEBUG1: ', x
    def angle(genes, x):
#        print 'angle(sub function) called.'
        if len(genes) == 0:
            return 0
        xnu = x - genes[0]
#        print 'DEBUG2: ', genes, xnu
        if xnu < 0:
            return 0
        else:
            return angle(genes[1:], xnu) + 1

    a = angle(animal['genes'], x)
#    print '  turn: dir = %d, x = %d,  angle = %d' % (animal['dir'], x, a)
    animal['dir'] = (animal['dir'] + a) % 8
#    animal['dir'] = (animal['dir'] + angle(animal['genes'], x)) % 8
    return

def eat(animal):
#    print 'eat called.'
    pos = {'x': animal['x'], 'y': animal['y']}
    if pos in plants:
        animal['energy'] += plant_energy
#        print '  eat: removing...: ', pos
        plants.remove(pos)
    return

def reproduce(animal):
#    print 'reproduce called.'
    e = animal['energy']
    if e >= reproduce_energy:
        animal['energy'] = (e - 1) / 2
        animal_new = animal.copy()
        # last [:] is important for copying the entire list. or deepcopy()?
        genes = list(animal_new['genes'])[:]
        mutation = random.randint(0, 7)
#        print 'before', genes, mutation, genes[mutation]
        original = True
        if original:
            genes[mutation] = max(1, genes[mutation] + random.randint(0, 2) - 1)
        else:
            g = random.randint(1, 10)
            if genes[mutation] == g:
                genes[mutation] = 1
            else:
                genes[mutation] = g           
#        print 'after ', genes, mutation, genes[mutation]
        animal_new['genes'] = genes
        animals.append(animal_new)
    return

def random_plant(pos):
#    print 'random_plants called.'
    (left, top, width, height) = pos
#   Precisely speaking, here must be some roundup.
    x = (left + random.randint(0, width - 1))
    y = (top + random.randint(0, height - 1))
    if not {'x': x, 'y': y} in plants:
        plants.append({'x': x, 'y': y})
    return

def add_plants():
#    print 'add_plants called.'
    global width, height, jungle
    random_plant(jungle)
    random_plant([0, 0, width, height])
    return


def update_world():
#    print 'update_world called.'
    global counter, killed_animal
    counter += 1
    for animal in animals:
        if animal['energy'] <= 0:
            animals.remove(animal)
            killed_animal += 1
    for animal in animals:
        turn(animal)
        move(animal)
        eat(animal)
        reproduce(animal)
    add_plants()
    return


def evolution():
#    print 'evolution'
    draw_world()
    line = sys.stdin.readline()
    while line:
        x = line[:-1]
#        print 'read: "%s"' % x
        if x == 'quit':
            print 'quitting...'
            sys.exit(0)
        elif x == 'dump':
            x = int(0)
            for a in animals:
                print a
        elif x == 'dumpplant':
            x = int(0)
            for p in plants:
                print p
        elif x.isdigit():
            x = int(line)
        else:
            x = int(1)

        for i in range(0, x):
            update_world()
        evolution()


if __name__ == '__main__':

    debug=0
    width = 100
    height = 30

    counter = 0
    killed_animal = 0

    plant_energy = 80
    reproduce_energy = 200

    plants = []
    jungle = [45, 10, 10, 10]
    animals = [{'x': int((width - 1) / 2),
              'y': int((height - 1) / 2),
              'energy':1000,
              'dir': 0, 
              'genes':   [random.randint(0, 9) for r in range(8)]
              }]

    add_plants()
    evolution()
