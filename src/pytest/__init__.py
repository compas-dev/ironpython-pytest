# -*- encoding: utf-8 -*-
"""

Ridiculously minimal and incomplete pytest replacement for IronPython.

This is **not** an attempt to fork ``pytest`` to IronPython, instead
it's intended to provide the bare minimum for a drop-in replacement
of a subset of ``pytest`` conventions and framework required to run
unit tests on IronPython.

It makes a ton of assumptions and has very little configurability.

Deal with it.

(•_•) ( •_•)>⌐■-■ (⌐■_■)
"""
from __future__ import absolute_import
from __future__ import print_function

from .__version__ import *    # noqa: F401 F403
from .pytest import *         # noqa: F401 F403
from .test_runner import *    # noqa: F401 F403
from .mock import mocker      # noqa: F401 F403
