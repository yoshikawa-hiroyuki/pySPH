#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPH File representation for Sphere framework
"""
import sys
import struct
import numpy


class SPH:
    (DT_SINGLE, DT_DOUBLE) = (1, 2)
    def __init__(self):
        self._dims = [0, 0, 0]
        self._org = [0.0, 0.0, 0.0]
        self._pitch = [0.0, 0.0, 0.0]
        self._dtype = SPH.DT_SINGLE
        self._veclen = 1
        self._time = 0.0
        self._step = 0
        self._min = {0.0}
        self._max = {0.0}
        self._data = None
        self._path = None
        return

    def load(self, path):
        self._data = None
        self._path = None

        # open file
        try:
            ifp = open(path, "rb")
        except:
            print "open failed: %s" % path
            return False

        # type record
        bo = '<'
        header = ifp.read(16)
        buff = struct.unpack(bo+'iiii', header)
        svType = buff[1]
        dType = buff[2]
        if ( svType == 1 ):
            self._veclen = 1
        elif ( svType == 2 ):
            self._veclen = 3
        else:
            bo = '>'
            buff = struct.unpack(bo+'iiii', header)
            svType = buff[1]
            dType = buff[2]
            if ( svType == 1 ):
                self._veclen = 1
            elif ( svType == 2 ):
                self._veclen = 3
            else:
                ifp.close()
                return False

        if ( dType == 1 ):
            self._dtype = SPH.DT_SINGLE
        elif ( dType == 2 ):
            self._dtype = SPH.DT_DOUBLE
        else:
            ifp.close()
            return False

        # size record
        if ( dType == 1 ):
            buff = struct.unpack(bo+'iiiii', ifp.read(20))
            self._dims = (buff[1], buff[2], buff[3])
        elif ( dType == 2 ):
            buff = struct.unpack(bo+'i', ifp.read(4))
            buff = struct.unpack(bo+'qqq', ifp.read(24))
            self._dims = (buff[0], buff[1], buff[2])
            buff = struct.unpack(bo+'i', ifp.read(4))

        # org record
        if ( dType == 1 ):
            buff = struct.unpack(bo+'ifffi', ifp.read(20))
            self._org = (buff[1], buff[2], buff[3])
        elif ( dType == 2 ):
            buff = struct.unpack(bo+'i', ifp.read(4))
            buff = struct.unpack(bo+'ddd', ifp.read(24))
            self._org = (buff[0], buff[1], buff[2])
            buff = struct.unpack(bo+'i', ifp.read(4))

        # pitch record
        if ( dType == 1 ):
            buff = struct.unpack(bo+'ifffi', ifp.read(20))
            self._pitch = (buff[1], buff[2], buff[3])
        elif ( dType == 2 ):
            buff = struct.unpack(bo+'i', ifp.read(4))
            buff = struct.unpack(bo+'ddd', ifp.read(24))
            self._pitch = (buff[0], buff[1], buff[2])
            buff = struct.unpack(bo+'i', ifp.read(4))

        # time record
        if ( dType == 1 ):
            buff = struct.unpack(bo+'iifi', ifp.read(16))
            self._step = buff[1]
            self._time = buff[2]
        elif ( dType == 2 ):
            buff = struct.unpack(bo+'i', ifp.read(4))
            buff = struct.unpack(bo+'qd', ifp.read(16))
            self._step = buff[0]
            self._time = buff[1]
            buff = struct.unpack(bo+'i', ifp.read(4))

        # skip data sz
        ifp.read(4)

        dimSz = self._dims[0] * self._dims[1] * self._dims[2]
        if ( svType == 1 ):
            self._min = [0.0,]
            self._max = [0.0,]
            if ( dType == 1 ):
                packStr = 'f'
                dlen = 4
                self._data = numpy.array(0, dtype=numpy.float32)
            else:
                packStr = 'd'
                dlen = 8
                self._data = numpy.array(0, dtype=numpy.float64)
        else:
            self._min = [0.0, 0.0, 0.0]
            self._max = [0.0, 0.0, 0.0]
            if ( dType == 1 ):
                packStr = 'fff'
                dlen = 12
                self._data = numpy.array(0, dtype=numpy.float32)
            else:
                packStr = 'ddd'
                dlen = 24
                self._data = numpy.array(0, dtype=numpy.float64)
        self._data.resize(dimSz*self._veclen)

        # read the first data
        vals = struct.unpack(bo+packStr, ifp.read(dlen))
        for l in range(0, self._veclen):
            self._data[l] = vals[l]
            self._min[l] = vals[l]
            self._max[l] = vals[l]

        # read datas folowing
        for i in range(1, dimSz):
            vals = struct.unpack(bo+packStr, ifp.read(dlen))
            for l in range(0, self._veclen):
                self._data[i*self._veclen + l] = vals[l]
                if ( self._min[l] > vals[l] ):
                    self._min[l] = vals[l]
                elif ( self._max[l] < vals[l] ):
                    self._max[l] = vals[l]

        # done
        ifp.close()
        self._path = path
        return True

    def save(self, path =None):
        if self._data == None: return False
        xpath = path
        if xpath == None: xpath = self._path
        if xpath == None: return False

        # open output file
        try:
            ofp = open(xpath, "wb")
        except:
            print "open failed: %s" % xpath
            return False

        # attr record
        buff = [8, 1, 1, 8]
        if self._veclen == 3: buff[1] = 2
        if self._dtype == SPH.DT_DOUBLE: buff[2] = 2
        ofp.write(struct.pack('4i', buff[0], buff[1], buff[2], buff[3]))

        # size record
        if self._dtype == SPH.DT_DOUBLE:
            ofp.write(struct.pack('i3qi', 24, self._dims[0], self._dims[1],
                                  self._dims[2], 24))
        else:
            ofp.write(struct.pack('5i', 12, self._dims[0], self._dims[1],
                                  self._dims[2], 12))

        # org record
        if self._dtype == SPH.DT_DOUBLE:
            ofp.write(struct.pack('i3di', 24, self._org[0], self._org[1],
                                  self._org[2], 24))
        else:
            ofp.write(struct.pack('i3fi', 12, self._org[0], self._org[1],
                                  self._org[2], 12))

        # pitch record
        if self._dtype == SPH.DT_DOUBLE:
            ofp.write(struct.pack('i3di', 24, self._pitch[0], self._pitch[1],
                                  self._pitch[2], 24))
        else:
            ofp.write(struct.pack('i3fi', 12, self._pitch[0], self._pitch[1],
                                  self._pitch[2], 12))

        # time record
        if self._dtype == SPH.DT_DOUBLE:
            ofp.write(struct.pack('iqdi', 16, self._step, self._time, 16))
        else:
            ofp.write(struct.pack('iifi', 8, self._step, self._time, 8))

        # data record
        dimSz = self._dims[0] * self._dims[1] * self._dims[2]
        dimVX = self._veclen * self._dims[0]
        k = 0
        if self._dtype == SPH.DT_DOUBLE:
            dfmt = '%dd' % dimVX
            ofp.write(struct.pack('i', dimSz*self._veclen*8))
            for i in range(self._dims[2]):
                for j in range(self._dims[1]):
                    ofp.write(struct.pack(dfmt, *self._data[k:k+dimVX]))
                    k = k + dimVX
                    continue # end of for(j)
                continue # end of for(i)
            ofp.write(struct.pack('i', dimSz*self._veclen*8))
        else:
            dfmt = '%df' % dimVX
            ofp.write(struct.pack('i', dimSz*self._veclen*4))
            for i in range(self._dims[2]):
                for j in range(self._dims[1]):
                    ofp.write(struct.pack(dfmt, *self._data[k:k+dimVX]))
                    k = k + dimVX
                    continue # end of for(j)
                continue # end of for(i)
            ofp.write(struct.pack('i', dimSz*self._veclen*4))

        ofp.close()
        self._path = xpath
        return True
