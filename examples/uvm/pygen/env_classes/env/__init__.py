
import importlib
import os

pkg_dir = os.path.dirname(os.path.abspath(__file__))

for f in os.listdir(pkg_dir):
    if f.endswith(".py") and f != "__init__.py":
        base = f[:-3]
        importlib.import_module(f".{base}", package=__name__)
            