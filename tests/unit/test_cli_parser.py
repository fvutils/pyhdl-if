import argparse

from hdl_if.__main__ import getparser


def _subparsers(parser):
    for act in parser._actions:
        if isinstance(act, argparse._SubParsersAction):
            return act.choices
    return {}


def test_every_subcommand_has_handler():
    parser = getparser()
    subs = _subparsers(parser)
    assert len(subs) > 0
    missing = [name for name, sp in subs.items()
               if sp.get_default("func") is None]
    assert missing == []


def test_ifc_gen_types_handler():
    from hdl_if.cmd.cmd_ifc_gen_types import CmdIfcGenTypes
    from hdl_if.cmd.cmd_ifc_gen_sv import CmdIfcGenSv
    subs = _subparsers(getparser())
    assert isinstance(subs["ifc-gen-types"].get_default("func"), CmdIfcGenTypes)
    assert isinstance(subs["ifc-gen-sv"].get_default("func"), CmdIfcGenSv)
