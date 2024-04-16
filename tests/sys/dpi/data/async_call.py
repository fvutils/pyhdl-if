import hdl_call_if as hci

class MyC(object):

    def __init__(self):
        print("MyC::__init__", flush=True)

    def inbound(self):
        print("inbound", flush=True)

        if hasattr(self, "__proxy"):
            print("has", flush=True)
            proxy = getattr(self, "__proxy")
        else:
            print("doesn't have", flush=True)

        try:
            ret = proxy.invoke_hdl_f("outbound", ())
        except Exception as e:
            print("Exception(inbound): %s" % str(e), flush=True)

        return ret
    
    async def inbound_t(self):
        print("--> inbound_t");

        if hasattr(self, "__proxy"):
            print("has", flush=True)
            proxy = getattr(self, "__proxy")
        else:
            print("doesn't have", flush=True)

        for i in range(10):
            await proxy.invoke_hdl_t(
                "outbound_t",
                ()
            )
#            await self.outbound_t()

        print("<-- inbound_t");
    
    
