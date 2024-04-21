#****************************************************************************
#* cmd_ifc_gen_sv.py
#*
#* Copyright 2023 Matthew Ballance and Contributors
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
#* Created on:
#*     Author: 
#*
#****************************************************************************
import importlib
import os
import traceback
from hdl_if.impl.tlm.gen_ifc_sv import GenIfcSv
from hdl_if.tlm.tlm_ifc_rgy import TlmIfcRgy

class CmdIfcGenSv(object):

    def __init__(self):
        pass

    def __call__(self, args):
        # First, load up the specified modules
        if not hasattr(args, "module") or args.module is None or len(args.module) == 0:
            raise Exception("Must specify modules to load")

        for m in args.module:
            try:
                importlib.import_module(m)
            except ImportError as e:
                traceback.print_exception(e)
                raise Exception("Failed to import module \"%s\": %s" % (
                    m, str(e)))
            
        rgy = TlmIfcRgy.inst()

        if len(rgy.getTlmIfcs()) == 0:
            raise Exception("No interfaces defined")
        
        if os.path.dirname(args.output) != "" and not os.path.isdir(os.path.dirname(args.output)):
            os.makedirs(os.path.dirname(args.output))

        with open(args.output, "w") as fp:
            gen = GenIfcSv(args.style in ("vl", "verilog"))

            for ifc in rgy.getTlmIfcs():
                gen.gen_ifc_module(ifc, fp)

        
        pass

