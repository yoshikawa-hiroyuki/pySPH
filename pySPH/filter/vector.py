#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPH vector filter
"""

import sys, os
import numpy as np
from .. import SPH
from . import filter_exmod

def extractScalar(d: SPH.SPH, dataIdx: int) -> SPH.SPH:
    ''' extractScalar
    ベクトルデータを持つSPHからスカラーのSPHを生成する

    Parameters
    ----------
    d: SPH.SPH
      vectorデータを持つSPHデータ
    dataIdx: int
      抽出するスカラーデータのインデックス番号

    Returns
    -------
    SPH.SPH: 抽出したスカラーのSPHデータ、None: 失敗
    '''
    if d._veclen < 1:
        return None
    if dataIdx < 0 or dataIdx >= d._veclen:
        return None

    sph = SPH.SPH()
    sph._dims[:] = d._dims[:]
    sph._org[:] = d._org[:]
    sph._pitch[:] = d._pitch[:]
    sph._veclen = 1
    sph._step = d._step
    sph._time = d._time
    if d._dtype == SPH.SPH.DT_DOUBLE:
        sph._dtype = SPH.SPH.DT_DOUBLE
        sph._data = np.array(0, dtype=np.float64)
    else:
        sph._dtype = SPH.SPH.DT_SINGLE
        sph._data = np.array(0, dtype=np.float32)
    dimSz = sph._dims[0] * sph._dims[1] * sph._dims[2]
    if dimSz < 1:
        return None
    sph._data.resize(dimSz)

    val = d._data[dataIdx]
    sph._min = [val]
    sph._max = [val]
    for i in range(dimSz):
        val  = d._data[i*sph._datalen + dataIdx]
        sph._data[i] = val
        if val < sph._min[0]: sph._min[0] = val
        if val > sph._max[0]: sph._max[0] = val
        continue # end of for(i)
    return sph

def vectorMag(d: SPH.SPH) -> SPH.SPH:
    ''' vectorMag
    ベクトルデータを持つSPHからベクトルのノルムをスカラーとして持つSPHを生成する

    Parameters
    ----------
    d: SPH.SPH
      vectorデータを持つSPHデータ

    Returns
    -------
    SPH.SPH: ベクトルノルムのスカラーSPHデータ、None: 失敗
    '''
    if d._veclen < 1:
        return None

    sph = SPH.SPH()
    sph._dims[:] = d._dims[:]
    sph._org[:] = d._org[:]
    sph._pitch[:] = d._pitch[:]
    sph._veclen = 1
    sph._step = d._step
    sph._time = d._time
    if d._dtype == SPH.SPH.DT_DOUBLE:
        sph._dtype = SPH.SPH.DT_DOUBLE
        sph._data = np.array(0, dtype=np.float64)
    else:
        sph._dtype = SPH.SPH.DT_SINGLE
        sph._data = np.array(0, dtype=np.float32)
    dimSz = sph._dims[0] * sph._dims[1] * sph._dims[2]
    if dimSz < 1:
        return None
    sph._data.resize(dimSz)

    vl = np.linalg.norm(d._data[0:d._veclen], ord=2)
    sph._min = [vl]
    sph._max = [vl]
    for i in range(dimSz):
        idx = i * d._veclen
        vl = np.linalg.norm(d._data[idx:idx+d._veclen], ord=2)
        sph._data[i] = vl
        if vl < sph._min[0]: sph._min[0] = vl
        if vl > sph._max[0]: sph._max[0] = vl
        continue # end of for(i)
    return sph

def vectorCurl(d: SPH.SPH) -> SPH.SPH:
    ''' vectorCurl
    ベクトルデータを持つSPHからベクトルの回転をベクトルとして持つSPHを生成する
    (C++で実装)

    Parameters
    ----------
    d: SPH.SPH
      vectorデータを持つSPHデータ

    Returns
    -------
    SPH.SPH: ベクトルの回転場のSPHデータ、None: 失敗
    '''
    if not d._veclen == 3:
        return None
    sph = SPH.SPH()
    sph._dims[:] = d._dims[:]
    sph._org[:] = d._org[:]
    sph._pitch[:] = d._pitch[:]
    sph._veclen = d._veclen
    sph._step = d._step
    sph._time = d._time
    if d._dtype == SPH.SPH.DT_DOUBLE:
        sph._dtype = SPH.SPH.DT_DOUBLE
        sph._data = np.array(0, dtype=np.float64)
    else:
        sph._dtype = SPH.SPH.DT_SINGLE
        sph._data = np.array(0, dtype=np.float32)
    dimSz = sph._dims[0] * sph._dims[1] * sph._dims[2]
    if dimSz < 8:
        return None

    dd = d._data.reshape([sph._dims[2], sph._dims[1], sph._dims[0], 3])
    td = filter_exmod.calc_curl(dd, sph._pitch[0],sph._pitch[1],sph._pitch[2])
    sph._data = td.ravel()

    sph._min = sph._data[[l for l in range(sph._veclen)]]
    sph._max = sph._data[[l for l in range(sph._veclen)]]
    for i in range(1, dimSz):
        for l in range(0, sph._veclen):
            vals = sph._data[[i*sph._veclen+l for l in range(sph._veclen)]]
            if ( sph._min[l] > vals[l] ):
                sph._min[l] = vals[l]
            elif ( sph._max[l] < vals[l] ):
                sph._max[l] = vals[l]
            continue # end of for(l)
        continue # end of for(i)
    return sph        
    
def vectorCurlPy(d: SPH.SPH) -> SPH.SPH:
    ''' vectorCurlPy
    ベクトルデータを持つSPHからベクトルの回転をベクトルとして持つSPHを生成する
    (Pythonで実装)

    Parameters
    ----------
    d: SPH.SPH
      vectorデータを持つSPHデータ

    Returns
    -------
    SPH.SPH: ベクトルの回転場のSPHデータ、None: 失敗
    '''
    if not d._veclen == 3:
        return None

    sph = SPH.SPH()
    sph._dims[:] = d._dims[:]
    sph._org[:] = d._org[:]
    sph._pitch[:] = d._pitch[:]
    sph._veclen = d._veclen
    sph._step = d._step
    sph._time = d._time
    if d._dtype == SPH.SPH.DT_DOUBLE:
        sph._dtype = SPH.SPH.DT_DOUBLE
        sph._data = np.array(0, dtype=np.float64)
    else:
        sph._dtype = SPH.SPH.DT_SINGLE
        sph._data = np.array(0, dtype=np.float32)
    dimSz = sph._dims[0] * sph._dims[1] * sph._dims[2]
    if dimSz < 8:
        return None
    sph._data.resize(dimSz * sph._veclen)

    dim = sph._dims
    dd = d._data
    td = sph._data
    for k in range(sph._dims[2]):
        for j in range(sph._dims[1]):
            for i in range(sph._dims[0]):
                if i == 0:
                    dvdx = (dd[(dim[0]*dim[1]*k +dim[0]*j +i+1)*3 +1] - \
                            dd[(dim[0]*dim[1]*k +dim[0]*j +i)*3 +1]) / \
                            sph._pitch[0]
                    dwdx = (dd[(dim[0]*dim[1]*k +dim[0]*j +i+1)*3 +2] - \
                            dd[(dim[0]*dim[1]*k +dim[0]*j +i)*3 +2]) / \
                            sph._pitch[0]
                elif i == dim[0] - 1:
                    dvdx = (dd[(dim[0]*dim[1]*k +dim[0]*j +i)*3 +1] - \
                            dd[(dim[0]*dim[1]*k +dim[0]*j +i-1)*3 +1]) / \
                            sph._pitch[0]
                    dwdx = (dd[(dim[0]*dim[1]*k +dim[0]*j +i)*3 +2] - \
                            dd[(dim[0]*dim[1]*k +dim[0]*j +i-1)*3 +2]) / \
                            sph._pitch[0]
                else:
                    dvdx = (dd[(dim[0]*dim[1]*k +dim[0]*j +i+1)*3 +1] - \
                            dd[(dim[0]*dim[1]*k +dim[0]*j +i-1)*3 +1]) / \
                            (sph._pitch[0] * 2)
                    dwdx = (dd[(dim[0]*dim[1]*k +dim[0]*j +i+1)*3 +2] - \
                            dd[(dim[0]*dim[1]*k +dim[0]*j +i-1)*3 +2]) / \
                            (sph._pitch[0] * 2)
                if j == 0:
                    dudy = (dd[(dim[0]*dim[1]*k +dim[0]*(j+1) +i)*3] - \
                            dd[(dim[0]*dim[1]*k +dim[0]*j +i)*3]) / \
                            sph._pitch[1]
                    dwdy = (dd[(dim[0]*dim[1]*k +dim[0]*(j+1) +i)*3 +2] - \
                            dd[(dim[0]*dim[1]*k +dim[0]*j +i)*3 +2]) / \
                            sph._pitch[1]
                elif j == dim[1] - 1:
                    dudy = (dd[(dim[0]*dim[1]*k +dim[0]*j +i)*3] - \
                            dd[(dim[0]*dim[1]*k +dim[0]*(j-1) +i)*3]) / \
                            sph._pitch[1]
                    dwdy = (dd[(dim[0]*dim[1]*k +dim[0]*j +i)*3 +2] - \
                            dd[(dim[0]*dim[1]*k +dim[0]*(j-1) +i)*3 +2]) / \
                            sph._pitch[1]
                else:
                    dudy = (dd[(dim[0]*dim[1]*k +dim[0]*(j+1) +i)*3] - \
                            dd[(dim[0]*dim[1]*k +dim[0]*(j-1) +i)*3]) / \
                            (sph._pitch[1] * 2)
                    dwdy = (dd[(dim[0]*dim[1]*k +dim[0]*(j+1) +i)*3 +2] - \
                            dd[(dim[0]*dim[1]*k +dim[0]*(j-1) +i)*3 +2]) / \
                            (sph._pitch[1] * 2)
                if k == 0:
                    dudz = (dd[(dim[0]*dim[1]*(k+1) +dim[0]*j +i)*3] - \
                            dd[(dim[0]*dim[1]*k +dim[0]*j +i)*3]) / \
                            sph._pitch[2]
                    dvdz = (dd[(dim[0]*dim[1]*(k+1) +dim[0]*j +i)*3 +1] - \
                            dd[(dim[0]*dim[1]*k +dim[0]*j +i)*3 +1]) / \
                            sph._pitch[2]
                elif k == dim[2] - 1:
                    dudz = (dd[(dim[0]*dim[1]*k +dim[0]*j +i)*3] - \
                            dd[(dim[0]*dim[1]*(k-1) +dim[0]*j +i)*3]) / \
                            sph._pitch[2]
                    dvdz = (dd[(dim[0]*dim[1]*k +dim[0]*j +i)*3 +1] - \
                            dd[(dim[0]*dim[1]*(k-1) +dim[0]*j +i)*3 +1]) / \
                            sph._pitch[2]
                else:
                    dudz = (dd[(dim[0]*dim[1]*(k+1) +dim[0]*j +i)*3] - \
                            dd[(dim[0]*dim[1]*(k-1) +dim[0]*j +i)*3]) / \
                            (sph._pitch[2] * 2)
                    dvdz = (dd[(dim[0]*dim[1]*(k+1) +dim[0]*j +i)*3 +1] - \
                            dd[(dim[0]*dim[1]*(k-1) +dim[0]*j +i)*3 +1]) / \
                            (sph._pitch[2] * 2)
                td[(dim[0]*dim[1]*k + dim[0]*j + i)*3   ] = dwdy - dvdz
                td[(dim[0]*dim[1]*k + dim[0]*j + i)*3 +1] = dudz - dwdx
                td[(dim[0]*dim[1]*k + dim[0]*j + i)*3 +2] = dvdx - dudy
                continue # end of for(i)
            continue # end of for(j)
        continue # end of for(i)

    sph._min = sph._data[[l for l in range(sph._veclen)]]
    sph._max = sph._data[[l for l in range(sph._veclen)]]
    for i in range(1, dimSz):
        for l in range(0, sph._veclen):
            vals = sph._data[[i*sph._veclen+l for l in range(sph._veclen)]]
            if ( sph._min[l] > vals[l] ):
                sph._min[l] = vals[l]
            elif ( sph._max[l] < vals[l] ):
                sph._max[l] = vals[l]
            continue # end of for(l)
        continue # end of for(i)
    return sph        
