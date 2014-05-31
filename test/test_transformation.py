from koalas import transformation as t
import pytest

class TestSelect(object):
    def test_nolist(self, frame):
        with pytest.raises(ValueError):
            t.select(frame, '')

    def test_good(self, frame):
        filtered = t.select(frame, ['name'])
        assert frame[['name']].to_dict(outtype='rows') == filtered.to_dict(outtype='rows')


def test_lt(frame):
    filtered = t.lt(frame, 'zip', 63304)
    assert frame[frame['zip'] < 63304].to_dict() == filtered.to_dict()

def test_lte(frame):
    filtered = t.lte(frame, 'zip', 63304)
    assert frame[frame['zip'] <= 63304].to_dict() == filtered.to_dict()

def test_gt(frame):
    filtered = t.gt(frame, 'zip', 63304)
    assert frame[frame['zip'] > 63304].to_dict() == filtered.to_dict()

def test_gte(frame):
    filtered = t.gte(frame, 'zip', 63304)
    assert frame[frame['zip'] >= 63304].to_dict() == filtered.to_dict()

def test_eq(frame):
    filtered = t.eq(frame, 'zip', 63304)
    assert frame[frame['zip'] == 63304].to_dict() == filtered.to_dict()

def test_ne(frame):
    filtered = t.ne(frame, 'zip', 63304)
    assert frame[frame['zip'] != 63304].to_dict() == filtered.to_dict()
