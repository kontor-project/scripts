import matplotlib.pyplot as plt
from vsp_interface import VspModel

filename = '/home/mregger/Documents/HardwareStuff/kontor/design/openVSP/kontor.vsp3'

performance = {
    'h': [],
    'c': [],
    't': []
}

t = 100      # number of iterations
c = 0.40     # change factor (multiply values by this)

h = 0         # current heuristic value
old_h = None  # previous heuristic value

# minimum size constraints so we have space inside the plane
tail_min_width = 0.5
tail_min_height = 0.5
cockpit_min_width = 2
cockpit_min_height = 3.5
nose_min_height = 3

model = VspModel(filename)
while t > 0:
    pass
    i = 0
    # open file

    # modify by constant
    base_sections = model['FuselageBase']['XSecCurve']
    slope_sections = model['FuselageBase']['XSec']
    tail_sections = model['TailFuselage']['XSecCurve']
    for i in range(0, len(base_sections)):
        pass
        for element in base_sections[i]:
            pass
            if 'Width' in element:
                pass
                value = model['FuselageBase']['XSecCurve'][i][element]['value'] * (c + 1)
                id = model['FuselageBase']['XSecCurve'][i][element]['_id']

                if i <= 2 and value > tail_min_width:
                    model.set_param(id=id, value=value)
                elif i > 2 and value > cockpit_min_width:
                    model.set_param(id=id, value=value)

            elif 'Height' in element:
                value = model['FuselageBase']['XSecCurve'][i][element]['value'] * (c + 1)
                id = model['FuselageBase']['XSecCurve'][i][element]['_id']

                if i <= 5 and value > cockpit_min_height:
                    model.set_param(id=id, value=value)
                elif i > 5 and value > nose_min_height:
                    model.set_param(id=id, value=value)

    for i in range(0, len(tail_sections)):
        pass
        for element in tail_sections[i]:
            pass
            if 'Width' in element:
                pass
                value = model['TailFuselage']['XSecCurve'][i][element]['value'] * (1 + c)
                id = model['TailFuselage']['XSecCurve'][i][element]['_id']

                if value > 0.5:
                    model.set_param(id=id, value=value)

            elif 'Height' in element:
                value = model['TailFuselage']['XSecCurve'][i][element]['value'] * (1 + c)
                id = model['TailFuselage']['XSecCurve'][i][element]['_id']

                if value > 0.5:
                    model.set_param(id=id, value=value)

    model.save_file(filename=filename)
    model = VspModel(filename)
    # run heuristic
    h = model.h()
    print('C: ', c, ' h: ', h, ' t: ', t)
    performance['h'].append(h)
    performance['c'].append(c+1)
    performance['t'].append(t)
    # if heuristic is better than before, continue. Else change direction
    if old_h is not None and old_h < h:
        pass
        print('Wrong way, turn around...')
        c *= -0.99
    elif old_h is not None and old_h >= h:
        pass
        print('Getting closer...')
        c *= 0.99
    old_h = h
    t -= 1

plt.plot(performance['h'], label='h')
plt.plot(performance['c'], label='c')
plt.savefig('r.png')
plt.clf()
