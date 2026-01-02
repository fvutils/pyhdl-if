# PyHDL-IF JSON Schema

This JSON Schema defines the format for PyHDL-IF API definitions. It provides:
- Validation for API definition JSON files
- Auto-completion in editors like VS Code
- Documentation of the expected format

## Schema Location

The schema is available at:
- **Local**: `doc/pyhdl-if.schema.json`
- **Published**: Will be available in the documentation at the project root after building

## Using the Schema

### In Your JSON Files

Add the `$schema` property at the top of your JSON file:

```json
{
  "$schema": "https://raw.githubusercontent.com/fvutils/pyhdl-if-pytest/main/doc/pyhdl-if.schema.json",
  "fullname": "mymodule.MyClass",
  "methods": [...]
}
```

### VS Code Integration

VS Code will automatically provide:
- Schema validation (red squiggles for errors)
- Auto-completion (Ctrl+Space for suggestions)
- Hover documentation

### Command-Line Validation

```bash
pip install jsonschema

python -c "
import json
import jsonschema

with open('doc/pyhdl-if.schema.json', 'r') as f:
    schema = json.load(f)

with open('your-api.json', 'r') as f:
    api_def = json.load(f)

jsonschema.validate(api_def, schema)
print('Valid!')
"
```

## Schema Features

### Supported Formats

1. **Single API Definition**:
```json
{
  "fullname": "test.MyApi",
  "methods": [...]
}
```

2. **Multiple APIs (Object)**:
```json
{
  "apis": [
    {"fullname": "test.Api1", ...},
    {"fullname": "test.Api2", ...}
  ]
}
```

3. **Multiple APIs (Array)**:
```json
[
  {"fullname": "test.Api1", ...},
  {"fullname": "test.Api2", ...}
]
```

### Type System

All supported types are validated:
- Integers: `int8`, `int16`, `int32`, `int64`, `int`
- Unsigned: `uint8`, `uint16`, `uint32`, `uint64`
- Floating point: `float`, `double`
- Boolean: `bool`
- String: `str`, `string`
- Objects: `pyobject`, `object`

### Method Kinds

Valid method kinds:
- `imp_task` - Import task (async, SV→Python)
- `imp_func` - Import function (sync, SV→Python)
- `exp_task` - Export task (async, Python→SV)
- `exp_func` - Export function (sync, Python→SV)
- `imp` - Auto-detect (async if coroutine)
- `exp` - Auto-detect (async if coroutine)

## Examples

See the `examples` section in the schema file for complete working examples.

## Testing

The schema is tested with:
```bash
pytest tests/unit/test_json_schema.py
```

These tests verify:
- Schema itself is valid
- All type variations work
- All method kinds work
- Invalid inputs are rejected
- Test data validates correctly
