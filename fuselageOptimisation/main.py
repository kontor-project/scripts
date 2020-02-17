from vsp_interface import VspModel

filename = '/home/mregger/Documents/HardwareStuff/kontor/design/openVSP/kontor.vsp3'

t = 50      # number of iterations
c = 2   # change factor (multiply values by this)

h = 0         # current heuristic value
old_h = None  # previous heuristic value

# minimum size constraints so we have space inside the plane
tail_min_width = 0.5
tail_min_height = 0.5
cockpit_min_width = 2
cockpit_min_height = 3.5
nose_min_height = 3

while t > 0:
    pass
    i = 0
    # open file
    model = VspModel(filename)

    # modify by constant
    base_sections = model['FuselageBase']['XSecCurve']
    tail_sections = model['TailFuselage']['XSecCurve']
    for i in range(0, len(base_sections)):
        pass
        for element in base_sections[i]:
            pass
            if 'Width' in element:
                pass
                value = model['FuselageBase']['XSecCurve'][i][element]['value'] * c
                id = model['FuselageBase']['XSecCurve'][i][element]['_id']

                if i <= 2 and value > tail_min_width:
                    model.set_param(id=id, value=value)
                elif i > 2 and value > cockpit_min_width:
                    model.set_param(id=id, value=value)

            elif 'Height' in element:
                value = model['FuselageBase']['XSecCurve'][i][element]['value'] * c
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
                value = model['TailFuselage']['XSecCurve'][i][element]['value'] * c
                id = model['TailFuselage']['XSecCurve'][i][element]['_id']

                if value > 0.5:
                    model.set_param(id=id, value=value)

            elif 'Height' in element:
                value = model['TailFuselage']['XSecCurve'][i][element]['value'] * c
                id = model['TailFuselage']['XSecCurve'][i][element]['_id']

                if value > 0.5:
                    model.set_param(id=id, value=value)

    model.save_file(filename=filename)
    # run heuristic
    h = model.h()
    # if heuristic is better than before, continue. Else change direction
    if old_h is not None and old_h < h:
        pass
        print('Wrong way, turn around...')
        c *= -0.95
    elif old_h is not None and old_h >= h:
        pass
        print('Getting closer...')
        c *= 0.95
    old_h = h
    print('C: ', c, ' h: ', h, ' t: ', t)
    t -= 1
