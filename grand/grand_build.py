from cffi import FFI
import io
import os
from pathlib import Path
from pcpp.preprocessor import Preprocessor
import re


GRAND_DIR  = Path('grand/c')
TURTLE_DIR = Path('share/turtle')

'''
Public includes exported to Python
'''
INCLUDES = (
    GRAND_DIR / 'include/vectorization.h',
    TURTLE_DIR / 'include/turtle.h',
)

'''
Extra search paths for the compiler.

Since the build is done in a temporary dir and since the C source(s) might be
located out of the Python package these paths need to be specified explicitly.
'''
INCLUDE_DIRS = (
    GRAND_DIR / 'include',
    TURTLE_DIR / 'include',
    TURTLE_DIR / 'src',
    TURTLE_DIR / 'src/deps',
    TURTLE_DIR / 'src/turtle'
)

'''
Source C files compiled for libgrand
'''
SOURCES = (
    # grand specific C sources
    GRAND_DIR / 'src/vectorization.c',

    # The TURTLE library
    TURTLE_DIR / 'src/deps/jsmn.c',
    TURTLE_DIR / 'src/deps/tinydir.c',
    TURTLE_DIR / 'src/turtle/client.c',
    TURTLE_DIR / 'src/turtle/error.c',
    TURTLE_DIR / 'src/turtle/list.c',
    TURTLE_DIR / 'src/turtle/projection.c',
    TURTLE_DIR / 'src/turtle/stepper.c',
    TURTLE_DIR / 'src/turtle/ecef.c',
    TURTLE_DIR / 'src/turtle/io.c',
    TURTLE_DIR / 'src/turtle/io/asc.c',
    TURTLE_DIR / 'src/turtle/io/geotiff16.c',
    TURTLE_DIR / 'src/turtle/io/grd.c',
    TURTLE_DIR / 'src/turtle/io/hgt.c',
    TURTLE_DIR / 'src/turtle/io/png16.c',
    TURTLE_DIR / 'src/turtle/map.c',
    TURTLE_DIR / 'src/turtle/stack.c'
)



def load_headers(*paths):
    '''
    Load the given header file(s) and prune them with a C preprocessor.
    '''
    headers = []
    for path in paths:
        with open(path) as f:
            header_content = f.read()

        # Remove includes (not supported)
        header_content = re.sub('#\s*include\s*["<](.+?)[>"]', '',
            header_content)

        cpp = Preprocessor()
        cpp.parse(header_content)
        output = io.StringIO()
        cpp.write(output)

        headers.append(output.getvalue())
    return os.linesep.join(headers)


def generate_source(*paths):
    '''
    Generate the source code for the cffi API wrapper.

    This code simply #include's the public include files listed in INCLUDES.
    The source files listed in SOURCES are compiled separately.
    '''
    lines = []
    for path in paths:
        prefix, suffix = str(path).split('include/')
        lines.append(f'#include "{suffix}"')

    return os.linesep.join(lines)


ffi = FFI()
ffi.set_source('grand.libgrand', generate_source(*INCLUDES),
    sources=[str(v) for v in SOURCES],
    include_dirs=[str(v) for v in INCLUDE_DIRS],
    extra_compile_args=['-std=c99']
)
ffi.cdef(load_headers(*INCLUDES))


if __name__ == '__main__':
    ffi.compile(verbose=True)
