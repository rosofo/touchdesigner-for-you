"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

from pathlib import Path
import subprocess
import sys
from TDStoreTools import StorageManager
import TDFunctions as TDF


class VenvExt:
    """
    VenvExt description
    """

    def __init__(self, ownerComp):
        # The component to which this extension is attached
        self.ownerComp = ownerComp

        self.Exists = tdu.Dependency(False)
        self.Loaded = tdu.Dependency(False)

    def Load(self):
        self.Exists.val = False
        self.Loaded.val = False

        venv = Path(self.ownerComp.par.Venv.eval())
        site_packages = venv / "lib" / "python3.11" / "site-packages"
        print(site_packages)
        if site_packages.exists():
            self.Exists.val = True
            if site_packages not in sys.path:
                sys.path.append(str(site_packages))
                self.ownerComp.par.Syspath = ", ".join(sys.path)
            self.Loaded.val = True

    def InstallRequires(self):
        requires = self.ownerComp.par.Requires.eval()
        if not requires:
            return
        venv_path = Path(self.ownerComp.par.Venv.eval())
        pip_binary = venv_path / "bin" / "pip3"
        try:
            ## open a terminal and run the command
            subprocess.run(
                # touchdesigner does something weird with the python path that breaks SSL
                f"unset PYTHONPATH && {pip_binary} install {requires}",
                shell=True,
                executable="/bin/bash",
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(e)
