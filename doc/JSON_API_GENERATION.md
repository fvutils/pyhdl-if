# JSON-Based API Generation

This feature allows you to specify HDL-IF API definitions using structured formats (currently JSON, with YAML and TOML planned for the future) instead of Python classes with decorators. This is useful for:

1. Generating both SystemVerilog and Python implementations from a single source
2. Tool-based API generation
3. Cross-language API definitions

## Supported Formats

Currently supported:
- **JSON** - Fully supported

Planned for future releases:
- **YAML** - Format detected but not yet implemented
- **TOML** - Format detected but not yet implemented

## JSON Schema

The JSON format is defined by the [JSON Schema](pyhdl-if.schema.json). You can use this schema to:
- Validate your API definitions
- Get auto-completion in editors like VS Code
- Generate documentation

To use the schema in your JSON files, add this at the top:
```json
{
  "$schema": "https://raw.githubusercontent.com/fvutils/pyhdl-if-pytest/main/doc/pyhdl-if.schema.json",
  "fullname": "...",
  ...
}
```

## JSON API Definition Format

```json
{
    "apis": [
        {
            "fullname": "module.ClassName",
            "init_params": [
                {"name": "param_name", "type": "uint32"}
            ],
            "methods": [
                {
                    "name": "method_name",
                    "kind": "imp_task",
                    "params": [
                        {"name": "addr", "type": "uint32"},
                        {"name": "data", "type": "uint32"}
                    ],
                    "return_type": "uint32"
                }
            ]
        }
    ]
}
```

### Supported Types

- `bool` - Boolean
- `int8`, `int16`, `int32`, `int64` - Signed integers
- `uint8`, `uint16`, `uint32`, `uint64` - Unsigned integers
- `float`, `double` - Floating point
- `string`, `str` - Strings
- `pyobject`, `object` - Python objects

### Method Kinds

- `imp_task` - Import task (async, called from SV to Python)
- `imp_func` - Import function (sync, called from SV to Python)
- `exp_task` - Export task (async, called from Python to SV)
- `exp_func` - Export function (sync, called from Python to SV)

## Usage

### Generate SystemVerilog from Spec

Using command line with inline JSON:
```bash
python -m hdl_if api-gen-sv \
    -s '{"fullname": "mymod.MyClass", "methods": [...]}' \
    -p my_pkg \
    -o output.sv
```

Using command line with spec file:
```bash
python -m hdl_if api-gen-sv \
    -s api_def.json \
    -p my_pkg \
    -o output.sv
```

You can explicitly specify the format (useful for future YAML/TOML support):
```bash
python -m hdl_if api-gen-sv \
    -s api_def.json \
    --spec-fmt json \
    -p my_pkg \
    -o output.sv
```

Using DFM task with inline spec:
```python
gen_api = pyhdl_dvflow.mkTask(
    "pyhdl-if.APIGenSV",
    pkgname="my_pkg",
    filename="my_pkg.sv",
    spec='{"fullname": "mymod.MyClass", ...}')
```

Using DFM task with spec file:
```python
gen_api = pyhdl_dvflow.mkTask(
    "pyhdl-if.APIGenSV",
    pkgname="my_pkg",
    filename="my_pkg.sv",
    spec="path/to/api_def.json")
```

**Backward Compatibility Note**: The `-j`/`--json` and `json_spec` parameters are deprecated but still supported. Use `-s`/`--spec` and `spec` instead.

### Generate Python Classes from JSON

```bash
python scripts/gen_py_from_json.py \
    -j '{"fullname": "mymod.MyClass", "methods": [...]}' \
    -o mymod.py
```

Or in code:
```python
from hdl_if.impl.call.api_def_from_json import ApiDefFromJson
from hdl_if.impl.call.gen_py_class import GenPyClass

apis = ApiDefFromJson.parse(json_str)
gen = GenPyClass(output_file)
gen.gen_module(apis)
```

## Example

JSON definition (`api.json`):
```json
{
    "apis": [
        {
            "fullname": "mybfm.WishboneInitiator",
            "methods": [
                {
                    "name": "write",
                    "kind": "imp_task",
                    "params": [
                        {"name": "addr", "type": "uint32"},
                        {"name": "data", "type": "uint32"}
                    ]
                },
                {
                    "name": "read",
                    "kind": "imp_task",
                    "params": [
                        {"name": "addr", "type": "uint32"}
                    ],
                    "return_type": "uint32"
                }
            ]
        },
        {
            "fullname": "mybfm.Test",
            "methods": [
                {
                    "name": "run",
                    "kind": "exp_task",
                    "params": [
                        {"name": "bfm", "type": "pyobject"}
                    ]
                }
            ]
        }
    ]
}
```

Generate Python implementation:
```bash
python scripts/gen_py_from_json.py -j "$(cat api.json)" -o mybfm.py
```

Generate SystemVerilog package:
```bash
python -m hdl_if api-gen-sv -j "$(cat api.json)" -p mybfm_pkg -o mybfm_pkg.sv
```

Then implement the methods in Python:
```python
# In mybfm.py (modify the generated skeleton)
import ctypes as ct
import hdl_if as hif

@hif.api
class WishboneInitiator(object):
    
    @hif.imp
    async def write(self, addr: ct.c_uint32, data: ct.c_uint32):
        pass  # Implementation here
    
    @hif.imp
    async def read(self, addr: ct.c_uint32) -> ct.c_uint32:
        pass  # Implementation here

@hif.api
class Test(object):
    
    @hif.exp
    async def run(self, bfm: ct.py_object):
        # Test implementation
        await bfm.write(0x1000, 0x42)
        val = await bfm.read(0x1000)
        print(f"Read: {val}")
```

## Testing

Run the JSON API tests:
```bash
pytest tests/unit/test_api_gen_sv_json.py  # Unit tests
pytest tests/unit/test_json_api.py -k vlt  # Integration test
```
