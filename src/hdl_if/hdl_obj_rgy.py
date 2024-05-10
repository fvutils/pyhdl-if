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
import re

class HdlObjRgy(object):

    _inst = None

    def __init__(self):
        self.obj_instname_m = {}
        self.obj_l = []
        pass

    def registerObj(self, obj, inst_name, replace=False):
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
        ret = None
        if regex:
            match = []
            re_p = re.compile(inst_name)
            for name in self.obj_instname_m.keys():
                if re_p.match(name):
                    match.append(self.obj_instname_m[name])

            if len(match) == 1:
                ret = match[0];
            elif len(match) == 0:
                raise Exception("Multiple matches to pattern %s: %s" % (inst_name, str(ret)))
        else:
            for name in self.obj_instname_m.keys():
                if inst_name == name:
                    ret = self.obj_instname_m[name]
                    break
        return ret
    
    def getInstNames(self):
        return list(self.obj_instname_m.keys())
    
    def getObjs(self):
        return self.obj_l

    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = HdlObjRgy()
        return cls._inst

