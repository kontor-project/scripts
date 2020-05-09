import copy
import multiprocessing
import time
import random
import os
import matplotlib.pyplot as plt
from vsp_interface import VspModel

class Node():
    def __init__(self, model, child_number=None, filename=None):
        pass
        if child_number is not None:
            pass
            self._filename = 'tmp' + str(child_number) + '.vsp3'
        elif filename is not None:
            self._filename = filename
        self._mutations = []
        self._model = copy.copy(model)
        self.h = None

    def get_model(self):
        pass
        return self._model

    def get_mutations(self):
        pass
        return self._mutations

    def load_model(self):
        pass
        self._model = VspModel(self._filename)

    def set_filename(self, filename):
        pass
        self._filename = filename

    def set_model_param(self, id, value):
        pass
        self._model.set_param(id=id, value=value)
        self.save_model()
        self.load_model()
        self.h = self._model.h()
        print('->', self.h)
        self._mutations.append({'id': id, 'value': value})

    def set_model_params(self, params):
        pass
        for mutation in params:
            pass
            self._model.set_param(id=mutation['id'], value=mutation['value'])
            self._mutations.append({'id': mutation['id'], 'value': mutation['value']})

        self.save_model()
        self.load_model()
        self.h = self._model.h()
        print('->', self.h)

    def save_model(self):
        pass
        self._model.save_file(self._filename)

def detached_worker(mother, father, m, c, child_number, population):
    pass
    global section_start_bound
    model = 0
    # get model
    if mother is not None:
        model = mother.get_model()
    elif model is not None:
        model = m

    # append fathers attributes
    if father is not None:
        mutations = father.get_mutations()
    else:
        mutations = []

    # pick a random attribute
    sections = model['FuselageBase']['XSec']
    elements = sections[random.randint(section_start_bound, len(sections)-1)]
    filtered_elements = list(filter(lambda x: 'Angle' in x or 'Slew' in x or 'Strength' in x, elements))
    random_element = filtered_elements[random.randint(0, len(filtered_elements)-1)]

    # cause a random mutation to the random attribute
    value = elements[random_element]['value'] * (c + 1) * random.uniform(0, 1)
    id = elements[random_element]['_id']
    mutations.append({'id': id, 'value': value})

    # give birth
    child = Node(child_number=child_number + 1, model=model)

    # set parameters
    child.set_model_params(mutations)

    # sometimes we get h = 0 because of who knows
    population.append(child)

filename = '/home/mregger/Documents/HardwareStuff/kontor/design/openVSP/kontor.vsp3'

performance = {
    'h': [],
    'c': [],
    't': []
}
max_workers = 10 # max number of subproccesses allowed

t = 100       # number of iterations
c = 0.30    # change factor (multiply values by this)
dc = 0.9    # rate of change in c

r = 1.0       # probability of making a wrong step
dr = 0.8      # rate of change of randomness probability
h = 0         # current heuristic value
old_h = None  # previous heuristic value

# minimum size constraints so we have space inside the plane
tail_min_width = 0.5
tail_min_height = 0.5
cockpit_min_width = 2
cockpit_min_height = 3.5
nose_min_height = 3
section_start_bound = 3

population_size = 100
child_number = -int(population_size/10) - 1
jobs = []
job_number = 0

manager = multiprocessing.Manager()
parent_population = manager.list()

starting_model = VspModel(filename)

# start population
for i in range(0, int(population_size/10)):
    parent = Node(starting_model, filename=filename)
    parent.h = 99
    child = multiprocessing.Process(target=detached_worker, args=(None, None, starting_model, c, child_number, parent_population, ))
    child.start()
    jobs.append(child)
    parent_population.append(parent)

for parent in jobs:
    pass
    parent.join()
jobs = []


while t > 0:
    pass
    i = 0

    jobs = []
    population = manager.list()
    print('++++++++++++++++++++...>>', len(parent_population))
    for mother in parent_population:
        for father in parent_population:
            pass
            child = multiprocessing.Process(target=detached_worker, args=(mother, father, None, c, child_number, population, ))
            child.start()
            jobs.append(child)
            child_number += 1
            if len(jobs) >= max_workers:
                print('waiting for population...')
                for child in jobs:
                    pass
                    child.join()
                jobs = []

    for child in jobs:
        pass
        child.join()
    jobs = []

    pool = multiprocessing.Pool(processes=population_size)
    # population = pool.map(child, [c for c in range(child_number)])
    print('done')
    pool.close()

    # record parent population
    parent_population = sorted(population[:],key = lambda x: x.h)[:len(parent_population)]
    print('------------------>', len(parent_population))
    child_number = -len(parent_population)-1
    for parent in parent_population:
        parent.load_model()
        parent.set_filename('tmp'+str(child_number))
        child_number += 1
        parent.save_model()

    # reset values
    t -= 1
    c *= dc
    r *= dr
    child_number = 0
    print('---------------------------\nt: ', t, ' -- ', r)

winner = parent_population[0]
winner.load_model()
winner.set_filename(filename)
winner.save_model()

# plt.plot(performance['h'], label='h')
# plt.plot(performance['c'], label='c')
# plt.savefig('r.png')
# plt.clf()
