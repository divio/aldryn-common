import unittest


def foo(x):
    return x + 1


class TestSample(unittest.TestCase):
    def test_foo(self):
        self.assertEqual(foo(3), 4)
