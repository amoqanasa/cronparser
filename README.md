[![Build Status](https://travis-ci.org/abugnais/cronparser.svg?branch=master)](https://travis-ci.org/abugnais/cronparser) 
[![codecov](https://codecov.io/gh/abugnais/cronparser/branch/master/graph/badge.svg)](https://codecov.io/gh/abugnais/cronparser)


Cron Expression Parser Written In Python
========================================

## Installation
```bash
git clone https://github.com/abugnais/cronparser.git
cd cronparser
pip3 install -r requirements.txt
```
**Note**: This was tested against python versions 3.4, 3.5, 3.6, 3.7

## Run tests
```bash
python3 cronparser_test.py
```
Test expressions were generated using https://crontab.guru

## Usage

### CLI
Pass the cron expression as parameter to the cli.py script, and make sure surround the expression parameter with quotes
```bash
python3 cli.py "*/15 0 1,15 * 1-5 /usr/bin/find"
```

### Python

```python
from cronparser import Parser
expression = "*/15 0 1,15 * 1-5 /usr/bin/find"
result = Parser().parse(expression)
```

## Known issue/Corner case
In the case where the step expression combined with either a literal or a range of values like this example
```
* * * * 1-5/20 /usr/bin/find
```
Or this example
```
* * * * */20 /usr/bin/find
```
Note that 20 is larger than the maximum value for the day of the week which is 6, although this expression is valid in most crontab implementations, it is quiet tricky to represent as a list of values, therefore I decided not to raise and error in such cases, until I figure out a solid and predictable solution for such cases.

For now the current behaviour for such cases is represented in test cases ```test_month_range_large_step``` and ```test_month_large_step```.
