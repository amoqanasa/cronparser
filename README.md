[![Build Status](https://travis-ci.org/abugnais/cronparser.svg?branch=master)](https://travis-ci.org/abugnais/cronparser)

Cron Expression Parser Written In Python
========================================

## Installation
```bash
git clone https://github.com/abugnais/cronparser.git
cd cronparser
pip3 install -r requirements.txt
```

## Run tests
```bash
python3 cronparser_test.py 
```

## Usage

### CLI
Pass the cron expression as parameter to the cli.py script, and make sure to escape the special characters

```bash
python3 cli.py \*/15 0 1,15 \* 1-5 /usr/bin/find
```

### Python

```python
from cronparser import Parser
result = Parser().parse(expression)
```