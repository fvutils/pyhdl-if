#****************************************************************************
#* setup.py for pyhdl-if
#****************************************************************************
import os
import sys
import sysconfig
from setuptools import Extension, setup, find_namespace_packages

version="0.2.0"

proj_dir = os.path.dirname(os.path.abspath(__file__))
pythondir = os.path.join(proj_dir, "src")

try:
    import sys
    sys.path.insert(0, os.path.join(proj_dir, "src"))
    from hdl_if.__build_num__ import BUILD_NUM
    version += ".%d" % BUILD_NUM
except ImportError:
    pass

isSrcBuild = False

try:
    from ivpm.setup import setup
    isSrcBuild = os.path.isdir(os.path.join(proj_dir, "src"))
    print("Note: performing IVPM source build")
except ImportError as e:
    from setuptools import setup
    print("Note: Falling back to non-IVPM build")

include_dirs = []

if isSrcBuild:
    include_dirs.append(pythondir)
    include_dirs.append(os.path.join(proj_dir, "scripts"))
    include_dirs.append(os.path.join(proj_dir, "build"))
else:
    # TODO: must consider installation from actual source
    include_dirs.append(pythondir)
    if os.path.isdir(os.path.join(proj_dir, "build")):
        include_dirs.append(os.path.join(proj_dir, "build"))
    include_dirs.append(os.path.join(proj_dir, "scripts"))


for cv in sysconfig.get_config_vars():
    print("%s: %s" % (cv, sysconfig.get_config_var(cv)))

PYTHON_LIB = sysconfig.get_config_var("LDLIBRARY")
PYTHON_LIB = PYTHON_LIB[3:]
PYTHON_LIB = PYTHON_LIB[:-3]
PYTHON_LIBDIR = sysconfig.get_config_var("LIBDEST")
PYTHON_LINK_OBJS = sysconfig.get_config_var("LINK_PYTHON_OBJS")
PYTHON_LIB_LIBS = sysconfig.get_config_var("LIBS")

extra_link_args = []
library_dirs = []
#library_dirs.extend([PYTHON_LIBDIR])
#extra_link_args.extend(PYTHON_LINK_OBJS.split())
#extra_link_args.extend(PYTHON_LIB_LIBS.split())

ext = Extension("hdl_if.entry",
            sources=[
                os.path.join(pythondir, "entry.c"), 
            ],
            library_dirs=library_dirs,
            extra_link_args=extra_link_args,
            language="c",
            include_dirs=include_dirs
        )

setup_args = dict(
  name = "pyhdl-if",
  version=version,
  packages=find_namespace_packages(where='src'),
  package_dir = {'' : 'src'},
  package_data = {
      'hdl_if': [
          'share/dpi/*',
          'share/uvm/*',
          'share/vpi/*',
          'share/*',
          'dfm/flow.dv'
#          "*pyhdl_if.*",
      ]
  },
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = ("Python interface for HDL programming interfaces"),
  long_description = """
  Provides a library interface for creating and evaluating ARL models at an API level
  """,
  license = "Apache 2.0",
  keywords = ["SystemVerilog", "Verilog", "VHDL", "RTL", "Python"],
  url = "https://github.com/fvutils/pyhdl-if",
  install_requires=[
  ],
  extras_require={
    'pytest' : [
        'pytest',
        'pytest-asyncio'
    ]
  },
  setup_requires=[
    'setuptools_scm',
    'cython',
    'ivpm',
    'pcpp',
    'cxxheaderparser'
  ],
  entry_points={
      'console_scripts': [
        'pyhdl-if = hdl_if.__main__:main'
      ],
      'ivpm.pkginfo': [
        'pyhdl-if = hdl_if.pkginfo:PkgInfo'
      ],
      'dv_flow.mgr': [
        'pyhdl-if = hdl_if.dfm.__ext__'
      ],
  },
  ext_modules=[ ext ]
)

if isSrcBuild:
    def gen_py_api(build):
        import sys
        import subprocess
        
        print("--> gen_py_api")
        cmd = [sys.executable, 
               os.path.join(proj_dir, "scripts", "gen_py_if.py")]
        
        res = subprocess.run(cmd, stderr=subprocess.STDOUT)

        if res.returncode != 0:
            raise Exception("Failed to run cmd %s" % str(cmd))

        print("<-- gen_py_api")

        print("--> gen_uvm_if")
#        cmd = [sys.executable, 
#               os.path.join(proj_dir, "scripts", "gen_via_if.py")]
        
#        res = subprocess.run(cmd, stderr=subprocess.STDOUT)

#        if res.returncode != 0:
#            raise Exception("Failed to run cmd %s" % str(cmd))

        print("<-- gen_uvm_if")

    setup_args["ivpm_hooks"] = {
        "setup.pre" : [
            gen_py_api
        ]
    }
    setup_args["ivpm_ext_name_m"] = {
        "hdl_if.entry" : "{dllpref}pyhdl_if{dllext}"
    }

setup(**setup_args)

