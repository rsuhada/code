#!/usr/bin/env python
import sys
import os
import math
from numpy import *
import re

def parse_xspec_err_log(f, parid):
    """
    Parses an Xspec output log giving back parameter and its error
    bars.

    Arguments:
    - `f`: opend file
    - `parid`: name of the parameter [luminosity]
    """
    regexpdict = {
        'luminosity': '#Model Luminosity .*(0.50000 - 2.0000 keV rest frame)'
        }

    searchExp=regexpdict[parid]
    searchReal=r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"

    bufferline=''               # search has to work one line ahead

    val = []
    val_err_lo = []
    val_err_hi = []

    for line in f:
        if re.search(searchExp, bufferline):
            # print
            # print bufferline
            # print line

            x = re.findall(searchReal, bufferline)
            val.append(float(x[0]))

            x = re.findall(searchReal, line)
            val_err_lo.append(float(x[0]))
            val_err_hi.append(float(x[1]))

        bufferline = line

    return (val, val_err_lo, val_err_hi)


def parse_xspec_log(f, parid):
    """
    Parses an Xspec output log giving back parameter (no error)
    bars.

    Arguments:
    - `f`: opend file
    - `parid`: name of the parameter [luminosity]
    """
    regexpdict = {
        'luminosity': '#Model Luminosity .*(0.50000 - 2.0000 keV rest frame)'
        }

    searchExp=regexpdict[parid]
    searchReal=r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"

    val = []

    for line in f:
        if re.search(searchExp, line):
            # print
            # print line
            x = re.findall(searchReal, line)
            val.append(float(x[0]))

    return val


if __name__ == '__main__':
    print
    # intab = '/Users/rs/w/xspt/data/SPT-CL-J2137-6307/spec/001/SPT-CL-J2137-6307-001-fx-lx-err.log'
    intab = '/Users/rs/w/xspt/data/SPT-CL-J0205-5829/spec/012/SPT-CL-J0205-5829-012-fx-lx-err.log'

    paramater="luminosity"
    f = open(intab, "r")

    # get the error bars
    (lx_abs, lx_abs_err_lo, lx_abs_err_hi) = parse_xspec_err_log(f, paramater)

    lx_abs = array(lx_abs)
    lx_abs_err_lo = array(lx_abs_err_lo)
    lx_abs_err_hi = array(lx_abs_err_hi)

    print lx_abs
    print lx_abs_err_lo
    print lx_abs_err_hi

    # get the unabsorbed luminosity
    # intab2 = '/Users/rs/w/xspt/data/SPT-CL-J2137-6307/spec/001/SPT-CL-J2137-6307-001-fx-lx.log'
    intab2 = '/Users/rs/w/xspt/data/SPT-CL-J0205-5829/spec/012/SPT-CL-J0205-5829-012-fx-lx.log'
    f = open(intab2, "r")
    lx = array(parse_xspec_log(f, paramater))
    print lx

    correction = lx - lx_abs
    lx_err_lo = lx_abs_err_lo + correction - lx
    lx_err_hi = lx_abs_err_hi + correction - lx

    print
    print lx
    print lx_err_lo
    print lx_err_hi

    print lx_abs[0], lx[0], lx_err_lo[0], lx_err_hi[0], lx_abs[1], lx[1], lx_err_lo[1], lx_err_hi[1], lx_abs[2], lx[2], lx_err_lo[2], lx_err_hi[2]

    print "Done!"

