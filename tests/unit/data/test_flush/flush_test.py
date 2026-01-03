
import ctypes as ct
import hdl_if as hif

@hif.api
class SVHelper(object):
    
    @hif.imp
    def display_msg(self, i : ct.c_uint32):
        pass

@hif.api
class Test(object):

    @hif.exp
    def run(self, helper : ct.py_object):
        # Non-async version to avoid task completion issues in Verilator
        for i in range(5):
            print(f'[Python] Before call {i}')
            helper.display_msg(i)
            print(f'[Python] After call {i}')
        
        with open("status.txt", "w") as fp:
            fp.write("PASS: flush test completed\n")
