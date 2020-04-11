import unittest
from unittest import mock

from sr.comp.cli.deploy import query, query_bool


def mock_get_input(autospec=True, **kwargs):
    return mock.patch('sr.comp.cli.deploy.get_input', autospec=autospec, **kwargs)


class DeployQueryHelpersTests(unittest.TestCase):
    # Test `query`

    @mock_get_input(return_value='nope')
    def test_query_with_default_nope(self, _):
        res = query('Question?', ('a'), default='a')
        self.assertEqual('a', res)

    @mock_get_input(return_value='a')
    def test_query_with_default_a(self, _):
        res = query('Question?', ('a', 'b'), default='b')
        self.assertEqual('a', res)

    @mock_get_input(side_effect=iter(['nope', 'a']))
    def test_query_nope_then_a(self, mocked_get_input):
        res = query('Question?', ('a', 'b'))
        self.assertEqual('a', res)

        self.assertEqual(2, mocked_get_input.call_count)

    # Test `query_bool` true results

    @mock_get_input(return_value='y')
    def test_query_bool_True_y(self, _):
        res = query_bool('Question?', True)
        self.assertTrue(res)

    @mock_get_input(return_value='n')
    def test_query_bool_True_n(self, _):
        res = query_bool('Question?', True)
        self.assertFalse(res)

    @mock_get_input(return_value='other')
    def test_query_bool_True_other(self, _):
        res = query_bool('Question?', True)
        self.assertTrue(res)

    # Test `query_bool` false results

    @mock_get_input(return_value='y')
    def test_query_bool_False_y(self, _):
        res = query_bool('Question?', False)
        self.assertTrue(res)

    @mock_get_input(return_value='n')
    def test_query_bool_False_n(self, _):
        res = query_bool('Question?', False)
        self.assertFalse(res)

    @mock_get_input(return_value='other')
    def test_query_bool_False_other(self, _):
        res = query_bool('Question?', False)
        self.assertFalse(res)

    # Test `query_bool` without default

    @mock_get_input(return_value='y')
    def test_query_bool_no_default_y(self, _):
        res = query_bool('Question?')
        self.assertTrue(res)

    @mock_get_input(return_value='n')
    def test_query_bool_no_default_n(self, _):
        res = query_bool('Question?')
        self.assertFalse(res)

    @mock_get_input(side_effect=iter(['other', 'y']))
    def test_query_bool_no_default_other_then_y(self, mocked_get_input):
        res = query_bool('Question?')
        self.assertTrue(res)

        self.assertEqual(2, mocked_get_input.call_count)
