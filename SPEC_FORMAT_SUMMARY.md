# API Specification Format Support - Implementation Summary

## Overview
Refactored the JSON-based API generation to use generic 'spec' terminology and infrastructure that will support JSON, YAML, and TOML formats in the future.

## Key Changes

### 1. Terminology Update
- Changed from "JSON" to "spec" (API specification) throughout
- Old parameters (`-j`/`--json`, `json_spec`) deprecated but retained for backward compatibility
- New parameters: `-s`/`--spec`, `spec`, `--spec-fmt`, `spec_fmt`

### 2. Format Detection
Added automatic format detection in `cmd_api_gen_sv.py`:
- **File-based**: Detects format from extension (.json, .yaml/.yml, .toml)
- **Inline string**: Attempts to parse as JSON
- **Explicit override**: `--spec-fmt` flag to force a specific format

### 3. File Path Support
- **DFM Task**: Can accept either inline spec string OR file path
- **Validation**: File paths must have .json extension (for now)
- **Command Line**: Works with both `-s "inline"` and `-s filepath.json`

### 4. Future-Proofing
- YAML format detected but returns "not yet implemented" error
- TOML format detected but returns "not yet implemented" error
- Infrastructure ready for adding YAML/TOML parsers in the future

## Files Modified

### Core Implementation
1. **src/hdl_if/cmd/cmd_api_gen_sv.py**
   - Added `_detect_spec_format()` method for auto-detection
   - Added `_load_spec()` method for format-agnostic loading
   - Updated `__call__()` to support both `spec` and legacy `json` parameters
   - Returns helpful error messages for unsupported formats

2. **src/hdl_if/__main__.py**
   - Added `-s`/`--spec` argument
   - Added `--spec-fmt` argument (choices: json, yaml, toml)
   - Deprecated `-j`/`--json` (still works)

3. **src/hdl_if/dfm/api_gen_sv.py**
   - Added support for `spec` and `spec_fmt` parameters
   - Validates .json extension for file paths
   - Falls back to legacy `json_spec` parameter
   - Falls back to `modules` parameter

4. **src/hdl_if/dfm/flow.dv**
   - Added `spec` parameter definition
   - Added `spec_fmt` parameter definition
   - Deprecated `json_spec` parameter (still works)

### Testing
5. **tests/unit/test_api_spec_format.py** (NEW - 13 tests)
   - Tests format detection (JSON, YAML, TOML)
   - Tests inline strings vs file paths
   - Tests explicit format override
   - Tests error handling for unsupported formats
   - Tests backward compatibility with `-j`/`--json`
   - Tests new `-s`/`--spec` functionality

6. **tests/unit/test_spec_file.py** (NEW - integration test)
   - Tests using spec file path in DFM task
   - Full end-to-end test with Verilator

7. **tests/unit/test_json_api.py** (MODIFIED)
   - Updated to use new `spec` parameter instead of `json_spec`

### Documentation
8. **doc/JSON_API_GENERATION.md** (UPDATED)
   - Updated to use spec terminology
   - Added examples for inline and file-based specs
   - Added note about future YAML/TOML support
   - Added backward compatibility notes

## API Compatibility

### Command Line
```bash
# New way (recommended)
python -m hdl_if api-gen-sv -s api_def.json -p pkg -o out.sv
python -m hdl_if api-gen-sv -s '{"fullname": ...}' -p pkg -o out.sv
python -m hdl_if api-gen-sv -s api_def.json --spec-fmt json -p pkg -o out.sv

# Old way (deprecated but still works)
python -m hdl_if api-gen-sv -j '{"fullname": ...}' -p pkg -o out.sv
```

### DFM Task
```python
# New way (recommended)
gen_api = pyhdl_dvflow.mkTask(
    "pyhdl-if.APIGenSV",
    spec="api_def.json",  # or inline JSON string
    spec_fmt="json",      # optional, auto-detected
    pkgname="pkg")

# Old way (deprecated but still works)
gen_api = pyhdl_dvflow.mkTask(
    "pyhdl-if.APIGenSV",
    json_spec=json_content,
    pkgname="pkg")
```

## Test Results

**All 50 unit tests pass:**
- ✅ 13/13 spec format detection and handling tests (NEW)
- ✅ 15/15 JSON schema validation tests
- ✅ 10/10 JSON parsing and generation tests
- ✅ 12/12 API filtering tests (no regression)

**All 3 integration tests pass with Verilator:**
- ✅ test_json_api (inline spec)
- ✅ test_spec_file (file path spec) (NEW)
- ✅ test_smoke (no regression)

## Validation Rules

### File Path Specs
- **Extension validation**: Must be `.json` (will support `.yaml`, `.yml`, `.toml` in future)
- **Existence check**: File must exist
- **Format detection**: Automatic based on extension

### Inline Specs
- **Format detection**: Attempts JSON parse, can be overridden with `--spec-fmt`
- **No extension restriction**: Inline specs can be any format

## Future Work

To add YAML support:
1. Add YAML parser dependency
2. Implement YAML parsing in `_load_spec()`
3. Update tests
4. Update documentation

To add TOML support:
1. Add TOML parser dependency (e.g., tomli/tomllib)
2. Implement TOML parsing in `_load_spec()`
3. Update tests
4. Update documentation

The infrastructure is already in place - just need to implement the parsers!

## Migration Guide

### For Users
- Start using `-s`/`--spec` instead of `-j`/`--json`
- Use `spec` instead of `json_spec` in DFM tasks
- No immediate action required - old parameters still work

### For Developers
- New code should use spec terminology
- Legacy parameters will be removed in a future major version
- Format detection makes it easy to add new formats
