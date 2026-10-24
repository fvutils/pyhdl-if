"""Python side of the UVM records test: coverage-style code that works on a
copy or on a reference alike."""
import pkt_gen_api as g

errors = []


def _check(cond, msg):
    if not cond:
        print("[Py] FAIL: %s" % msg, flush=True)
        errors.append(msg)


def sample(t):
    """Identical for a copy (dataclass) and a reference (SV-backed)."""
    return (t.src, t.dst, t.ttl, bytes(t.payload), t.kind, bytes(t.udata),
            bytes(t.mac), list(t.nums), [o.code for o in t.opts])


class PyMon(object):
    def __init__(self):
        self.got = []

    def write(self, t):
        _check(type(t) is g.pkt_item, "write: type %s" % type(t))
        self.got.append(sample(t))


mon = PyMon()


def make_mon():
    return mon


def cover_ref(r):
    _check(isinstance(r, g.pkt_item_sv_ref), "cover_ref: type %s" % type(r))
    s = sample(r)
    _check(s == mon.got[0], "ref and copy differ: %r vs %r" % (s, mon.got[0]))
    r.ttl = 99
    r.payload = r.payload + b"\xff"
    r.udata = b"\x10\x20"
    r.mac = b"\xaa\xbb\xcc\xdd\xee\xff"
    r.nums = [-1, 2]
    r.opts = [g.opt_c(code=9)]


def check():
    _check(mon.got == [(0x0A000001, 0xC0A80001, 7, b"\x01\x02\x83", g.pkt_kind_e.K_CTRL,
                        b"\xfe", b"\x00\x01\x02\x03\x04\x05", [5, -6], [1, 2])],
           "got %r" % mon.got)
    return len(errors)
