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


if __name__ == '__main__':
    plt.close('all')

    fitid              = sys.argv[1]
    MODEL              = sys.argv[2]
    MAKE_CONTROL_PLOT  = sys.argv[3]
    r500_proj_ang      = double(sys.argv[4])
    energy             = double(sys.argv[5])
    prof_fname_pn      = sys.argv[6]
    theta_pn           = double(sys.argv[7])
    prof_fname_mos1    = sys.argv[8]
    theta_mos1         = double(sys.argv[9])
    prof_fname_mos2    = sys.argv[10]
    theta_mos2         = double(sys.argv[11])
    INSTRUMENT_SETUP   = sys.argv[12]
    instruments        = sys.argv[13].split()

    ######################################################################
    # input parameters

    print '-'*70
    print "fitid             :: ", fitid
    print "MODEL             :: ", MODEL
    print "INSTRUMENT_SETUP  :: ", INSTRUMENT_SETUP
    print "MAKE_CONTROL_PLOT :: ", MAKE_CONTROL_PLOT
    print "r500_proj_ang     :: ", r500_proj_ang
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
    # load sb profile

    # dictionary for file names
    sb_file_dict = {
        'pn': prof_fname_pn,
        'mos1': prof_fnamm_mos1,
        'mos2': prof_fname_mos2
        }

    # dictionary for the data

    sb_data_dict = {}

    sb_src_pn, sb_bg_pn, sb_src_pn_err, sb_bg_pn_err

    for instrument in instruments:

        (r, sb_src_pn, sb_bg_pn, sb_src_pn_err, sb_bg_pn_err) = sanitize_sb_curve(load_sb_curve(prof_fname_pn))
    (r, sb_src_mos1, sb_bg_mos1, sb_src_mos1_err, sb_bg_mos1_err) = sanitize_sb_curve(load_sb_curve(prof_fname_mos1))
    (r, sb_src_mos2, sb_bg_mos2, sb_src_mos2_err, sb_bg_mos2_err) = sanitize_sb_curve(load_sb_curve(prof_fname_mos2))

    # take only the profile inside r500
    ids = where(r<=r500_proj_ang)

    r = r[ids]

    sb_src_pn = sb_src_pn[ids]
    sb_bg_pn = sb_bg_pn[ids]
    sb_src_pn_err = sb_src_pn_err[ids]
    sb_bg_pn_err = sb_bg_pn_err[ids]

    sb_src_mos1 = sb_src_mos1[ids]
    sb_bg_mos1 = sb_bg_mos1[ids]
    sb_src_mos1_err = sb_src_mos1_err[ids]
    sb_bg_mos1_err = sb_bg_mos1_err[ids]

    sb_src_mos2 = sb_src_mos2[ids]
    sb_bg_mos2 = sb_bg_mos2[ids]
    sb_src_mos2_err = sb_src_mos2_err[ids]
    sb_bg_mos2_err = sb_bg_mos2_err[ids]

    n = len(r)

    print "SB curves loaded!"

    ######################################################################
    # control plot

    if MAKE_CONTROL_PLOT=="True":
        for instrument in instruments:
            print instrument
            # outfig = prof_fname_+','+fitid+'.png'

            # print outfig

            # plot_sb_profile(r, sb_src, sb_src_err, sb_bg, sb_bg_err, outfig)
            # os.system("open "+outfig)

    print "going to sleep!"
    from time import sleep
    sleep(1000)

    ######################################################################
    # do the actual fitting

    outpickle = fname+'.'+fitid+'.pk'

    if MODEL=="beta":
        fit_beta_model(r, sb_src, sb_src_err, instrument, theta, energy, outpickle)

    if MODEL=="v06":
        fit_v06_model(r, sb_src, sb_src_err, instrument, theta, energy, outpickle)

    print "done!"

