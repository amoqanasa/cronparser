
import re
from typing import List

class Rule(object):
    def match(self, expression:str) -> bool:
        raise RuntimeError('match is not implemented')

    def parse(self, expression:str, values:List[int]) -> List[int]:
        raise RuntimeError('parse is not implemented')

class StepRule(Rule):
    step_regex = '^(\d*|\*)\/\d*$'

    def match(self, expression:str) -> bool:
        return re.match(self.step_regex, expression) != None

    def parse(self, expression:str, values:List[int]) -> List[int]:
        params = expression.split('/')
        base = params[0]
        step = int(params[1])

        if base == '*':
            base = 0
        else:
            base = int(base)

        if step > values[-1]:
            step = step % values[-1]
        return [val for val in range(base, values[-1], step)]

class ListRule(Rule):
    regex = '^\d+(,\d+)+$'

    def match(self, expression:str) -> bool:
        return re.match(self.regex, expression) != None

    def parse(self, expression:str, values:List[int]) -> List[int]:
        params = [int(param) for param in expression.split(',')]
        for param in params:
            if param not in values:
                raise Exception('invalid list values')
        return sorted(params)

class WildCardRule(Rule):
    def match(self, expression:str) -> bool:
        return expression == '*'

    def parse(self, expression:str, values:List[int]) -> List[int]:
        return values

class LiteralRule(Rule):
    regex = '^\d*$'

    def match(self, expression:str) -> bool:
        return re.match(self.regex, expression) != None

    def parse(self, expression:str, values:List[int]) -> List[int]:
        value = int(expression)
        if  value not in values:
            raise RuntimeError("invalid value {} not included in {}".format(str(value), values))
        return [value]

class RangeRule(Rule):
    regex = '^\d*\-\d*(\/\d*)?$'

    def match(self, expression:str) -> bool:
        return re.match(self.regex, expression) != None

    def parse(self, expression:str, values:List[int]) -> List[int]:
        params = re.compile('[\-\/]').split(expression)
        start = int(params[0])
        end = int(params[1])
        step = int(params[2]) if len(params) == 3 else 1

        if step > values[-1]:
            step = step % values[-1]

        if start > end:
            raise RuntimeError('invalid expression beginning of the range {} is greater than the end of the range {}'.format(start, end))
        if start < values[0]:
            raise RuntimeError('invalid expression beginning of the range {} is less than the minimum allowed value {}'.format(start, values[0]))
        if end > values[-1]:
            raise RuntimeError('invalid expression end of the range {} is greater than the maximum allowed value {}'.format(end, values[-1]))
        return [v for v in range(start, end + 1, step)]

class DefaultRule(Rule):
    def match(self, expression):
        raise RuntimeError('none of the rules were matched for expression {}'.format(expression))

    def parse(self, expression:str, values:List[int]) -> List[int]:
        raise RuntimeError('none of the rules were matched for expression {}'.format(expression))

class Parser(object):
    rules = [LiteralRule(), WildCardRule(), StepRule(), RangeRule(), ListRule(), DefaultRule()]

    chunks = [
        {'label': 'minute', 'values': [minute for minute in range(0, 60)]},
        {'label': 'hour', 'values': [hour for hour in range(0, 24)]},
        {'label': 'day of month', 'values': [day for day in range(1, 32)]},
        {'label': 'month', 'values': [month for month in range(1, 13)]},
        {'label': 'day of week', 'values': [day for day in range(0, 7)]}
    ]

    def parse(self, expression) -> dict:
        tokens = expression.split(" ")
        result = {}
        entry = {}

        entry["expression"] = expression

        if len(tokens) < 6:
            raise RuntimeError("invalid expression '{}' it needs to have at least 6 space separated values".format(expression))

        entry['command'] = " ".join(tokens[5:])
        tokens = tokens[:5]

        for index, token in enumerate(tokens):
            label = self.chunks[index]['label']
            values = self.chunks[index]['values']
            rule = next(filter(lambda rule: rule.match(token), self.rules))
            entry[label] = rule.parse(token, values)

        return entry