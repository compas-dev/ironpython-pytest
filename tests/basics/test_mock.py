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
