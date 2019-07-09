from test import divide
import unittest


class TestSum(unittest.TestCase):

    def test_multiply(self):
        self.assertEqual(divide(6, 6), 1, "Should be 1")

    def test_sum(self):
        self.assertEqual(sum([2, 3]), 3, '5')


if __name__ == '__main__':
    unittest.main()

