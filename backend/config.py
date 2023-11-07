classes = ['asphalt', 'pavement', 'gravel', 'dirt']


def map_to_int(c):
    for i, e in enumerate(classes):
        if c == e:
            return i


def map_to_string(i):
    return classes[i]
