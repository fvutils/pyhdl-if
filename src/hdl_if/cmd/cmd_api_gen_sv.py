#****************************************************************************
#* cmd_api_gen_sv.py
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
import fnmatch
import importlib
import os
from hdl_if.impl.call.gen_sv_class import GenSVClass
from hdl_if.impl.call.api_def_rgy import ApiDefRgy

class CmdApiGenSV(object):

    def __init__(self):
        pass

    def __call__(self, args):

        # First, load up the specified modules
        if not hasattr(args, "module") or args.module is None or len(args.module) == 0:
            raise Exception("Must specify modules to load")

        loaded_modules = []
        for m in args.module:
            try:
                importlib.import_module(m)
                loaded_modules.append(m)
            except ImportError as e:
                raise Exception("Failed to import module \"%s\": %s" % (
                    m, str(e)))

        all_apis = ApiDefRgy.inst().getApis()

        if len(all_apis) == 0:
            raise Exception("No APIs defined")

        # Filter APIs to those from explicitly loaded modules
        apis = self._filter_apis(all_apis, loaded_modules, args)

        if len(apis) == 0:
            raise Exception("No APIs matched from specified modules")

        if os.path.dirname(args.output) != "" and not os.path.isdir(os.path.dirname(args.output)):
            os.makedirs(os.path.dirname(args.output))

        with open(args.output, "w") as fp:
            gen = GenSVClass(fp, uvm=args.uvm, deprecated=getattr(args, "deprecated", False))

            if args.package is not None:
                gen.println('`include "pyhdl_if_macros.svh"')
                gen.println("package %s;" % args.package)
                gen.inc_ind()
                gen.println("import pyhdl_if::*;")

            for api in apis:
                gen.gen(api)

            if args.package is not None:
                gen.dec_ind()
                gen.println("endpackage")

        pass

    def _filter_apis(self, all_apis, loaded_modules, args):
        """Filter APIs based on loaded modules, include/exclude patterns, and follow-deps."""
        rgy = ApiDefRgy.inst()
        
        # Build a map of fullname -> ApiDef for quick lookup
        api_by_fullname = {a.fullname: a for a in all_apis}
        
        # Step 1: Select APIs from explicitly loaded modules
        selected = set()
        for api in all_apis:
            if self._api_in_modules(api, loaded_modules):
                selected.add(api.fullname)
        
        # Step 2: If --follow-deps, add base class APIs
        if getattr(args, "follow_deps", False):
            deps = set()
            for fullname in selected:
                api = api_by_fullname[fullname]
                self._collect_deps(api, api_by_fullname, deps)
            selected.update(deps)
        
        # Step 3: Apply include patterns (if specified, only include matching)
        include_patterns = getattr(args, "include", None)
        if include_patterns:
            included = set()
            for fullname in selected:
                for pattern in include_patterns:
                    if fnmatch.fnmatch(fullname, pattern):
                        included.add(fullname)
                        break
            selected = included
        
        # Step 4: Apply exclude patterns
        exclude_patterns = getattr(args, "exclude", None)
        if exclude_patterns:
            excluded = set()
            for fullname in selected:
                for pattern in exclude_patterns:
                    if fnmatch.fnmatch(fullname, pattern):
                        excluded.add(fullname)
                        break
            selected -= excluded
        
        # Return APIs in original registration order
        return [a for a in all_apis if a.fullname in selected]

    def _api_in_modules(self, api, modules):
        """Check if an API's fullname belongs to one of the specified modules."""
        for mod in modules:
            # API fullname is module.qualified_name (e.g. "mymod.submod.MyClass")
            # Module prefix must match: "mymod.submod.MyClass".startswith("mymod.")
            # or exact match for the module itself
            if api.fullname.startswith(mod + ".") or api.fullname == mod:
                return True
        return False

    def _collect_deps(self, api, api_by_fullname, deps):
        """Collect API dependencies (base classes) for an API."""
        pycls = getattr(api, "pycls", None)
        if pycls is None:
            return
        
        for cls in pycls.__mro__:
            if cls is object:
                continue
            cls_fullname = cls.__module__ + "." + cls.__qualname__
            if cls_fullname in api_by_fullname and cls_fullname != api.fullname:
                if cls_fullname not in deps:
                    deps.add(cls_fullname)
                    # Recursively collect deps of deps
                    self._collect_deps(api_by_fullname[cls_fullname], api_by_fullname, deps)
