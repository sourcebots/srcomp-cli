import unittest
from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from freezegun import freeze_time

from sr.comp.cli.add_delay import (
    BadDurationException,
    parse_datetime,
    parse_duration,
)


class ParseDurationTests(unittest.TestCase):
    def test_bad_inputs(self) -> None:
        data = [
            "nope",
            "now",
            "5dd",
        ]

        for time_str in data:
            with self.subTest(time_str=time_str):
                with self.assertRaises(BadDurationException):
                    parse_duration(time_str)

    def test_valid_inputs(self) -> None:
        data = [
            ("1m", timedelta(minutes=1)),
            ("1s", timedelta(seconds=1)),
            ("42", timedelta(seconds=42)),
            ("42s", timedelta(seconds=42)),
            ("1hr", timedelta(hours=1)),
        ]

        for time_str, expected in data:
            with self.subTest(time_str=time_str):
                td = parse_duration(time_str)
                self.assertEqual(expected, td)


class ParseDatetimeTests(unittest.TestCase):
    def test_bad_dates(self) -> None:
        data = [
            "fail",
            "five of the clock",
            "135135",
            "",
            "5 minutes ago",
            "14:45 ago",
            "in 14:45",
        ]

        for when in data:
            with self.subTest(when=when):
                with self.assertRaises(ValueError):
                    parse_datetime(when)

    @freeze_time('2015-01-01 14:00')
    def test_valid_dates(self) -> None:
        data = [
            ("now", datetime(2015, 1, 1, 14, 0, tzinfo=tzlocal())),
            ("16:00", datetime(2015, 1, 1, 16, 0, tzinfo=tzlocal())),
            ("2019-04-13 12:20", datetime(2019, 4, 13, 12, 20, tzinfo=tzlocal())),
            ("5m ago", datetime(2015, 1, 1, 13, 55, tzinfo=tzlocal())),
            ("in 5m", datetime(2015, 1, 1, 14, 5, tzinfo=tzlocal())),
        ]

        for when, expected in data:
            with self.subTest(when=when):
                self.assertEqual(expected, parse_datetime(when))
