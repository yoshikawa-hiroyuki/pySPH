# pySPH
Python interface for SPH file of [Sphere](http://vcad-hpsv.riken.jp/jp/release_software/V-Sphere) framework.

## Requires
- numpy
- pybind11
- wheel
- setuptools
- scikit-image (for isosurf)

## Install
```
pip3 install .
```

## Usage

### Load/Save sph file
```
from pySPH import SPH
sph = SPH.SPH()
sph.load('mydata.sph')
sph.save('mydata2.sph', dtype=SPH.SPH.DT_DOUBLE)
```

### Load/Save FORTRAN unformatted file
```
from pySPH import SPH
sph = SPH.SPH()
sph.loadFromFort('fort.10', dims=(128, 64, 256), veclen=1, dtype=SPH.SPH.DT_DOUBLE)
sph.saveToFort('fort.11', dtype=SPH.SPH.DT_SINGLE)
```

### Use filter module
```
from pySPH.filter import *
# generate scalar SPH data from vector SPH data
sph1 = vecproc.extractScalar(sph3, 0)
```

## Author
YOSHIKAWA Hiroyuki, FUJITSU LTD.

