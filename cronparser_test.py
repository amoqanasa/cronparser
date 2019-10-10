import unittest
import cronparser

class ParserTest(unittest.TestCase):

    parser = cronparser.Parser()
    
    def test_parse_daily(self):
        expression = "0 0 * * * /test/command"
        result = self.parser.parse(expression)

        self.assertEqual(result['day of week'], [day for day in range(7)])
        self.assertEqual(result['day of month'], [day for day in range(1, 32)])
        self.assertEqual(result['hour'], [0])
        self.assertEqual(result['minute'], [0])
        self.assertEqual(result['month'], [month for month in range(1, 13)])
        self.assertEqual(result['command'], '/test/command')

    def test_parse_minutely(self):
        expression = '* * * * * /test/command'
        result = self.parser.parse(expression)

        self.assertEqual(result['day of week'], [day for day in range(7)], "should run on any day of the week")
        self.assertEqual(result['day of month'], [day for day in range(1, 32)])
        self.assertEqual(result['hour'], [hour for hour in range(24)], "should run on every hour")
        self.assertEqual(result['minute'], [minute for minute in range(60)], "should fun on every minute")
        self.assertEqual(result['month'], [month for month in range(1, 13)])
        self.assertEqual(result['command'], '/test/command')

    def test_parse_hourly(self):
        expression = '0 * * * * /test/command'
        result = self.parser.parse(expression)

        self.assertEqual(result['day of week'], [day for day in range(7)], "should run on any day of the week")
        self.assertEqual(result['day of month'], [day for day in range(1, 32)])
        self.assertEqual(result['hour'], [hour for hour in range(24)], "should run on every hour")
        self.assertEqual(result['minute'], [0], "should run on minute 0")
        self.assertEqual(result['month'], [month for month in range(1, 13)])
        self.assertEqual(result['command'], '/test/command')

    def test_parse_monthly(self):
        expression = '0 0 1 * * /test/command'
        result = self.parser.parse(expression)

        self.assertEqual(result['day of week'], [day for day in range(7)], "should run on any day of the week")
        self.assertEqual(result['day of month'], [1], "should run on the first")
        self.assertEqual(result['hour'], [0], "should run on midnight")
        self.assertEqual(result['minute'], [0], "should run on minute 0")
        self.assertEqual(result['month'], [month for month in range(1, 13)])
        self.assertEqual(result['command'], '/test/command')


    def test_parse_yearly(self):
        expression = '0 0 1 1 * /test/command'
        result = self.parser.parse(expression)

        self.assertEqual(result['day of week'], [day for day in range(7)], "should run on any day of the week")
        self.assertEqual(result['day of month'], [1], "should only run on 1st of january")
        self.assertEqual(result['hour'], [0], "should run on midnight")
        self.assertEqual(result['minute'], [0], "should run on minute 0")
        self.assertEqual(result['month'], [1], "should run in january")
        self.assertEqual(result['command'], '/test/command')

if __name__ == '__main__':
    unittest.main()