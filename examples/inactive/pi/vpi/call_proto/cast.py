import ctypes

class MyC(object):
    def doit(self):
        print("Hello from doit")
    pass

obj = MyC()

py_obj = ctypes.py_object(obj).value
#i_obj = ctypes.cast(obj, ctypes.c_void_p).value
i_obj = id(py_obj)

print("i_obj: 0x%08x" % i_obj)

obj2 = ctypes.cast(i_obj, ctypes.py_object).value
#py_obj2 = ctypes.py_object(py_obj2_v)

#print("py_obj2: %s" % str(py_obj2))
print("obj2: %s" % str(obj2))
obj2.doit()

