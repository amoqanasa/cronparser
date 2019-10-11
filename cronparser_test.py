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

    def test_parse_monday_tuesday(self):
        expression = '0 0 * * 1,2 /test/command'
        result = self.parser.parse(expression)

        self.assertEqual(result['day of week'], [1, 2], "should run on day 1 and 2 of the week")
        self.assertEqual(result['command'], '/test/command')

    def test_parse_every_five_minutes(self):
        expression = '*/5 * * * * /test/command'
        result = self.parser.parse(expression)

        self.assertEqual(result['minute'], [minute for minute in range(0, 60, 5)], "should run every five minutes")
        self.assertEqual(result['command'], '/test/command')

    def test_parse_every_2_minutes_from10(self):
        expression = '10/2 * * * * /test/command'
        result = self.parser.parse(expression)

        self.assertEqual(result['minute'], [minute for minute in range(10, 60, 2)], "should run every 2 minutes starting from 10")
        self.assertEqual(result['command'], '/test/command')

    def test_january_to_march(self):
        expression = '*/5 * * 1-3 * /test/command'
        result = self.parser.parse(expression)

        self.assertEqual(result['month'], [1, 2, 3], "should run in months 1, 2, 3")
        self.assertEqual(result['command'], '/test/command')

    def test_missing_command(self):
        expression = '0 0 * * 1,2'
        self.assertRaises(RuntimeError, self.parser.parse, expression)

    def test_none_expression(self):
        expression = None
        self.assertRaises(RuntimeError, self.parser.parse, expression)

    def test_invalid_day_range(self):
        expression = '0 0 * * 1-15 /test/command'
        self.assertRaises(RuntimeError, self.parser.parse, expression)

    def test_invalid_literal_value(self):
        expression = '0 0 * * 9 /test/command'
        self.assertRaises(RuntimeError, self.parser.parse, expression)

    def test_invalid_minute_range(self):
        expression = '15-10 0 * * 1 /test/command'
        self.assertRaises(RuntimeError, self.parser.parse, expression)

    def test_month_range_large_step(self):
        expression = '1-10 0 * 1-5/13 1 /test/command'
        self.assertRaises(RuntimeError, self.parser.parse, expression)

    def test_month_range_zero_step(self):
        expression = '1-10 0 * 1-5/0 1 /test/command'
        self.assertRaises(RuntimeError, self.parser.parse, expression)

    def test_norule_matched(self):
        expression = '0 0 * * sun-mon /test/command'
        self.assertRaises(RuntimeError, self.parser.parse, expression)

    def test_invalid_list(self):
        expression = '0 0 * * 1,4,8 /test/command'
        self.assertRaises(RuntimeError, self.parser.parse, expression)


if __name__ == '__main__':
    unittest.main()
