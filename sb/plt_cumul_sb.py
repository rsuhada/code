import sys
import math
from numpy import *
from pylab import rc
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, LogLocator
from sb_plotting_utils import plot_sb_profile, plot_cts_profile

if len(sys.argv) < 2:
    print >> sys.stderr,  "** Error: missing file nam for the cumulative surface brightness profile!"
    sys.exit(1)

fname = sys.argv[1]

dat=loadtxt(fname, dtype='string', comments='#', delimiter=None, converters=None,
            skiprows=0, unpack=False,
            usecols=(0,1,2,4,5)
            )

r = double(dat[:,0])
cumul_sb_src = double(dat[:,1])
cumul_sb_bg = double(dat[:,2])
cumul_sb_src_err = double(dat[:,3])
cumul_sb_bg_err = double(dat[:,4])

# plot_sb_profile(r, cumul_sb_src, cumul_sb_src_err, cumul_sb_bg, cumul_sb_bg_err, fname+'.png')
plot_cts_profile(r, cumul_sb_src, cumul_sb_bg, fname+'.png')
