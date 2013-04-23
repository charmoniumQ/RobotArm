import collections
import functools

# The lengths I have to run in order to create picklable dictionaries
# with a defualt value
def default(default):
    return default

def def_dict(default_val, start):
    return collections.defaultdict(
        functools.partial(default, default_val), start)


framework = {
    'controller': def_dict(False, {
    }),
    'executor': def_dict(False, {
    }),
    'process': def_dict(False, {
        '__init__': True,
        'double_start': True,
        'quit': True,
        'double_quit': True,
        'error': True,
    }),
    'gui': def_dict(False, {
    }),
    'joystick': def_dict(False, {
    }),
    'joystick': def_dict(False, {
    }),
}

core = {
    'comm': def_dict(False, {
    }),
    'robot': def_dict(False, {
        'direct_move': True,
    }),
    'manual_control': def_dict(False, {
    }),
    'auomatic_control': def_dict(False, {
    }),
    'master': def_dict(False, {
    }),
    'joystick': def_dict(False, {
    }),
    'simple_joy': def_dict(False, {
    }),
}

testing = {
    'slider': def_dict(False, {
    }),
}