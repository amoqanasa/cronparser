import sys
from cronparser import Parser

def pretty_print(entry):
    keys = entry.params.keys()
    longest_key = max(keys, key=len)

    print(entry.expression)

    for key in entry.params:
        space_padding = (len(longest_key) - len(key) + 5) * " "
        values =  ' '.join(str(val) for val in entry.params[key])
        print("{}{}{}".format(key, space_padding, values))

    print("{}{}{}".format("command", (len(longest_key) - len("command") + 5) * " ", entry.command))
    print("\n")

args = sys.argv[1:]
entry = Parser().parse(" ".join(args))
pretty_print(entry)
