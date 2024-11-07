import os
import sys

hdl_if_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "src")

sys.path.insert(0, hdl_if_dir)
