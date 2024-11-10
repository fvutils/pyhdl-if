##########
Quickstart 
##########

Installing PyHDL-IF
===================

It's easiest to install PyHDL-IF as a binary package from PyPi:

.. code:: shell

    % pip install pyhdl-if

Installing PyHDL-IF from Source
-------------------------------

Installing PyHDL-IF from source requires the installation of three 
Python packages that are only used during the build process:

.. code:: shell

    % pip install cxxheaderparser pcpp ivpm

Once these pre-requisites are installed, the package can be built
using the following command:

.. code:: shell

    % python3 setup.py build_ext --inplace

