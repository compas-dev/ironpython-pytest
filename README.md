
# ironpython-pytest

![Version](https://img.shields.io/pypi/v/ironpython-pytest) ![License](https://img.shields.io/pypi/l/ironpython-pytest)

> Ridiculously minimal and incomplete pytest replacement for IronPython.

This is **not** an attempt to fork [`pytest`](https://docs.pytest.org/) to IronPython (as the seemingly abandoned [pytest-ironpython](https://bitbucket.org/dahlia/pytest-ironpython/)), instead it's intended to provide the bare minimum for a drop-in replacement of a subset of `pytest` conventions and framework required to run unit tests on IronPython.

It makes a ton of assumptions and has very little configurability.

Deal with it.

(•\_•) ( •\_•)>⌐■-■ (⌐■\_■)

## Installation

    ipy -X:Frames -m ensurepip
    ipy -X:Frames -m pip install ironpython-pytest 

## Usage

From the command line:

    ipy -m pytest file_or_dir

Or programmatically:

```python
import os

import pytest

if __name__ == '__main__':
    # Fake some modules
    pytest.load_fake_module('Rhino')
    pytest.load_fake_module('Rhino.Geometry', fake_types=['RTree', 'Sphere', 'Point3d'])

    pytest.run('project/test_dir/')
```
