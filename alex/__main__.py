from sys import argv

from . import alex


with open(argv[1]) as f:
    for token in alex(f.read()):
        print(repr(token))
