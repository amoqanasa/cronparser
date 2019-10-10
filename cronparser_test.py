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

    def test_parse_hourly(self):
        expression = '* * * * * /test/command'
        result = self.parser.parse(expression)

        self.assertEqual(result['day of week'], [day for day in range(7)])
        self.assertEqual(result['day of month'], [day for day in range(1, 32)])
        self.assertEqual(result['hour'], [hour for hour in range(24)])
        self.assertEqual(result['minute'], [minute for minute in range(60)])
        self.assertEqual(result['month'], [month for month in range(1, 13)])
        self.assertEqual(result['command'], '/test/command')

    def test_parse_monthly(self):
        expression = '0 0 1 * * /test/command'
        result = self.parser.parse(expression)

        self.assertEqual(result['day of week'], [day for day in range(7)])
        self.assertEqual(result['day of month'], [1])
        self.assertEqual(result['hour'], [0])
        self.assertEqual(result['minute'], [0])
        self.assertEqual(result['month'], [month for month in range(1, 13)])
        self.assertEqual(result['command'], '/test/command')


    def test_parse_yearly(self):
        expression = '0 0 1 1 * /test/command'
        result = self.parser.parse(expression)

        self.assertEqual(result['day of week'], [day for day in range(7)])
        self.assertEqual(result['day of month'], [1])
        self.assertEqual(result['hour'], [0])
        self.assertEqual(result['minute'], [0])
        self.assertEqual(result['month'], [1])
        self.assertEqual(result['command'], '/test/command')

if __name__ == '__main__':
    unittest.main()