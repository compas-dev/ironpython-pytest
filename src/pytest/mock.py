"""Add mock and patch functionality in the same minimal, assuming, spirit of this package"""
from collections import namedtuple

from pytest import fixture

__all__ = ["mocker"]


MockFuncCall = namedtuple("MockFuncCall", ["args", "kwargs"])


class Mock(object):
    """Accepts any call or dot lookup without causing trouble.

    side_effect allows executing callables
    return_value, if set, is returned for any call using the call operator.
    Any dot lookup which comes back empty sets an attribute with the looked-up name with a Mock() instance as value.
    """

    def __init__(self, *_, **kwargs):
        self.return_value = None
        self._side_effect = None
        self._func_calls = []

        try:
            side_effect = kwargs.pop("side_effect")
            self.side_effect = side_effect
        except KeyError:
            pass

        for key_value in kwargs.items():
            object.__setattr__(self, *key_value)

    @property
    def side_effect(self):
        return self._side_effect

    @property
    def call_count(self):
        return len(self._func_calls)

    @side_effect.setter
    def side_effect(self, value):
        self._side_effect = None
        self._func_calls.clear()
        try:
            # Exceptions are iterable :(
            if not isinstance(self._side_effect, BaseException):
                self._side_effect = iter(value)
        except TypeError:
            pass
        self._side_effect = self._side_effect or value

    def __call__(self, *args, **kwargs):
        """Calls the next side_effect if set. If not, returns the set return_value (default: None).

        Raises
        ------
        StopIteration
            Raised when side_effect is set but no more items are available.

        """
        self._func_calls.append(MockFuncCall(args, kwargs))
        if self.side_effect:
            if isinstance(self._side_effect, BaseException):
                raise self._side_effect
            if callable(self._side_effect):
                return self._side_effect(*args, **kwargs)
            return next(self._side_effect)
        return self.return_value

    def __getattribute__(self, item):
        try:
            value = object.__getattribute__(self, item)
        except AttributeError:
            value = Mock()
            object.__setattr__(self, item, value)
        return value

    def assert_called_once(self):
        """Asserts if this mock has been called exactly once. If not, an assertion error is raised.

        Raises
        ------
        AssertionError
            Raised if this mock's call count is different from 1.

        """
        assert self.call_count == 1

    def assert_not_called(self):
        """Asserts if this mock has not been called. If it has, an assertion error is raised.

        Raises
        ------
        AssertionError
            Raised if this mock's has been called as least once.

        """
        assert self.call_count == 0

    def assert_called(self):
        """Asserts if this mock has been called at all. If not, an assertion error is raised.
        Raises
        ------
        AssertionError
            Raised if this mock has not been called.

        """
        return self.call_count > 0

    def assert_called_with(self, *args, **kwargs):
        """Asserts if this mock has been called with the given combination of arguments. If not, an assertion error is raised.

        Parameters
        ----------
        args : list, optional
            A list of expected positional arguments.
        kwargs : list, optional
            A dictionary of the expected keyword arguments.
            
        Raises
        ------
        AssertionError
            Raised if this mock's has not been called with the expected arguments.

        """
        is_called_with = any([call.args == args and call.kwargs == kwargs for call in self._func_calls])
        if not is_called_with:
            raise AssertionError("Call with args: {} kwargs: {} not found in call list!".format(args, kwargs))


class Patcher(object):
    """
    Patches attributes/methods of types, replacing them with a Mock() object.
    """
    def __init__(self):
        self.original = None
        self.target = None
        self.attribute_name = None

    def __call__(self, *args, **kwargs):
        """
        Parameters:
        ----------
        target : str
            The target attribute or method to mock. A complete path to target including package and module.

        >>> patcher = Patcher()
        >>> patcher("path.to.module.Type.attribute")
        """
        if "target" in kwargs:
            target = kwargs["target"]
        elif len(args) > 0:
            target = args[0]
        else:
            raise ValueError("Expected at least argument `target`")

        if not isinstance(target, str):
            raise TypeError("target is expected to be a string")
        self._patch_target(target)

    def _patch_target(self, target):
        target_path, self.attribute_name = target.rsplit(".", 1)
        self.target = self._importer(target_path)
        self.original = getattr(self.target, self.attribute_name)
        setattr(self.target, self.attribute_name, Mock())

    @staticmethod
    def _dot_lookup(thing, comp, import_path):
        try:
            return getattr(thing, comp)
        except AttributeError:
            __import__(import_path)
            return getattr(thing, comp)

    @staticmethod
    def _importer(target):
        components = target.split('.')
        import_path = components.pop(0)
        thing = __import__(import_path)

        for comp in components:
            import_path += ".{}".format(comp)
            thing = Patcher._dot_lookup(thing, comp, import_path)
        return thing

    def stop(self):
        """Restore the patched attribute to its original state"""
        if self.target:
            setattr(self.target, self.attribute_name, self.original)
            del self.target
            del self.original


class Mocker(object):
    """
    Provides a minimal interface which behaves, to a miserable extent, as the pytest-mock.MockerFixture.
    """

    def __init__(self):
        self.patch = Patcher()
        self.Mock = Mock

    def stop(self):
        """Reset all patched attributes"""
        self.patch.stop()


@fixture
def mocker():
    return Mocker()
