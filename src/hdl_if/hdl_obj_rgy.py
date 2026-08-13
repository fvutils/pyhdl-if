#****************************************************************************
#* hdl_obj_rgy.py
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
"""Registry mapping HDL instance paths to Python objects."""

import re

class HdlObjRgy(object):
    """Maps HDL instance paths to the Python objects bound to them.

    When an interface object is constructed for a particular HDL scope it is
    registered here under that scope's instance path, so later code -- a test,
    another interface -- can find it by path instead of threading a reference
    through.

    Use :meth:`inst` to reach the singleton.
    """

    _inst = None

    def __init__(self):
        self.obj_instname_m = {}
        self.obj_l = []
        pass

    def registerObj(self, obj, inst_name, replace=False):
        """Register an object against an HDL instance path.

        Args:
            obj: The object to register.
            inst_name: The HDL instance path to register it under.
            replace: Whether to replace an existing registration for this
                path. When False, a duplicate path is an error.

        Raises:
            Exception: If the path is already registered and ``replace`` is
                False.
        """
        if inst_name not in self.obj_instname_m.keys():
            self.obj_instname_m[inst_name] = obj
            self.obj_l.append(obj)
        elif replace:
            self.obj_l.remove(self.obj_instname_m[inst_name])
            self.obj_instname_m[inst_name] = obj
            self.obj_l.append(obj)
        else:
            raise Exception("An object with instance-path %s is already registered" % inst_name)
        
    def findObj(self, inst_name, regex=False):
        """Find a registered object by instance path.

        Args:
            inst_name: The instance path to look for, or a regular expression
                matching one when ``regex`` is True.
            regex: Whether to treat ``inst_name`` as a regular expression.

        Returns:
            The registered object, or None if nothing matched.

        Raises:
            Exception: If ``regex`` is True and the pattern matches more than
                one registered path.
        """
        ret = None
        if regex:
            match = []
            re_p = re.compile(inst_name)
            for name in self.obj_instname_m.keys():
                if re_p.match(name):
                    match.append(self.obj_instname_m[name])

            if len(match) == 1:
                ret = match[0];
            elif len(match) > 1:
                raise Exception("Multiple matches to pattern %s: %s" % (
                    inst_name, str([o for o in match])))
        else:
            for name in self.obj_instname_m.keys():
                if inst_name == name:
                    ret = self.obj_instname_m[name]
                    break
        return ret
    
    def getInstNames(self):
        """Return the instance paths of every registered object."""
        return list(self.obj_instname_m.keys())

    def getObjs(self):
        """Return every registered object, in registration order."""
        return self.obj_l

    @classmethod
    def inst(cls):
        """Return the registry singleton, creating it on first use."""
        if cls._inst is None:
            cls._inst = HdlObjRgy()
        return cls._inst

