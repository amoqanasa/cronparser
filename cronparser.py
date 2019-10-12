from rules import LiteralRule, WildCardRule, StepRule, RangeRule, ListRule, DefaultRule
import re

class Parser(object):
    rules = [LiteralRule(), WildCardRule(), StepRule(), RangeRule(), ListRule(), DefaultRule()]

    tokens_properties = [
        {'label': 'minute', 'values': [minute for minute in range(0, 60)]},
        {'label': 'hour', 'values': [hour for hour in range(0, 24)]},
        {'label': 'day of month', 'values': [day for day in range(1, 32)]},
        {'label': 'month', 'values': [month for month in range(1, 13)]},
        {'label': 'day of week', 'values': [day for day in range(0, 7)]}
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
            values = self.tokens_properties[index]['values']

            try:
                rule = next(filter(lambda rule: rule.match(token), self.rules))
                entry[label] = rule.parse(token, values)
            except RuntimeError as e:
                raise RuntimeError('error while parsing `{}` with value `{}` and position `{}`, {}'.format(label, token, index, e))
        return entry
