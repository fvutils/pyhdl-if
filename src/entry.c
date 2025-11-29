/****************************************************************************
 * entry.c
 *
 * Copyright 2023 Matthew Ballance and Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may 
 * not use this file except in compliance with the License.  
 * You may obtain a copy of the License at:
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software 
 * distributed under the License is distributed on an "AS IS" BASIS, 
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
 * See the License for the specific language governing permissions and 
 * limitations under the License.
 *
 * Created on:
 *     Author: 
 *
 * Handles Python- and simulator-integration start-up tasks for pyhdl-if
 ****************************************************************************/
#if defined(_WIN32)
#include <windows.h>
#else
#include <ctype.h>
#include <dlfcn.h>
#include <poll.h>
#include <spawn.h>
#include <sys/wait.h>
#endif
#include <sys/types.h>
#include <sys/stat.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define DEBUG_INIT
#define DEBUG_PREF "PyHDL-IF: "

#ifdef DEBUG_INIT
#define DEBUG(fmt, ...) if (prv_debug) {fprintf(stdout, fmt, ##__VA_ARGS__) ; fputs("\n", stdout); fflush(stdout); }
#define DEBUG_LEVEL(level, fmt, ...) if (prv_debug >= level) {fprintf(stdout, fmt, ##__VA_ARGS__) ; fputs("\n", stdout); fflush(stdout); }
#else
#define DEBUG(fmt, ...)
#define DEBUG_LEVEL(level, fmt, ...)
#endif

static int prv_debug = 0;
typedef void *lib_h_t;
static lib_h_t find_loaded_lib(const char *sym);
static lib_h_t find_python_lib(const char *python);
static lib_h_t check_lib(const char *path, const char *sym);

#include "py_api_if.h"
#include "py_dpi_if.h"
#include "py_vpi_if.h"

#ifdef __cplusplus
extern "C" {
#endif

static lib_h_t _python_lib = 0;
static lib_h_t init_python(const char *python);

/**
 * The following ensures that this DPI library has a dependency
 * on DPI-exported symbols. This ensures that Python is able
 * to find the exports
 */
int pyhdl_pi_if_RegisterTimeCB();
int pyhdl_call_if_invoke_hdl_f(void);
int pyhdl_call_if_invoke_hdl_t(void);
int pyhdl_call_if_response_py_t(void);

void *funcs[] = {
    &pyhdl_pi_if_RegisterTimeCB,
    &pyhdl_call_if_invoke_hdl_f,
    &pyhdl_call_if_invoke_hdl_t,
    &pyhdl_call_if_response_py_t,
};

void *get_dpiexport_funcs() {
    return funcs;
}

//typedef void *PyObject;

/*******************************************************************
 * pyhdl_if_dpi_entry()
 * 
 * Manages start-up tasks for DPI integration
 *******************************************************************/
int pyhdl_if_dpi_entry(int debug, const char *python) {
    lib_h_t pylib;

    prv_debug = debug;

    if (getenv("PYHDL_IF_DEBUG") && getenv("PYHDL_IF_DEBUG")[0] == '1') {
        prv_debug = 1;
    }

    DEBUG("entry.c");

    if (!(pylib=init_python(python))) {
        DEBUG("pyhdl-if: Failed to initialize Python");
        return -1;
    }

    if (!py_load_api_struct(pylib)) {
        DEBUG("pyhdl-if: Failed to load Python API");
        return -1;
    }

    DEBUG("pyhdl-if: Successfully initialized native portion of DPI");
    return 1;
}

/*******************************************************************
 * pyhdl_if_vpi_entry()
 * 
 * Manages start-up tasks for VPI integration
 *******************************************************************/
void pyhdl_if_vpi_entry() {
    PyObject *hdl_pi_if_pkg, *hdl_pi_if_init, *res;
    PyObject *null_args;
    lib_h_t pylib, vpilib;

    (void)res;

    if (getenv("PYHDL_IF_DEBUG") && getenv("PYHDL_IF_DEBUG")[0] == '1') {
        prv_debug = 1;
    }

    DEBUG("entry.c");

    if (!(pylib=init_python(""))) {
        DEBUG("pyhdl-pi-if: Failed to initialize Python");
        return;
    }

    if (!py_load_api_struct(pylib)) {
        DEBUG("pyhdl-if: Failed to load Python API");
        return;
    }

    if (!(vpilib=find_loaded_lib("vpi_iterate"))) {
        fprintf(stdout, "PyHDL-IF Error: failed to load VPI symbols\n");
        fflush(stdout);
        DEBUG("pyhdl-if: Failed to load VPI symbols");
        return;
    }

    DEBUG("vpillib: %p", vpilib);

    if (!vpi_load_api_struct(vpilib)) {
        DEBUG("pyhdl-if: Failed to load VPI API\n");
        return;
    }

    // Just in case...
    DEBUG("--> Py_Initialize");
    prv_py_api.Py_Initialize();
    DEBUG("<-- Py_Initialize");

    hdl_pi_if_pkg = prv_py_api.PyImport_ImportModule("hdl_if.impl.vpi");
    DEBUG("hdl_pi_if_pkg=%p", hdl_pi_if_pkg);

    if (!hdl_pi_if_pkg) {
        fprintf(stdout, "PyHDL-IF Error: failed to import Python package hdl_if.impl.vpi\n");
        prv_py_api.PyErr_Print();
        fflush(stdout);
        return;
    }

    hdl_pi_if_init = prv_py_api.PyObject_GetAttrString(hdl_pi_if_pkg, "vpi_init");
    DEBUG("hdl_pi_if_init=%p", hdl_pi_if_init);
    if (!hdl_pi_if_init) {
        fprintf(stdout, "PyHDL-IF Error: failed to locate vpi_init in Python package hdl_if.impl.vpi\n");
        prv_py_api.PyErr_Print();
        fflush(stdout);
        return;
    }
    null_args = prv_py_api.PyTuple_New(0);
    res = prv_py_api.PyObject_Call(hdl_pi_if_init, null_args, 0);
    DEBUG("res=%p", res);

    vpi_register_python_tf();
}

/*******************************************************************
 * Default entry-point, as specified by Verilog LRM
 *******************************************************************/
void (*vlog_startup_routines[])() = {
    pyhdl_if_vpi_entry,
    0
};


/*******************************************************************
 * init_python()
 * 
 * - Discover which library implements Python
 * - On Linux, ensure this library is reloaded with global visibility
 *******************************************************************/
lib_h_t init_python(const char *python) {
    if (!_python_lib) {
        _python_lib = find_python_lib(python);
    }

    return _python_lib;
}

static lib_h_t find_config_python_lib(const char *python);
lib_h_t find_python_lib(const char *python) {
    lib_h_t lib = 0;

    if (getenv("LIBPYTHON_LOC") && getenv("LIBPYTHON_LOC")[0]) {
        const char *path = getenv("LIBPYTHON_LOC");
        DEBUG("Trying to load Python from %s", path);
        fprintf(stdout, "PyHDL-IF Note: Loading Python library from user-specified path: %s\n", path);
        lib = check_lib(path, "Py_Initialize");

        if (!lib) {
            fprintf(stdout, "PyHDL-IF Error: failed to load Python library from user-secified path: %s\n", path);
            fflush(stdout);
        }
    }

    // First, check to see if the library is already loaded
    if (!lib) {
        lib = find_loaded_lib("Py_Initialize");
    }

    if (!lib) {
        lib = find_config_python_lib(python);
    }

    return lib;
}

#if defined(_WIN32)
lib_h_t find_loaded_python_lib() {
    fprintf(stdout, "TODO: implement find_python_lib for Windows\n");
    fflush(stdout);
    return -1;
}
#elif defined(_DARWIN)
lib_h_t find_loaded_python_lib(lib_h_t *lib_h) {

}
#else // Linux
lib_h_t find_loaded_lib(const char *sym) {
    lib_h_t ret = 0;
    pid_t pid = getpid();
    char mapfile_path[256];
    FILE *map_fp;

    DEBUG("--> find_loaded_lib(linux) %s", sym);

    // First, try loading the executable
    {
        DEBUG("Try finding symbol \"%s\" in the executable", sym);
        ret = dlopen(0, RTLD_LAZY);
        if (dlsym(ret, sym)) {
            DEBUG("returning %p", ret);
            return ret;
        } else {
            DEBUG("didn't find symbol \"%s\" in the executable", sym);
            ret = 0;
        }
    }

    sprintf(mapfile_path, "/proc/%d/maps", pid);
    map_fp = fopen(mapfile_path, "r");

    DEBUG("map_fp: %p", map_fp);

    while (!ret && fgets(mapfile_path, sizeof(mapfile_path), map_fp)) {
        char *path_s = strdup(mapfile_path);
        char *path = path_s;
        char *idx;
        DEBUG_LEVEL(3, "path_s: %s", path_s);

        if ((idx=strchr(path, '/'))) {
            path = idx;
            int32_t eidx = strlen(path)-1;

            while (isspace(path[eidx])) {
                path[eidx--] = 0;
            }

            struct stat statbuf;
            if (stat(path, &statbuf) == -1) {
                // File doesn't exist. Read another line to complete the path
                if (fgets(mapfile_path, sizeof(mapfile_path), map_fp)) {
                    char *tpath;
                    DEBUG_LEVEL(3, "malloc %lld", (unsigned long long)(strlen(path) + strlen(mapfile_path)+2));
                    tpath = (char *)malloc(strlen(path) + strlen(mapfile_path) + 2);

                    strcpy(tpath, path);
                    strcat(tpath, mapfile_path);

                    free(path_s);
                    path = tpath;
                    path_s = tpath;

                    int32_t eidx = strlen(path)-1;
                    while (isspace(path[eidx])) {
                        path[eidx--] = 0;
                    }
                }
            }

            DEBUG("Final path: %s", path);

            if (strstr(path, ".so")) {
                // Check to see if this is a Python library
                ret = check_lib(path, sym);
            }
        }
        free(path_s);
    }

    DEBUG("<-- find_loaded_lib(linux) %s %p", sym, ret);

    return ret;
}

lib_h_t check_lib(const char *path, const char *sym) {
    lib_h_t ret = 0;
    DEBUG("--> check_lib(%s, %s)", path, sym);
    lib_h_t lib = dlopen(path, RTLD_LAZY);
    if (lib) {
        void *sym_h = dlsym(lib, sym);
        if (sym_h) {
            DEBUG("Found ");
            // Re-open the library in global model
            lib = dlopen(path, RTLD_LAZY | RTLD_GLOBAL);
            ret = lib;
        }
    }
    DEBUG("<-- check_lib(%s, %s) %p", path, sym, ret);
    return ret;
}

#endif

char *clean_env(const char *name, const char *omit) {
    const char *value = getenv(name);
    char *new_value;
    const char *cp, *cpn;
    int first_entry = 1;

    if (!value || !value[0]) {
        return 0;
    }

    cp = value;

    new_value = (char *)malloc(strlen(name)+strlen(value)+2);
    strcpy(new_value, name);
    strcat(new_value, "=");

    while (cp && *cp) {
        cpn = strchr(cp, ':');
        if (!cpn) {
            cpn = cp + strlen(cp);
       }
                    
       // Check if this path starts with pythonhome
       if (strncmp(cp, omit, strlen(omit)) != 0) {
            if (!first_entry) {
                strcat(new_value, ":");
            }
            strncat(new_value, cp, cpn - cp);
            first_entry = 0;
        }
                    
        if (*cpn == ':') {
            cp = cpn + 1;
        } else {
            cp = NULL;
        }
    }

    return new_value;
}

#ifdef _WIN32
#else
lib_h_t find_config_python_lib(const char *python) {
    lib_h_t ret = 0;
    int cout_pipe[2];
    posix_spawn_file_actions_t action;
    pid_t pid;
    int exit_code, sz;
    const char **args = (const char **)malloc(sizeof(char *)*4);
    char buf[1024];
    char *linebuf = 0;
    int32_t linebuf_len = 0, linebuf_max = 0;
    char *ldlibrary = 0;
    char *libdest = 0;
    char *libdir = 0;
    extern char **environ;

    if (getenv("PYHDL_IF_PYTHON") && getenv("PYHDL_IF_PYTHON")[0]) {
        python = getenv("PYHDL_IF_PYTHON");
        fprintf(stdout, "PyHDL-IF Note: Using Python interpreter \"%s\", specified by $PYHDL_IF_PYTHON\n",
            python);
        fflush(stdout);
    }

    if (python && python[0]) {
        const char *pythonhome = getenv("PYTHONHOME");
        if (pythonhome && pythonhome[0]) {
//            const char *pythonpath = getenv("PYTHONPATH");
//            const char *ldlibrarypath = getenv("LD_LIBRARY_PATH");
//            const char *path = getenv("PATH");

            fprintf(stdout, "PyHDL-IF Note: Clearing PYTHONHOME and cleaning PYTHONPATH\n");
            fflush(stdout);

            {
                char *new_pythonpath = clean_env("PYTHONPATH", pythonhome);
                if (new_pythonpath) {
                    fprintf(stdout, "PyHDL-IF Note: Setting PYTHONPATH to \"%s\"\n", new_pythonpath);
                    putenv(new_pythonpath);
                }
            }
            {
                char *new_ldlibrarypath = clean_env("LD_LIBRARY_PATH", pythonhome);
                if (new_ldlibrarypath) {
                    fprintf(stdout, "PyHDL-IF Note: Setting LD_LIBRARY_PATH to \"%s\"\n", new_ldlibrarypath);
                    putenv(new_ldlibrarypath);
                }
            }

            {
                char *new_path = clean_env("PATH", pythonhome);
                if (new_path) {
                    fprintf(stdout, "PyHDL-IF Note: Setting PATH to \"%s\"\n", new_path);
                    putenv(new_path);
                }
            }

            putenv(strdup("PYTHON="));
            putenv(strdup("PYTHONHOME="));
        }

        // Now, add the new Python interpreter to the PATH
        {
            char *python_dir = strdup(python);
            char *slash = strrchr(python_dir, '/');
            char *new_path;
            if (slash) {
                *slash = 0; // Remove the filename
            }

            DEBUG("Python directory: %s", python_dir);
            new_path = (char *)malloc(strlen(python_dir)+strlen(getenv("PATH"))+16);
            strcpy(new_path, "PATH=");
            strcat(new_path, python_dir);
            strcat(new_path, ":");
            strcat(new_path, getenv("PATH"));
            DEBUG("New PATH: %s", new_path);
            putenv(new_path);
            free(python_dir);
        }

    } else {
        // Default to whatever is in the path
        python = "python3";
    }

    args[0] = python;
    args[1] = "-m";
    args[2] = "sysconfig";
    args[3] = 0;
    
    {
        int i;
        extern char **environ;
        const char *ld_library_path = getenv("LD_LIBRARY_PATH");
        DEBUG("LD_LIBRARY_PATH: %s", ld_library_path?ld_library_path:"null");

        if (prv_debug >= 2) {
            for (i=0; environ[i]; i++) {
                DEBUG("environ[%d]: %s", i, environ[i]);
            }
        }

    }

    (void)pipe(cout_pipe);
    posix_spawn_file_actions_init(&action);
    posix_spawn_file_actions_addclose(&action, cout_pipe[0]);
    posix_spawn_file_actions_adddup2(&action, cout_pipe[1], 1);
    posix_spawn_file_actions_addclose(&action, cout_pipe[1]);

    if (posix_spawnp(&pid, args[0], &action, 0, (char *const *)&args[0], environ) != 0) {
        fprintf(stderr, "Fatal Error: failed to run Python\n");
        return 0;
    }

    close(cout_pipe[1]);

    // Now, read data from the pipe
    while ((sz=read(cout_pipe[0], buf, sizeof(buf)-1)) > 0) {
        char *bp = buf;
        buf[sz] = 0;

        while (bp) {
            int32_t newlen;
            char *eol = strchr(bp, '\n');

            if (eol) {
                newlen = (eol-bp); // exclude the '\n'
            } else {
                newlen = (&buf[sz]-bp);
                DEBUG_LEVEL(3, "no eol: newlen=%d (%s)", (int)(&buf[sz]-bp), bp);
            }

            // Append to buffer
            if (!linebuf) {
                linebuf = (char *)malloc(newlen+1);
                linebuf_len = newlen+1;
                linebuf_max = newlen+1;
                memcpy(linebuf, bp, newlen);
                linebuf[newlen] = 0;
            } else {
                // Have existing content
                if (linebuf_len+newlen >= linebuf_max) {
                    // Realloc the buffer
                    int32_t newsz = ((2*linebuf_max)>linebuf_len+newlen)?(2*linebuf_max):linebuf_len+newlen+1;
                    char *tmp = (char *)malloc(newsz);
                    DEBUG_LEVEL(3, "Realloc buffer %d -> %d", linebuf_max, newsz);
                    memcpy(tmp, linebuf, linebuf_len);
                    free(linebuf);
                    linebuf = tmp;
                    linebuf_max = newsz;
                }
                memcpy(&linebuf[linebuf_len], bp, newlen);
                linebuf_len += newlen;
                linebuf[linebuf_len] = 0;
                DEBUG_LEVEL(3, "Total linebuf: (%s)", linebuf);
            }

            if (eol) {
                char *key_start = linebuf;
                char *key_end;
                char *val_start;
                char *val_end;

                DEBUG_LEVEL(3, "Line: %s\n", linebuf);

                while (isspace(*key_start)) {
                    key_start++;
                }
                key_end = strchr(key_start, '=');
                if (key_end) {
                    val_start = key_end+3;
                    key_end--;
                    *key_end = 0;

                    val_end = strchr(val_start, '"');
                    *val_end = 0;

                    if (val_end) {
                        if (!strcmp(key_start, "LDLIBRARY")) {
                            ldlibrary = strdup(val_start);
                        } else if (!strcmp(key_start, "LIBDEST")) {
                            libdest = strdup(val_start);
                        } else if (!strcmp(key_start, "LIBDIR")) {
                            libdir = strdup(val_start);
                        }
                    }
                }
                linebuf_len = 0;
                bp = eol+1;
            } else {
                bp = 0;
            }
        }
    }

    waitpid(pid, &exit_code, 0);

    if (exit_code != 0) {
        fprintf(stderr, "Fatal Error: Python return code is %d\n", exit_code);
        return 0;
    }

    DEBUG("ldlibrary=%s libdest=%s libdir=%s", ldlibrary, libdest, libdir);

    if (ldlibrary && libdir) {
        char *libname = (char *)malloc(strlen(ldlibrary)+16);
        char *a_ptr;
        char *fullpath = (char *)malloc(strlen(ldlibrary)+strlen(libdir)+strlen(libdest)+4);
        strcpy(fullpath, libdest);
        strcat(fullpath, "/");

        strcpy(libname, ldlibrary);
        if ((a_ptr=strstr(libname, ".a"))) {
            // Sometimes Python is built statically, but still has a shared library
            DEBUG("Python appears to be built statically (lib=%s)", ldlibrary);
            strcpy(libname, ldlibrary);
            strcpy(a_ptr, ".so");
            DEBUG("Trying to load %s instead", libname);
        }
        strcat(fullpath, libname);

        // First, try full path
        if ((ret = dlopen(fullpath, RTLD_LAZY+RTLD_GLOBAL))) {
            DEBUG("Successfully loaded via fullpath(1) %s", fullpath);
        } else if (strcpy(fullpath, libdir) && strcat(fullpath, "/") && strcat(fullpath, libname) &&
            (ret=dlopen(fullpath, RTLD_LAZY+RTLD_GLOBAL))) {
            DEBUG("Successfully loaded via fullpath(2) %s", fullpath);
        } else if ((ret=dlopen(libname, RTLD_LAZY+RTLD_GLOBAL))) {
            DEBUG("Successfully loaded library via relative path %s", libname);
        } else {
            DEBUG("Faied to load library");
        }
        DEBUG("PYTHONPATH: %s", getenv("PYTHONPATH")?getenv("PYTHONPATH"):"null");
        free(fullpath);
        free(libname);
    }
    
    if (linebuf) {
        free(linebuf);
    }
    if (ldlibrary) {
        free(ldlibrary);
    }
    if (libdest) {
        free(libdest);
    }

    return ret;
}
#endif

#ifdef __cplusplus
}
#endif
