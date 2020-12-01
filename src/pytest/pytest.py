"""Emulate pytest API."""
from __future__ import print_function

import argparse
import contextlib
import itertools

FIXTURES = dict()

__all__ = ['fixture', 'mark', 'parametrize', 'raises', 'skip']


def fixture(func):
    FIXTURES[func.__name__] = func
    return func


def parametrize(argnames='', argvalues=None):
    def decorator_param(func):
        # If the argnames are single arguments, we assume it is a stacked parametrize decorator
        if isinstance(argnames, str) and ',' not in argnames:
            if not hasattr(func, '_stacked_parametrized_names'):
                func._stacked_parametrized_names = []
                func._stacked_parametrized_values = []
            func._stacked_parametrized_names.append(argnames)
            func._stacked_parametrized_values.append(argvalues)
            if len(func._stacked_parametrized_names) == 1:
                func._parametrized_arguments = dict(argnames=argnames, argvalues=argvalues)
            else:
                func._parametrized_arguments = dict(
                    argnames=func._stacked_parametrized_names,
                    argvalues=list(itertools.product(*func._stacked_parametrized_values))
                )
        else:
            func._parametrized_arguments = dict(argnames=argnames, argvalues=argvalues)
        return func

    return decorator_param


def skip(test_method=None, reason=None):
    def wrapped(func):
        func._skip = True
        return func

    if test_method is not None:
        return wrapped(test_method)
    else:
        return wrapped


@contextlib.contextmanager
def raises(exception_type):
    did_raise = False
    try:
        yield []
    except Exception as e:
        if isinstance(e, exception_type):
            did_raise = True
    finally:
        if not did_raise:
            raise AssertionError('Did not raise exception of type {}'.format(exception_type))


mark = argparse.Namespace(parametrize=parametrize, skip=skip)
