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


def test_lmfit_v06_psf_1d(fname='cluster-im-v06-psf.fits'):
    """
    Testing simple 1D fit of v06 model with psf convolution
    """
    APPLY_PSF = True
    DO_ZERO_PAD = True

    ######################################################################
    # image setup

    xsize = input_im.shape[0]
    ysize = xsize
    xcen = xsize/2 #+ 1
    ycen = ysize/2 #+ 1

    imsize = input_im.shape         # FIXME: is this necessary? I could just use it inside the model

    rmax = 1.5 * r500_pix
    xsize_obj = 2 * rmax   # has to be at least 1 pix less than the
                           # "data" image

    ysize_obj = xsize_obj
    xcen_obj = xsize_obj / 2
    ycen_obj = ysize_obj / 2

    ######################################################################
    # getting the "data"

    # cut out the relevant part of the image
    subidx1 = xcen-xsize_obj/2
    subidx2 = xcen+xsize_obj/2
    subidy1 = ycen-ysize_obj/2
    subidy2 = ycen+ysize_obj/2

    data = input_im[subidx1:subidx2, subidy1:subidy2]
    imsize = data.shape

    # setup data for the profile extraction - for speedup
    distmatrix = distance_matrix(data, xcen_obj, ycen_obj).astype('int') + 1 # +1 bc of the divergence

    # FIXME: bgrid should be removed and replaced by r_data in the
    # extract_profile_fast2 call
    bgrid = unique(distmatrix.flat)

    # defining the binning scheme
    r_length = data.shape[0]/2
    r_data = arange(0, r_length, 1.0)

    # extract profile for *data*
    (profile_data, geometric_area_data) = extract_profile_fast2(data, distmatrix, bgrid)
    profile_norm_data = profile_data[0:r_length] / geometric_area_data[0:r_length]    # trim the corners

    # print 'v06', profile_data[0:10]
    # print 'v06', geometric_area_data[0:10]
    # print 'v06', profile_norm_data[0:10]

    # normalize and get errors
    profile_norm_data_err = sqrt(profile_norm_data)
    profile_norm_data_err[profile_norm_data_err==0.0] = sqrt(profile_norm_data.max())

    # plot_data_model_simple(r_data, profile_norm_data, None, None, None, profile_norm_data_err,
    #                        None, None)

    ######################################################################
    # init fit parameters

    n0 = 7e+0
    rc = 20.0
    beta = 4.0/3.0
    rs = 20.0
    alpha = 1.5
    gamma = 3.0
    epsilon = 1.5

    # convert pars to lmfit structure
    pars = lm.Parameters()
    pars.add('n0'      , value=n0, vary=True, min=1.0e-9, max=1.0e3)
    pars.add('rc'      , value=rc, vary=True, min=0.05, max=r500_pix)
    pars.add('beta'    , value=beta, vary=True, min=0.05, max=2.0)
    pars.add('rs'      , value=rs, vary=True, min=0.05, max=2*r500_pix)
    pars.add('alpha'   , value=alpha, vary=True, min=0.01, max=3.0)
    pars.add('epsilon' , value=epsilon, vary=True, min=0.0, max=5.0)
    pars.add('gamma'   , value=gamma, vary=False)

    # set the ancilarry parameters
    distmatrix_input = distmatrix.copy()

    nonfit_args = (distmatrix_input, bgrid, r500_pix, psf_pars,
                   xcen_obj, ycen_obj)

    (r_true, profile_norm_true) = v06_psf_2d_lmfit_profile(pars_true,
                                                           *nonfit_args)

    ######################################################################
    # fits

    fname = 'smooth_model.fits'
    (model_image, hdr2) = load_fits_im(fname)

    distmatrix = distance_matrix(model_image, xcen_obj, ycen_obj).astype('int') + 1 # +1 bc of the divergence
    bgrid = unique(distmatrix.flat)

    (profile, geometric_area) = extract_profile_fast2(model_image, distmatrix, bgrid)
    profile_norm_true2 = profile / geometric_area
    r_true2 = arange(0, len(profile), 1.0)

    # start here
    # plot_data_model_simple(r_data, profile_norm_data,
    #                        r_true2, profile_norm_true2,
    #                        None, profile_norm_data_err,
    #                        r_true, profile_norm_true)

    ######################################################################
    # do the fit

    DO_FIT = True

    nonfit_args = (distmatrix_input, bgrid, r500_pix, psf_pars,
                   xcen_obj, ycen_obj, profile_norm_data,
                   profile_norm_data_err)

    leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+7}

    if DO_FIT:
        print "starting fit"
        t1 = time.clock()

        result = lm.minimize(v06_psf_2d_lmfit_profile,
                             pars,
                             args=nonfit_args,
                             **leastsq_kws)
        result.leastsq()

        # get the final fitted model
        nonfit_args = (distmatrix_input, bgrid, r500_pix, psf_pars,
                   xcen_obj, ycen_obj)
        (r_fit_model, profile_norm_fit_model) = v06_psf_2d_lmfit_profile(pars, *nonfit_args)

        ######################################################################
        ######################################################################
        ######################################################################

        # nonfit_args = (imsize, xsize_obj, ysize_obj, instrument, theta,
        #            energy, APPLY_PSF, DO_ZERO_PAD, profile_norm_data,
        #            profile_norm_data_err)

        # pars = lm.Parameters()
        # pars.add('norm', value=1.0, vary=True, min=0.0, max=sum(input_im))
        # pars.add('rcore', value=15.0, vary=True, min=1.0, max=80.0)
        # pars.add('beta', value=0.7, vary=True, min=0.1, max=10.0)
        # pars.add('xcen', value=xcen_obj, vary=False)
        # pars.add('ycen', value=ycen_obj, vary=False)

        # result = lm.minimize(beta_psf_2d_lmfit_profile,
        #                      pars,
        #                      args=nonfit_args,
        #                      **leastsq_kws)
        # result.leastsq()

        # # get the output model
        # (r_fit_model, profile_norm_fit_model) = beta_psf_2d_lmfit_profile(pars,
        #                                                           imsize,
        #                                                           xsize_obj,
        #                                                           ysize_obj,
        #                                                           instrument,
        #                                                           theta,
        #                                                           energy,
        #                                                           APPLY_PSF,
        #                                                           DO_ZERO_PAD)

        ######################################################################
        ######################################################################
        ######################################################################

        t2 = time.clock()
        print "fitting took: ", t2-t1, " s"

    ######################################################################
    # output

    if DO_FIT:
        lm.printfuncs.report_errors(result.params)
        print_result_tab(pars_true, pars)

    ######################################################################
    # confidence intervals

    CALC_1D_CI = False
    CALC_2D_CI = False

    if CALC_1D_CI:
        print "Calculating 1D confidence intervals"
        # sigmas = [0.682689492137, 0.954499736104, 0.997300203937]
        sigmas = [0.682689492137, 0.954499736104]
        ci_pars = ['rcore', 'beta']

        ci, trace = lm.conf_interval(result, p_names=ci_pars, sigmas=sigmas,
                              trace=True, verbose=True, maxiter=1)

        lm.printfuncs.report_ci(ci)

    if CALC_2D_CI:
        from timer import Timer

        with Timer() as t:
            print "Calculating 2D confidence intervals"
            x, y, prob = lm.conf_interval2d(result,'rcore','beta',20,20)
            plt.contourf(x,y,grid)

        print "elasped time:", t.secs, " s"

    ######################################################################
    # plot profiles

    PLOT_PROFILE = True

    if DO_FIT and PLOT_PROFILE:

        print 30*'#'
        print

        output_figure = 'lmfit_v06_psf_1d.png'
        plot_data_model_simple(r_data, profile_norm_data,
                               r_fit_model, profile_norm_fit_model,
                               output_figure, profile_norm_data_err,
                               r_true, profile_norm_true)




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
    FIT_V06_MODEL = False

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

    if FIT_V06_MODEL:
        fit_beta_model(r, sb_src, sb_src_err)


    print "done!"


