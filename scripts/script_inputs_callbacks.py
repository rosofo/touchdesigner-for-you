# me - this DAT
import numpy as np
# scriptOp - the OP which is cooking


# press 'Setup Parameters' in the OP to call this function to re-create the parameters.
def onSetupParameters(scriptOp):
    page = scriptOp.appendCustomPage("Custom")
    p = page.appendFloat("Valuea", label="Value A")
    p = page.appendFloat("Valueb", label="Value B")
    return


# called whenever custom pulse parameter is pushed
def onPulse(par):
    return


def onCook(scriptOp):
    scriptOp.clear()
    inputs = parent().Inputs
    if inputs is None:
        return
    pad = len(max(inputs, key=len))
    inputs = np.array(
        [np.pad(i, ((0, pad - len(i)),)) for i in inputs], dtype=np.float32
    )
    scriptOp.copyNumpyArray(inputs)
    return
