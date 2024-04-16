.. PyHDL-IF documentation master file, created by
   sphinx-quickstart on Sat Apr  6 19:07:21 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyHDL-IF Documentation
=========================
PyHDL-IF provides low-level procedural interfaces between Python and
various HDL simulator interfaces. PyHDL-IF provides some minimal 
abstraction interfaces across HDL simulator APIs, but primarily focuses
on providing direct interfaces.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
  
   sim_integ
   sv_api

Status and Roadmap
==================

PyHDL-IF is still under active development. The information here attempts
to capture the status of available features and a roadmap of planned 
future features.

.. list-table:: Platform Support
    :header-rows: 1

    * - Linux
      - Windows (x86_64)
      - MacOS (x86_64)
      - MacOS (arm64)
    * - Yes
      - Planned
      - Planned
      - Planned

The native-compiled portions of PyHDL-IF are compiled according
to the relevant Python version-specific requirements. 
If your favorite platform is not listed above and you would like 
PyHDL-IF to support, please file a feature-request ticket and
note the platform and the simulator you typically use on that 
platform.

.. list-table:: HDL Calling Python API
    :header-rows: 1

    * - DPI
      - FLI
      - VPI
      - VHPI
    * - Yes
      - Planned
      - Planned
      - Planned

Supporting HDL calls to the Python API allows HDL to interact with
Python as if it was a Python extension by calling the Python C API.
    
.. list-table:: Python calling HDL API
    :header-rows: 1

    * - DPI
      - FLI
      - VPI
      - VHPI
    * - Yes
      - Planned
      - Yes
      - Planned

Support Python calls to an HDL API allows Python to interact with
simulator APIs as if it were a shared library loaded by the 
simulator. For example, support for VPI allows a Python module
to walk through the design design hierachy and implement 
system tasks that the HDL can call.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
