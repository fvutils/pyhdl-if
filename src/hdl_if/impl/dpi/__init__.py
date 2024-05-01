
from hdl_if.hdl_services import HdlServices
from .hdl_services_dpi import HdlServicesDpi

services = None


def dpi_init(scope):
    global services
    from hdl_if.impl.call.context import Context
    from hdl_if.impl.call.hdl_call_endpoint_dpi import HdlCallEndpointDPI

    services = HdlServicesDpi(scope)
    HdlServices.registerServices(services)

    ep = None
    try:
        ctxt = Context.inst()

        ep = HdlCallEndpointDPI(scope)
        ctxt.addEndpoint(ep)
    except Exception as e:
        print("Exception: %s" % str(e), flush=True)

    return ep

