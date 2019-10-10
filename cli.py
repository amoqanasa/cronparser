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

if len(sys.argv) < 2:
    print("you need to pass a crontab expression as a first parameter")
    exit(1)

args = sys.argv[1:]
expression = " ".join(args)

try:
    entry = Parser().parse(expression)
    pretty_print(entry)
except RuntimeError as e:
    print("unable to parse the expression {} an error was thrown by the parser\n{}".format(expression, e))
