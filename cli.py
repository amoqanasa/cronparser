import sys
from cronparser import Parser

def pretty_print(entry):
    print("minute       {}".format(entry['minute']))
    print("hour         {}".format(entry['hour']))
    print("day of month {}".format(entry['day of month']))
    print("day of week  {}".format(entry['day of week']))
    print("month        {}".format(entry['month']))
    print("command      {}".format(entry['command']))

args = sys.argv[1:]
entry = Parser().parse(" ".join(args))
pretty_print(entry)
