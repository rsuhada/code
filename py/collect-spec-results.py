#!/usr/bin/env python
import sys
import os
import math
from numpy import *
import re

def parse_xspec_log(f, parid):
    """
    Parses an Xspec output log giving back parameter and its error
    bars.

    Arguments:
    - `f`: opend file
    - `parid`: name of the parameter [luminosity]
    """

    # FIXME: at some point move to a dictionary
    if parid == "luminosity":
        searchExp='#Model Luminosity .*(0.50000 - 2.0000 keV rest frame)'

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



if __name__ == '__main__':
    intab = '/Users/rs/w/xspt/data/SPT-CL-J2137-6307/spec/001/SPT-CL-J2137-6307-001-fx-lx-err.log'
    paramater="luminosity"

    f = open(intab, "r")
    (lx_abs, lx_abs_err_lo, lx_abs_err_hi) = parse_xspec_log(f, paramater)

    lx_abs = array(lx_abs)
    lx_abs_err_lo = array(lx_abs_err_lo)
    lx_abs_err_hi = array(lx_abs_err_hi)

    print lx_abs
    print lx_abs_err_lo
    print lx_abs_err_hi



    print "Done!"
