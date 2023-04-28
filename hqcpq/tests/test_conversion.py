import unittest
import datetime
from hqcpq.helpers import conversion


class TestStringToInt(unittest.TestCase):
    def test_string_to_int(self):
        self.assertEqual(1, conversion.string_to_int('1'))
        self.assertEqual(23, conversion.string_to_int('23'))
        self.assertEqual(None, conversion.string_to_int('a'))
        self.assertEqual(None, conversion.string_to_int('!'))


class TestStringToFloat(unittest.TestCase):
    def test_string_to_float(self):
        self.assertEqual(1.0, conversion.string_to_float('1'))
        self.assertEqual(1.3, conversion.string_to_float('1.3'))
        self.assertEqual(None, conversion.string_to_float('a'))
        self.assertEqual(None, conversion.string_to_float('!'))


class TestStringToDate(unittest.TestCase):
    def test_string_to_date(self):
        self.assertEqual(datetime.datetime(1999, 10, 1).date(), conversion.string_to_date('1/10/1999'))
        self.assertEqual(datetime.datetime(1999, 10, 1).date(), conversion.string_to_date('01/10/1999'))
        self.assertEqual(datetime.datetime(1999, 10, 1).date(), conversion.string_to_date('1/10/99'))
        self.assertEqual(None, conversion.string_to_date('a'))
        self.assertEqual(None, conversion.string_to_date('!'))
        self.assertEqual(None, conversion.string_to_date('0'))


if __name__ == '__main__':
    unittest.main()