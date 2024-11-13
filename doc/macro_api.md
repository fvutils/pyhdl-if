
- define Python API with SystemVerilog macros
- Implement with Python API

```python
  class my_class:
    def my_method(self, a, b, c) -> int:
        pass
```

```systemverilog
  class my_api extends base;
    function new();
        super.new("my_module", "my_class");
    endfunction

    `hdl_if_long_fn(my_method, "%0d %0d %0s", (int a, int b, string c))

  endclass

```