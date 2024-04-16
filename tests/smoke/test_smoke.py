#****************************************************************************
#* test_smoke.py
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
import os
import pytest
import sysconfig
from pytest_fv import *
from ..util import Util

def test_smoke(request):
    utils = Util(request)

    testdir = os.path.dirname(os.path.abspath(__file__))
    pyhdl_dir = os.path.abspath(os.path.join(testdir, "../.."))

    fs = FuseSoc()
    fs.add_library(os.path.join(pyhdl_dir, "packages/uvmf-core/uvmf_base_pkg"))
    fs.add_library(os.path.join(pyhdl_dir, "src/hdl_call_if/share/sv"))
    fs.add_library(testdir)

    sim = HdlSim.create(testdir, "vlt")
    sim.addFiles(fs.getFiles("smoke"))
    sim.top.add("top")

    libs = sysconfig.get_config_var("LIBS")
    libdir = sysconfig.get_config_var("LIBDIR")
    libpython = sysconfig.get_config_var("LDLIBRARY")

    # LDLIBRARY
    # LIBDIR
    sim.dpi_libs.append(os.path.join(libdir, libpython))

    sim.build()

#    for key,val in sysconfig.get_config_vars().items():
#        print("Elem: %s = %s" % (key, val))


    args = sim.mkRunArgs(testdir)

    sim.run(args)
