
import argparse
from .cmd.cmd_api_gen_sv import CmdApiGenSV
from .cmd.cmd_ifc_gen_sv import CmdIfcGenSv
from .cmd.cmd_ifc_gen_types import CmdIfcGenTypes
from .cmd.cmd_libs import CmdLibs
from .cmd.cmd_share import CmdShare

def getparser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    share_cmd = subparsers.add_parser("share",
        help="Displays the path to the 'share' directory")
    share_cmd.set_defaults(func=CmdShare())

    libs_cmd = subparsers.add_parser("libs",
        help="Displays the simulator library paths")
    libs_cmd.add_argument("-t", "--type",
        help="Specifies the type of library to retrieve. Currently optional",
        choices=("dpi", "vpi"))
    libs_cmd.set_defaults(func=CmdLibs())


    api_gen_sv = subparsers.add_parser("api-gen-sv",
        help="Generate one or more SV classes, optionally enclosed in a package")
    api_gen_sv.add_argument("-m", "--module",
        action="append",
        required=True,
        help="Specify a Python module to load for API discovery")
    api_gen_sv.add_argument("-uvm", action="store_true",
        help="Generates UVM-friendly interface classes")
    api_gen_sv.add_argument("--deprecated", action="store_true",
        help="Enable deprecated SV class output")
    api_gen_sv.add_argument("-i", "--include",
        action="append",
        help="Specify a pattern for API inclusion")
    api_gen_sv.add_argument("-e", "--exclude",
        action="append",
        help="Specify a pattern for API exclusion")
    api_gen_sv.add_argument("--follow-deps", action="store_true",
        help="Also generate classes for API base classes (dependencies)")
    api_gen_sv.add_argument("-p", "--package",
        help="Place the generated class APIs in a package")
    api_gen_sv.add_argument("-o", "--output",
        default="hdl_call_if_api.svh",
        help="Specifies the output filename")
    api_gen_sv.set_defaults(func=CmdApiGenSV())

    ifc_gen_sv = subparsers.add_parser("ifc-gen-sv",
        help="Generates ")
    ifc_gen_sv.add_argument("-m", "--module", action="append",
        help="Specifies a Python module to load")
    ifc_gen_sv.add_argument("-t", "--types", action="store_true",
        help="Generate a 'types' file containing packed struct definitions")
    ifc_gen_sv.add_argument("-s", "--style", choices=("vl", "verilog", "sv", "systemverilog"),
        default="sv",
        help="Specifies the style of output")
    ifc_gen_sv.add_argument("-o", "--output", 
        help="Specifies the output file")
    ifc_gen_sv.add_argument("ifc",
        help="Specifies the interface to generate")
    
    ifc_gen_types = subparsers.add_parser("ifc-gen-types",
        help="Generates struct types for use with the TLM interface")
    ifc_gen_types.add_argument("-m", "--module", action="append",
        help="Specifies a Python module to load")
    ifc_gen_types.add_argument("-o", "--output", 
        help="Specifies the output file")
    ifc_gen_types.add_argument("ifc",
        help="Specifies the interfaces for which to generate types")

    ifc_gen_sv.set_defaults(func=CmdIfcGenTypes())


    return parser


def main():
    parser = getparser()
    args = parser.parse_args()

    args.func(args)
    pass

if __name__ == "__main__":
    main()
