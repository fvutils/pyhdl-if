#****************************************************************************
#* pytest_runner.py
#*
#* Copyright 2024 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#*
#****************************************************************************
import sys
import os
import inspect
import asyncio
from typing import List, Optional, Tuple, Callable, Any
import traceback

class PytestRunnerError(Exception):
    """Exception raised when pytest runner encounters an error"""
    pass

def check_pytest_available() -> str:
    """
    Check if pytest is available.
    
    Returns:
        pytest version
        
    Raises:
        PytestRunnerError: If pytest not available
    """
    try:
        import pytest
        return pytest.__version__
    except ImportError:
        raise PytestRunnerError(
            "pytest is not installed. Install with: pip install pytest"
        )


class TestCollectorPlugin:
    """
    Pytest plugin to collect test items without executing them.
    
    This is used with --collect-only to gather test functions
    while benefiting from pytest's assertion rewriting.
    """
    def __init__(self):
        self.items = []
    
    def pytest_collection_finish(self, session):
        """Called after collection is complete"""
        self.items = session.items


def discover_tests_with_pytest(
    testpath: str,
    testname: Optional[str] = None,
    filter_expr: Optional[str] = None
) -> List[Any]:
    """
    Use pytest to discover and collect tests.
    
    This uses pytest.main() with --collect-only to gather test items,
    which gives us the benefit of pytest's assertion rewriting for better
    error messages.
    
    Args:
        testpath: Path to test file or directory
        testname: Optional specific test name
        filter_expr: Optional -k filter expression
        
    Returns:
        List of pytest test items
        
    Raises:
        PytestRunnerError: If collection fails
    """
    import pytest
    
    if not os.path.exists(testpath):
        raise PytestRunnerError(f"Test path does not exist: {testpath}")
    
    # Build pytest args for collection only
    args = [testpath, "--collect-only", "-q"]
    
    if filter_expr:
        args.extend(["-k", filter_expr])
    
    if testname:
        # Append specific test to path
        if "::" not in testname:
            args[0] = f"{testpath}::{testname}"
        else:
            args[0] = testname
    
    # Create collector plugin
    collector = TestCollectorPlugin()
    
    # Run pytest to collect tests (doesn't execute them)
    ret = pytest.main(args, plugins=[collector])
    
    if ret != 0 and ret != 5:  # 5 = no tests collected
        raise PytestRunnerError(f"Test collection failed with return code {ret}")
    
    return collector.items


async def run_async_test(item: Any) -> Tuple[str, str, Optional[str]]:
    """
    Run a single async test item collected by pytest.
    
    Args:
        item: pytest test item
        
    Returns:
        Tuple of (nodeid, status, error_msg)
        status is one of: PASS, FAIL, ERROR, SKIP
    """
    nodeid = item.nodeid
    func = item.obj
    
    # Validate it's async
    if not inspect.iscoroutinefunction(func):
        return (nodeid, "SKIP", f"Test is not an async function")
    
    try:
        # Get any fixtures or parameters needed by the test
        # For now, we call with no arguments - fixtures could be added later
        funcargs = {}
        
        # Check the function signature to see what it expects
        sig = inspect.signature(func)
        if len(sig.parameters) > 0:
            # Test requires fixtures - skip for now
            param_names = list(sig.parameters.keys())
            return (nodeid, "SKIP", 
                   f"Test requires fixtures/parameters: {param_names} (not yet supported)")
        
        # Call the async test function
        # The function was loaded by pytest, so it has assertion rewriting
        await func()
        return (nodeid, "PASS", None)
        
    except AssertionError as e:
        # Pytest's assertion rewriting gives us better error messages
        error_msg = str(e)
        if not error_msg:
            # Get traceback for context
            error_msg = traceback.format_exc()
        return (nodeid, "FAIL", error_msg)
    
    except Exception as e:
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        return (nodeid, "ERROR", error_msg)


async def run_pytest(
    testpath: str,
    testname: Optional[str] = None,
    filter_expr: Optional[str] = None
) -> dict:
    """
    Main entry point for running pytest tests from SystemVerilog.
    
    This function:
    1. Uses pytest.main(--collect-only) to discover and collect tests
       (benefits from assertion rewriting)
    2. Runs the collected async test functions directly in our event loop
    3. Reports results
    
    Args:
        testpath: Path to search for test files (required)
        testname: Optional specific test name to run
        filter_expr: Optional -k filter expression
        
    Returns:
        Dictionary with test results and statistics
        
    Raises:
        PytestRunnerError: If pytest setup or test discovery fails
    """
    print(f"[PyHDL-IF Pytest] Starting pytest runner", flush=True)
    print(f"[PyHDL-IF Pytest]   testpath: {testpath}", flush=True)
    if testname:
        print(f"[PyHDL-IF Pytest]   testname: {testname}", flush=True)
    if filter_expr:
        print(f"[PyHDL-IF Pytest]   filter: {filter_expr}", flush=True)
    
    # Check pytest availability
    try:
        pytest_ver = check_pytest_available()
        print(f"[PyHDL-IF Pytest] pytest: {pytest_ver}", flush=True)
    except PytestRunnerError as e:
        print(f"[PyHDL-IF Pytest] ERROR: {str(e)}", flush=True)
        raise
    
    # Use pytest to collect tests (with assertion rewriting)
    print(f"[PyHDL-IF Pytest] Collecting tests with pytest...", flush=True)
    try:
        test_items = discover_tests_with_pytest(testpath, testname, filter_expr)
        print(f"[PyHDL-IF Pytest] Collected {len(test_items)} test(s)", flush=True)
    except PytestRunnerError as e:
        print(f"[PyHDL-IF Pytest] ERROR: {str(e)}", flush=True)
        raise
    
    if len(test_items) == 0:
        print(f"[PyHDL-IF Pytest] WARNING: No tests found", flush=True)
        return {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0,
            'results': []
        }
    
    # Run tests asynchronously
    print(f"[PyHDL-IF Pytest] Running tests...", flush=True)
    print("=" * 70, flush=True)
    
    results = []
    passed = 0
    failed = 0
    errors = 0
    skipped = 0
    
    for item in test_items:
        nodeid, status, error_msg = await run_async_test(item)
        
        results.append({
            'name': nodeid,
            'status': status,
            'error': error_msg
        })
        
        if status == "PASS":
            passed += 1
            print(f"[PyHDL-IF Pytest] PASSED: {nodeid}", flush=True)
        elif status == "FAIL":
            failed += 1
            print(f"[PyHDL-IF Pytest] FAILED: {nodeid}", flush=True)
            if error_msg:
                # Print first few lines of error
                lines = error_msg.split('\n')
                for line in lines[:3]:  # First 3 lines
                    if line.strip():
                        print(f"  {line}", flush=True)
        elif status == "ERROR":
            errors += 1
            print(f"[PyHDL-IF Pytest] ERROR: {nodeid}", flush=True)
            if error_msg:
                first_line = error_msg.split('\n')[0]
                print(f"  {first_line}", flush=True)
        elif status == "SKIP":
            skipped += 1
            print(f"[PyHDL-IF Pytest] SKIPPED: {nodeid}", flush=True)
            if error_msg:
                print(f"  {error_msg}", flush=True)
    
    print("=" * 70, flush=True)
    print(f"[PyHDL-IF Pytest] Test Summary:", flush=True)
    print(f"[PyHDL-IF Pytest]   Total:   {len(results)}", flush=True)
    print(f"[PyHDL-IF Pytest]   Passed:  {passed}", flush=True)
    print(f"[PyHDL-IF Pytest]   Failed:  {failed}", flush=True)
    print(f"[PyHDL-IF Pytest]   Errors:  {errors}", flush=True)
    print(f"[PyHDL-IF Pytest]   Skipped: {skipped}", flush=True)
    
    summary = {
        'total': len(results),
        'passed': passed,
        'failed': failed,
        'errors': errors,
        'skipped': skipped,
        'results': results
    }
    
    if failed > 0 or errors > 0:
        print(f"[PyHDL-IF Pytest] RESULT: FAILED", flush=True)
    else:
        print(f"[PyHDL-IF Pytest] RESULT: PASSED", flush=True)
    
    return summary
