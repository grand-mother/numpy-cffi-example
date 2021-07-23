from setuptools import setup

setup(name='grand',
      version='0.1',
      description='Demonstration package using cffi',
      author='Valentin Niess',
      packages=['grand'],
      setup_requires=['cffi>=1.0.0'],
      cffi_modules=['grand/grand_build.py:ffi'],
      install_requires=['cffi>=1.0.0']
)
