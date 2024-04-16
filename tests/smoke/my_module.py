import ctypes
import hdl_call_if.svdpi as svdpi
print("My Module", flush=True)

def thread_1(lib, scope):
    try:
        print("--> thread_1 %s scope=0x%08x" % (str(lib), scope), flush=True)
        print("--> svSetScope", flush=True)
        top = svdpi.svGetScopeFromName("top".encode())
#        print("top=0x%08x scope=0x%08x" % (int(top), scope), flush=True)
        svdpi.svSetScope(top)
        print("<-- svSetScope", flush=True)
        lib.timed_task()
        print("<-- thread_1 %s" % str(lib), flush=True)
    except Exception as e:
        print("Exception: %s" % str(e), flush=True)

def thread_2():
    print("thread_2", flush=True)

_closure = None

def my_method(top_scope):
    global _closure
    print("my_method %s" % str(top_scope), flush=True)
    try:
        lib = ctypes.CDLL(None)
    except Exception as e:
        print("Exception: %s" % str(e), flush=True)

    print("lib: %s" % str(lib), flush=True)

    try:
        svGetScope = lib.svGetScope
    except Exception as e:
        print("Exception: %s" % str(e), flush=True)
    scope = svdpi.svGetScope()
    print("scope: %s" % str(scope), flush=True)

    _closure = lambda : thread_1(lib, top_scope)
    lib.pyhdl_queue_runnable(ctypes.py_object(_closure))
#    lib.pyhdl_queue_runnable(ctypes.py_object(thread_2))





