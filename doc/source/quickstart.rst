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

Running Pytest Tests from SystemVerilog
========================================

PyHDL-IF includes a pytest runner for executing async Python tests from 
SystemVerilog testbenches. First, ensure pytest is installed:

.. code:: shell

    % pip install pytest

Then, run tests from your SystemVerilog testbench:

.. code:: systemverilog

    module my_test;
        initial begin
            pyhdl_if::pyhdl_if_start();
            pyhdl_if::pyhdl_pytest("tests/my_async_tests.py");
            $finish;
        end
    endmodule

For complete details, see :doc:`pytest_runner`.

