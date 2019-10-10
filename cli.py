#!/usr/bin/python3

import sys
from cronparser import Parser

def print_numlist(numlist):
    return " ".join([str(num) for num in numlist])

def pretty_print(entry):
    print("minute       {}".format(print_numlist(entry['minute'])))
    print("hour         {}".format(print_numlist(entry['hour'])))
    print("day of month {}".format(print_numlist(entry['day of month'])))
    print("month        {}".format(print_numlist(entry['month'])))
    print("day of week  {}".format(print_numlist(entry['day of week'])))
    print("command      {}".format(entry['command']))

args = sys.argv[1:]
entry = Parser().parse(" ".join(args))
pretty_print(entry)
