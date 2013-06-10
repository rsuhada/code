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
r500_pix=float("50.0")      # [pixel]
fitid='v06-joint-test-quick'
theta_pn="65.8443"                 # [arcsec]
theta_mos1="65.8443"                 # [arcsec]
theta_mos2="65.8443"                 # [arcsec]
energy="1.5"                # [keV]
MODEL="v06"
MAKE_CONTROL_PLOT=True
INSTRUMENT_SETUP="joint"       # "single" or "joint"
# instruments=("pn mos1 mos2") # any for individual, or "joint" "on" "mos1" etc.
instruments=("pn") # any for individual, or "joint" "on" "mos1" etc.

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
    ids = where(r<=r500_pix)
    r = r[ids]

    sb_src[instrument] = sb_src[instrument][ids]
    sb_bg[instrument] = sb_bg[instrument][ids]
    sb_src_err[instrument] = sb_src_err[instrument][ids]
    sb_bg_err[instrument] = sb_bg_err[instrument][ids]

    n = len(r)

    # create the control the plot
    if MAKE_CONTROL_PLOT=="True":
        outfig = sb_file[instrument]+'.'+fitid+'.png'
        print "Creating control plot :: ", instrument, outfig
        plot_sb_profile(r, sb_src[instrument], sb_src_err[instrument], sb_bg[instrument], sb_bg_err[instrument], outfig)


print "SB curves loaded!"
# reload(sb_utils)
rbin = optibingrid(binnum=20, rmax=1.5*r500_pix, c=1.5)[:3]

x=sb_src['pn']
x=arange(1, 6)
r=x

xb2 = histogram(x,bins=rbin,weights=x)[0]


for i in range(len(r)):
    print r[i], x[i]

print
print
# for i in xrange(len(rbin)):
for i in xrange(3):
    print rbin[i], xb[i], xb2[i]

print
print

# for i in xrange(len(r)):
# for i in xrange(4):
    # print r[i], x[i]



# 0.838525491562 0.0017056771
# 2.37170824513 0.0009961027
# 4.35710626448 0.0011220168
# 6.7082039325 0.0005805488




# 1.0 0.0004767233
# 2.0 0.0007265975
# 3.0 0.0005023563
# 4.0 0.0005278483
# 5.0 0.0004682544
# 6.0 0.0004167865
# 7.0 0.000398113
# 8.0 0.0003071173
# 9.0 0.0003214037
# 10.0 0.0002591451
