import sys
import os
import math
from numpy import *
from pylab import rc
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, LogLocator
from sb_plotting_utils import plot_sb_profile, plot_cts_profile


def load_sb_curve(fname):
    """
    Loads the surface brightness curve from file.

    Arguments:
    - `fname`: file name
    """

    dat=loadtxt(fname, dtype='string', comments='#', delimiter=None, converters=None,
            skiprows=0, unpack=False,
            usecols=(0,1,2,4,5)
            )

    r = double(dat[:,0])
    sb_src = double(dat[:,1])
    sb_bg = double(dat[:,2])
    sb_src_err = double(dat[:,3])
    sb_bg_err = double(dat[:,4])

    return r, sb_src, sb_bg, sb_src_err, sb_bg_err


def sanitize_sb_curve(sb_curve_tuple):
    """
    Clean the curves by removing bins with negative values.

    Arguments: sb_curve_tuple containing:
    - `r`:
    - `sb_src`:
    - `sb_bg`:
    - `sb_src_err`:
    - `sb_bg_err`:
    """
    (r, sb_src, sb_bg, sb_src_err, sb_bg_err) = sb_curve_tuple

    # non-0 and non-NaN
    ids1 = where(sb_src>0.0)
    ids2 = where(negative(isnan(sb_src)))

    ids = unique(hstack((ids1, ids2)))

    r = r[ids]
    sb_src = sb_src[ids]
    sb_bg = sb_bg[ids]
    sb_src_err = sb_src_err[ids]
    sb_bg_err = sb_bg_err[ids]

    return (r, sb_src, sb_bg, sb_src_err, sb_bg_err)




if __name__ == '__main__':
    print

    reload(sb_plotting_utils)

    ######################################################################
    # settings
    fname = '/Users/rs/w/xspt/data/dev/0559/sb/sb-prof-pn-003.dat'
    outfig = fname+'.dev.png'

    r_500_proj_ang = 153.0   # projected radius [arcsec]

    ######################################################################
    # loading the data
    # (r, sb_src, sb_bg, sb_src_err, sb_bg_err) = sanitize_sb_curve(load_sb_curve(fname))
    (r, sb_src, sb_bg, sb_src_err, sb_bg_err) = load_sb_curve(fname)

    ids = where(r<=r_500_proj_ang)

    r = r[ids]
    sb_src = sb_src[ids]
    sb_bg = sb_bg[ids]
    sb_src_err = sb_src_err[ids]
    sb_bg_err = sb_bg_err[ids]


    ######################################################################
    # control plot
    plot_sb_profile(r, sb_src, sb_src_err, sb_bg, sb_bg_err, outfig)
    os.system("open "+outfig)




    print "done!"


