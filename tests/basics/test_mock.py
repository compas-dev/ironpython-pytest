import pytest


def test_patch_fixture(mocker):
    from Queue import Queue
    q = Queue()
    mocker.patch("Queue.Queue.qsize")
    q.qsize.return_value = 10

    assert q.qsize() == 10


def test_mock(mocker):
    mocked_object = mocker.Mock(return_value="hello")
    mocked_object.attr1 = "some_attribute_value"
    assert mocked_object() == "hello"

    assert mocked_object.attr1 == "some_attribute_value"
    assert isinstance(mocked_object.attr1, str)
    assert isinstance(mocked_object.attr2, mocker.Mock)
    assert isinstance(mocked_object.attr3, mocker.Mock)


def test_assert_not_called(mocker):
    obj = mocker.Mock(return_value="hello")
    obj.assert_not_called()


def test_assert_called_once_w_ret_value(mocker):
    obj = mocker.Mock(return_value="hello")
    obj()
    obj.assert_called_once()


def test_assert_called_with_nothing(mocker):
    obj = mocker.Mock(return_value="hello")
    obj()
    obj.assert_called_with()


def test_assert_called_with_args(mocker):
    obj = mocker.Mock(return_value="hello")
    obj(1, 2, 3)
    obj.assert_called_with(1, 2, 3)


def test_assert_called_with_kwargs(mocker):
    obj = mocker.Mock(return_value="hello")
    obj(one=1, two=2, three=3)
    obj.assert_called_with(one=1, two=2, three=3)


def test_assert_called_with_args_kwargs(mocker):
    obj = mocker.Mock(return_value="hello")
    obj(1, 2, 3, one=1, two=2, three=3)
    obj.assert_called_with(1, 2, 3, one=1, two=2, three=3)


def test_assert_called_with_args_kwargs_not_matching(mocker):
    obj = mocker.Mock(return_value="hello")
    obj(1, 2, 3, one=1, two=2, three=3)

    with pytest.raises(AssertionError):
        obj.assert_called_with(1, 2, 3)
