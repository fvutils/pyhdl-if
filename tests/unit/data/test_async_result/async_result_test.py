import ctypes as ct
import time

import hdl_if as hif

# Number of pad characters appended to a result string. Every result produced
# by this module has the same length, which is deliberate: CPython's
# small-object allocator only hands a freed block back out for a same-size
# allocation. Equal lengths make a stale result pointer alias another call's
# result silently -- exactly the failure mode being tested. Varying lengths
# would instead surface as a truncated string or a crash, which is a weaker
# and less repeatable signal.
PAYLOAD_PAD = 48


def payload(label : str) -> str:
    """Build the result string that SV expects back for `label`."""
    return "%s:%s" % (label, "." * PAYLOAD_PAD)


@hif.api
class Delay(object):
    """Simulation-time delay, implemented on the SystemVerilog side."""

    @hif.imp
    async def wait_ns(self, delay_ns : ct.c_uint32):
        pass


@hif.api
class AsyncResultTest(object):
    """Async (@hif.exp) methods whose results SV collects via the call semaphore."""

    @hif.exp
    async def echo(self,
                   delay : ct.py_object,
                   label : str,
                   delay_ns : ct.c_uint32) -> str:
        await delay.wait_ns(delay_ns)
        return payload(label)

    @hif.exp
    async def echo_two_delays(self,
                              delay : ct.py_object,
                              label : str,
                              d1_ns : ct.c_uint32,
                              d2_ns : ct.c_uint32) -> str:
        await delay.wait_ns(d1_ns)
        await delay.wait_ns(d2_ns)
        return payload(label)

    @hif.exp
    async def echo_blocking(self,
                            label : str,
                            sleep_ms : ct.c_uint32) -> str:
        # Blocking sleep: no wait_ns is issued, so the SV scheduler is never
        # asked for a delay and simulation time must not advance.
        time.sleep(sleep_ms / 1000.0)
        return payload(label)
