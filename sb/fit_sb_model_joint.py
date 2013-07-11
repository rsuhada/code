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
from sb_utils import distance_matrix
from sb_models import beta_psf_2d_lmfit_profile, v06_psf_2d_lmfit_profile
import lmfit as lm
import time
import asciitable as atab
import pickle
from sb_fitting_utils import *

plt.close('all')

fitid              = sys.argv[1]
MODEL              = sys.argv[2]
MAKE_CONTROL_PLOT  = sys.argv[3]
rsbfit             = double(sys.argv[4])
rsbexc             = double(sys.argv[5])
energy             = double(sys.argv[6])
prof_fname_pn      = sys.argv[7]
theta_pn           = double(sys.argv[8]) / 60.0
prof_fname_mos1    = sys.argv[9]
theta_mos1         = double(sys.argv[10]) / 60.0
prof_fname_mos2    = sys.argv[11]
theta_mos2         = double(sys.argv[12]) / 60.0
INSTRUMENT_SETUP   = sys.argv[13]
instruments        = sys.argv[14].split()

######################################################################
# input parameters

print '-'*70
print "fitid             :: ", fitid
print "MODEL             :: ", MODEL
print "INSTRUMENT_SETUP  :: ", INSTRUMENT_SETUP
print "MAKE_CONTROL_PLOT :: ", MAKE_CONTROL_PLOT
print "rsbfit            :: ", rsbfit
print "rsbexc            :: ", rsbexc
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
for instrument in instruments:
    print "Loading SB data for :: ", instrument

    (r,
     sb_src[instrument],
     sb_bg[instrument],
     sb_src_err[instrument],
     sb_bg_err[instrument]
     ) = sanitize_sb_curve(load_sb_curve(sb_file[instrument]))

    # take only the profile inside r500

    # with binning this is probably rudimentary - because cutting
    # should happen before binning (i.e. the curve read here should be
    # already *exactly* what you want to fit including binning)
    ids = where(logical_and(r<=rsbfit, r>rsbexc))
    r = r[ids]

    print r
    print "going to sleep!"
    from time import sleep
    sleep(1000)


    sb_src[instrument] = sb_src[instrument][ids]
    sb_bg[instrument] = sb_bg[instrument][ids]
    sb_src_err[instrument] = sb_src_err[instrument][ids]
    sb_bg_err[instrument] = sb_bg_err[instrument][ids]

    n = len(r)

    # create the control the plot
    if MAKE_CONTROL_PLOT=="True":
        outfig = sb_file[instrument]+'.'+fitid+'.png'
        print "Creating control plot :: ", instrument, outfig
        plot_sb_profile(r, sb_src[instrument], sb_src_err[instrument],
                        sb_bg[instrument], sb_bg_err[instrument],
                        outfig)

print "SB curves loaded!"

######################################################################
# do the actual fitting

outpickle = sb_file[instruments[0]]+'.'+fitid+'.pk'
outpickle = outpickle.replace(instruments[0], 'joint')

if MODEL=="beta":
    fit_beta_model_joint(r, sb_src, sb_src_err, instruments, theta, energy, outpickle)

if MODEL=="v06":
    fit_v06_model_joint(r, sb_src, sb_src_err, instruments, theta, energy, outpickle)

print "done!"

