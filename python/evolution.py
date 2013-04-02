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


def draw_world():
    global counter, killed_animal, sym_space, sym_animal, sym_plant, quiet
#    print 'draw_world called.'

    num_alive = 0
    age_total = 0
    energy_total = 0

    aa = []
    for a in animals:
        aa.append([a['x'], a['y']])
        age_total += (counter - a['birth'])
        energy_total += a['energy']
        num_alive += 1

    print 'w: %d h: %d update: %d #animals: %d #killed: %d ' \
        '#plants: %d avg.age: %.1f avg.energy %.1f' \
        % (width, height, counter, len(animals), killed_animal, len(plants),
           float(age_total) / num_alive, float(energy_total) / num_alive)

    if quiet:
        return

    for y in range(0, height):
        msg = ''
        for x in range(0, width):
            if [x, y] in aa:
                msg = msg + sym_animal
            elif {'x': x, 'y': y} in plants:
                msg = msg + sym_plant
            else:
                msg = msg + sym_space
        print '%s%s%s' % ('|', msg, '|')
    return


def move(animal):
#    print 'move called.'
    direction = animal['dir']
    x = animal['x']
    y = animal['y']

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

    animal['x'] = (x + movex(direction)) % width
    # oops... here was a critical bug. the below 'y' was 'x'...orz
    animal['y'] = (y + movey(direction)) % height
    animal['energy'] -= 1
    return


def turn(animal):
#    print 'turn called.'
    global debug
    x = random.randint(0, sum(animal['genes']))

    def angle(genes, x):
        if len(genes) == 0:
            return 0
        xnu = x - genes[0]
        if xnu < 0:
            return 0
        else:
            return angle(genes[1:], xnu) + 1

    a = angle(animal['genes'], x)
    animal['dir'] = (animal['dir'] + a) % 8
    return


def eat(animal):
#    print 'eat called.'
    pos = {'x': animal['x'], 'y': animal['y']}
    if pos in plants:
        animal['energy'] += plant_energy
        plants.remove(pos)
    return


def reproduce(animal):
#    print 'reproduce called.'
    global animals_added, animal_id, counter
    e = animal['energy']
    if e >= reproduce_energy:
        animal['energy'] = (e - 1) / 2
        animal_new = animal.copy()
        # last [:] is important for copying the entire list. or deepcopy()?
        genes = list(animal_new['genes'])[:]
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
        animal_new['genes'] = genes
        animal_id += 1
        animal_new['id'] = animal_id
        animal_new['birth'] = counter
        animal_new['parent'] = animal['id']
        animals_added.append(animal_new)
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
    global counter, killed_animal, animals_added, animals_dead, track_animals
    counter += 1
    for animal in animals:
        if animal['energy'] <= 0:
            animals.remove(animal)
            if track_animals:
                animals_dead.append(animal)
            animal['death'] = counter
            killed_animal += 1
    animals_added = []
    for animal in animals:
        turn(animal)
        move(animal)
        eat(animal)
        reproduce(animal)
    animals.extend(animals_added)
    add_plants()
    return


def print_animal(animal):
    print 'id: %6d p: %6d x: %3d y: %3d dir: %d e: %3d b:%6d d: %6d g: %s' \
        % (animal['id'],
           animal['parent'],
           animal['x'],
           animal['y'],
           animal['dir'],
           animal['energy'],
           animal['birth'],
           animal['death'],
           animal['genes'])


def evolution():
#    print 'evolution'
    import readline
    global prompt

    draw_world()

    while True:
        try:
            x = 0
            line = raw_input(prompt)

        except EOFError:
            print 'quitting...'
            sys.exit(0)

        if line == 'quit':
            print 'quitting...'
            sys.exit(0)

        elif line == 'dump':
            x = 0
            print 'Alive animals'
            for a in animals:
                print_animal(a)
            continue

        elif line == 'dumpd':
            x = 0
            print 'Dead animals'
            for a in animals_dead:
                print_animal(a)
            continue

        elif line == 'dumpplant':
            x = 0
            for p in plants:
                print p
            continue

        elif line.isdigit():
            x = int(line)

        else:
            x = 1

        for i in range(0, x):
            update_world()

        draw_world()

def usage():
    print 'Usage: ', sys.argv[0], ' [options]'
    print '  options: -i <interval>      : interval to show status info.'
    print '           -t <total update>  : total update count'
    print '           -b                 : batch mode'
    print '           -q                 : quiet mode'
    print '           -T                 : track killed animals too'

if __name__ == '__main__':

    debug = 0
    prompt = 'evolution: '
    sym_space = '-'
    sym_animal = 'A'
    sym_plant = 'T'

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
                'energy': 1000,
                'dir': 0,
                'id': 0,
                'birth': 0,
                'death': 0,
                'parent': 0,
                'genes': [random.randint(0, 9) for r in range(8)]
                }]
    animals_added = []
    animals_dead = []
    animal_id = 0

    batch = 0
    quiet = 0
    interval = 1
    total = 1000
    track_animals = 0
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   'i:t:bqT',
                                   ['interval=', 'total=',
                                    'batch', 'quiet'])
    except getopt.GetoptError:
        print sys.exc_info()[1]
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-b' or '--batch'):
            batch = 1
        elif opt in ('-q' or '--quiet'):
            quiet = 1
        elif opt in ('-i' or '--interval'):
            interval = int(arg)
        elif opt in ('-t' or '--total'):
            total = int(arg)
        elif opt in ('-T' or '--track-animals'):
            track_animals = 1
        else:
            sys.exit(1)

    add_plants()
    if batch:
        for x in range(0, total):
            update_world()
            if counter % interval == 0:
                draw_world()
    else:
        evolution()
