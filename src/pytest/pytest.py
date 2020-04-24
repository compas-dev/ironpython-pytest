"""Emulate pytest API."""
from __future__ import print_function

import argparse
import contextlib

FIXTURES = dict()

__all__ = ['fixture', 'mark', 'parametrize', 'raises']


def fixture(func):
    FIXTURES[func.__name__] = func
    return func


def parametrize(argnames='', argvalues=None):
    def decorator_param(func):
        func._parametrized_arguments = dict(argnames=argnames, argvalues=argvalues)
        return func

    return decorator_param


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


mark = argparse.Namespace(parametrize=parametrize)
