from django.test import SimpleTestCase
from app import calc

class CalcTests (SimpleTestCase):
    def test_add_numbers (self):
        res = calc.add(10, 5)
        self.assertEqual(res, 15)

    def test_subtract_number (self):
        res = calc.subtract(15, 10)
        self.assertEqual(res, 5)