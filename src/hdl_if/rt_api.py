#****************************************************************************
#* rt_api.py
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
"""Version of the runtime API that generated code is written against.

Code produced by the ``gen-from-*`` commands is checked in, so the runtime
functions it calls are a compatibility contract. Each generated file is
stamped with the runtime API version it targets and checks it when loaded.

The SystemVerilog package ``pyhdl_if`` carries the same two numbers as
``PYHDL_IF_RT_API_VERSION`` and ``PYHDL_IF_RT_API_MIN_VERSION``; keep them
equal.
"""

#: Runtime API version this release provides. Bumped whenever the API that
#: generated code calls changes.
PYHDL_IF_RT_API_VERSION = 1

#: Oldest runtime API version this release still accepts from generated code.
PYHDL_IF_RT_API_MIN_VERSION = 1


def check_rt_api_version(version: int, source: str = "<generated code>") -> None:
    """Check that generated code targets a runtime API this release provides.

    Args:
        version: The runtime API version the generated code was stamped with.
        source: Names the generated file or package, for the error message.

    Raises:
        RuntimeError: If ``version`` is newer than this runtime, or older than
            the oldest version it still supports. The fix is to regenerate the
            code, or to install a matching pyhdl-if.
    """
    if version > PYHDL_IF_RT_API_VERSION:
        raise RuntimeError(
            "%s targets pyhdl-if runtime API version %d, but the installed "
            "pyhdl-if provides version %d. Upgrade pyhdl-if." % (
                source, version, PYHDL_IF_RT_API_VERSION))
    if version < PYHDL_IF_RT_API_MIN_VERSION:
        raise RuntimeError(
            "%s targets pyhdl-if runtime API version %d, which the installed "
            "pyhdl-if no longer supports (oldest supported: %d). Regenerate "
            "it." % (source, version, PYHDL_IF_RT_API_MIN_VERSION))
