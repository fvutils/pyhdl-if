#****************************************************************************
#* test_api_gen_sv_json.py
#*
#* Tests for JSON-based API generation
#*
#****************************************************************************
import io
import os
import sys
import pytest
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from hdl_if.impl.call.api_def_rgy import ApiDefRgy
from hdl_if.impl.call.ctor import Ctor
from hdl_if.impl.call.gen_sv_class import GenSVClass
from hdl_if.impl.call.api_def_from_json import ApiDefFromJson
from hdl_if.impl.call.gen_py_class import GenPyClass
from hdl_if.cmd.cmd_api_gen_sv import CmdApiGenSV


class MockArgs:
    """Mock argument object for testing CmdApiGenSV."""
    def __init__(self, **kwargs):
        self.module = kwargs.get('module', [])
        self.json = kwargs.get('json', None)
        self.uvm = kwargs.get('uvm', False)
        self.deprecated = kwargs.get('deprecated', False)
        self.include = kwargs.get('include', None)
        self.exclude = kwargs.get('exclude', None)
        self.follow_deps = kwargs.get('follow_deps', False)
        self.package = kwargs.get('package', None)
        self.output = kwargs.get('output', '/dev/null')


class TestApiGenSvJson:
    """Tests for JSON-based API generation."""

    def setup_method(self):
        """Reset registries before each test."""
        ApiDefRgy.init()
        Ctor.init()

    def test_parse_simple_json_api(self):
        """Test parsing a simple JSON API definition."""
        json_str = '''
        {
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
        '''
        
        apis = ApiDefFromJson.parse(json_str)
        assert len(apis) == 1
        
        api = apis[0]
        assert api.fullname == "test.SimpleApi"
        assert api.name == "SimpleApi"
        assert len(api.methods) == 1
        
        method = api.methods[0]
        assert method.name == "do_something"
        assert len(method.params) == 1
        assert method.params[0][0] == "value"

    def test_parse_json_with_multiple_apis(self):
        """Test parsing JSON with multiple API definitions."""
        json_str = '''
        {
            "apis": [
                {
                    "fullname": "test.ApiOne",
                    "methods": [
                        {"name": "method1", "kind": "exp_func"}
                    ]
                },
                {
                    "fullname": "test.ApiTwo",
                    "methods": [
                        {"name": "method2", "kind": "imp_task"}
                    ]
                }
            ]
        }
        '''
        
        apis = ApiDefFromJson.parse(json_str)
        assert len(apis) == 2
        assert apis[0].fullname == "test.ApiOne"
        assert apis[1].fullname == "test.ApiTwo"

    def test_parse_json_with_init_params(self):
        """Test parsing JSON with init parameters."""
        json_str = '''
        {
            "fullname": "test.ApiWithInit",
            "init_params": [
                {"name": "addr", "type": "uint32"},
                {"name": "size", "type": "uint32"}
            ],
            "methods": []
        }
        '''
        
        apis = ApiDefFromJson.parse(json_str)
        assert len(apis) == 1
        
        api = apis[0]
        assert len(api.init_params) == 2
        assert api.init_params[0][0] == "addr"
        assert api.init_params[1][0] == "size"

    def test_parse_json_imp_exp_methods(self):
        """Test parsing JSON with both imp and exp methods."""
        json_str = '''
        {
            "fullname": "test.BfmApi",
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
                },
                {
                    "name": "run",
                    "kind": "exp_task",
                    "params": [
                        {"name": "bfm", "type": "pyobject"}
                    ]
                }
            ]
        }
        '''
        
        apis = ApiDefFromJson.parse(json_str)
        assert len(apis) == 1
        
        api = apis[0]
        assert len(api.methods) == 3
        
        # Check method kinds
        from hdl_if.impl.call.method_def import MethodKind
        assert api.methods[0].kind == MethodKind.ImpTask
        assert api.methods[1].kind == MethodKind.ImpTask
        assert api.methods[2].kind == MethodKind.ExpTask

    def test_generate_sv_from_json(self):
        """Test generating SV code from JSON API definition."""
        json_str = '''
        {
            "fullname": "test.MyBfm",
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
        }
        '''
        
        apis = ApiDefFromJson.parse(json_str)
        api = apis[0]
        
        out = io.StringIO()
        gen = GenSVClass(out, ind="", uvm=False, deprecated=False)
        gen.gen(api)
        sv_content = out.getvalue()
        
        # Check that SV code contains expected elements
        assert "interface class MyBfm_imp_if" in sv_content
        assert "class MyBfm_imp_impl" in sv_content
        assert "write" in sv_content
        assert "read" in sv_content
        assert "int unsigned" in sv_content  # uint32

    def test_cmd_api_gen_sv_with_json(self):
        """Test CmdApiGenSV with JSON input."""
        json_str = '''
        {
            "fullname": "test.JsonApi",
            "methods": [
                {
                    "name": "test_method",
                    "kind": "exp_func",
                    "params": [
                        {"name": "x", "type": "int32"}
                    ],
                    "return_type": "int32"
                }
            ]
        }
        '''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sv', delete=False) as f:
            output_file = f.name
        
        try:
            args = MockArgs(json=json_str, output=output_file)
            cmd = CmdApiGenSV()
            cmd(args)
            
            # Check that output file was created
            assert os.path.exists(output_file)
            
            # Check content
            with open(output_file, 'r') as f:
                content = f.read()
                assert "JsonApi" in content
                assert "test_method" in content
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_generate_python_class_from_json(self):
        """Test generating Python class with imp methods from JSON."""
        json_str = '''
        {
            "fullname": "test.WishboneInitiator",
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
        }
        '''
        
        apis = ApiDefFromJson.parse(json_str)
        api = apis[0]
        
        out = io.StringIO()
        gen = GenPyClass(out)
        gen.gen_class(api)
        py_content = out.getvalue()
        
        # Check that Python code contains expected elements
        assert "@hif.api" in py_content
        assert "class WishboneInitiator(object):" in py_content
        assert "@hif.imp" in py_content
        assert "async def write(self, addr: ct.c_uint32, data: ct.c_uint32):" in py_content
        assert "async def read(self, addr: ct.c_uint32) -> ct.c_uint32:" in py_content

    def test_json_with_package_generation(self):
        """Test generating SV package from JSON API."""
        json_str = '''
        {
            "fullname": "test.PackageApi",
            "methods": [
                {
                    "name": "method1",
                    "kind": "exp_func"
                }
            ]
        }
        '''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sv', delete=False) as f:
            output_file = f.name
        
        try:
            args = MockArgs(json=json_str, output=output_file, package="test_pkg")
            cmd = CmdApiGenSV()
            cmd(args)
            
            with open(output_file, 'r') as f:
                content = f.read()
                assert "package test_pkg;" in content
                assert "endpackage" in content
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_json_array_format(self):
        """Test parsing JSON as array of API definitions."""
        json_str = '''
        [
            {
                "fullname": "test.Api1",
                "methods": [{"name": "m1", "kind": "exp_func"}]
            },
            {
                "fullname": "test.Api2",
                "methods": [{"name": "m2", "kind": "imp_func"}]
            }
        ]
        '''
        
        apis = ApiDefFromJson.parse(json_str)
        assert len(apis) == 2
        assert apis[0].fullname == "test.Api1"
        assert apis[1].fullname == "test.Api2"

    def test_json_type_mapping(self):
        """Test various type mappings from JSON to ctypes."""
        json_str = '''
        {
            "fullname": "test.TypeTest",
            "methods": [
                {
                    "name": "test_types",
                    "kind": "exp_func",
                    "params": [
                        {"name": "p_bool", "type": "bool"},
                        {"name": "p_int8", "type": "int8"},
                        {"name": "p_int16", "type": "int16"},
                        {"name": "p_int32", "type": "int32"},
                        {"name": "p_int64", "type": "int64"},
                        {"name": "p_uint8", "type": "uint8"},
                        {"name": "p_uint32", "type": "uint32"},
                        {"name": "p_str", "type": "string"},
                        {"name": "p_obj", "type": "pyobject"}
                    ]
                }
            ]
        }
        '''
        
        apis = ApiDefFromJson.parse(json_str)
        api = apis[0]
        method = api.methods[0]
        
        import ctypes
        assert len(method.params) == 9
        # Just verify parsing doesn't fail and types are mapped
        assert method.params[0][1] == ctypes.c_bool
        assert method.params[4][1] == ctypes.c_int64
        assert method.params[7][1] == str
        assert method.params[8][1] == ctypes.py_object
