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
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#undef DEBUG_INIT

#ifdef DEBUG_INIT
#define DEBUG(fmt, ...) fprintf(stdout, fmt, ##__VA_ARGS__) ; fputs("\n", stdout); fflush(stdout)
#else
#define DEBUG(fmt, ...)
#endif

#ifdef __cplusplus
extern "C" {
#endif

typedef void *lib_h_t;
static int _python_initialized = 0;

static int init_python();

typedef void *PyObject;

/*******************************************************************
 * pyhdl_if_dpi_entry()
 * 
 * Manages start-up tasks for DPI integration
 *******************************************************************/
int pyhdl_if_dpi_entry() {
    PyObject *hdl_pi_if_pkg, *hdl_pi_if_init, *res;
    PyObject *null_args;
    DEBUG("entry.c");

    if (init_python() == -1) {
        DEBUG("pyhdl-pi-if: Failed to initialize Python");
        return -1;
    }

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
    DEBUG("entry.c");

    if (init_python() == -1) {
        DEBUG("pyhdl-pi-if: Failed to initialize Python");
        return -1;
    }

// TODO:
#ifdef UNDEFINED
    // Just in case...
    DEBUG("--> Py_Initialize");
    Py_Initialize();
    DEBUG("<-- Py_Initialize");

    hdl_pi_if_pkg = PyImport_ImportModule("hdl_pi_if");
    DEBUG("hdl_pi_if_pkg=%p", hdl_pi_if_pkg);
    hdl_pi_if_init = PyObject_GetAttrString(hdl_pi_if_pkg, "vpi_init");
    DEBUG("hdl_pi_if_init=%p", hdl_pi_if_init);
    null_args = PyTuple_New(0);
    res = PyObject_Call(hdl_pi_if_init, null_args, 0);
    DEBUG("res=%p", res);
#endif
}

/*******************************************************************
 * Default entry-point, as specified by Verilog LRM
 *******************************************************************/
void (*vlog_startup_routines[])() = {
    pyhdl_if_vpi_entry,
    0
};

static lib_h_t find_python_lib();

/*******************************************************************
 * init_python()
 * 
 * - Discover which library implements Python
 * - On Linux, ensure this library is reloaded with global visibility
 *******************************************************************/
int init_python() {
    if (!_python_initialized) {
        lib_h_t pylib = find_python_lib();

        if (!pylib) {
            return 0;
        }
        
        _python_initialized = 1;
    }

    return _python_initialized;
}

static lib_h_t find_loaded_python_lib();
static lib_h_t find_config_python_lib();
lib_h_t find_python_lib() {
    lib_h_t lib = 0;

    // First, check to see if the library is already loaded
    if (!(lib = find_loaded_python_lib())) {
        lib = find_config_python_lib();
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
lib_h_t find_loaded_python_lib() {
    lib_h_t ret = 0;
    pid_t pid = getpid();
    char mapfile_path[256];
    FILE *map_fp;

    DEBUG("find_python_lib(linux)");

    sprintf(mapfile_path, "/proc/%d/maps", pid);
    map_fp = fopen(mapfile_path, "r");

    DEBUG("map_fp: %p", map_fp);

    while (!ret && fgets(mapfile_path, sizeof(mapfile_path), map_fp)) {
        char *path_s = strdup(mapfile_path);
        char *path = path_s;
        char *idx;
        DEBUG("path_s: %s", path_s);

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
                    DEBUG("malloc %d", (strlen(path) + strlen(mapfile_path)+2));
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
                lib_h_t lib = dlopen(path, RTLD_LAZY);
                if (lib) {
                    void *sym = dlsym(lib, "Py_Initialize");
                    if (sym) {
                        DEBUG("Found ");
                        // Re-open the library in global model
                        lib = dlopen(path, RTLD_LAZY | RTLD_GLOBAL);
                        ret = lib;
                    }
                }
            }
        }
        free(path_s);
    }

    return ret;
}

#endif

#ifdef _WIN32
#else
lib_h_t find_config_python_lib() {
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

    args[0] = "python3";
    args[1] = "-m";
    args[2] = "sysconfig";
    args[3] = 0;

    pipe(cout_pipe);
    posix_spawn_file_actions_init(&action);
    posix_spawn_file_actions_addclose(&action, cout_pipe[0]);
    posix_spawn_file_actions_adddup2(&action, cout_pipe[1], 1);
    posix_spawn_file_actions_addclose(&action, cout_pipe[1]);

    if (posix_spawnp(&pid, args[0], &action, 0, (char *const *)&args[0], 0) != 0) {
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
                DEBUG("no eol: newlen=%d (%s)", &buf[sz]-bp, bp);
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
                    DEBUG("Realloc buffer %d -> %d", linebuf_max, newsz);
                    memcpy(tmp, linebuf, linebuf_len);
                    free(linebuf);
                    linebuf = tmp;
                    linebuf_max = newsz;
                }
                memcpy(&linebuf[linebuf_len], bp, newlen);
                linebuf_len += newlen;
                linebuf[linebuf_len] = 0;
                DEBUG("Total linebuf: (%s)", linebuf);
            }

            if (eol) {
                char *key_start = linebuf;
                char *key_end;
                char *val_start;
                char *val_end;

                DEBUG("Line: %s\n", linebuf);

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

    DEBUG("ldlibrary=%s libdest=%s", ldlibrary, libdest);

    if (ldlibrary && libdest) {
        char *fullpath = (char *)malloc(strlen(ldlibrary)+strlen(libdest)+2);
        strcpy(fullpath, libdest);
        strcat(fullpath, "/");
        strcat(fullpath, ldlibrary);

        // First, try full path
        if (!(ret = dlopen(fullpath, RTLD_LAZY+RTLD_GLOBAL))) {
            // Try again with just a relative path
            DEBUG("Failed to load library via full path %s", fullpath);
            if (!(ret = dlopen(ldlibrary, RTLD_LAZY+RTLD_GLOBAL))) {
                DEBUG("Failed to load library via relative path %s", ldlibrary);
            } else {
                DEBUG("Successfully loaded library via relative path %s", ldlibrary);
            }
        } else {
            DEBUG("Successfully loaded library via fullpath %s", fullpath);
        }
        free(fullpath);
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