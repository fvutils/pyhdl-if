
def get_none():
    return None

def mkTask(coro):
    from hdl_if.backend import Backend
    be = Backend.inst()
    print("-- mkTask", flush=True)
    task = be.mkTask(coro)

    be.idle()

    return task
