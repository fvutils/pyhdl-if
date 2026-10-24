"""Python half of the records_types simulation test."""
from hdl_if import rt
import types_api as t
from types_api import base_rec, derived_rec, empty_rec, sev_e, big_e

_errors = []

UNI = "héllo ✓ \"q\" \\ \t"


def _check(cond, msg):
    if not cond:
        print("[Py] FAIL: %s" % msg, flush=True)
        _errors.append(msg)


def errors():
    return len(_errors)


def expected_derived():
    """The value SV builds in mk_derived()."""
    return derived_rec(
        a=1, b=-2048, c=(1 << 64) - 1, d=-(1 << 63), e=1.5, s=-128, t=65535,
        items=[base_rec(b=5), base_rec(b=-1)],
        grid=[[1, 2, 3], [], [255]],
        strs=["", UNI],
        w=-(1 << 79), sev=sev_e.SEV_LOW, big=big_e.BIG_TOP,
        blobs=[b"", b"\x00\xff"], flag=True, x=-0.125)


def check_derived(d):
    """SV sent a copy of mk_derived(); check it and return a changed copy."""
    exp = expected_derived()
    _check(type(d) is derived_rec, "type %s" % type(d))
    for f in ("a", "b", "c", "d", "e", "s", "t", "items", "grid", "strs",
              "w", "sev", "big", "blobs", "flag", "x"):
        _check(getattr(d, f) == getattr(exp, f),
               "field %s: %r != %r" % (f, getattr(d, f), getattr(exp, f)))
    _check(type(d.sev) is sev_e and type(d.big) is big_e, "enum types")
    _check(type(d.items[0]) is base_rec, "list element type")
    r = d.copy()
    r.b = 2047
    r.w = (1 << 79) - 1
    r.items.append(base_rec(c=7))
    r.grid[1].append(9)
    r.sev = sev_e.SEV_HIGH
    r.big = big_e.BIG_ZERO
    r.strs = [UNI + "!"]
    r.blobs = [bytes(range(256))]
    return r


class PySvc2(object):
    """Python implementation of svc2, with the same behavior as sv_svc2."""

    def __init__(self):
        self.kept = base_rec(b=77)

    async def t0(self):
        pass

    def f_list(self, l):
        ret = []
        for d in reversed(l):
            c = d.copy()
            c.b += 1
            ret.append(c)
        return ret

    def f_ref(self, r):
        r.flag = not r.flag
        r.items = r.items + [base_rec(b=3)]
        return self.kept

    def f_if(self, i):
        return i

    def f_bytes(self, b):
        return bytes(reversed(b))

    def f_str(self, s):
        return s + "!"

    def f_real(self, x, y):
        return x + y

    def f_bool(self, b):
        return not b

    def f_enum(self, e):
        return big_e.BIG_TOP if e == sev_e.SEV_HIGH else big_e.BIG_ZERO

    def f_wide(self, w):
        return w & ((1 << 100) - 1)

    def f_names(self, state, args, method, ret, m_impl, m_obj):
        return state + args + method + ret + m_impl + m_obj

    async def t_names(self, state, args):
        return empty_rec()

    def f_empty(self, e, x):
        _check(type(e) is empty_rec, "f_empty e %r" % (e,))


def make_py_svc2():
    return PySvc2()


async def run_svc2(svc, local_is_sv):
    """Exercise an implementation of svc2 from Python.

    Works on an SV implementation (svc is an svc2_sv_proxy) and on a Python
    one, so both implementations are held to the same behavior.
    """
    print("[Py] run_svc2 (%s)" % ("SV" if local_is_sv else "Py"), flush=True)
    if local_is_sv:
        _check(isinstance(svc, t.svc2_sv_proxy), "proxy type %s" % type(svc))
    await svc.t0()

    l = [expected_derived(), derived_rec(b=10)]
    out = svc.f_list(l)
    _check([d.b for d in out] == [11, -2047], "f_list %r" % [d.b for d in out])
    _check(out[1].w == -(1 << 79) and out[1].strs[1] == UNI, "f_list deep")
    _check(svc.f_list([]) == [], "f_list empty")

    d = expected_derived()
    k = svc.f_ref(d)
    _check(d.flag is False and d.items[-1].b == 3, "f_ref by reference: %r" % (d.flag,))
    _check(k is not None and k.b == 77, "f_ref returned ref b")
    if local_is_sv:
        _check(isinstance(k, t.base_rec_sv_ref), "f_ref returns an SV ref %s" % type(k))

    _check(svc.f_if(svc) is not None, "f_if")
    _check(svc.f_bytes(b"") == b"", "f_bytes empty")
    big = bytes(i & 0xFF for i in range(4096))
    _check(svc.f_bytes(big) == bytes(reversed(big)), "f_bytes 4096")
    _check(svc.f_str(UNI) == UNI + "!", "f_str %r" % svc.f_str(UNI))
    _check(svc.f_str("") == "!", "f_str empty")
    _check(svc.f_real(1.25, 0.5) == 1.75, "f_real")
    _check(svc.f_bool(True) is False and svc.f_bool(False) is True, "f_bool")
    _check(svc.f_enum(sev_e.SEV_HIGH) is big_e.BIG_TOP, "f_enum high")
    _check(svc.f_enum(sev_e.SEV_LOW) is big_e.BIG_ZERO, "f_enum low")
    _check(svc.f_wide(-1) == (1 << 100) - 1, "f_wide -1 %x" % svc.f_wide(-1))
    _check(svc.f_wide(5) == 5, "f_wide 5")
    _check(svc.f_names(1, 2, 3, 4, 5, 6) == 21, "f_names")
    _check(type(await svc.t_names(1, 2)) is empty_rec, "t_names")
    svc.f_empty(empty_rec(), None)
    return errors()
