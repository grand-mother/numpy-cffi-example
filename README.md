# Demo package for grand using numpy+cffi

This is a demonstration of using numpy and cffi in order to build a grand Python
package on top of existing C libaries. For the purpose of this demonstration
we condider the case of [`grand.coordinates`](grand/coordinates.py).

Coordinates objects are created by [subclassing
numpy.ndarray](https://numpy.org/doc/stable/user/basics.subclassing.html#). The
[TURTLE](https://niess.github.io/turtle-pages/) C library is used for
transforms between different coordinates systems.

In order to be efficient the CPU time spent at interfaces between Python and C
must be minimal. In numpy this is achieved by vectorizing operations.  Instead
of repeating Python calls on each element of a collection a single Python call
is made on a `numpy.ndarray`. The looping over the array elements is done at the
C level, not at the Python one. However, the TURTLE library functions are not
natively vectorized.  Yet, this is simple to achieve by providing
straightforward C wrappers. Examples of those are located in
[vectorization.h](grand/c/include/vectorization.h) and
[vectorization.c](grand/c/src/vectorization.c).


# Installation

_The compilation requires to clone the present repository as well as
[TURTLE](https://github.com/niess/turtle) ones. The latter is expected to be
cloned under `share/turtle` in the local copy of the present repository._

The demonstration `grand` package can be compiled from the repository by using
the provided [Makefile](Makefile). This generates `libgrand.abi3.so`. Note that
the latter is a standard dynamic library that can be linked to C applications as
well.

The compilation is done with `cffi`. This is taken care by the
[grand_build.py](grand/grand_build.py) script. A local installation of
`grand.libgrand` is done with `setuptools`, see e.g. [setup.py](setup.py).
Note that this procedure should allow to generate binary wheels of the grand
package as well for distributing over PyPI, though this was not yet tested.


# Usage

An example of usage is provided as
[examples/coordinates.py](examples/coordinates.py). Note that you might need to
export the repository path to your `PYTHONPATH` in order to locate the `grand`
package.
