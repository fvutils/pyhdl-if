#****************************************************************************
#* test_json_schema.py
#*
#* Tests for JSON schema validation
#*
#****************************************************************************
import json
import os
import pytest

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

schema_file = os.path.join(
    os.path.dirname(__file__), '..', '..', 'doc', 'pyhdl-if.schema.json')

@pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
class TestJsonSchema:
    """Tests for JSON schema validation."""

    def setup_method(self):
        """Load schema before each test."""
        with open(schema_file, 'r') as f:
            self.schema = json.load(f)

    def test_schema_is_valid(self):
        """Test that the schema itself is valid."""
        # This will raise an exception if the schema is invalid
        jsonschema.Draft7Validator.check_schema(self.schema)

    def test_validate_simple_api(self):
        """Test validation of a simple API definition."""
        api_def = {
            "fullname": "test.SimpleApi",
            "methods": [
                {
                    "name": "do_something",
                    "kind": "exp_func",
                    "params": [
                        {"name": "value", "type": "int32"}
                    ],
                    "return_type": "int32"
                }
            ]
        }
        jsonschema.validate(api_def, self.schema)

    def test_validate_multiple_apis(self):
        """Test validation of multiple API definitions."""
        api_def = {
            "apis": [
                {
                    "fullname": "test.ApiOne",
                    "methods": [{"name": "method1", "kind": "exp_func"}]
                },
                {
                    "fullname": "test.ApiTwo",
                    "methods": [{"name": "method2", "kind": "imp_task"}]
                }
            ]
        }
        jsonschema.validate(api_def, self.schema)

    def test_validate_array_format(self):
        """Test validation of array format."""
        api_def = [
            {
                "fullname": "test.Api1",
                "methods": [{"name": "m1", "kind": "exp_func"}]
            },
            {
                "fullname": "test.Api2",
                "methods": [{"name": "m2", "kind": "imp_func"}]
            }
        ]
        jsonschema.validate(api_def, self.schema)

    def test_validate_with_init_params(self):
        """Test validation with init parameters."""
        api_def = {
            "fullname": "test.ApiWithInit",
            "init_params": [
                {"name": "addr", "type": "uint32"},
                {"name": "size", "type": "uint32"}
            ],
            "methods": []
        }
        jsonschema.validate(api_def, self.schema)

    def test_validate_all_types(self):
        """Test validation of all supported types."""
        types = [
            "bool", "byte", "char",
            "int8", "int16", "int32", "int64", "int",
            "uint8", "uint16", "uint32", "uint64",
            "float", "double", "str", "string",
            "pyobject", "object"
        ]
        
        for typ in types:
            api_def = {
                "fullname": f"test.Test{typ.capitalize()}",
                "methods": [
                    {
                        "name": "test_method",
                        "kind": "exp_func",
                        "params": [{"name": "param", "type": typ}],
                        "return_type": typ
                    }
                ]
            }
            jsonschema.validate(api_def, self.schema)

    def test_validate_all_method_kinds(self):
        """Test validation of all method kinds."""
        kinds = ["imp_task", "imp_func", "exp_task", "exp_func", "imp", "exp"]
        
        for kind in kinds:
            api_def = {
                "fullname": f"test.Test{kind.capitalize()}",
                "methods": [
                    {
                        "name": "test_method",
                        "kind": kind
                    }
                ]
            }
            jsonschema.validate(api_def, self.schema)

    def test_invalid_fullname(self):
        """Test that invalid fullnames are rejected."""
        api_def = {
            "fullname": "invalid-name-with-dashes",
            "methods": []
        }
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(api_def, self.schema)

    def test_invalid_type(self):
        """Test that invalid types are rejected."""
        api_def = {
            "fullname": "test.InvalidType",
            "methods": [
                {
                    "name": "test_method",
                    "params": [{"name": "param", "type": "invalid_type"}]
                }
            ]
        }
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(api_def, self.schema)

    def test_invalid_method_kind(self):
        """Test that invalid method kinds are rejected."""
        api_def = {
            "fullname": "test.InvalidKind",
            "methods": [
                {
                    "name": "test_method",
                    "kind": "invalid_kind"
                }
            ]
        }
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(api_def, self.schema)

    def test_missing_fullname(self):
        """Test that APIs without fullname are rejected."""
        api_def = {
            "methods": []
        }
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(api_def, self.schema)

    def test_test_data_validates(self):
        """Test that our test data validates against the schema."""
        test_data_file = os.path.join(
            os.path.dirname(__file__), 'data', 'test_json_api', 'api_def.json')
        
        if os.path.exists(test_data_file):
            with open(test_data_file, 'r') as f:
                test_data = json.load(f)
            jsonschema.validate(test_data, self.schema)

    def test_void_return_type(self):
        """Test that void/None return types are accepted."""
        for ret_type in ["void", "None"]:
            api_def = {
                "fullname": "test.VoidReturn",
                "methods": [
                    {
                        "name": "test_method",
                        "return_type": ret_type
                    }
                ]
            }
            jsonschema.validate(api_def, self.schema)

    def test_no_return_type(self):
        """Test that methods without return_type are accepted."""
        api_def = {
            "fullname": "test.NoReturn",
            "methods": [
                {
                    "name": "test_method"
                }
            ]
        }
        jsonschema.validate(api_def, self.schema)

    def test_schema_examples_validate(self):
        """Test that examples in the schema are valid."""
        # The schema includes examples that should validate
        if 'examples' in self.schema:
            for example in self.schema['examples']:
                jsonschema.validate(example, self.schema)
