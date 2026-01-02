#****************************************************************************
#* test_api_spec_format.py
#*
#* Tests for API spec format detection and validation
#*
#****************************************************************************
import os
import sys
import json
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from hdl_if.cmd.cmd_api_gen_sv import CmdApiGenSV


class TestApiSpecFormat:
    """Tests for API spec format detection and handling."""

    def test_detect_json_inline(self):
        """Test detection of inline JSON."""
        cmd = CmdApiGenSV()
        json_str = '{"fullname": "test.Api", "methods": []}'
        fmt = cmd._detect_spec_format(json_str)
        assert fmt == 'json'

    def test_detect_json_file(self):
        """Test detection of JSON file by extension."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"fullname": "test.Api", "methods": []}, f)
            filepath = f.name
        
        try:
            cmd = CmdApiGenSV()
            fmt = cmd._detect_spec_format(filepath)
            assert fmt == 'json'
        finally:
            os.unlink(filepath)

    def test_detect_yaml_file_not_implemented(self):
        """Test that YAML files are detected but not yet supported."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("fullname: test.Api\nmethods: []\n")
            filepath = f.name
        
        try:
            cmd = CmdApiGenSV()
            fmt = cmd._detect_spec_format(filepath)
            assert fmt == 'yaml'
        finally:
            os.unlink(filepath)

    def test_detect_toml_file_not_implemented(self):
        """Test that TOML files are detected but not yet supported."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write('fullname = "test.Api"\nmethods = []\n')
            filepath = f.name
        
        try:
            cmd = CmdApiGenSV()
            fmt = cmd._detect_spec_format(filepath)
            assert fmt == 'toml'
        finally:
            os.unlink(filepath)

    def test_explicit_format_override(self):
        """Test explicit format specification overrides auto-detection."""
        cmd = CmdApiGenSV()
        json_str = '{"fullname": "test.Api", "methods": []}'
        fmt = cmd._detect_spec_format(json_str, spec_fmt='JSON')
        assert fmt == 'json'

    def test_unsupported_file_extension(self):
        """Test that unsupported file extensions raise an error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('some text')
            filepath = f.name
        
        try:
            cmd = CmdApiGenSV()
            with pytest.raises(Exception, match="Unsupported spec file extension"):
                cmd._detect_spec_format(filepath)
        finally:
            os.unlink(filepath)

    def test_load_json_inline(self):
        """Test loading inline JSON spec."""
        cmd = CmdApiGenSV()
        json_str = '{"fullname": "test.SimpleApi", "methods": [{"name": "foo", "kind": "exp_func"}]}'
        apis = cmd._load_spec(json_str)
        
        assert len(apis) == 1
        assert apis[0].fullname == "test.SimpleApi"
        assert len(apis[0].methods) == 1

    def test_load_json_file(self):
        """Test loading JSON spec from file."""
        spec_data = {
            "fullname": "test.FileApi",
            "methods": [{"name": "bar", "kind": "imp_func"}]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(spec_data, f)
            filepath = f.name
        
        try:
            cmd = CmdApiGenSV()
            apis = cmd._load_spec(filepath)
            
            assert len(apis) == 1
            assert apis[0].fullname == "test.FileApi"
            assert len(apis[0].methods) == 1
        finally:
            os.unlink(filepath)

    def test_yaml_not_implemented(self):
        """Test that YAML format raises not implemented error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("fullname: test.Api\nmethods: []\n")
            filepath = f.name
        
        try:
            cmd = CmdApiGenSV()
            with pytest.raises(Exception, match="YAML format not yet implemented"):
                cmd._load_spec(filepath)
        finally:
            os.unlink(filepath)

    def test_toml_not_implemented(self):
        """Test that TOML format raises not implemented error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write('fullname = "test.Api"\nmethods = []\n')
            filepath = f.name
        
        try:
            cmd = CmdApiGenSV()
            with pytest.raises(Exception, match="TOML format not yet implemented"):
                cmd._load_spec(filepath)
        finally:
            os.unlink(filepath)

    def test_spec_argument_backward_compatibility(self):
        """Test that --json argument still works (backward compatibility)."""
        from argparse import Namespace
        
        cmd = CmdApiGenSV()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sv', delete=False) as f:
            output_file = f.name
        
        try:
            args = Namespace(
                json='{"fullname": "test.LegacyApi", "methods": []}',
                spec=None,
                spec_fmt=None,
                module=None,
                output=output_file,
                package=None,
                uvm=False,
                deprecated=False,
                include=None,
                exclude=None,
                follow_deps=False
            )
            
            cmd(args)
            
            # Check that file was created
            assert os.path.exists(output_file)
            
            # Check content contains expected class
            with open(output_file, 'r') as f:
                content = f.read()
                assert 'LegacyApi' in content
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_spec_argument_new_way(self):
        """Test that --spec argument works with inline JSON."""
        from argparse import Namespace
        
        cmd = CmdApiGenSV()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sv', delete=False) as f:
            output_file = f.name
        
        try:
            args = Namespace(
                json=None,
                spec='{"fullname": "test.NewApi", "methods": []}',
                spec_fmt=None,
                module=None,
                output=output_file,
                package=None,
                uvm=False,
                deprecated=False,
                include=None,
                exclude=None,
                follow_deps=False
            )
            
            cmd(args)
            
            # Check that file was created
            assert os.path.exists(output_file)
            
            # Check content contains expected class
            with open(output_file, 'r') as f:
                content = f.read()
                assert 'NewApi' in content
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_spec_file_path(self):
        """Test that --spec works with file path."""
        from argparse import Namespace
        
        spec_data = {
            "fullname": "test.FileSpecApi",
            "methods": [{"name": "test_method", "kind": "exp_func"}]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(spec_data, f)
            spec_file = f.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sv', delete=False) as f:
            output_file = f.name
        
        try:
            cmd = CmdApiGenSV()
            
            args = Namespace(
                json=None,
                spec=spec_file,
                spec_fmt=None,
                module=None,
                output=output_file,
                package=None,
                uvm=False,
                deprecated=False,
                include=None,
                exclude=None,
                follow_deps=False
            )
            
            cmd(args)
            
            # Check that file was created and contains expected class
            assert os.path.exists(output_file)
            with open(output_file, 'r') as f:
                content = f.read()
                assert 'FileSpecApi' in content
        finally:
            if os.path.exists(spec_file):
                os.unlink(spec_file)
            if os.path.exists(output_file):
                os.unlink(output_file)
