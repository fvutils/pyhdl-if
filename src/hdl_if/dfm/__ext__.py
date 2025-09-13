

def dfm_packages():
    """Returns the DFM packages"""
    import os

    dfm_dir = os.path.dirname(os.path.abspath(__file__))

    return {
        'pyhdl-if': os.path.join(dfm_dir, "flow.dv"),
    }

