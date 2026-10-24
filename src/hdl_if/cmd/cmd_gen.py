#****************************************************************************
#* cmd_gen.py
#*
#* Copyright 2026 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may
#* not use this file except in compliance with the License.
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software
#* distributed under the License is distributed on an "AS IS" BASIS,
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#* See the License for the specific language governing permissions and
#* limitations under the License.
#*
#****************************************************************************
"""The ``gen-from-py``, ``gen-from-spec`` and ``gen-from-sv`` commands.

Each reads definitions with one front end and writes both halves: an SV
package (``--sv-out``) and a Python module (``--py-out``). With ``--check``
nothing is written; the command fails if a file differs from what would be
generated.
"""
import difflib
import os
import sys
from typing import Dict, List

from ..gen.ir import TypeUniverse, IrError

__all__ = ["add_gen_args", "add_check_arg", "GenOptions", "generate_outputs",
           "write_or_check", "CmdGenFromPy", "CmdGenFromSpec", "CmdGenFromSv",
           "add_sv_args"]


def add_gen_args(p):
    """Add the output options shared by the gen-from-* commands."""
    p.add_argument("--sv-out",
        help="Write the SV package to this file")
    p.add_argument("--py-out",
        help="Write the Python module to this file")
    p.add_argument("--spec-out",
        help="Also write the definitions as a v2 JSON spec to this file")
    p.add_argument("-p", "--package",
        help="SV package name (default: --sv-out file name without extension)")
    p.add_argument("--py-module",
        help="Python module name the SV package imports at run time "
             "(default: --py-out file name without extension)")
    add_check_arg(p)


def add_check_arg(p):
    p.add_argument("--check", action="store_true",
        help="Write nothing; exit 1 and print a diff if any output file "
             "differs from what would be generated")


class GenOptions(object):
    """Resolved output options."""

    def __init__(self, args):
        self.sv_out = getattr(args, "sv_out", None)
        self.py_out = getattr(args, "py_out", None)
        self.spec_out = getattr(args, "spec_out", None)
        self.check = getattr(args, "check", False)
        self.package = getattr(args, "package", None)
        self.py_module = getattr(args, "py_module", None)

        if self.sv_out is None and self.py_out is None and self.spec_out is None:
            raise IrError("Nothing to generate: give --sv-out, --py-out and/or --spec-out")
        if self.package is None and self.sv_out is not None:
            self.package = os.path.splitext(os.path.basename(self.sv_out))[0]
        if self.py_module is None and self.py_out is not None:
            self.py_module = os.path.splitext(os.path.basename(self.py_out))[0]
        if self.sv_out is not None and self.py_module is None:
            raise IrError("--sv-out needs the Python module name: give --py-out or --py-module")


def generate_outputs(u: TypeUniverse, opts: GenOptions, source: str) -> Dict[str, str]:
    """Return ``{path: text}`` for every requested output."""
    from ..gen.sv import gen_sv
    from ..gen.py import gen_py
    from ..gen.spec import dumps_spec
    ret = {}
    if opts.sv_out is not None:
        ret[opts.sv_out] = gen_sv(u, opts.package, opts.py_module, source)
    if opts.py_out is not None:
        ret[opts.py_out] = gen_py(u, source)
    if opts.spec_out is not None:
        ret[opts.spec_out] = dumps_spec(u)
    return ret


def write_or_check(outputs: Dict[str, str], check: bool, out=None) -> int:
    """Write the outputs, or compare them with the files on disk.

    Returns:
        0 on success; 1 if ``check`` is set and any file differs or is
        missing (a unified diff is printed for each).
    """
    if out is None:
        out = sys.stdout
    status = 0
    for path in sorted(outputs.keys()):
        text = outputs[path]
        if check:
            if not os.path.isfile(path):
                out.write("%s: missing (would be generated)\n" % path)
                status = 1
                continue
            with open(path, "r") as fp:
                cur = fp.read()
            if cur != text:
                status = 1
                out.write("%s: differs from generated output\n" % path)
                out.writelines(difflib.unified_diff(
                    cur.splitlines(True), text.splitlines(True),
                    fromfile=path, tofile=path + " (generated)"))
        else:
            d = os.path.dirname(path)
            if d != "" and not os.path.isdir(d):
                os.makedirs(d)
            with open(path, "w") as fp:
                fp.write(text)
    if check and status == 0:
        out.write("Generated files are up to date\n")
    return status


def _run(build, args) -> int:
    try:
        opts = GenOptions(args)
        u, source = build()
        status = write_or_check(generate_outputs(u, opts, source), opts.check)
    except IrError as e:
        sys.stderr.write("Error: %s\n" % str(e))
        status = 2
    return status


class CmdGenFromPy(object):
    """Generates both halves from Python dataclasses, IntEnums and Protocols."""

    def __call__(self, args):
        def build():
            from ..gen.front.py import universe_from_py
            for p in (args.pythonpath or []):
                if p not in sys.path:
                    sys.path.insert(0, p)
            if not args.module:
                raise IrError("Give at least one module with -m")
            u = universe_from_py(args.module, args.include, args.exclude)
            return u, "Python module(s) %s" % ", ".join(args.module)
        sys.exit(_run(build, args))


class CmdGenFromSpec(object):
    """Generates both halves from a v2 JSON spec."""

    def __call__(self, args):
        def build():
            from ..gen.spec import load_spec
            return load_spec(args.spec), os.path.basename(args.spec)
        sys.exit(_run(build, args))


def add_sv_args(p):
    """Add the source and filter options of gen-from-sv."""
    p.add_argument("sources", nargs="*",
        help="SV source files")
    p.add_argument("-f", dest="filelists", action="append", default=[],
        help="File list (slang/simulator -f syntax; repeatable)")
    p.add_argument("-I", "--incdir", action="append", default=[],
        help="Include directory (repeatable)")
    p.add_argument("-D", "--define", action="append", default=[],
        help="Macro definition NAME or NAME=VALUE (repeatable)")
    p.add_argument("--slang-arg", action="append", default=[],
        help="Extra argument passed to the slang front end (repeatable)")
    p.add_argument("-i", "--include", action="append", default=[],
        help="Use only definitions whose pkg::name matches this pattern "
             "(repeatable); definitions they use are always included")
    p.add_argument("-e", "--exclude", action="append", default=[],
        help="Skip definitions whose pkg::name matches this pattern (repeatable)")
    p.add_argument("--sv-fields", choices=("public", "rand"), default="public",
        help="Which class data members become fields: all public ones "
             "(default) or only rand/randc ones")
    p.add_argument("--field-include", action="append", default=[],
        help="Use only fields whose pkg::Class.field matches (repeatable)")
    p.add_argument("--field-exclude", action="append", default=[],
        help="Skip fields whose pkg::Class.field matches (repeatable)")
    p.add_argument("--method-include", action="append", default=[],
        help="Use only interface methods whose pkg::Iface.method matches (repeatable)")
    p.add_argument("--method-exclude", action="append", default=[],
        help="Skip interface methods whose pkg::Iface.method matches (repeatable)")
    p.add_argument("--stop-at", action="append", default=[],
        help="Stop the base-class walk at classes whose pkg::Class matches "
             "(repeatable; in addition to the default, every class in uvm_pkg)")
    p.add_argument("--no-default-stops", action="store_true",
        help="Do not stop at uvm_pkg classes by default")
    p.add_argument("--skip-base", action="append", default=[],
        help="Pass over base classes whose pkg::Class matches, dropping "
             "their fields (repeatable)")
    p.add_argument("--skip-unsupported", action="store_true",
        help="Skip class fields of unsupported types, with a warning, "
             "instead of failing")


class CmdGenFromSv(object):
    """Generates both halves from SV classes, interface classes and enums."""

    def __call__(self, args):
        def build():
            from ..gen.front.sv import SvOptions, universe_from_sv, DEFAULT_STOP_AT
            slang = list(args.sources)
            for f in args.filelists:
                slang.extend(["-f", f])
            for d in args.incdir:
                slang.extend(["-I", d])
            for d in args.define:
                slang.extend(["-D", d])
            slang.extend(args.slang_arg)
            if len(slang) == 0:
                raise IrError("Give SV source files or -f file lists")
            stops = ([] if args.no_default_stops else list(DEFAULT_STOP_AT)) + args.stop_at
            opts = SvOptions(
                include=args.include, exclude=args.exclude, fields=args.sv_fields,
                field_include=args.field_include, field_exclude=args.field_exclude,
                method_include=args.method_include, method_exclude=args.method_exclude,
                stop_at=stops, skip_base=args.skip_base,
                skip_unsupported=args.skip_unsupported)
            u, warnings = universe_from_sv(slang, opts)
            for w in warnings:
                sys.stderr.write("Warning: %s\n" % w)
            names = [os.path.basename(s) for s in args.sources] + \
                [os.path.basename(f) for f in args.filelists]
            return u, "SV %s" % ", ".join(names)
        sys.exit(_run(build, args))

