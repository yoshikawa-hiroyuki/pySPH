#!/usr/bin/env python
from distutils.core import setup
setup(name="pySPH",
    version="0.2",
    description="Python interface for SPH file of Sphere framework",
    requires=["numpy", "pybind11"],
    author="YOSHIKAWA Hiroyuki, FUJITSU LTD.",
    author_email="yoh@fujitsu.com",
    packages=["pySPH"],
    )

