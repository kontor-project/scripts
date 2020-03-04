import copy
import multiprocessing
import time
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

        self._model = copy.copy(model)
        self.h = None

    def get_model(self):
        pass
        return self._model

    def load_model(self):
        pass
        self._model = VspModel(self._filename)

    def set_model_param(self, id, value):
        pass
        self._model.set_param(id=id, value=value)
        self.save_model()
        self.load_model()
        self.h = self._model.h()
        print('->', self.h)
    def save_model(self):
        pass
        self._model.save_file(self._filename)

def modify_detached(model, i, element, c, child_number, children):
    pass
    value = model['FuselageBase']['XSec'][i][element]['value'] * c
    id = model['FuselageBase']['XSec'][i][element]['_id']
    # create new node
    child = Node(child_number=child_number + 1, model=model)
    child.set_model_param(id=id, value=value)
    # sometimes we get h = 0 because of who knows
    children[child_number] = child

filename = '/home/mregger/Documents/HardwareStuff/kontor/design/openVSP/kontor.vsp3'

performance = {
    'h': [],
    'c': [],
    't': []
}

t = 2      # number of iterations
c = 0.90     # change factor (multiply values by this)

h = 0         # current heuristic value
old_h = None  # previous heuristic value

# minimum size constraints so we have space inside the plane
tail_min_width = 0.5
tail_min_height = 0.5
cockpit_min_width = 2
cockpit_min_height = 3.5
nose_min_height = 3

starting_model = VspModel(filename)
parent = Node(starting_model, filename=filename)


while t > 0:
    pass
    i = 0

    manager = multiprocessing.Manager()
    model = parent.get_model()
    sections = model['FuselageBase']['XSec']
    jobs = []
    child_number = 0
    children = manager.dict()

    for i in range(3, len(sections)):
        pass
        for element in sections[i]:
            pass
            # if 'Angle' in element or 'Strength' in element or 'Slew' in element:
            if 'Angle' in element and 'Top' in element:
                pass
                child = multiprocessing.Process(target=modify_detached, args=(model, i, element, (1 + c), child_number, children, ))
                child.start()
                jobs.append(child)
                child_number += 1
                # time.sleep(2)
                child = multiprocessing.Process(target=modify_detached, args=(model, i, element, (1 - c), child_number, children, ))
                child.start()
                jobs.append(child)
                child_number += 1
                # time.sleep(2)

    pool = multiprocessing.Pool(processes=child_number)
    # children = pool.map(child, [c for c in range(child_number)])
    print('waiting for children...')
    for child in jobs:
        pass
        child.join()
    print('done')
    pool.close()
    # run heuristic
    dir(children.values())
    results = children.values().sort(key=lambda x: x.h, reverse=True)
    print(len(children))
    parent = Node(model=children[0].get_model(), filename=filename)
    print('pick of the litter: ', children[0]._filename)
    print('---------------------------\nt: ', t)
    t -= 1
    c *= 0.9
    child_number = 0
# plt.plot(performance['h'], label='h')
# plt.plot(performance['c'], label='c')
# plt.savefig('r.png')
# plt.clf()
