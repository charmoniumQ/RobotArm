import collections as c
import functools


# The lengths I have to run in order to create picklable dictionaries
# with a defualt value
def default(default):
    return default


framework = {
    'controller': c.defaultdict(functools.partial(default, False), {
        'command': True,
    }),
    'executor': c.defaultdict(functools.partial(default, False), {}),
    'process': c.defaultdict(functools.partial(default, True), {
        'loop': False,
        '__init__': True,
        'do_action': False,
        'action_input': False,
        'double_quit': False,
        'paused': False,
        'idle': False,
    }),
    'gui': c.defaultdict(functools.partial(default, False), {}),
}

core = {
    'comm': c.defaultdict(functools.partial(default, False), {
        'try_uno_ports': False,
        'successful_port': True,
    }),
    'robot': c.defaultdict(functools.partial(default, False), {
        'command': True
    }),
}

testing = {
    'slider': c.defaultdict(functools.partial(default, False), {
        'moving': False,
        'name': False,
    }),
}
