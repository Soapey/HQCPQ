import unittest
from hqcpq.helpers import comparison


class TestCanBeFloat(unittest.TestCase):
    def test_can_be_float(self):
        self.assertEqual(True, comparison.can_be_float('1.0'))
        self.assertEqual(True, comparison.can_be_float('1.3'))
        self.assertEqual(True, comparison.can_be_float('1'))
        self.assertEqual(False, comparison.can_be_float('a'))


class TestCanBeDate(unittest.TestCase):
    def test_can_be_date(self):
        self.assertEqual(True, comparison.can_be_date('22/03/2023'))
        self.assertEqual(True, comparison.can_be_date('22/3/23'))
        self.assertEqual(False, comparison.can_be_date('1'))
        self.assertEqual(False, comparison.can_be_date('a'))


if __name__ == "__main__":
    unittest.main()
