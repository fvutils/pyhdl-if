#****************************************************************************
#* test_imp_default_params.py
#*
#* Tests for @imp decorated methods with default parameter values
#*
#****************************************************************************
import inspect
import os
import sys
import pytest

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from hdl_if.decorators import api, imp, exp
from hdl_if.impl.call.api_def_rgy import ApiDefRgy
from hdl_if.impl.call.ctor import Ctor
from hdl_if.impl.call.imp_func_impl import ImpFuncImpl
from hdl_if.impl.call.imp_task_impl import ImpTaskImpl


class TestImpDefaultParams:
    """Tests for @imp method default parameter handling."""

    def setup_method(self):
        """Reset registries before each test."""
        ApiDefRgy.init()
        Ctor.init()

    def test_defaults_captured_in_method_def(self):
        """Test that default values are properly captured in MethodDef."""
        @api
        class TestApi:
            def __init__(self):
                pass

            @imp
            def method_with_defaults(self, a: int, b: int = 5, c: str = "hello") -> int:
                pass

        apis = ApiDefRgy.inst().getApis()
        test_api = next(a for a in apis if "TestApi" in a.fullname)
        method = next(m for m in test_api.methods if m.name == "method_with_defaults")

        assert len(method.params) == 3
        assert len(method.defaults) == 3
        assert method.defaults[0] is inspect.Parameter.empty
        assert method.defaults[1] == 5
        assert method.defaults[2] == "hello"

    def test_build_args_all_positional(self):
        """Test _build_args when all args are provided positionally."""
        @api
        class TestApi:
            def __init__(self):
                pass

            @imp
            def method_with_defaults(self, a: int, b: int = 5, c: str = "hello") -> int:
                pass

        apis = ApiDefRgy.inst().getApis()
        test_api = next(a for a in apis if "TestApi" in a.fullname)
        method = next(m for m in test_api.methods if m.name == "method_with_defaults")

        impl = ImpFuncImpl(method)
        result = impl._build_args((1, 2, "test"), {})
        assert result == (1, 2, "test")

    def test_build_args_only_required(self):
        """Test _build_args when only required args are provided."""
        @api
        class TestApi:
            def __init__(self):
                pass

            @imp
            def method_with_defaults(self, a: int, b: int = 5, c: str = "hello") -> int:
                pass

        apis = ApiDefRgy.inst().getApis()
        test_api = next(a for a in apis if "TestApi" in a.fullname)
        method = next(m for m in test_api.methods if m.name == "method_with_defaults")

        impl = ImpFuncImpl(method)
        result = impl._build_args((1,), {})
        assert result == (1, 5, "hello")

    def test_build_args_partial_positional(self):
        """Test _build_args with partial positional args."""
        @api
        class TestApi:
            def __init__(self):
                pass

            @imp
            def method_with_defaults(self, a: int, b: int = 5, c: str = "hello") -> int:
                pass

        apis = ApiDefRgy.inst().getApis()
        test_api = next(a for a in apis if "TestApi" in a.fullname)
        method = next(m for m in test_api.methods if m.name == "method_with_defaults")

        impl = ImpFuncImpl(method)
        result = impl._build_args((1, 10), {})
        assert result == (1, 10, "hello")

    def test_build_args_with_kwargs(self):
        """Test _build_args with keyword arguments."""
        @api
        class TestApi:
            def __init__(self):
                pass

            @imp
            def method_with_defaults(self, a: int, b: int = 5, c: str = "hello") -> int:
                pass

        apis = ApiDefRgy.inst().getApis()
        test_api = next(a for a in apis if "TestApi" in a.fullname)
        method = next(m for m in test_api.methods if m.name == "method_with_defaults")

        impl = ImpFuncImpl(method)
        result = impl._build_args((1,), {"c": "world"})
        assert result == (1, 5, "world")

    def test_build_args_mixed_kwargs(self):
        """Test _build_args with mixed positional and keyword arguments."""
        @api
        class TestApi:
            def __init__(self):
                pass

            @imp
            def method_with_defaults(self, a: int, b: int = 5, c: str = "hello") -> int:
                pass

        apis = ApiDefRgy.inst().getApis()
        test_api = next(a for a in apis if "TestApi" in a.fullname)
        method = next(m for m in test_api.methods if m.name == "method_with_defaults")

        impl = ImpFuncImpl(method)
        result = impl._build_args((1,), {"b": 20, "c": "foo"})
        assert result == (1, 20, "foo")

    def test_build_args_missing_required_raises(self):
        """Test that missing required args raises TypeError."""
        @api
        class TestApi:
            def __init__(self):
                pass

            @imp
            def method_with_defaults(self, a: int, b: int = 5, c: str = "hello") -> int:
                pass

        apis = ApiDefRgy.inst().getApis()
        test_api = next(a for a in apis if "TestApi" in a.fullname)
        method = next(m for m in test_api.methods if m.name == "method_with_defaults")

        impl = ImpFuncImpl(method)
        with pytest.raises(TypeError, match="missing required argument"):
            impl._build_args((), {})

    def test_build_args_unexpected_kwarg_raises(self):
        """Test that unexpected kwargs raises TypeError."""
        @api
        class TestApi:
            def __init__(self):
                pass

            @imp
            def method_with_defaults(self, a: int, b: int = 5, c: str = "hello") -> int:
                pass

        apis = ApiDefRgy.inst().getApis()
        test_api = next(a for a in apis if "TestApi" in a.fullname)
        method = next(m for m in test_api.methods if m.name == "method_with_defaults")

        impl = ImpFuncImpl(method)
        with pytest.raises(TypeError, match="unexpected keyword argument"):
            impl._build_args((1,), {"unknown": 42})

    def test_task_build_args_works(self):
        """Test that ImpTaskImpl also has working _build_args."""
        @api
        class TestApi:
            def __init__(self):
                pass

            @imp
            async def async_method(self, x: int, y: int = 10) -> int:
                pass

        apis = ApiDefRgy.inst().getApis()
        test_api = next(a for a in apis if "TestApi" in a.fullname)
        method = next(m for m in test_api.methods if m.name == "async_method")

        impl = ImpTaskImpl(method)
        result = impl._build_args((5,), {})
        assert result == (5, 10)

    def test_no_defaults_method(self):
        """Test that methods without defaults still work correctly."""
        @api
        class TestApi:
            def __init__(self):
                pass

            @imp
            def method_no_defaults(self, a: int, b: str) -> int:
                pass

        apis = ApiDefRgy.inst().getApis()
        test_api = next(a for a in apis if "TestApi" in a.fullname)
        method = next(m for m in test_api.methods if m.name == "method_no_defaults")

        assert len(method.defaults) == 2
        assert method.defaults[0] is inspect.Parameter.empty
        assert method.defaults[1] is inspect.Parameter.empty

        impl = ImpFuncImpl(method)
        result = impl._build_args((1, "test"), {})
        assert result == (1, "test")

        with pytest.raises(TypeError, match="missing required argument"):
            impl._build_args((1,), {})

    def test_all_defaults_method(self):
        """Test that methods with all default parameters work correctly."""
        @api
        class TestApi:
            def __init__(self):
                pass

            @imp
            def method_all_defaults(self, a: int = 1, b: int = 2, c: int = 3) -> int:
                pass

        apis = ApiDefRgy.inst().getApis()
        test_api = next(a for a in apis if "TestApi" in a.fullname)
        method = next(m for m in test_api.methods if m.name == "method_all_defaults")

        impl = ImpFuncImpl(method)
        
        # No args - all defaults
        result = impl._build_args((), {})
        assert result == (1, 2, 3)

        # Override just the first
        result = impl._build_args((10,), {})
        assert result == (10, 2, 3)

        # Override using kwargs
        result = impl._build_args((), {"b": 20})
        assert result == (1, 20, 3)
