#!/usr/bin/env python3
#****************************************************************************
#* gen_py_from_json.py
#*
#* Generate Python API classes from JSON API definitions
#*
#****************************************************************************
import sys
import argparse
from hdl_if.impl.call.api_def_from_json import ApiDefFromJson
from hdl_if.impl.call.gen_py_class import GenPyClass

def main():
    parser = argparse.ArgumentParser(
        description='Generate Python API classes from JSON API definitions')
    parser.add_argument('-j', '--json', 
        help='JSON string defining the API classes',
        required=True)
    parser.add_argument('-o', '--output',
        default='-',
        help='Output file (default: stdout)')
    
    args = parser.parse_args()
    
    # Parse JSON to create API definitions
    apis = ApiDefFromJson.parse(args.json)
    
    # Generate Python code
    if args.output == '-':
        out = sys.stdout
        gen = GenPyClass(out)
        gen.gen_module(apis)
    else:
        with open(args.output, 'w') as out:
            gen = GenPyClass(out)
            gen.gen_module(apis)
            print(f"Generated Python classes in: {args.output}")

if __name__ == '__main__':
    main()
