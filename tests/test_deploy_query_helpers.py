import unittest
from unittest import mock

from sr.comp.cli.deploy import query, query_bool

input_name = 'sr.comp.cli.deploy.get_input'


class DeployQueryHelpersTests(unittest.TestCase):
    # Test `query`

    @mock.patch(input_name, lambda x: 'nope')
    def test_query_with_default_nope(self):
        res = query('Question?', ('a'), default='a')
        self.assertEqual('a', res)

    @mock.patch(input_name, lambda x: 'a')
    def test_query_with_default_a(self):
        res = query('Question?', ('a', 'b'), default='b')
        self.assertEqual('a', res)

    @mock.patch(input_name)
    def test_query_nope_then_a(self, mock_get_input):
        values = ['nope', 'a']
        mock_get_input.side_effect = lambda x: values.pop(0)

        res = query('Question?', ('a', 'b'))
        self.assertEqual('a', res)

        self.assertEqual(2, mock_get_input.call_count)

    # Test `query_bool` true results

    @mock.patch(input_name, lambda x: 'y')
    def test_query_bool_True_y(self):
        res = query_bool('Question?', True)
        self.assertTrue(res)

    @mock.patch(input_name, lambda x: 'n')
    def test_query_bool_True_n(self):
        res = query_bool('Question?', True)
        self.assertFalse(res)

    @mock.patch(input_name, lambda x: 'other')
    def test_query_bool_True_other(self):
        res = query_bool('Question?', True)
        self.assertTrue(res)

    # Test `query_bool` false results

    @mock.patch(input_name, lambda x: 'y')
    def test_query_bool_False_y(self):
        res = query_bool('Question?', False)
        self.assertTrue(res)

    @mock.patch(input_name, lambda x: 'n')
    def test_query_bool_False_n(self):
        res = query_bool('Question?', False)
        self.assertFalse(res)

    @mock.patch(input_name, lambda x: 'other')
    def test_query_bool_False_other(self):
        res = query_bool('Question?', False)
        self.assertFalse(res)

    # Test `query_bool` without default

    @mock.patch(input_name, lambda x: 'y')
    def test_query_bool_no_default_y(self):
        res = query_bool('Question?')
        self.assertTrue(res)

    @mock.patch(input_name, lambda x: 'n')
    def test_query_bool_no_default_n(self):
        res = query_bool('Question?')
        self.assertFalse(res)

    @mock.patch(input_name)
    def test_query_bool_no_default_other_then_y(self, mock_get_input):
        values = ['other', 'y']
        mock_get_input.side_effect = lambda x: values.pop(0)

        res = query_bool('Question?')
        self.assertTrue(res)

        self.assertEqual(2, mock_get_input.call_count)
