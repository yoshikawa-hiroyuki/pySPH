#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPH divide filter
"""

import sys, os
import numpy as np
from .. import SPH

def divideShareEdge(d: SPH.SPH, div: []) -> []:
    ''' divideShareEdge
    SPHデータについて、隣接格子点を共有した分割を行う
    格子サイズが5の次元を2分割する場合、分割されたデータの格子サイズは(3, 3)になる.
    分割されたデータの格子サイズは1以上でならなければならない.

    Parameters
    ----------
    d: SPH.SPH
      分割するSPHデータ
    div: int[3]
      各軸方向の分割数(>0)

    Returns
    -------
    SPH.SPH[]: 分割されたSPHデータのリスト、空のリスト=失敗
    '''
    sb_lst = []
    if d._veclen < 1:
        return sb_lst
    if div[0] < 1 or div[1] < 1 or div[2] < 1:
        return sb_lst
    sbDim = [int(d._dims[i] / div[i]) + (1 if div[i] != 1 else 0) \
             for i in range(3)]
    if sbDim[0] < 1 or sbDim[1] < 1 or sbDim[2] < 1:
        return sb_lst
    sbDimE = [d._dims[i] - (sbDim[i] -1) * (div[i] - 1) for i in range(3)]
    if sbDimE[0] < 1 or sbDimE[1] < 1 or sbDimE[2] < 1:
        return sb_lst

    newOrg = list(d._org)
    newOrgIdx = [0, 0, 0]
    newDims = [0, 0, 0]
    for k in range(div[2]):
        newOrg[1] = d._org[1]
        newOrgIdx[1] = 0
        newDims[2] = sbDimE[2] if k == div[2] -1 else sbDim[2]

        for j in range(div[1]):
            newOrg[0] = d._org[0]
            newOrgIdx[0] = 0
            newDims[1] = sbDimE[1] if j == div[1] -1 else sbDim[1]

            for i in range(div[0]):
                newDims[0] = sbDimE[0] if i == div[0] -1 else sbDim[0]

                sph = SPH.SPH()
                sph._dims[:] = newDims[:]
                sph._org[:] = newOrg[:]
                sph._pitch[:] = d._pitch[:]
                sph._veclen = d._veclen
                sph._step = d._step
                sph._time = d._time
                sph._dtype = d._dtype
                sph._min = list(d._min)
                sph._max = list(d._max)
                if d._dtype == SPH.SPH.DT_DOUBLE:
                    sph._data = np.array(0, dtype=np.float64)
                else:
                    sph._data = np.array(0, dtype=np.float32)
                dimSz = sph._dims[0]*sph._dims[1]*sph._dims[2]*d._veclen
                sph._data.resize(dimSz)

                for kk in range(newDims[2]):
                    for jj in range(newDims[1]):
                        sst_idx = d._dims[0]*d._dims[1]*(kk+newOrgIdx[2]) \
                            + d._dims[0]*(jj+newOrgIdx[1]) + newOrgIdx[0]
                        sst_idx = sst_idx * d._veclen
                        sed_idx = sst_idx + newDims[0] * d._veclen

                        dst_idx = sph._dims[0]*sph._dims[1]*kk \
                                  + sph._dims[0]*jj
                        dst_idx = dst_idx * d._veclen
                        ded_idx = dst_idx + newDims[0] * d._veclen

                        sph._data[dst_idx:ded_idx] \
                            = d._data[sst_idx:sed_idx]
                        continue # jj
                    continue # kk
                sb_lst.append(sph)

                newOrg[0] += d._pitch[0] * (newDims[0] - 1)
                newOrgIdx[0] += (newDims[0] - 1)
                continue # i

            newOrg[1] += d._pitch[1] * (newDims[1] - 1)
            newOrgIdx[1] += (newDims[1] - 1)
            continue # j

        newOrg[2] += d._pitch[2] * (newDims[2] - 1)
        newOrgIdx[2] += (newDims[2] - 1)
        continue # k

    return sb_lst
