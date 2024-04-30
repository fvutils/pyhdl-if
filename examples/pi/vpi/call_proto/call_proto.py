import hdl_if as hif

def countones(v):
    ones = 0
    print("countones: v=%d" % v, flush=True)
    
    while v:
        if v & 1:
            ones += 1
        v >>= 1

    return ones

async def main(call_if):
    print("main", flush=True)

    print("--> invoked", flush=True)
    res = await call_if._proxy.invoke_hdl_t("put", ())
    print("<-- invoked (%s)" % str(res), flush=True)

    print("--> invoked", flush=True)
    await call_if._proxy.invoke_hdl_t("put", ())
    print("<-- invoked", flush=True)

    print("--> invoked", flush=True)
    await call_if._proxy.invoke_hdl_t("put", ())
    print("<-- invoked", flush=True)
    pass

@hif.api
class CallIF(object):
    pass

def init(call_if):
    from hdl_if.backend import Backend
    print("init", flush=True)
    be = Backend.inst()
    be.mkTask(main(call_if))

def info(obj):
    print("info: %s" % str(obj), flush=True)
    print("type: %s" % str(type(obj)))
    for f in dir(obj):
        print("Field: %s" % f, flush=True)
    print("id: %d" % obj.id, flush=True)
