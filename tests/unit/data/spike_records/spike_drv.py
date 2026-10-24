"""Python half of the records/interfaces spike test."""
import gc
import sys
import weakref

from hdl_if import rt
import spike_api as api
from spike_api import pkt, hdr, proto_e

print("[Py] spike_api from %s" % api.__file__, flush=True)

_errors = []


def _check(cond, msg):
    if not cond:
        print("[Py] FAIL: %s" % msg, flush=True)
        _errors.append(msg)


def errors():
    return len(_errors)


# ------------------------------------------------------------------
# Copies
# ------------------------------------------------------------------
def check_copy(p):
    """SV sent a copy. Check it, then return a modified copy."""
    _check(type(p) is pkt, "check_copy: type %s" % type(p))
    _check(p.ttl == 200, "ttl %d" % p.ttl)
    _check(p.id == -5, "id %d" % p.id)
    _check(p.valid is True, "valid %s" % p.valid)
    _check(p.weight == 2.5, "weight %s" % p.weight)
    _check(p.name == "hello, \"world\"!", "name %r" % p.name)
    _check(p.payload == bytes([0, 1, 0x7f, 0x80, 0xff]), "payload %r" % p.payload)
    _check(p.kind is proto_e.PROTO_UDP, "kind %r" % p.kind)
    _check(p.h.src == 0xC0A80001 and p.h.dst == 0xFFFFFFFF, "h %r" % p.h)
    _check(p.h.proto is proto_e.PROTO_TCP, "h.proto %r" % p.h.proto)
    _check(p.opts == [1, -1, 0x7fffffff, -0x80000000], "opts %r" % p.opts)
    _check(p.tag == (0xA5 << 88) | 0x1234, "tag %x" % p.tag)
    q = p.copy()
    q.ttl -= 1
    q.payload = p.payload + b"\x42"
    q.h.src = 1
    q.opts.append(7)
    _check(p.h.src == 0xC0A80001, "copy() is not deep")
    return q


def make_big_copy(n):
    return pkt(payload=bytes(i & 0xFF for i in range(n)), opts=list(range(n)))


# ------------------------------------------------------------------
# References to SV objects
# ------------------------------------------------------------------
def mod_ref(r):
    """SV sent a reference to its pkt. Modify it through the reference."""
    _check(isinstance(r, api.pkt_sv_ref), "mod_ref: type %s" % type(r))
    _check(r.ttl == 200, "ref ttl %d" % r.ttl)
    _check(r.name == "hello, \"world\"!", "ref name %r" % r.name)
    _check(r.kind is proto_e.PROTO_UDP, "ref kind %r" % r.kind)
    _check(r.payload == bytes([0, 1, 0x7f, 0x80, 0xff]), "ref payload")
    _check(r.tag == (0xA5 << 88) | 0x1234, "ref tag %x" % r.tag)

    snap = r.copy()
    _check(type(snap) is pkt, "copy() type %s" % type(snap))

    r.ttl = 64
    r.id = -100
    r.valid = False
    r.weight = -0.25
    r.name = "ref-set"
    r.payload = b"\x09\x08"
    r.kind = proto_e.PROTO_ICMP
    r.opts = [3, 4, 5]
    r.tag = (1 << 95) | 1

    # Nested record: a reference all the way down
    h = r.h
    _check(isinstance(h, api.hdr_sv_ref), "nested type %s" % type(h))
    h.src = 0x0A000001
    _check(r.h.src == 0x0A000001, "nested write not visible")

    # The snapshot does not change when the SV object does
    _check(snap.ttl == 200 and snap.h.src == 0xC0A80001, "snapshot changed")

    # Copies of a reference can be passed where a copy is expected
    _check(rt.rec_to_sv(r)[0] == 64, "rec_to_sv(ref)")


def take_ref(r):
    """Drop a reference immediately (lifetime test)."""
    return r.ttl


# ------------------------------------------------------------------
# References to Python objects
# ------------------------------------------------------------------
_py_pkt = None
_py_pkt_wr = None


def make_py_pkt():
    global _py_pkt, _py_pkt_wr
    _py_pkt = pkt(ttl=33, id=-7, name="py", payload=b"\x01\x02\x03",
                  kind=proto_e.PROTO_TCP, opts=[10, 20], tag=0x77,
                  h=hdr(src=5, dst=6, proto=proto_e.PROTO_UDP))
    _py_pkt_wr = weakref.ref(_py_pkt)
    return _py_pkt


def check_py_pkt():
    p = _py_pkt
    _check(p.ttl == 34, "py ttl %d" % p.ttl)
    _check(p.name == "py+sv", "py name %r" % p.name)
    _check(p.payload == b"\x01\x02\x03\x04", "py payload %r" % p.payload)
    _check(p.kind is proto_e.PROTO_UDP, "py kind %r" % p.kind)
    _check(p.h.src == 55, "py h.src %d" % p.h.src)
    _check(p.h.dst == 66 and p.h.proto is proto_e.PROTO_ICMP, "py set_h %r" % p.h)
    _check(p.opts == [10, 20, 30], "py opts %r" % p.opts)
    _check(p.tag == (1 << 90) | 0x77, "py tag %x" % p.tag)


def py_pkt_refcount():
    # Minus the getrefcount argument and this function's local
    return sys.getrefcount(_py_pkt) - 2


def drop_py_pkt():
    global _py_pkt
    _py_pkt = None
    gc.collect()
    return _py_pkt_wr() is None


# ------------------------------------------------------------------
# Interfaces
# ------------------------------------------------------------------
class PyCb(object):
    def __init__(self):
        self.got = []

    def notify(self, v):
        self.got.append(v)


class PySvc(object):
    """Python implementation of pkt_svc."""

    def __init__(self):
        self.cb = None
        self.kept = None

    def add(self, a, b):
        return a + b

    def bump(self, p):
        _check(type(p) is pkt, "PySvc.bump: type %s" % type(p))
        p.ttl -= 1
        return p

    def touch(self, p):
        _check(isinstance(p, api.pkt_sv_ref), "PySvc.touch: type %s" % type(p))
        p.ttl = p.ttl - 1
        p.opts = p.opts + [99]

    def make_ref(self, ttl):
        self.kept = pkt(ttl=ttl, name="kept")
        return self.kept

    async def xfer(self, p):
        p.id += 1
        return p

    async def touch_t(self, p):
        p.ttl = p.ttl + 10

    def subscribe(self, cb):
        _check(isinstance(cb, api.cb_if_sv_proxy), "subscribe: type %s" % type(cb))
        self.cb = cb

    def fire(self, v):
        self.cb.notify(v)


class FailingSvc(PySvc):
    def add(self, a, b):
        raise RuntimeError("deliberate failure in add")

    async def xfer(self, p):
        raise RuntimeError("deliberate failure in xfer")


def make_py_svc():
    return PySvc()


def make_failing_svc():
    return FailingSvc()


def check_py_svc_kept(svc_adapter):
    svc = svc_adapter._impl if isinstance(svc_adapter, rt.PyAdapter) else svc_adapter
    _check(svc.kept.ttl == 13, "kept ttl %d" % svc.kept.ttl)


async def run_sv_svc(svc):
    """Drive an SV implementation of pkt_svc from Python."""
    print("[Py] run_sv_svc", flush=True)
    _check(isinstance(svc, api.pkt_svc_sv_proxy), "svc type %s" % type(svc))
    _check(svc.add(2, -5) == -3, "add")

    p = pkt(ttl=10, name="copy", opts=[1])
    q = svc.bump(p)
    _check(q.ttl == 9 and p.ttl == 10, "bump: %d %d" % (q.ttl, p.ttl))
    _check(q.name == "copy-bumped", "bump name %r" % q.name)

    # By reference: SV modifies this Python object
    svc.touch(p)
    _check(p.ttl == 9 and p.opts == [1, 99], "touch(py obj): %r" % p)

    # SV hands back a reference to its own object...
    r = svc.make_ref(50)
    _check(isinstance(r, api.pkt_sv_ref), "make_ref type %s" % type(r))
    _check(r.ttl == 50, "make_ref ttl %d" % r.ttl)
    # ...and gets the same object back when it is passed in again
    svc.touch(r)
    _check(r.ttl == 49 and r.opts == [99], "touch(sv ref): %d %r" % (r.ttl, r.opts))

    x = await svc.xfer(pkt(id=41))
    _check(x.id == 42, "xfer id %d" % x.id)

    await svc.touch_t(p)
    _check(p.ttl == 19, "touch_t ttl %d" % p.ttl)

    cb = PyCb()
    svc.subscribe(cb)
    svc.fire(5)
    svc.fire(6)
    _check(cb.got == [5, 6], "callbacks %r" % cb.got)

    # Many references created and dropped: SV slots must be reclaimed
    for i in range(500):
        rr = svc.make_ref(i & 0xFF)
        _check(rr.ttl == (i & 0xFF), "loop ref")
    del rr
    return errors()


# ------------------------------------------------------------------
# Timing
# ------------------------------------------------------------------
def touch_fields_copy(p):
    return p.ttl + p.id + len(p.payload) + p.h.src


def touch_fields_ref(r):
    return r.ttl + r.id + len(r.payload) + r.h.src


async def time_sv_svc(svc, n):
    """Calls from Python into an SV implementation (timing only)."""
    import time
    t0 = time.perf_counter()
    for i in range(n):
        svc.add(i, 1)
    t1 = time.perf_counter()
    print("[Py] TIMING Py calls SV function (2 ints): %0.2f us/op" % (1e6 * (t1 - t0) / n), flush=True)

    p = pkt(id=1)
    t0 = time.perf_counter()
    for i in range(n // 4):
        await svc.xfer(p)
    t1 = time.perf_counter()
    print("[Py] TIMING Py calls SV task (pkt copy in/out, #10): %0.2f us/op" % (1e6 * (t1 - t0) / (n // 4)), flush=True)

    r = svc.make_ref(1)
    t0 = time.perf_counter()
    for i in range(n):
        r.ttl
    t1 = time.perf_counter()
    print("[Py] TIMING Py reads 1 field of an SV ref: %0.2f us/op" % (1e6 * (t1 - t0) / n), flush=True)
    return 0
