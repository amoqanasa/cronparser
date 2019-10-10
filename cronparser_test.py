import unittest
import cronparser

class ParserTest(unittest.TestCase):

    parser = cronparser.Parser()
    
    def test_parse_daily(self):
        expression = "0 0 * * * /test/command"
        result = self.parser.parse(expression)

        self.assertEqual(result.params['day of week'], [day for day in range(7)])
        self.assertEqual(result.params['day of month'], [day for day in range(1, 32)])
        self.assertEqual(result.params['hour'], [0])
        self.assertEqual(result.params['minute'], [0])
        self.assertEqual(result.params['month'], [month for month in range(1, 13)])
        self.assertEqual(result.command, '/test/command')

    def test_parse_hourly(self):
        expression = '* * * * * /test/command'
        result = self.parser.parse(expression)

        self.assertEqual(result.params['day of week'], [day for day in range(7)])
        self.assertEqual(result.params['day of month'], [day for day in range(1, 32)])
        self.assertEqual(result.params['hour'], [hour for hour in range(24)])
        self.assertEqual(result.params['minute'], [minute for minute in range(60)])
        self.assertEqual(result.params['month'], [month for month in range(1, 13)])
        self.assertEqual(result.command, '/test/command')

    def test_parse_monthly(self):
        expression = '0 0 1 * * /test/command'
        result = self.parser.parse(expression)

        self.assertEqual(result.params['day of week'], [day for day in range(7)])
        self.assertEqual(result.params['day of month'], [1])
        self.assertEqual(result.params['hour'], [0])
        self.assertEqual(result.params['minute'], [0])
        self.assertEqual(result.params['month'], [month for month in range(1, 13)])
        self.assertEqual(result.command, '/test/command')


    def test_parse_yearly(self):
        expression = '0 0 1 1 * /test/command'
        result = self.parser.parse(expression)

        self.assertEqual(result.params['day of week'], [day for day in range(7)])
        self.assertEqual(result.params['day of month'], [1])
        self.assertEqual(result.params['hour'], [0])
        self.assertEqual(result.params['minute'], [0])
        self.assertEqual(result.params['month'], [1])
        self.assertEqual(result.command, '/test/command')




if __name__ == '__main__':
    unittest.main()