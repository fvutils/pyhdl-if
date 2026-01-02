# JSON API Generation Implementation Summary

## Overview
Added support for specifying HDL-IF API definitions using JSON format instead of requiring Python classes with decorators. This allows:
- Single-source API definitions that generate both SystemVerilog and Python code
- Tool-based API generation
- API definitions from non-Python sources

## Files Added

### Core Implementation
1. **src/hdl_if/impl/call/api_def_from_json.py**
   - Parses JSON API definitions into ApiDef objects
   - Supports all standard types (int8-64, uint8-64, bool, float, string, pyobject)
   - Handles all method kinds (imp_task, imp_func, exp_task, exp_func)

2. **src/hdl_if/impl/call/gen_py_class.py**
   - Generates Python class skeletons from ApiDef objects
   - Creates proper @hif.api and @hif.imp/@hif.exp decorators
   - Generates async methods for tasks

### Schema
3. **doc/pyhdl-if.schema.json**
   - JSON Schema (Draft 7) for API definitions
   - Validates API structure, types, and method kinds
   - Provides auto-completion in VS Code and other editors
   - Published to docs root via Sphinx configuration

4. **doc/SCHEMA_README.md**
   - Documentation for using the JSON schema
   - Examples and validation instructions

### Testing
5. **tests/unit/test_api_gen_sv_json.py**
   - 10 unit tests covering JSON parsing, SV generation, and Python generation
   - Tests various formats (single API, array, with init params)
   - Tests type mapping and method kinds

6. **tests/unit/test_json_schema.py**
   - 15 unit tests for JSON schema validation
   - Tests all types, method kinds, and error cases
   - Validates schema against test data

7. **tests/unit/test_json_api.py**
   - Integration test using DFM task with JSON input
   - Full end-to-end test with Verilator simulation
   - Validates that JSON-generated APIs work correctly at runtime

8. **tests/unit/data/test_json_api/**
   - api_def.json - Example JSON API definition (with schema reference)
   - call_json_bfm.py - Python implementation using JSON-generated API
   - call_json_bfm.sv - SystemVerilog testbench
   - wb_init_bfm.sv - Wishbone BFM module

### Utilities
6. **scripts/gen_py_from_json.py**
   - Standalone script to generate Python classes from JSON
   - Can output to file or stdout

### Documentation
7. **doc/JSON_API_GENERATION.md**
   - Complete documentation of JSON format
   - Usage examples for command line and DFM tasks
   - Type reference and method kind descriptions

## Files Modified

1. **src/hdl_if/cmd/cmd_api_gen_sv.py**
   - Added JSON argument handling
   - Parses JSON and registers APIs if JSON provided
   - Falls back to module loading if no JSON

2. **src/hdl_if/__main__.py**
   - Added -j/--json argument to api-gen-sv command
   - Made -m/--module optional (required if no JSON)

3. **src/hdl_if/dfm/api_gen_sv.py**
   - Added json_spec parameter support to DFM task
   - Passes JSON to command line if provided

4. **src/hdl_if/dfm/flow.dv**
   - Added 'json_spec' parameter definition to APIGenSV task

5. **doc/source/conf.py**
   - Added html_extra_path to publish schema to docs root

## Usage Examples

### Generate SV from JSON (command line):
```bash
python -m hdl_if api-gen-sv \
    -j '{"fullname": "mymod.MyClass", "methods": [...]}' \
    -p my_pkg -o output.sv
```

### Generate Python from JSON:
```bash
python scripts/gen_py_from_json.py -j '...' -o output.py
```

### Use in DFM tasks:
```python
gen_api = pyhdl_dvflow.mkTask(
    "pyhdl-if.APIGenSV",
    pkgname="my_pkg",
    filename="my_pkg.sv",
    json_spec=json_content)
```

## Test Results
All tests pass with Verilator (vlt):
- 10/10 JSON parsing and generation unit tests pass
- 15/15 JSON schema validation tests pass
- 12/12 API filtering tests pass (no regression)
- 3/3 integration tests pass (JSON API, smoke test, and schema validation)

## Benefits
1. **Single Source of Truth**: Define API once in JSON, generate both SV and Python
2. **Tool Integration**: APIs can be generated from other tools/formats
3. **Language Agnostic**: API definitions not tied to Python syntax
4. **Backward Compatible**: Existing module-based workflow still works
