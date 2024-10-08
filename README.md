# Utilities for TouchDesigner

Important points:

- Tested only on MacOS
- Most utilities use the `Venv` COMP internally to manage their dependencies. You shouldn't have to include a separate instance of it.
- Issues, requests, PRs are welcome!

## Venv

A Python venv management COMP.

- Expects there to be a `~/.pyenv` folder, this can be changed in the `Global Python` parameter
- Defaults to Python 3.11.1, the version used by TD as of version `2023.12000`

### Setup

> Other components using Venv will take care of this automatically

1. Save your project, ideally in a project folder as this is where the `.venv` folder will be created
2. Click `Create` and expect TD to freeze temporarily
3. Click `Load` to add the new venv to `sys.path`, which makes libraries accessible within TD. (Only necessary the first time, on project reload it should load automatically).
4. Dependencies: Either click `Copy Activate Cmd` so you can work with the venv in a terminal, or enter your requires in `Requires` and click `Install`.

## TouchTest

An integration of [hypothesis](https://hypothesis.readthedocs.io/en/latest/) for testing TD networks.

### Setup

1. Save your project, ideally in a project folder as this is where the `.venv` folder will be created
2. On first load the venv will be created and hypothesis installed. TD will freeze for a bit while this takes place.
3. Click `Create Tests` to create a DAT alongside the COMP. This DAT contains your test functions
4. Hook up the CHOP output to your network
5. Enter OPs you'd like to test into `OPs`. This does *not* do anything special really, it just provides the OPs to your test functions for convenience
6. Click `Run` and observe the results in textport

### How to write tests

- The generated data will be fed into your network via the CHOP output
- The most important thing to note is that your test functions are responsible for making sure things cook, moving time forward etc. TouchTest force cooks its input CHOP just to ensure the data is available to your network before calling the test function, but that's it.
  - **Cooking**: TD allows you to synchronously ensure things have cooked all from Python. In your test function you should probably call `.cook()` or `.cook(force=True)` for each of the OPs being monitored
  - **Time**: you can move the global time forward frame-by-frame by doing `op.time.frame += 1` on any OP. This allows you to observe a time-dependent process all within one call of your test function.

### Example

Let's say you've got a CHOP network hooked up to the output of TouchTest consisting of `math1` -> `null1`.

**given**: arbitrary channels and sample lengths, values between 0 and 1
**invariant**: output - input is always 1, i.e. the network is adding 1 to the inputs.

```python
import numpy as np


def test_adding_one(input_data: np.ndarray, ops: list[OP]):
    null_op = ops[0]
    null_op.cook(force=True) # ensure the network has cooked before comparing
    result = null_op.numpyArray()

    assert np.all(np.isclose(result - input_data, 1)), f"{result}"
```