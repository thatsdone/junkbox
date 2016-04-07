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
import sys
import random
import getopt

class Animal(object):
    id = 0
    x = 0
    y = 0
    energy = 0
    dir = 0
    id = 0
    birth = 0
    death = 0
    parent = 0
    genes = []

    def __init__(self, world):
        #print 'Animal.__init__ called.'
        if self.id == 0:
            self.x = int((world.width - 1) / 2)
            self.y = int((world.height - 1) / 2)
            self.energy = 1000
            self.dir = 0
            self.id = 0
            self.birth = 0
            self.death = 0
            self.parent = 0
            self.genes = [random.randint(0, 9) for r in range(8)]

    def update(self, world):
        #print 'Animal::update called.'
        self.turn()
        self.move(world)
        self.eat(world)
        new = self.reproduce(world)
        return new

    def turn(self):
        #print 'Animal.turn called.'
        x = random.randint(0, sum(self.genes))

        def angle(genes, x):
            if len(genes) == 0:
                return 0
            xnu = x - genes[0]
            if xnu < 0:
                return 0
            else:
                return angle(genes[1:], xnu) + 1

        a = angle(self.genes, x)
        self.dir = (self.dir + a) % 8

    def move(self, world):
        #print 'Animal.move called.'
        direction = self.dir
        x = self.x
        y = self.y

        def movex(direction):
            if (direction >= 2 and direction <= 4):
                return 1
            elif (direction == 1 or direction == 5):
                return 0
            else:
                return -1

        def movey(direction):
            if (direction >= 0 and direction <= 2):
                return -1
            elif (direction >= 4 and direction <= 6):
                return 1
            else:
                return 0

        self.x = (x + movex(direction)) % world.width
        # oops... here was a critical bug. the below 'y' was 'x'...orz
        self.y = (y + movey(direction)) % world.height
        self.energy -= 1

    def eat(self, world):
        #print 'Animal.eat called.'
        for p in world.plants:
            if p.x == self.x and p.y == self.y:
                self.energy += world.plant_energy
                world.plants.remove(p)

    def reproduce(self, world):
        #print 'Animal.reproduce called.'
        import copy
        e = self.energy
        if e >= world.reproduce_energy:
            self.energy = (e - 1) / 2
            animal_new = copy.copy(self)
            # last [:] is important for copying the entire list. or deepcopy()?
            genes = list(animal_new.genes)[:]
            mutation = random.randint(0, 7)
            original = True
            if original:
                genes[mutation] = max(1, genes[mutation]
                                      + random.randint(0, 2) - 1)
            else:
                g = random.randint(1, 10)
                if genes[mutation] == g:
                    genes[mutation] = 1
                else:
                    genes[mutation] = g

            animal_new.genes = genes
            world.animal_id += 1
            animal_new.id = world.animal_id
            animal_new.birth = world.clock
            animal_new.parent = self.id
            return animal_new
        else:
            return None

    def kill(self):
        print 'Animal.kill called.'
        return

    def show(self):
        print 'id: %6d p: %6d x: %3d y: %3d dir: %d e: %3d b:%6d d: %6d g: %s' \
            % (self.id,
               self.parent,
               self.x,
               self.y,
               self.dir,
               self.energy,
               self.birth,
               self.death,
               self.genes)
        return


class Plant(object):
    x = 0
    y = 0

    def __init__(self, world, pos):
        #print 'Plant.__init__ called.'
        (left, top, width, height) = pos
        deltax = width - left
        deltay = height - top
        x = (left + random.randint(0, deltax - 1))
        y = (top + random.randint(0, deltay - 1))
        for p in  world.plants:
            if p.x != x and p.y != y:
                self.x = x
                self.y = y
        else:
            return None

    def show(self):
        print 'x: %3d y: %3d' % (self.x, self.y)


class World(object):
    # the entire wold, and jungle
    width = 100
    height = 30
    land = [0, 0, width, height]
#    jungle = [45, 10, 10, 10]
    jungle = [45, 10, 65, 20]
    # world clock
    clock = 0
    #
    killed_animal = 0
    # constants
    plant_energy = 80
    reproduce_energy = 200
    #
    # list of Plant object
    plants = []
    # list of Animal object
    animals = []
    animals_dead = []
    animal_id = 0

    def __init__(self):
        #print 'World.__init__ called.'
        self.animals.append(Animal(self))
        self.plants.append(Plant(self, self.land))
        self.plants.append(Plant(self, self.jungle))
        return

    def update(self):
        #print 'World.update called.'
        self.clock += 1
        for animal in self.animals:
            if animal.energy <= 0:
                self.animals.remove(animal)
                if self.track_animals:
                    self.animals_dead.append(animal)
                animal.death = self.clock
                self.killed_animal += 1
        animals_new = []
        for animal in self.animals:
#            animal.turn()
#            animal.move(self)
#            animal.eat(self)
#            new = animal.reproduce(self)
            new = animal.update(self)
            if new:
                animals_new.append(new)
        self.animals.extend(animals_new)
        self.plants.append(Plant(self, self.land))
        self.plants.append(Plant(self, self.jungle))

    def draw(self):
        #print 'World.draw called'
        num_alive = 0
        age_total = 0
        energy_total = 0

        # better algorithm/data structure for lookup ???
        aa = []
        for a in self.animals:
            aa.append([a.x, a.y])
            age_total += (self.clock - a.birth)
            energy_total += a.energy
            num_alive += 1

        pp = []
        for p in self.plants:
            pp.append([p.x, p.y])

        # work around...
        if num_alive == 0:
            num_alive = 1
        print 'w: %d h: %d update: %d #animals: %d #killed: %d ' \
            '#plants: %d avg.age: %.1f avg.energy %.1f' \
            % (self.width, self.height, self.clock,
               len(self.animals), self.killed_animal,
               len(self.plants), float(age_total) / num_alive,
               float(energy_total) / num_alive)

        if self.quiet:
            return

        print '+%s+' % ('-' * self.width)
        for y in range(0, self.height):
            msg = ''
            for x in range(0, self.width):
                if [x, y] in aa:
                    msg = msg + self.sym_animal
                elif [x, y] in pp:
                    msg = msg + self.sym_plant
                else:
                    msg = msg + self.sym_space
            print '%s%s%s' % ('|', msg, '|')
        print '+%s+' % ('-' * self.width)

    def dump(self):
        return


class Evolution(World):
    #
    # config variables
    #
    debug = 0
    prompt = 'evolution: '
    sym_space = '-'
    sym_animal = 'A'
    sym_plant = 'T'
    batch = 0
    quiet = 0
    interval = 1
    total = 1000
    track_animals = 0

    def __init__(self, argv):
        super(Evolution, self).__init__()
        self.parse_args(argv)

    def usage(self, argv):
        print 'Usage: ', argv[0], ' [options]'
        print '  options: -i <interval>      : interval to show status info.'
        print '           -t <total update>  : total update count'
        print '           -b                 : batch mode'
        print '           -q                 : quiet mode'
        print '           -T                 : track killed animals too'

    def parse_args(self, argv):
        #print 'Evolution.parse_args called.'
        try:
            opts, args = getopt.getopt(argv[1:],
                                       'i:t:bqTA:P:S:',
                                       ['interval=', 'total=',
                                        'batch', 'quiet'])
        except getopt.GetoptError:
            print sys.exc_info()[1]
            self.usage(argv)
            sys.exit(2)

        for opt, arg in opts:
            if opt in ('-b' or '--batch'):
                self.batch = 1
            elif opt in ('-q' or '--quiet'):
                self.quiet = 1
            elif opt in ('-i' or '--interval'):
                self.interval = int(arg)
            elif opt in ('-t' or '--total'):
                self.total = int(arg)
            elif opt in ('-T' or '--track-animals'):
                self.track_animals = 1
            elif opt in ('-A'):
                self.sym_animal = arg
            elif opt in ('-P'):
                self.sym_plant = arg
            elif opt in ('-S'):
                self.sym_space = arg
            else:
                sys.exit(1)

    def interact(self):
        # print 'Evolution.interact called'
        import readline

        self.draw()

        while True:
            try:
                x = 0
                line = raw_input(self.prompt)

            except EOFError:
                print 'quitting...'
                sys.exit(0)

            if line == 'quit':
                print 'quitting...'
                sys.exit(0)
                    
            elif line == 'dump':
                x = 0
                print 'Alive animals'
                for a in self.animals:
                    a.show()
                continue

            elif line == 'dumpd':
                x = 0
                print 'Dead animals'
                for a in self.animals_dead:
                    a.show()
                continue

            elif line == 'dumpplant':
                x = 0
                for p in self.plants:
                    p.show()
                continue

            elif line.isdigit():
                x = int(line)

            else:
                x = 1

            for i in range(0, x):
                self.update()

            self.draw()

    def run(self):
        #print 'Evolution.run called.'
        if self.batch == 0:
            self.interact()

        else:
            for x in range(0, self.total):
                self.update()
                if self.clock % self.interval == 0:
                    self.draw()


if __name__ == '__main__':

    ev = Evolution(sys.argv)
    ev.run()
