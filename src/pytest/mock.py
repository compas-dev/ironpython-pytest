"""Add mock and patch functionality in the same minimal, assuming, spirit of this package"""
import importlib

from pytest import fixture

__all__ = ["mocker"]


class Mock(object):
    """
    Accepts any call or dot lookup without causing trouble.
    return_value, if set, is returned for any call using the call operator.

    Any dot lookup which comes back empty sets an attribute with the looked-up name with a Mock() instance as value.
    """

    def __init__(self, *_, **kwargs):
        self.return_value = None
        for key_value in kwargs.items():
            object.__setattr__(self, *key_value)

    def __call__(self, *args, **kwargs):
        """
        Call this mock as a method.
        No side effects. Returns None or self.return_value, if set.

        TODO: add side effect functionality
        """
        return self.return_value

    def __getattribute__(self, item):
        try:
            value = object.__getattribute__(self, item)
        except AttributeError:
            value = Mock()
            object.__setattr__(self, item, value)
        return value


class Patcher(object):
    """
    Patches attributes/methods of types, replacing them with a Mock() object.
    """

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

    @staticmethod
    def _patch_target(target):
        module_path, type_name, attr_name = target.rsplit(".", 2)
        module = importlib.import_module(module_path)
        type_ = getattr(module, type_name)
        setattr(type_, attr_name, Mock())


class Mocker(object):
    """
    Provides a minimal interface which behaves, to a miserable extent, as the pytest-mock.MockerFixture.
    """

    def __init__(self):
        self.patch = Patcher()
        self.Mock = Mock


@fixture
def mocker():
    return Mocker()
