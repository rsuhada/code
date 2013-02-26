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
from sb_models import beta_psf_2d_lmfit_profile
import lmfit as lm
import time


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

    # ids = unique(hstack((ids1, ids2)))
    ids = ids2

    r = r[ids]
    sb_src = sb_src[ids]
    sb_bg = sb_bg[ids]
    sb_src_err = sb_src_err[ids]
    sb_bg_err = sb_bg_err[ids]

    return (r, sb_src, sb_bg, sb_src_err, sb_bg_err)


def fit_beta_model(r, sb_src, sb_src_err):
    """
    Fit a beta x psf model

    Arguments:
    - `r`:
    - `sb_src`:
    - `sb_src_err`:
    """

    # settings
    APPLY_PSF = True
    DO_ZERO_PAD = True
    DO_FIT = True
    PLOT_PROFILE = True

    ######################################################################
    # modelling is done in 2D and then projected - setup here the 2D
    # parameters

    size = 2.0 * r.max()
    xsize = size
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2
    # imsize = input_im.shape         # FIXME: is this necessary? I could just use it inside the model
    imsize = (size, size)         # FIXME: is this necessary? I could just use it inside the model

    xsize_obj = xsize # 100             # if running t1.fits set to 100 else xsize
    ysize_obj = xsize_obj
    xcen_obj = xsize_obj / 2
    ycen_obj = ysize_obj / 2
    r_aper = xsize_obj  / 2        # aperture for the fitting

    ######################################################################
    # init model

    pars = lm.Parameters()
    pars.add('norm', value=mean(sb_src), vary=True, min=0.0, max=sum(abs(sb_src)))
    pars.add('rcore', value=15.0, vary=True, min=1.0, max=80.0)
    pars.add('beta', value=0.66, vary=True, min=0.1, max=10.0)
    pars.add('xcen', value=xcen_obj, vary=False)
    pars.add('ycen', value=ycen_obj, vary=False)

    nonfit_args = (imsize, xsize_obj, ysize_obj, instrument, theta,
                   energy, APPLY_PSF, DO_ZERO_PAD, sb_src,
                   sb_src_err)

    # leastsq_kws={'ptol': 1.0e7, 'ftol': 1.0e7, 'maxfev': 1.0e+0} # debug set
    leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+3}

    ######################################################################
    # do the fit

    if DO_FIT:
        print "starting fit"
        t1 = time.clock()

        result = lm.minimize(beta_psf_2d_lmfit_profile,
                             pars,
                             args=nonfit_args,
                             **leastsq_kws)

        result.leastsq()

        t2 = time.clock()
        print "fitting took: ", t2-t1, " s"

        # get the output model
        (r_model, profile_norm_model) = beta_psf_2d_lmfit_profile(pars,
                                                                  imsize,
                                                                  xsize_obj,
                                                                  ysize_obj,
                                                                  instrument,
                                                                  theta,
                                                                  energy,
                                                                  APPLY_PSF,
                                                                  DO_ZERO_PAD)

        ######################################################################
        # output

        # print_result_tab(pars_true, pars)
        lm.printfuncs.report_errors(result.params)
        print "fitting subroutine done!"

    ######################################################################
    # plot profiles

    if DO_FIT and PLOT_PROFILE:

        output_figure = 'lmfit_beta_psf_1d.png'

        plot_data_model_resid(r, sb_src,
                               r_model, profile_norm_model,
                               output_figure, sb_src_err)

    return 0


if __name__ == '__main__':
    print

    reload(sb_plotting_utils)

    ######################################################################
    # settings
    fname = '/Users/rs/w/xspt/data/dev/0559/sb/sb-prof-pn-003.dat'
    outfig = fname+'.dev.png'

    # r_500_proj_ang = 153.0   # projected radius [arcsec]
    r_500_proj_ang = 100.0   # projected radius [arcsec]

    # PSF parameters
    theta = 65.8443 / 60.0
    energy = 1.5
    instrument = "pn"
    psf_pars = (instrument, theta, energy)

    # module settings
    MAKE_CONTROL_PLOT = False
    FIT_BETA_MODEL = True

    ######################################################################
    # loading the data
    (r, sb_src, sb_bg, sb_src_err, sb_bg_err) = sanitize_sb_curve(load_sb_curve(fname))
    # (r, sb_src, sb_bg, sb_src_err, sb_bg_err) = load_sb_curve(fname)

    ids = where(r<=r_500_proj_ang)

    r = r[ids]
    sb_src = sb_src[ids]
    sb_bg = sb_bg[ids]
    sb_src_err = sb_src_err[ids]
    sb_bg_err = sb_bg_err[ids]
    n = len(r)

    # for i in xrange(n):
    #     print r[i], sb_src[i], sb_bg[i], sb_src_err[i], sb_bg_err[i]

    ######################################################################
    # control plot

    if MAKE_CONTROL_PLOT:
        plot_sb_profile(r, sb_src, sb_src_err, sb_bg, sb_bg_err, outfig)
        os.system("open "+outfig)

    if FIT_BETA_MODEL:
        fit_beta_model(r, sb_src, sb_src_err)


    print "done!"


