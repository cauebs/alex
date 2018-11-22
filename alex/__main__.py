from sys import argv

from . import alex


def call_alex_and_print_errors(string):
    errors = yield from alex(string)
    for error in errors:
        print(error)


with open(argv[1]) as f:
    for token in call_alex_and_print_errors(f.read()):
        print(repr(token))
