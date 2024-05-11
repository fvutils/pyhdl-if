
from hdl_if.hdl_services import HdlServices
from .hdl_services_dpi import HdlServicesDpi

services = None


def dpi_init():
    global services
    from hdl_if.impl.call.context import Context
    from hdl_if.impl.call.hdl_call_endpoint_dpi import HdlCallEndpointDPI

    print("dpi_init", flush=True)

    ep = None
    try:
        services = HdlServicesDpi()
        HdlServices.registerServices(services)

        ctxt = Context.inst()

        ep = HdlCallEndpointDPI(services.getPkgScope())
        ctxt.addEndpoint(ep)
    except Exception as e:
        print("Exception: %s" % str(e), flush=True)

    return ep

