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
import asciitable as atab
from sb_fitting_utils import *


if __name__ == '__main__':
    plt.close('all')

    ######################################################################
    # input parameters

    fname=sys.argv[1]
    fitid=sys.argv[2]
    r500_proj_ang=double(sys.argv[3])
    instrument=sys.argv[4]
    theta=double(sys.argv[5]) / 60.0
    energy=double(sys.argv[6])
    MODEL=sys.argv[7]
    MAKE_CONTROL_PLOT=sys.argv[8]

    print '-'*70
    print fname
    print r500_proj_ang
    print theta
    print energy
    print instrument
    print MODEL
    print MAKE_CONTROL_PLOT
    print '-'*70

    # # 2332
    # # fname = '/Users/rs/w/xspt/data/dev/0559/sb/SPT-CL-J2332-5358/sb-prof-pn-004.dat'

    # # 0559
    # fname = '/Users/rs/w/xspt/data/dev/0559/sb/SPT-CL-J0559-5249/sb-prof-pn-003.dat'

    # # fname = '/Users/rs/w/xspt/data/dev/0559/sb/sb-prof-mock-02-beta-ideal.dat'
    # # fname = '/Users/rs/w/xspt/data/dev/0559/sb/v06_image_obs-02.fits-prof.dat'
    # # fname = '/Users/rs/w/xspt/data/dev/0559/sb/beta_image_obs-03.fits-prof.dat'
    # # fname = '/Users/rs/w/xspt/data/dev/0559/sb/v06_image_obs-03.fits-prof.dat'
    # # fname = '/Users/rs/w/xspt/data/dev/0559/sb/beta_image_obs-05.fits-prof.dat'

    # # radius
    # r500_proj_ang = 153.0   # 0559 projected radius [arcsec]
    # # r500_proj_ang = 100.0   # projected radius [arcsec]
    # # r500_proj_ang = 200.0   # 2332 test, projected radius [arcsec]

    # # PSF parameters
    # theta = 65.8443 / 60.0
    # energy = 1.5
    # instrument = "pn"
    # psf_pars = (instrument, theta, energy)

    # # module settings
    # MAKE_CONTROL_PLOT = False
    # MODEL = "beta"

    ######################################################################
    # loading sb curve

    (r, sb_src, sb_bg, sb_src_err, sb_bg_err) = sanitize_sb_curve(load_sb_curve(fname))


    # take only the profile inside r500
    ids = where(r<=r500_proj_ang)

    r = r[ids]
    sb_src = sb_src[ids]
    sb_bg = sb_bg[ids]
    sb_src_err = sb_src_err[ids]
    sb_bg_err = sb_bg_err[ids]
    n = len(r)

    ######################################################################
    # control plot

    if MAKE_CONTROL_PLOT=="True":
        outfig = fname+'.'+fitid+'.png'

        plot_sb_profile(r, sb_src, sb_src_err, sb_bg, sb_bg_err, outfig)
        os.system("open "+outfig)


    ######################################################################
    # do the actual fitting

    outpickle = fname+'.'+fitid+'.pk'

    if MODEL=="beta":
        fit_beta_model(r, sb_src, sb_src_err, instrument, theta, energy, outpickle)

    if MODEL=="v06":
        fit_v06_model(r, sb_src, sb_src_err, instrument, theta, energy, outpickle)

    print "done!"

