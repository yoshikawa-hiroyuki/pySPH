# pySPH
Python interface for SPH file of [Sphere](http://vcad-hpsv.riken.jp/jp/release_software/V-Sphere) framework.

## Install
```
  sudo python setup.py install
```
or
```
  python setup.py install --home=~ ...
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

## Author
  YOSHIKAWA Hiroyuki, FUJITSU LTD.

