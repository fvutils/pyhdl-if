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
import sys
import pytest

# Import fixtures from the unit tests module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from unit import pyhdl_dvflow, hdl_if_env, available_sims_dpi

@pytest.mark.parametrize("pyhdl_dvflow", available_sims_dpi(incl=["vlt"]), indirect=True)
def test_smoke(pyhdl_dvflow, hdl_if_env):
    testdir = os.path.dirname(os.path.abspath(__file__))
    
    pyhdl_dvflow.setEnv(hdl_if_env)
    
    hdl_if_pkg = pyhdl_dvflow.mkTask("pyhdl-if.SvPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")
    
    test_sv = pyhdl_dvflow.mkTask("std.FileSet",
                                   base=testdir,
                                   include=["top.sv"],
                                   type="systemVerilogSource")
    
    sim_img = pyhdl_dvflow.mkTask("hdlsim.%s.SimImage" % pyhdl_dvflow.sim,
                                   top=["top"],
                                   needs=[hdl_if_pkg, hdl_if_dpi, test_sv])
    
    sim_run = pyhdl_dvflow.mkTask("hdlsim.%s.SimRun" % pyhdl_dvflow.sim,
                                   needs=[sim_img])
    
    status, out = pyhdl_dvflow.runTask(sim_run)
    
    assert status == 0, "Simulation failed"
