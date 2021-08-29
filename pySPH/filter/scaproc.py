#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPH scalar process filter
"""

import sys, os
import numpy as np
from .. import SPH
from . import filter_exmod

def asUchar(d: SPH.SPH, minMax:[]=None) -> np.ndarray:
    ''' asUchar
    minMaxで指定された値域を(0~255)に正規化して、dtype=uint8のnumpy配列に変換する

    Parameters
    ----------
    d: SPH.SPH
      vectorデータを持つSPHデータ
    minMax: [min, max]
      値域: Noneの場合はdの最小値・最大値で正規化する

    Returns
    -------
    np.ndarray: dtype=uint8のNumpy配列
    '''
    if d._veclen != 1:
        return None

    d_range = minMax
    if not d_range:
        d_range = [d._data.min(), d._data.max()]
    else:
        if not d_range[0]:
            d_range[0] = d._data.min()
        if not d_range[0]:
            d_range[1] = d._data.max()
    deno = d_range[1] - d_range[0]
    if deno <= 0.0:
        return None

    dsz = d._dims[2]* d._dims[1]* d._dims[0]
    if dsz < 1:
        return None
    ucd = np.array([0], dtype='uint8')
    ucd = np.resize(ucd, (dsz))

    for i in range(dsz):
        ucd[i] = 255 * (d._data[i] - d_range[0]) / deno
        continue # end of for(i)

    ucd = np.reshape(ucd, [d._dims[2], d._dims[1], d._dims[0]])
    return ucd


