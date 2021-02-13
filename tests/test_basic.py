import pytest


def test_minimal():
    assert True


@pytest.fixture
def data():
    return dict(name='test fixture')


def test_fixture(data):
    assert data['name'] == 'test fixture'


@pytest.fixture
def nested_data(data):
    data['name'] = 'nested fixture'
    return data


def test_nested_fixture(nested_data):
    assert nested_data['name'] == 'nested fixture'
