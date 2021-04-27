#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPH JSON filter
"""

import sys, os
import numpy as np
from .. import SPH

import json
import base64
import _pickle as pickle

def toJSON(d: SPH.SPH) -> str:
    ''' toJSON
    SPHデータについて、base64でエンコードしてJSON化する

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

def fromJSON(sd: str) -> SPH.SPH:
    ''' fromJSON
    base64エンコードでJSON化されたSPHデータを復元する

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
