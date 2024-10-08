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

1. Save your project, ideally in a project folder as this is where the `.venv` folder will be created
2. Click `Create` and expect TD to freeze temporarily
3. Click `Load` to add the new venv to `sys.path`, which makes libraries accessible within TD. (Only necessary the first time, on project reload it should load automatically).
4. Dependencies: Either click `Copy Activate Cmd` so you can work with the venv in a terminal, or enter your requires in `Requires` and click `Install`.