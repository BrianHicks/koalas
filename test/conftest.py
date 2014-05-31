import pytest
from pandas import DataFrame

@pytest.fixture
def frame():
    return DataFrame.from_csv('testdata/pharmacies.csv')
