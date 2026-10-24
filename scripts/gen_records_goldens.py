"""Regenerates the checked-in outputs of the record/interface generators
used by the tests. Run after an intended change to generated code; with
--check (as CI does), fails if any checked-in file is stale."""
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(root, "src"))

from hdl_if.gen.spec import load_spec   # noqa: E402
from hdl_if.gen.sv import gen_sv        # noqa: E402
from hdl_if.gen.py import gen_py        # noqa: E402

#: (spec, SV package, Python module, output directory)
GOLDENS = [
    ("tests/unit/gen/data/spike.json", "spike_pkg", "spike_api", "tests/unit/data/spike_records"),
    ("tests/unit/gen/data/types.json", "types_pkg", "types_api", "tests/unit/data/records_types"),
]


def generate(spec, pkg, mod):
    u = load_spec(os.path.join(root, spec))
    src = os.path.basename(spec)
    return {pkg + ".sv": gen_sv(u, pkg, mod, src), mod + ".py": gen_py(u, src)}


def main():
    import argparse
    from hdl_if.cmd.cmd_gen import write_or_check  # noqa: E402
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
        help="Write nothing; exit 1 with a diff if a checked-in file is stale")
    args = parser.parse_args()
    outputs = {}
    for spec, pkg, mod, outdir in GOLDENS:
        for name, text in generate(spec, pkg, mod).items():
            outputs[os.path.relpath(os.path.join(root, outdir, name))] = text
    status = write_or_check(outputs, args.check)
    if not args.check:
        for path in sorted(outputs.keys()):
            print("Wrote %s" % path)
    sys.exit(status)


if __name__ == "__main__":
    main()
