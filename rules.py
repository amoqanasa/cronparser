
import re
from typing import List
from abc import ABC, abstractmethod

class BaseRule(ABC):
    @abstractmethod
    def match(self, expression:str) -> bool:
        pass

    @abstractmethod
    def parse(self, expression:str, minimum:int, maximum:int) -> List[int]:
        pass

class StepRule(BaseRule):
    regex = '^(\d*|\*)\/\d*$'

    def match(self, expression:str) -> bool:
        return re.match(self.regex, expression) != None

    def parse(self, expression:str, minimum:int, maximum:int) -> List[int]:
        params = expression.split('/')
        base = params[0]
        step = int(params[1])

        if base == '*':
            base = 0
        else:
            base = int(base)

        if step > maximum:
            raise RuntimeError('invalid expression, the step `{}` cannot be larger than the maximum value `{}`'.format(step, maximum))
        if step == 0:
            raise RuntimeError('invalid expression, the step cannot be zero')
        return [val for val in range(base, maximum, step)]

class ListRule(BaseRule):
    regex = '^\d+(,\d+)+$'

    def match(self, expression:str) -> bool:
        return re.match(self.regex, expression) != None

    def parse(self, expression:str, minimum:int, maximum:int) -> List[int]:
        params = [int(param) for param in expression.split(',')]
        for param in params:
            if param > maximum:
                raise RuntimeError('invalid list values eleement `{}` is greater than maximum value `{}`'.format(param, maximum))
            if param < minimum:
                raise RuntimeError('invalid list values eleement `{}` is less than minimum value `{}`'.format(param, minimum))
        return sorted(params)

class WildCardRule(BaseRule):
    def match(self, expression:str) -> bool:
        return expression == '*'

    def parse(self, expression:str, minimum:int, maximum:int) -> List[int]:
        return [value for value in range(minimum, maximum + 1)]

class LiteralRule(BaseRule):
    regex = '^\d*$'

    def match(self, expression:str) -> bool:
        return re.match(self.regex, expression) != None

    def parse(self, expression:str, minimum:int, maximum:int) -> List[int]:
        value = int(expression)
        if  value > maximum:
            raise RuntimeError("invalid value `{}` cannot be greater than the maximum allowed value `{}`".format(value, maximum))
        
        if value < minimum:
            raise RuntimeError("invalid value `{}` cannot be less than the minimum allowed value `{}`".format(value, minimum))
        return [value]

class RangeRule(BaseRule):
    regex = '^\d*\-\d*(\/\d*)?$'

    def match(self, expression:str) -> bool:
        return re.match(self.regex, expression) != None

    def parse(self, expression:str, minimum:int, maximum:int) -> List[int]:
        params = re.compile('[\-\/]').split(expression)
        start = int(params[0])
        end = int(params[1])
        step = int(params[2]) if len(params) == 3 else 1

        if step > maximum:
            raise RuntimeError('invalid expression, the step `{}` cannot be larger than the maximum value `{}`'.format(step, maximum))
        if step == 0:
            raise RuntimeError('invalid expression, the step cannot be zero')
        if start > end:
            raise RuntimeError('invalid expression beginning of the range {} is greater than the end of the range {}'.format(start, end))
        if start < minimum:
            raise RuntimeError('invalid expression beginning of the range {} is less than the minimum allowed value {}'.format(start, minimum))
        if end > maximum:
            raise RuntimeError('invalid expression end of the range {} is greater than the maximum allowed value {}'.format(end, maximum))
        return [v for v in range(start, end + 1, step)]

class DefaultRule(BaseRule):
    def match(self, expression):
        return True

    def parse(self, expression:str, minimum:int, maximum:int) -> List[int]:
        raise RuntimeError('none of the rules were matched for expression {}'.format(expression))