"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

from TDStoreTools import StorageManager
import TDFunctions as TDF

import numpy as np
from hypothesis import given
from hypothesis.strategies import floats, lists
from typing import Callable


class TouchTestExt:
    """
    TouchTestExt description
    """

    def __init__(self, ownerComp):
        # The component to which this extension is attached
        self.Inputs = None
        self.ownerComp = ownerComp

    def get_tests(self) -> list[Callable]:
        tests_mod = parent().par.Tests.eval().module
        return [
            func
            for name, func in tests_mod.__dict__.items()
            if name.startswith("test_")
        ]

    def Run(self):
        tests = self.get_tests()
        for test in tests:
            wrapped = self.wrap_test(test)
            wrapped()
        self.report()

    def report(self): ...

    @staticmethod
    def pad_arr(arr):
        pad = len(max(arr, key=len))
        return np.array(
            [np.pad(i, ((0, pad - len(i)),)) for i in arr], dtype=np.float32
        )

    def wrap_test(self, test: Callable) -> Callable:
        parop = parent().parent().op
        ops = [
            parop(o) for o in parent().par.Ops.eval().split(" ") if o not in ["", " "]
        ]
        channels_range = (
            self.ownerComp.par.Channelsrange1.eval(),
            self.ownerComp.par.Channelsrange2.eval(),
        )
        values_range = (
            self.ownerComp.par.Valuesrange1.eval(),
            self.ownerComp.par.Valuesrange2.eval(),
        )
        samples_range = (
            self.ownerComp.par.Samplesrange1.eval(),
            self.ownerComp.par.Samplesrange2.eval(),
        )

        @given(
            lists(
                lists(
                    floats(
                        allow_infinity=False,
                        allow_nan=False,
                        min_value=values_range[0],
                        max_value=values_range[1],
                    ),
                    min_size=samples_range[0],
                    max_size=samples_range[1],
                ),
                min_size=channels_range[0],
                max_size=channels_range[1],
            )
        )
        def wrapped(lists):
            self.copy_to_inputs_chop(lists)
            try:
                test(self.pad_arr(lists), ops)
            except Exception as e:
                debug(e)
                raise e

        return wrapped

    def copy_to_inputs_chop(self, lists: list[float]):
        self.Inputs = lists
        op("script_inputs").cook(force=True)
