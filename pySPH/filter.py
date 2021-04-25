#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPH_filter
"""

import sys, os
import numpy as np
import SPH

import json
import base64
import _pickle as pickle

class SPH_filter:

    @staticmethod
    def extractScalar(d: SPH.SPH, dataIdx: int) -> SPH.SPH:
        ''' extractScalar
        ベクトルデータを持つSPHからスカラーのSPHを生成する(static method)

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

    @staticmethod
    def vectorMag(d: SPH.SPH) -> SPH.SPH:
        ''' vectorMag
        ベクトルデータを持つSPHからベクトルのノルムをスカラーとして持つSPHを
        生成する(static method)

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

    @staticmethod
    def vectorCurl(d: SPH.SPH) -> SPH.SPH:
        ''' vectorCurl
        ベクトルデータを持つSPHからベクトルの回転をベクトルとして持つSPHを
        生成する(static method)

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
    
    @staticmethod
    def divideShareEdge(d: SPH.SPH, div: []) -> []:
        ''' divideShareEdge
        SPHデータについて、隣接格子点を共有した分割を行う(static method)
        格子サイズが5の次元を2分割する場合、分割されたデータの格子サイズは
        (3, 3)になる.
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
    
    @staticmethod
    def toJSON(d: SPH.SPH) -> str:
        ''' toJSON
        SPHデータについて、base64でエンコードしてJSON化する(static method)

        Parameters
        ----------
        d: SPH.SPH
          JSON化するSPHデータ

        Returns
        -------
        str: 文字列化したJSONデータ
        '''
        jd = {
            'type': 'sph',
            'data': base64.b64encode(pickle.dumps(d)).decode('utf-8'),
            }
        str_data = json.dumps(jd)
        return str_data

    @staticmethod
    def fromJSON(sd: str) -> SPH.SPH:
        ''' fromJSON
        base64エンコードでJSON化されたSPHデータを復元する(static method)

        Parameters
        ----------
        sd: str
          文字列化したJSONデータ

        Returns
        -------
        SPH.SPH: 復元されたSPHデータ
        '''
        jd = json.loads(sd)
        d = base64.b64decode(jd['data'].encode())
        sph = pickle.loads(d)
        return sph
    
