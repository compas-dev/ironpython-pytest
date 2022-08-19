"""Add mock and patch functionality in the same minimal, assuming, spirit of this package"""
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
