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
    'executor': def_dict(False, {}),
    'process': def_dict(True, {
        'loop': False,
        'do_action': False,
        'make_object': False,
        'actions': False,
        'objects': False,
        'double_quit': False,
        'double_start': False,
        'pause': False,
        'idle': False,
    }),
    'gui': def_dict(False, {}),
    'joystick': def_dict(False, {
        'movement': True,
        'error': True,
    }),
    'joystick': def_dict(False, {
        'sanity': True,
    })
}

core = {
    'comm': def_dict(False, {
        'try_uno_ports': False,
        'successful_port': True,
    }),
    'robot': def_dict(False, {
        'movement': True,
    }),
    'manual_control': def_dict(False, {
    }),
    'auomatic_control': def_dict(False, {
    }),
    'master': def_dict(True, {
        'key': False,
        'do_key': False,
        'unmapped_key': False,
    }),
    'joystick': def_dict(False, {
    }),
}

testing = {
    'slider': def_dict(True, {
        'moving': False,
        'name': False,
    }),
    'simple_joy': def_dict(False, {
    }),
}