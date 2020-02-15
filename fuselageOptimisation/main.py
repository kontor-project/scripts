from vsp_interface import VspModel

filename = '/home/mregger/Documents/HardwareStuff/kontor/design/openVSP/kontor.vsp3'

t = 10
c = 1.5

h = 0
old_h = None

while t > 0:
    pass
    i = 0
    # open file

    model = VspModel(filename)
    # modify by constant
    sections = model['FuselageBase']['XSecCurve']
    for i in range(0, len(sections)):
        pass
        for element in sections[i]:
            pass
            if 'X' in element or 'Y' in element:
                pass
                value = model['FuselageBase']['XSecCurve'][i][element]['value'] * c
                id = model['FuselageBase']['XSecCurve'][i][element]['_id']
                print('before: ', model['FuselageBase']['XSecCurve'][i][element]['value'])
                model.set_param(id=id, value=value)
                print('after: ', model['FuselageBase']['XSecCurve'][i][element]['value'])
    # save file to create vspaero files
    model.save_file(filename=filename)
    # run heuristic
    h = model.h()
    # if heuristic is better than before, continue. Else change direction
    if old_h is not None and old_h < h:
        pass
        print('Wrong way, turn around...')
        c *= -0.9
    elif old_h is not None and old_h >= h:
        pass
        print('Getting closer...')
        c *= 0.9
    old_h = h
    print('C: ', c, ' h: ', h)
    t -= 1
