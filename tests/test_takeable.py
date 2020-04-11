import unittest

from sr.comp.cli.update_layout import Takeable


class TakeableTests(unittest.TestCase):
    def test_take_0_str(self):
        t = Takeable('abcd')

        self.assertEqual('', t.take(0))
        self.assertEqual('a', t.take(1))

    def test_take_1_str(self):
        t = Takeable('abcd')

        self.assertTrue(t.has_more)

        self.assertEqual('a', t.take(1))
        self.assertEqual('b', t.take(1))
        self.assertEqual('c', t.take(1))
        self.assertEqual('d', t.take(1))

        self.assertFalse(t.has_more)

    def test_take_2_str(self):
        t = Takeable('abcd')

        self.assertTrue(t.has_more)

        self.assertEqual('ab', t.take(2))
        self.assertEqual('cd', t.take(2))

        self.assertFalse(t.has_more)

    def test_take_0_list(self):
        t = Takeable(list('abcd'))

        self.assertEqual([], t.take(0))
        self.assertEqual(['a'], t.take(1))

    def test_take_1_list(self):
        t = Takeable(list('abcd'))

        self.assertTrue(t.has_more)

        self.assertEqual(['a'], t.take(1))
        self.assertEqual(['b'], t.take(1))
        self.assertEqual(['c'], t.take(1))
        self.assertEqual(['d'], t.take(1))

        self.assertFalse(t.has_more)

    def test_take_2_list(self):
        t = Takeable(list('abcd'))

        self.assertTrue(t.has_more)

        self.assertEqual(['a', 'b'], t.take(2))
        self.assertEqual(['c', 'd'], t.take(2))

        self.assertFalse(t.has_more)

    def test_take_too_many(self):
        t = Takeable('abcd')

        self.assertTrue(t.has_more)

        self.assertEqual('abc', t.take(3))
        self.assertEqual('d', t.take(3))
        self.assertEqual('', t.take(2))

        self.assertFalse(t.has_more)

    def test_remainder(self):
        t = Takeable('abcd')

        self.assertEqual('ab', t.take(2))

        self.assertEqual('cd', t.remainder)

        self.assertEqual('cd', t.take(2))

    def test_remainder_when_no_more(self):
        t = Takeable('abcd')

        self.assertEqual('abcd', t.take(4))

        self.assertEqual('', t.remainder)

    def test_remainder_when_beyond_end(self):
        t = Takeable('abcd')

        self.assertEqual('abcd', t.take(5))

        self.assertEqual('', t.remainder)
