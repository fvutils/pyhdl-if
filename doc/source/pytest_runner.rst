##############
Pytest Runner
##############

Overview
========

The PyHDL-IF pytest runner enables running async Python tests directly from SystemVerilog 
testbenches. This feature integrates pytest's powerful test collection and assertion 
rewriting with PyHDL-IF's async execution environment, allowing Python test code to interact 
seamlessly with HDL simulations.

Key Features
************

* **Pytest Integration**: Full pytest test collection with assertion rewriting for better error messages
* **Async Execution**: Tests run asynchronously within the HDL simulation event loop
* **Flexible Test Selection**: Filter tests using pytest's ``-k`` option or specify individual tests
* **Environment Variable Expansion**: Test paths automatically expand environment variables
* **Clear Reporting**: Detailed test results with pass/fail status and error information

Requirements
************

* ``pytest`` package must be installed: ``pip install pytest``
* Tests must be async functions (``async def test_*``)
* Tests requiring fixtures are currently not supported

Basic Usage
===========

Simple Example
**************

From SystemVerilog, call the ``pyhdl_pytest`` task after initializing PyHDL-IF:

.. code-block:: systemverilog

    module my_test;
        initial begin
            pyhdl_if::pyhdl_if_start();
            pyhdl_if::pyhdl_pytest("tests/my_async_tests.py");
            $finish;
        end
    endmodule

The corresponding Python test file would contain async test functions:

.. code-block:: python

    # tests/my_async_tests.py
    async def test_simple_pass():
        x = 10
        assert x == 10
        
    async def test_with_computation():
        result = 5 + 5
        assert result == 10

Advanced Usage
==============

Filtering Tests
***************

Run specific tests using the filter parameter:

.. code-block:: systemverilog

    // Run only tests matching "computation"
    pyhdl_if::pyhdl_pytest(
        .testpath("tests/my_tests.py"),
        .filter("computation")
    );

Or use plusargs:

.. code-block:: shell

    simulator +pyhdl.pytest.testpath=tests/my_tests.py +pyhdl.pytest.filter=computation

Running a Specific Test
************************

To run a single test by name:

.. code-block:: systemverilog

    pyhdl_if::pyhdl_pytest(
        .testpath("tests/my_tests.py"),
        .testname("test_specific_function")
    );

Environment Variables
*********************

Test paths support environment variable expansion:

.. code-block:: systemverilog

    pyhdl_if::pyhdl_pytest("$PROJECT_ROOT/tests/my_tests.py");

API Reference
=============

SystemVerilog Task
******************

.. code-block:: systemverilog

    task automatic pyhdl_pytest(
        string testpath = "",
        string testname = "",
        string filter = ""
    );

**Parameters:**

* ``testpath`` (required): Path to test file or directory. Supports environment variable expansion.
* ``testname`` (optional): Specific test function name to run
* ``filter`` (optional): pytest ``-k`` filter expression for test selection

**Plusargs:**

Arguments can also be specified via plusargs (these override task parameters):

* ``+pyhdl.pytest.testpath=<path>``
* ``+pyhdl.pytest.testname=<name>``
* ``+pyhdl.pytest.filter=<expr>``

**Requirements:**

Must call ``pyhdl_if_start()`` before using ``pyhdl_pytest``.

Python API
**********

The pytest runner can also be called directly from Python:

.. code-block:: python

    from hdl_if.pytest_runner import run_pytest
    
    # Run tests asynchronously
    result = await run_pytest(
        testpath="tests/my_tests.py",
        testname="test_specific",  # optional
        filter_expr="async"         # optional
    )

**Returns:**

A dictionary containing test results:

.. code-block:: python

    {
        'total': 3,
        'passed': 3,
        'failed': 0,
        'errors': 0,
        'skipped': 0,
        'results': [
            {'name': 'test_one', 'status': 'PASS', 'error': None},
            {'name': 'test_two', 'status': 'PASS', 'error': None},
            {'name': 'test_three', 'status': 'PASS', 'error': None}
        ]
    }

How It Works
============

The pytest runner uses a two-phase approach:

1. **Collection Phase**: Uses ``pytest.main(['--collect-only'])`` with a custom plugin to discover 
   tests. This enables pytest's assertion rewriting, which provides detailed error messages 
   (e.g., "assert 10 == 20" instead of just "AssertionError").

2. **Execution Phase**: Directly awaits each collected async test function within PyHDL-IF's 
   event loop. This integrates seamlessly with the HDL simulation without blocking or 
   creating event loop conflicts.

This approach provides the benefits of pytest's test infrastructure while maintaining full 
async integration with the HDL simulation environment.

Assertion Rewriting Benefits
*****************************

With pytest's assertion rewriting, failed assertions provide detailed context:

.. code-block:: python

    async def test_example():
        x = 10
        y = 20
        assert x == y  # Fails with: "AssertionError: assert 10 == 20"

Without assertion rewriting, you would only see a generic ``AssertionError`` message.

Limitations
===========

Current limitations of the pytest runner:

* Tests must be async functions (synchronous tests are skipped)
* Fixtures are not yet supported (tests requiring parameters are skipped)
* Only basic pytest features are available (no parametrize, marks, etc.)
* Test discovery follows pytest conventions (files/functions starting with ``test_``)

Example Output
==============

When running tests, you'll see output like:

.. code-block:: text

    [PyHDL-IF Pytest] Starting pytest runner
    [PyHDL-IF Pytest]   testpath: tests/sample_async_tests.py
    [PyHDL-IF Pytest] pytest: 7.4.0
    [PyHDL-IF Pytest] Collecting tests with pytest...
    [PyHDL-IF Pytest] Collected 3 test(s)
    [PyHDL-IF Pytest] Running tests...
    ======================================================================
    [PyHDL-IF Pytest] PASSED: test_simple_pass
    [PyHDL-IF Pytest] PASSED: test_with_computation
    [PyHDL-IF Pytest] PASSED: test_another_pass
    ======================================================================
    [PyHDL-IF Pytest] Test Summary:
    [PyHDL-IF Pytest]   Total:   3
    [PyHDL-IF Pytest]   Passed:  3
    [PyHDL-IF Pytest]   Failed:  0
    [PyHDL-IF Pytest]   Errors:  0
    [PyHDL-IF Pytest]   Skipped: 0
    [PyHDL-IF Pytest] RESULT: PASSED

Troubleshooting
===============

pytest Not Found
****************

If you see an error about pytest not being installed:

.. code-block:: text

    [PyHDL-IF Pytest] ERROR: pytest is not installed

Install pytest in your Python environment:

.. code-block:: shell

    pip install pytest

Event Loop Not Running
**********************

If you see:

.. code-block:: text

    [PyHDL-IF] Error: SV event loop is not running

Make sure to call ``pyhdl_if_start()`` before ``pyhdl_pytest()``:

.. code-block:: systemverilog

    initial begin
        pyhdl_if::pyhdl_if_start();  // Initialize first
        pyhdl_if::pyhdl_pytest("tests/my_tests.py");
        $finish;
    end

No Tests Collected
******************

If pytest collects no tests, verify:

* Test file names start with ``test_`` or end with ``_test.py``
* Test function names start with ``test_``
* Test functions are async (``async def``)
* The specified path is correct and accessible

Best Practices
==============

1. **Organize Tests**: Keep test files in a dedicated directory structure
2. **Use Descriptive Names**: Name test functions clearly to indicate what they test
3. **Keep Tests Focused**: Each test should verify one specific behavior
4. **Leverage Assertions**: Use Python's assert statements for clear test conditions
5. **Handle Async Properly**: Ensure all async operations are properly awaited
6. **Check Return Codes**: Monitor the test summary to ensure all tests pass
