from datetime import datetime, timedelta

from freezegun import freeze_time
from nose.tools import raises

from sr.comp.cli.add_delay import (
    BadDurationException,
    parse_datetime,
    parse_duration,
)


def test_bad_inputs():
    @raises(BadDurationException)
    def check(ts):
        parse_duration(ts)

    yield check, "nope"
    yield check, "now"
    yield check, "5dd"


def test_valid_inputs():
    def check(time_str, expected):
        td = parse_duration(time_str)
        assert expected == td

    yield check, "1m", timedelta(minutes = 1)
    yield check, "1s", timedelta(seconds = 1)
    yield check, "42", timedelta(seconds = 42)
    yield check, "42s", timedelta(seconds = 42)
    yield check, "1hr", timedelta(hours = 1)


def test_bad_dates():
    @raises(ValueError)
    def check(datetime):
        parse_datetime(datetime)

    yield check, "fail"
    yield check, "five of the clock"
    yield check, "135135"
    yield check, ""
    yield check, "5 minutes ago"
    yield check, "14:45 ago"
    yield check, "in 14:45"


def test_valid_dates():
    @raises(ValueError)
    @freeze_time('2015-01-01 14:00')
    def check(datetime, expected):
        assert expected == parse_datetime(datetime)

    yield check, "now", datetime(2015, 1, 1, 14, 0)
    yield check, "16:00", datetime(2015, 1, 1, 16, 0)
    yield check, "2019-04-13 12:20", datetime(2019, 4, 13, 12, 20)
    yield check, "5m ago", datetime(2015, 1, 1, 13, 55)
    yield check, "in 5m", datetime(2015, 1, 14, 5)
