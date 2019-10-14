from rules import *
import re

class Parser(object):
    rules = [LiteralRule(), WildCardRule(), StepRule(), RangeRule(), ListRule(), DefaultRule()]

    tokens_properties = [
        {'label': 'minute', 'min': 0, 'max': 59},
        {'label': 'hour', 'min': 0, 'max': 23},
        {'label': 'day of month', 'min':1, 'max': 31},
        {'label': 'month', 'min': 1, 'max': 12},
        {'label': 'day of week', 'min': 0, 'max': 6}
    ]

    def parse(self, expression:str) -> dict:
        if expression == None:
            raise RuntimeError("expression cannot be None!")

        tokens = re.compile("\s+").split(expression.strip())

        if len(tokens) < 6:
            raise RuntimeError("invalid expression '{}' it needs to have at least 6 space separated values".format(expression))

        entry = {'command': " ".join(tokens[5:])}
        tokens = tokens[:5]

        for index, token in enumerate(tokens):
            label = self.tokens_properties[index]['label']
            minimum = self.tokens_properties[index]['min']
            maximum = self.tokens_properties[index]['max']

            try:
                rule = next(filter(lambda rule: rule.match(token), self.rules))
                entry[label] = rule.parse(token, minimum, maximum)
            except RuntimeError as e:
                raise RuntimeError('error while parsing `{}` with value `{}` and position `{}`, {}'.format(label, token, index, e))
        return entry
