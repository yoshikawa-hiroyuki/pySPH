#!/usr/bin/env python
import os, sys
from setuptools import Extension, setup

import pybind11
include_dirs = [pybind11.get_include()]
library_dirs = []

ex_module = Extension(
    'pySPH.filter.filter_exmod',
    sources=['pySPH/filter/filter_exmod.cpp'],
    libraries=[],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    extra_compile_args=['-std=c++14', '-fPIC'],
)

setup(name="pySPH",
      version="0.2",
      description="Python interface for SPH file of Sphere framework",
      requires=["numpy", "pybind11"],
      author="YOSHIKAWA Hiroyuki, FUJITSU LTD.",
      author_email="yoh@fujitsu.com",
      packages=["pySPH", "pySPH.filter"],
      ext_modules=[ex_module]
    )

