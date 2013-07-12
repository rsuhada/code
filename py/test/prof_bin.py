import sys
import os
import math
from numpy import *
from pylab import rc
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, LogLocator
from sb_plotting_utils import plot_sb_profile, plot_cts_profile, plot_data_model_simple, plot_data_model_resid
from esaspi_utils import *
# from sb_utils import distance_matrix, optibingrid
from sb_utils import *
from sb_models import beta_psf_2d_lmfit_profile, v06_psf_2d_lmfit_profile
import lmfit as lm
import time
import asciitable as atab
import pickle
from sb_fitting_utils import *

# 0559
cluster='SPT-CL-J0559-5249'
profile_id='003'
r500_pix=float("60.0")      # [pixel]
fitid='binning_test'
theta_pn="65.8443"                 # [arcsec]
theta_mos1="65.8443"                 # [arcsec]
theta_mos2="65.8443"                 # [arcsec]
energy="1.5"                # [keV]
MODEL="v06"
MAKE_CONTROL_PLOT=False
INSTRUMENT_SETUP="joint"       # "single" or "joint"
# instruments=("pn mos1 mos2") # any for individual, or "joint" "on" "mos1" etc.
instruments=("pn") # any for individual, or "joint" "on" "mos1" etc.
# instruments=("")

# Profile name
prof_fname_pn="/Users/rs/w/xspt/data/dev/0559/sb/"+cluster+"/sb-prof-pn-"+profile_id+".dat"
prof_fname_mos1="/Users/rs/w/xspt/data/dev/0559/sb/"+cluster+"/sb-prof-mos1-"+profile_id+".dat"
prof_fname_mos2="/Users/rs/w/xspt/data/dev/0559/sb/"+cluster+"/sb-prof-mos2-"+profile_id+".dat"

######################################################################
# input parameters

print '-'*70
print "fitid             :: ", fitid
print "MODEL             :: ", MODEL
print "INSTRUMENT_SETUP  :: ", INSTRUMENT_SETUP
print "MAKE_CONTROL_PLOT :: ", MAKE_CONTROL_PLOT
print "r500_pix          :: ", r500_pix
print "energy            :: ", energy
print "prof_fname_pn     :: ", prof_fname_pn
print "theta_pn          :: ", theta_pn
print "prof_fname_mos1   :: ", prof_fname_mos1
print "theta_mos1        :: ", theta_mos1
print "prof_fname_mos2   :: ", prof_fname_mos2
print "theta_mos2        :: ", theta_mos2
print "instruments       :: ", instruments
print '-'*70

######################################################################
# prepare structures

# dictionary for file names
sb_file = {
    'pn'   : prof_fname_pn,
    'mos1' : prof_fname_mos1,
    'mos2' : prof_fname_mos2
    }

theta = {
    'pn'   : theta_pn,
    'mos1' : theta_mos1,
    'mos2' : theta_mos2
    }

# dictionary for the data
sb_src = {}
sb_bg = {}
sb_src_err = {}
sb_bg_err = {}

######################################################################
# load the data
for instrument in instruments.split():
    print "Loading SB data for :: ", instrument

    (r,
     sb_src[instrument],
     sb_bg[instrument],
     sb_src_err[instrument],
     sb_bg_err[instrument]
     ) = sanitize_sb_curve(load_sb_curve(sb_file[instrument]))

    # take only the profile inside r500
    ids = where(r<=1.5*r500_pix)
    r = r[ids]

    sb_src[instrument] = sb_src[instrument][ids]
    sb_bg[instrument] = sb_bg[instrument][ids]
    sb_src_err[instrument] = sb_src_err[instrument][ids]
    sb_bg_err[instrument] = sb_bg_err[instrument][ids]

    n = len(r)

    # create the control the plot
    if MAKE_CONTROL_PLOT:
        outfig = sb_file[instrument]+'.'+fitid+'.png'
        print "Creating control plot :: ", instrument, outfig
        plot_sb_profile(r, sb_src[instrument], sb_src_err[instrument], sb_bg[instrument], sb_bg_err[instrument], outfig)


######################################################################
#
# toy test
#
######################################################################

rbin = optibingrid(binnum=20, rmax=1.5*r500_pix, c=1.5)

# give the bin midpoint and symmetric range ("errorbar on r")
mid = [(rbin2[i] + rbin2[i+1])/2.0 for i in range(len(rbin2)-1)]
mid_range = rbin2[1:] - mid

# r = arange(0, 1.5*r500_pix)
# x = ones(len(r))
x = sb_src['pn'][:len(r)]
x_err = sb_src_err['pn'][:len(r)]

min_dist = 1.0    # [pix]

# merge innermost bins if they are too small
# rbin contains: start-end=start-end bin boundaries
rbin=hstack((0.0, rbin[rbin>=min_dist]))
xb = histogram(r, bins=rbin, weights=x)[0]
xb_err = histogram(r, bins=rbin, weights=x_err)[0]
num = histogram(r, bins=rbin)[0]

print len(r)
print len(x)
print len(rbin)
print len(xb)
print
print "profile unbined :: ", x
print "r unbinned      :: ", r
print "bin boundaries  :: ", rbin
print "profile binned  :: ", xb
print "bin counts  :: ", num
print

plt.ion()
plot_sb_profile(r, sb_src[instrument], sb_src_err[instrument], sb_bg[instrument], sb_bg_err[instrument], outfig)

# plt.plot(rbin[1:], xb/num,
plt.errorbar(mid, xb/num, xb_err/num, mid_range,
    color='red',
    linestyle='',              # -/--/:/-.
    linewidth=1,                # linewidth=1
    marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
    markerfacecolor='red',
    markersize=8,               # markersize=6
    label=r"data"               # '__nolegend__'
    )

plt.xscale('log', nonposx='clip')
plt.xlim(xmin=mid[0])
plt.show()

