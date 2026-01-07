/**
 * pyhdl_if_pytest.svh
 *
 * Copyright 2024 Matthew Ballance and Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may 
 * not use this file except in compliance with the License.  
 * You may obtain a copy of the License at:
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software 
 * distributed under the License is distributed on an "AS IS" BASIS, 
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
 * See the License for the specific language governing permissions and 
 * limitations under the License.
 *
 * Created on:
 *     Author: 
 */

/****************************************************************
 * PyHDL-IF Pytest Runner
 ****************************************************************/

/**
 * pyhdl_pytest
 *
 * Run async pytest tests from SystemVerilog.
 * Arguments can be specified via task parameters or plusargs.
 * Plusargs take precedence over task arguments.
 *
 * Args:
 *   testpath: Path to search for pytest files (required)
 *   testname: Optional specific test name to run
 *   filter: Optional -k filter expression
 *
 * Plusargs:
 *   +pyhdl.pytest.testpath=<path>
 *   +pyhdl.pytest.testname=<name>
 *   +pyhdl.pytest.filter=<expr>
 */
task automatic pyhdl_pytest(
    string testpath = "",
    string testname = "",
    string filter = ""
);
    PyGILState_STATE state;
    PyObject pytest_runner_m, run_pytest_h, args, kwargs, task_h, result;
    PyObject os_expandvars_h, expanded_str;
    string final_testpath, final_testname, final_filter;
    int has_error;
    
    // Ensure SV event loop is running
    if (!prv_run_q_running) begin
        $display("[PyHDL-IF] Error: SV event loop is not running. Call pyhdl_if_start() first.");
        $fatal(1);
    end
    
    // Get arguments from plusargs (they override task arguments)
    final_testpath = testpath;
    final_testname = testname;
    final_filter = filter;
    
    void'($value$plusargs("pyhdl.pytest.testpath=%s", final_testpath));
    void'($value$plusargs("pyhdl.pytest.testname=%s", final_testname));
    void'($value$plusargs("pyhdl.pytest.filter=%s", final_filter));
    
    // Expand environment variables using Python's os.path.expandvars
    state = PyGILState_Ensure();
    
    // Import os.path module
    pytest_runner_m = pyhdl_pi_if_HandleErr(PyImport_ImportModule("os.path"));
    if (pytest_runner_m != null) begin
        // Get expandvars function
        os_expandvars_h = PyObject_GetAttrString(pytest_runner_m, "expandvars");
        if (os_expandvars_h != null) begin
            // Expand testpath
            if (final_testpath != "") begin
                args = PyTuple_New(1);
                void'(PyTuple_SetItem(args, 0, PyUnicode_FromString(final_testpath)));
                expanded_str = PyObject_Call(os_expandvars_h, args, null);
                if (expanded_str != null) begin
                    final_testpath = PyUnicode_AsUTF8(expanded_str);
                    Py_DecRef(expanded_str);
                end
                Py_DecRef(args);
            end
            
            // Expand testname
            if (final_testname != "") begin
                args = PyTuple_New(1);
                void'(PyTuple_SetItem(args, 0, PyUnicode_FromString(final_testname)));
                expanded_str = PyObject_Call(os_expandvars_h, args, null);
                if (expanded_str != null) begin
                    final_testname = PyUnicode_AsUTF8(expanded_str);
                    Py_DecRef(expanded_str);
                end
                Py_DecRef(args);
            end
            
            // Expand filter
            if (final_filter != "") begin
                args = PyTuple_New(1);
                void'(PyTuple_SetItem(args, 0, PyUnicode_FromString(final_filter)));
                expanded_str = PyObject_Call(os_expandvars_h, args, null);
                if (expanded_str != null) begin
                    final_filter = PyUnicode_AsUTF8(expanded_str);
                    Py_DecRef(expanded_str);
                end
                Py_DecRef(args);
            end
            
            Py_DecRef(os_expandvars_h);
        end
        Py_DecRef(pytest_runner_m);
    end
    
    PyGILState_Release(state);
    
    // Validate required arguments
    if (final_testpath == "") begin
        $display("[PyHDL-IF] Error: testpath is required for pyhdl_pytest");
        $display("[PyHDL-IF] Usage: pyhdl_pytest(\"path/to/tests\")");
        $display("[PyHDL-IF]    or: +pyhdl.pytest.testpath=path/to/tests");
        $fatal(1);
    end
    
    $display("[PyHDL-IF] Running pytest with testpath=%s", final_testpath);
    
    state = PyGILState_Ensure();
    
    // Import pytest_runner module
    pytest_runner_m = pyhdl_pi_if_HandleErr(PyImport_ImportModule("hdl_if.pytest_runner"));
    if (pytest_runner_m == null) begin
        $display("[PyHDL-IF] Error: Failed to import hdl_if.pytest_runner");
        PyGILState_Release(state);
        $fatal(1);
    end
    
    // Get run_pytest function
    run_pytest_h = pyhdl_pi_if_HandleErr(PyObject_GetAttrString(pytest_runner_m, "run_pytest"));
    if (run_pytest_h == null) begin
        $display("[PyHDL-IF] Error: Failed to get run_pytest function");
        PyGILState_Release(state);
        $fatal(1);
    end
    
    // Build arguments
    args = PyTuple_New(1);
    void'(PyTuple_SetItem(args, 0, PyUnicode_FromString(final_testpath)));
    
    // Build keyword arguments
    kwargs = PyDict_New();
    if (final_testname != "") begin
        void'(PyDict_SetItemString(kwargs, "testname", PyUnicode_FromString(final_testname)));
    end
    if (final_filter != "") begin
        void'(PyDict_SetItemString(kwargs, "filter_expr", PyUnicode_FromString(final_filter)));
    end
    
    // Call run_pytest and create async task
    result = pyhdl_pi_if_HandleErr(PyObject_Call(run_pytest_h, args, kwargs));
    if (result == null) begin
        $display("[PyHDL-IF] Error: Failed to call run_pytest");
        PyGILState_Release(state);
        $fatal(1);
    end
    
    // Create async task
    task_h = pyhdl_pi_if_mkTask(result);
    if (task_h == null) begin
        $display("[PyHDL-IF] Error: Failed to create async task");
        PyGILState_Release(state);
        $fatal(1);
    end
    
    Py_DecRef(args);
    Py_DecRef(kwargs);
    
    PyGILState_Release(state);
    
    // Wait for task completion
    // The async task will run via the event loop
    // We need to wait for it to complete
    fork
        begin
            automatic PyObject done_h, done_result;
            automatic int is_done;
            
            is_done = 0;
            while (!is_done) begin
                #1000; // Wait a bit
                
                state = PyGILState_Ensure();
                
                // Check if task is done
                done_h = PyObject_GetAttrString(task_h, "done");
                if (done_h != null) begin
                    args = PyTuple_New(0);
                    done_result = PyObject_Call(done_h, args, null);
                    if (done_result != null) begin
                        is_done = PyObject_IsTrue(done_result);
                        Py_DecRef(done_result);
                    end
                    Py_DecRef(args);
                    Py_DecRef(done_h);
                end
                
                PyGILState_Release(state);
            end
            
            // Get result and check for exceptions
            state = PyGILState_Ensure();
            
            begin
                automatic PyObject exception_h, exc_result;
                exception_h = PyObject_GetAttrString(task_h, "exception");
                if (exception_h != null) begin
                    args = PyTuple_New(0);
                    exc_result = PyObject_Call(exception_h, args, null);
                    if (exc_result != null && exc_result != None) begin
                        $display("[PyHDL-IF] Pytest runner raised exception:");
                        PyErr_Print();
                        has_error = 1;
                    end else begin
                        has_error = 0;
                    end
                    if (exc_result != null) Py_DecRef(exc_result);
                    Py_DecRef(args);
                    Py_DecRef(exception_h);
                end
            end
            
            Py_DecRef(task_h);
            PyGILState_Release(state);
            
            if (has_error) begin
                $display("[PyHDL-IF] Pytest execution failed");
                $fatal(1);
            end
        end
    join
    
endtask
