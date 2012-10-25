#!/usr/bin/env python
import sys
import os
import math
import pyfits
from numpy import *
from pylab import rc
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, LogLocator
from test_2d_im import *
import lmfit as lm
from esaspi_utils import *
from sb_models import *
from sb_utils import *
from sb_plotting_utils import *
import time


def print_result_tab(pars_true, pars_fit):
    """
    Print a nice result table
    """
    print
    print "|"+12*"-"+"|"+12*"-"+"|"+12*"-"+"|"+12*"-"+"|"
    print "| %10s | %10s | %10s | %10s |" % ("name", "true", "fit", "error")
    print "|"+12*"-"+"|"+12*"-"+"|"+12*"-"+"|"+12*"-"+"|"
    for key in pars_true:
        print "| %10s | %10.5f | %10.5f | %10.5f |" % (key, pars_true[key].value, pars_fit[key].value, pars_fit[key].stderr)
    print "|"+12*"-"+"|"+12*"-"+"|"+12*"-"+"|"+12*"-"+"|"
    print

def iplot(x, y):
    """
    A simple interctive plot for debugging

    Arguments:
    - `x`:
    - `y`:
    """
    # interactive quick plot
    plt.figure()
    plt.ion()
    plt.clf()

    plt.plot(x, y,
        color='black',
        linestyle='-',              # -/--/-./:
        linewidth=1,                # linewidth=1
        marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='black',
        markersize=0,               # markersize=6
        label=r"data"               # '__nolegend__'
        )

    plt.xscale("linear")
    plt.yscale("linear")

    plt.show()
    plotPosition="+1100+0"          # large_screen="+1100+0"; lap="+640+0"
    plt.get_current_fig_manager().window.wm_geometry(plotPosition)


def test_lmfit_beta(fname='beta_image_cts.fits'):
    """
    Testing simple 2D fit of beta model (no psf)
    """
    input_im, hdr = load_fits_im(fname)

    ######################################################################
    # image setup
    xsize = input_im.shape[0]
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    xsize_obj = 100
    ysize_obj = xsize_obj
    xcen_obj = xsize_obj / 2
    ycen_obj = ysize_obj / 2
    r_aper = xsize_obj          # aperture for the fitting

    ######################################################################
    # we want just the relevant part of the image
    data = input_im[ycen-ysize_obj/2:ycen+ysize_obj/2, xcen-xsize_obj/2:xcen+xsize_obj/2]
    errors = sqrt(data)
    # errors[errors==0.0] = errors.max()

    ######################################################################
    # init model
    pars = lm.Parameters()
    pars.add('imsize' , value=(xsize_obj, ysize_obj), vary=False) # FIXME: should be moved from par list to args
    pars.add('xcen'   , value=xcen_obj, vary=False)
    pars.add('ycen'   , value=ycen_obj, vary=False)
    pars.add('norm'   , value=2.0, vary=True, min=0.0, max=sum(input_im))
    pars.add('rcore'  , value=10.0, vary=True, min=1.0, max=80.0)
    pars.add('beta'   , value=0.8, vary=True, min=0.1, max=10.0)

    ######################################################################
    # do the fit
    DO_FIT = True

    if DO_FIT:
        print "starting fit"

        t1 = time.clock()
        result = lm.minimize(beta_2d_lmfit, pars, args=(data, errors)) # fit in 2d
        t2 = time.clock()
        print "fitting took: ", t2-t1, " s"

        ######################################################################
        # output
        print
        print "parameter: true | fit"
        # print "norm", normalization
        print "rcore", rcore, pars['rcore'].value, "+/-", pars['rcore'].stderr
        print "beta", beta, pars['beta'].value, "+/-", pars['beta'].stderr
        print
        print


    ######################################################################
    # get the profiles

    # data
    (r, profile, geometric_area) = extract_profile_generic(data, xcen_obj, ycen_obj)
    profile_norm = profile / geometric_area
    profile_norm_err = sqrt(profile_norm)
    profile_norm_err[profile_norm_err==0.0] = sqrt(profile_norm.max())

    # model
    model = beta_2d_lmfit(pars)
    x = beta_2d_lmfit(pars, data, errors)

    (r_model, profile_model, geometric_area_model) = extract_profile_generic(model, xcen_obj, ycen_obj)
    profile_norm_model = profile_model / geometric_area_model
    profile_norm_model_err = sqrt(profile_norm_model)
    profile_norm_model_err[profile_norm_model_err==0.0] = sqrt(profile_norm_model.max())

    ######################################################################
    # plot
    MAKE_PLOT=True
    if MAKE_PLOT:
        print "plotting model"
        output_figure="fit_beta_mlfit.png"
        plot_data_model_simple(r, profile_norm, r_model, profile_norm_model, output_figure)


def test_create_beta_im(imname='beta_image_cts.fits'):
    """
    Create a simple testimage - poissonized beta model no psf
    """
    # settings
    POISSONIZE_IMAGE   = False            # poissonize image?
    DO_ZERO_PAD        = True
    APPLY_EXPOSURE_MAP = False
    ADD_BACKGROUND     = False

    # get a header
    fname='pn-test.fits'
    hdu = pyfits.open(fname)
    hdr = hdu[0].header

    # image setup
    xsize = 900
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    # if zero padded image for testing - this to check normalizations
    # - works fine
    xsize_obj = 100
    ysize_obj = xsize_obj

    # create beta
    print (xsize, ysize), xcen, ycen, normalization, rcore, beta
    im_beta = make_2d_beta((xsize, ysize), xcen, ycen, normalization, rcore, beta)
    im_beta = num_cts * im_beta/im_beta.sum()

    if POISSONIZE_IMAGE:
        im_beta = poisson.rvs(im_beta)
        print "poisson sum:", im_beta.sum()

    if DO_ZERO_PAD:
        im_beta[:, 0:xsize_obj] = 0.0
        im_beta[:, xsize-xsize_obj:] = 0.0
        im_beta[0:xsize_obj,:] = 0.0
        im_beta[xsize-xsize_obj:,:] = 0.0

    # poissonized beta model image [counts] - no background/mask
    hdu = pyfits.PrimaryHDU(im_beta, hdr)    # extension - array, header
    hdulist = pyfits.HDUList([hdu])          # list all extensions here
    hdulist.writeto(imname, clobber=True)


def test_lmfit_beta_1d(fname='beta_image_cts.fits'):
    """
    Testing simple 1D fit of beta model (no psf)
    """

    # FIXME: Fri Oct 12 15:03:37 2012 code currently outdated: look at
    # test_lmfit_beta_psf_1d(imname) function which is up to date
    # (change in extracxtion, model)

    input_im, hdr = load_fits_im(fname)

    ######################################################################
    # image setup
    xsize = input_im.shape[0]
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    xsize_obj = 100
    ysize_obj = xsize_obj
    xcen_obj = xsize_obj / 2
    ycen_obj = ysize_obj / 2
    r_aper = xsize_obj  / 2        # aperture for the fitting

    # we want just the relevant part of the image
    data = input_im[ycen-ysize_obj/2:ycen+ysize_obj/2, xcen-xsize_obj/2:xcen+xsize_obj/2]
    imsize = data.shape         # FIXME: is this necessary? I could just use it inside the model

    # work on full image
    data = input_im
    imsize = data.shape

    # extract data profile
    (r, profile, geometric_area) = extract_profile_generic(data, xcen_obj, ycen_obj)
    profile_norm = profile / geometric_area
    profile_norm_err = sqrt(profile_norm)
    profile_norm_err[profile_norm_err==0.0] = sqrt(profile_norm.max()) # FIXME - CRITICAL! - need binning

    ######################################################################
    # init model
    pars = lm.Parameters()

    pars.add('norm'   , value=2.0, vary=True, min=0.0, max=sum(input_im))
    pars.add('rcore'  , value=10.0, vary=True, min=1.0, max=80.0)
    pars.add('beta'   , value=0.8, vary=True, min=0.1, max=10.0)

    pars.add('xcen', value=xcen_obj, vary=False)
    pars.add('ycen', value=ycen_obj, vary=False)

    ######################################################################
    # do the fit
    DO_FIT = True
    FIT_1D_MODEL = False        # fit 1d model or 2d model via its profile

    # model in 2d and extract profile
    t1 = time.clock()
    # model_image = make_2d_beta(imsize, xcen, ycen, 2.0, 10.0, 0.8)
    (r_model, profile_norm_model) = beta_2d_lmfit_profile(pars, imsize)
    t2 = time.clock()
    print "objective outside minimize took: ", t2-t1, " s"

    if DO_FIT:
        print "starting fit"

        t1 = time.clock()

        if FIT_1D_MODEL:
            result = lm.minimize(beta_1d_lmfit, pars, args=(r, profile_norm, profile_norm_err))
            r_model = arange(0.0, r_aper, 0.1)
            profile_norm_model = beta_1d_lmfit(pars, r_model)
        else:
            result = lm.minimize(beta_2d_lmfit_profile, pars, args=(imsize, profile_norm, profile_norm_err))
            (r_model, profile_norm_model) = beta_2d_lmfit_profile(pars, imsize)

        t2 = time.clock()
        print "fitting took: ", t2-t1, " s"

        ######################################################################
        # output
        print
        print "parameter: true | fit"
        print "rcore", rcore, pars['rcore'].value, "+/-", pars['rcore'].stderr
        print "beta", beta, pars['beta'].value, "+/-", pars['beta'].stderr
        print
        print

    ######################################################################
    # plot profiles

    output_figure = 'lmfit_beta_1d.png'
    plot_data_model_simple(r, profile_norm, r_model, profile_norm_model, output_figure, profile_norm_err)


def test_create_beta_psf_im(imname='beta_image_cts.fits'):
    """
    Create a simple testimage - poissonized beta model x psf
    Validated wrt test_2d_im routines (minuit)
    """
    # settings
    APPLY_PSF          = True
    POISSONIZE_IMAGE   = True            # poissonize image?
    DO_ZERO_PAD        = True
    APPLY_EXPOSURE_MAP = False
    ADD_BACKGROUND     = False

    # get a header
    fname='pn-test.fits'
    hdu = pyfits.open(fname)
    hdr = hdu[0].header

    # image setup
    xsize = 900
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    # if zero padded image for testing - this to check normalizations
    # - works fine
    xsize_obj = 100
    ysize_obj = xsize_obj
    xcen_obj = xsize_obj / 2
    ycen_obj = ysize_obj / 2

    imsize = (ysize, xsize)

    # init model
    pars = lm.Parameters()
    pars.add('xcen'   , value=xcen)
    pars.add('ycen'   , value=ycen)
    pars.add('norm'   , value=normalization)
    pars.add('rcore'  , value=rcore)
    pars.add('beta'   , value=beta)

    im_conv = make_2d_beta_psf(pars, imsize, xsize_obj, ysize_obj,
                               instrument, theta, energy,
                               APPLY_PSF, DO_ZERO_PAD)

    im_conv = num_cts * im_conv/im_conv.sum()

    # slow extractor
    (r, profile_ref, geometric_area_ref) = extract_profile_generic(im_conv, xcen, ycen)

    # setup data for the profile extraction - for speedup
    distmatrix = distance_matrix(im_conv, xcen, ycen).astype(int) # need int for bincount
    rgrid_length = im_conv.shape[0]/2
    rgrid = arange(0, rgrid_length, 1.0)

    (profile, geometric_area) = extract_profile_fast(im_conv, distmatrix, xcen_obj, ycen_obj)

    if POISSONIZE_IMAGE:
        # fix current poissonize bug -poissonize only nonz-zero
        # elements (ok - we're poissonizing the model)
        ids = where(im_conv != 0.0)
        im_conv[ids] = poisson.rvs(im_conv[ids])
        # print "poisson sum:", im_conv.sum()

    # poissonized beta model image [counts] - no background/mask
    hdu = pyfits.PrimaryHDU(im_conv, hdr)    # extension - array, header
    hdulist = pyfits.HDUList([hdu])          # list all extensions here
    hdulist.writeto(imname, clobber=True)

def test_create_v06_psf_im(imname='v06_image_cts.fits'):
    """
    Create a simple testimage - poissonized beta model x psf
    Validated wrt test_2d_im routines (minuit)
    """
    # settings
    POISSONIZE_IMAGE   = True            # poissonize image?

    # get a header
    fname='pn-test.fits'
    hdu = pyfits.open(fname)
    hdr = hdu[0].header

    # image setup
    xsize = 900
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    # if zero padded image for testing - this to check normalizations
    # - works fine
    xsize_obj = 100
    ysize_obj = xsize_obj
    xcen_obj = xsize_obj / 2
    ycen_obj = ysize_obj / 2

    imsize = (ysize, xsize)

    # init model
    pars = lm.Parameters()
    pars.add('rc', value=rc)
    pars.add('rs', value=rs)
    pars.add('n0', value=n0)
    pars.add('alpha', value=alpha)
    pars.add('beta', value=beta)
    pars.add('gamma', value=gamma, vary=False)
    pars.add('epsilon', value=epsilon)

    # CONTINUE HERE
    distmatrix = distance_matrix(zeros(imsize), xcen, ycen)
    im_conv = make_2d_v06_psf(pars, distmatrix)
    im_conv = num_cts * im_conv/im_conv.sum()

    # slow extractor
    (r, profile_ref, geometric_area_ref) = extract_profile_generic(im_conv, xcen, ycen)

    # setup data for the profile extraction - for speed-up
    rgrid_length = im_conv.shape[0]/2
    rgrid = arange(0, rgrid_length, 1.0)

    (profile, geometric_area) = extract_profile_fast(im_conv, distmatrix, xcen_obj, ycen_obj)

    if POISSONIZE_IMAGE:
        # fix current poissonize bug -poissonize only nonz-zero
        # elements (ok - we're poissonizing the model)
        ids = where(im_conv != 0.0)
        im_conv[ids] = poisson.rvs(im_conv[ids])
        # print "poisson sum:", im_conv.sum()

    # poissonized beta model image [counts] - no background/mask
    hdu = pyfits.PrimaryHDU(im_conv, hdr)    # extension - array, header
    hdulist = pyfits.HDUList([hdu])          # list all extensions here
    hdulist.writeto(imname, clobber=True)

def test_lmfit_beta_psf_1d(fname='cluster_image_cts.fits'):
    """
    Testing simple 1D fit of beta model with psf convolution
    """
    APPLY_PSF = True
    DO_ZERO_PAD = True

    input_im, hdr = load_fits_im(fname)

    ######################################################################
    # image setup

    xsize = input_im.shape[0]
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2
    imsize = input_im.shape         # FIXME: is this necessary? I could just use it inside the model

    xsize_obj = 100
    ysize_obj = xsize_obj
    xcen_obj = xsize_obj / 2
    ycen_obj = ysize_obj / 2
    r_aper = xsize_obj  / 2        # aperture for the fitting

    ######################################################################
    # getting the "data"

    # we want just the relevant part of the image
    data = input_im[ycen-ysize_obj/2:ycen+ysize_obj/2, xcen-xsize_obj/2:xcen+xsize_obj/2]
    imsize = data.shape

    # extract data profile
    # (r, profile, geometric_area) = extract_profile_generic(data, xcen_obj, ycen_obj)
    # profile_norm = profile / geometric_area

    # setup data for the profile extraction - for speedup
    distmatrix = distance_matrix(data, xcen_obj, ycen_obj).astype(int) # need int for bincount
    r_length = data.shape[0]/2
    r = arange(0, r_length, 1.0)
    (profile, geometric_area) = extract_profile_fast(data, distmatrix, xcen_obj, ycen_obj)
    profile_norm = profile[0:r_length] / geometric_area[0:r_length]    # trim the corners

    # normalize and get errors
    profile_norm_err = sqrt(profile_norm)
    profile_norm_err[profile_norm_err==0.0] = sqrt(profile_norm.max()) # FIXME - CRITICAL! - need binning?

    ######################################################################
    # init model
    pars = lm.Parameters()

    pars.add('norm', value=1.0, vary=True, min=0.0, max=sum(input_im))
    pars.add('rcore', value=15.0, vary=True, min=1.0, max=80.0)
    pars.add('beta', value=0.7, vary=True, min=0.1, max=10.0)

    pars.add('xcen', value=xcen_obj, vary=False)
    pars.add('ycen', value=ycen_obj, vary=False)

    nonfit_args = (imsize, xsize_obj, ysize_obj, instrument, theta,
                   energy, APPLY_PSF, DO_ZERO_PAD, profile_norm,
                   profile_norm_err)

    leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+3}

    ######################################################################
    # do the fit
    DO_FIT = True

    if DO_FIT:
        print "starting fit"
        t1 = time.clock()

        result = lm.minimize(beta_psf_2d_lmfit_profile,
                             pars,
                             args=nonfit_args,
                             **leastsq_kws
                             )

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

    print_result_tab(pars_true, pars)
    lm.printfuncs.report_errors(result.params)

    # print
    # print "parameter: true | fit"
    # print "rcore", rcore, pars['rcore'].value, "+/-", pars['rcore'].stderr
    # print "beta", beta, pars['beta'].value, "+/-", pars['beta'].stderr
    # print
    # print

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

    from timer import Timer

    for i in range(1):
        with Timer() as t:
            if CALC_2D_CI:
                print "Calculating 2D confidence intervals"
                x, y, prob = lm.conf_interval2d(result,'rcore','beta',20,20)
                # plt.contourf(x,y,grid,np.linspace(0,1,11))
                plt.contourf(x,y,grid)
        print "elasped time:", t.secs, " s"

    ######################################################################
    # plot profiles

    pars_true.add('xcen', value=50.0, vary=False)
    pars_true.add('ycen', value=50.0, vary=False)

    result = lm.minimize(beta_psf_2d_lmfit_profile,
                         pars_true,
                         args=nonfit_args,
                         **leastsq_kws)

    (r_true, profile_norm_true) = beta_psf_2d_lmfit_profile(pars_true,
                                                            imsize,
                                                            xsize_obj,
                                                            ysize_obj,
                                                            instrument,
                                                            theta,
                                                            energy,
                                                            APPLY_PSF,
                                                            DO_ZERO_PAD)

    output_figure = 'lmfit_beta_psf_1d.png'

    plot_data_model_simple(r, profile_norm,
                           r_model, profile_norm_model,
                           output_figure, profile_norm_err,
                           r_true, profile_norm_true)

def test_full_model():
    """
    Run lmfitting on a full image incl. exposure map, masking and
    background
    """
    # load images
    im_full, hdr = load_fits_im(im_file)
    expmap, hdr = load_fits_im(expmap_file)
    bgmap, hdr = load_fits_im(bgmap_file)
    maskmap, hdr = load_fits_im(maskmap_file, 1) # mask is in ext1

    ######################################################################
    # setup image coordinates

    rmax = 75.0                 # [pix], should be 1.5 r500
    xsize_obj = 2*rmax
    ysize_obj = xsize_obj
    xcen_obj = xsize_obj / 2
    ycen_obj = ysize_obj / 2

    # get the bined radial boundaries
    rgrid = optibingrid(rmax=rmax)
    # rgrid = arange(1, 51, 1)

    # we want just the relevant part of the image
    subidx1 = xcen-xsize_obj/2
    subidx2 = xcen+xsize_obj/2
    subidy1 = ycen-ysize_obj/2
    subidy2 = ycen+ysize_obj/2

    im = im_full[subidx1:subidx2, subidy1:subidy2]
    imsize = im.shape
    distmatrix = distance_matrix(im, xcen_obj, ycen_obj)

    # extract all the subimages
    expmap  = expmap[subidx1:subidx2, subidy1:subidy2]
    bgmap   = bgmap[subidx1:subidx2, subidy1:subidy2]
    maskmap = maskmap[subidx1:subidx2, subidy1:subidy2]

    # apply mask - since we are doing the correction, mask shouldn't
    # be applied here
    # expmap = expmap * maskmap   # since we are
    # bgmap = bgmap * maskmap

    # cts_tot, cts_tot_err, ctr_tot, ctr_tot_err, sb_tot, sb_tot_err, cts_bg, cts_bg_err, ctr_bg, ctr_bg_err, sb_bg, sb_bg_err = extract_binned_sb_profiles(distmatrix, rgrid, im, expmap, bgmap, maskmap)

    sb_tot, sb_tot_err, sb_bg, sb_bg_err = extract_binned_sb_profiles(distmatrix, rgrid, im, expmap, bgmap, maskmap)
    rgrid = delete(rgrid, 0)    # remove the left-boundary of the first bin

    print rgrid
    # print cts_tot
    # print cts_bg
    # print geo_area
    # print mask_area
    # print ps_area_corr

    print im_full[xcen, ycen]
    print im[xcen_obj, ycen_obj]

    print sb_bg
    print sb_bg_err

    fname='test.png'
    plot_sb_profile(rgrid, sb_tot, sb_tot_err, sb_bg, sb_bg_err, fname)

    # for i in range(len(rgrid)):
    #     print rgrid[i], sb_tot[i], sb_tot_err[i]

######################################################################
######################################################################
######################################################################

if __name__ == '__main__':
    print
    DEBUG = True

    ######################################################################
    # devel/debug
    if DEBUG:

        import test_2d_im
        import sb_models
        import sb_utils
        import esaspi_utils

        reload(test_2d_im)
        reload(sb_models)
        reload(sb_utils)
        reload(esaspi_utils)
        # module_visible()

    ######################################################################
    # setup basic parameters
    theta = 65.8443 / 60.0
    energy = 1.5
    instrument = "pn"
    instid = get_instrument_id(instrument)

    # setup for the gaussian test
    a_sigmax = 15.0               # [pix]
    a_sigmay = 15.0               # [pix]
    b_sigmax = 20.0               # [pix]
    b_sigmay = 20.0               # [pix]
    c_sigmax = sqrt(a_sigmax**2 + b_sigmax**2)              # [pix]
    c_sigmay = sqrt(a_sigmay**2 + b_sigmay**2)              # [pix]

    # setup for the beta model
    num_cts       = 2.0e5             # Will be the normalization
    rcore         = 10.0              # [pix]
    beta          = 2.0 / 3.0
    normalization = 1.0
    imname='t1.fits'

    ######################################################################
    # pars
    pars_true = lm.Parameters()

    pars_true.add('norm', value=normalization, vary=True)
    pars_true.add('rcore', value=rcore, vary=False)
    pars_true.add('beta', value=beta, vary=False)
    pars_true.add('xcen', value=450, vary=False)
    pars_true.add('ycen', value=450, vary=False)

    ######################################################################
    # images for fitting tests
    # test_create_beta_im(imname)
    # test_create_beta_psf_im(imname)

    ######################################################################
    # creating a v06 model

    n0 = 1.0e-3
    rc = 10.0                   # ballpark 0.1 r500
    beta = 2.0/3.0
    rs = 90.0                   # ballpark 0.5-1 r500
    alpha = 1.0                 # <3
    gamma = 3.0                 # fix = 3
    epsilon = 2.5               # <5

    pars_true = lm.Parameters()
    pars_true.add('n0', value=n0, vary=False)
    pars_true.add('rc', value=rc, vary=False)
    pars_true.add('beta', value=beta, vary=False)
    pars_true.add('rs', value=rs, vary=False)
    pars_true.add('alpha', value=alpha, vary=False)
    pars_true.add('gamma', value=gamma, vary=False)
    pars_true.add('epsilon', value=epsilon, vary=False)

    test_create_v06_psf_im(imname)



    ######################################################################
    # test lmfit
    # test_lmfit_beta(imname)
    # test_lmfit_beta_1d(imname)

    # test_lmfit_beta_psf_1d(imname)

    ######################################################################
    # make a synthetic image from precreated image

    # im_file = "t1.fits"
    # expmap_file = "pn-test-exp.fits"
    # bgmap_file  = "pn-test-bg-2cp.fits"
    # maskmap_file= "pn-test-mask.fits"
    # outfile_file= "cluster-im.fits"

    # make_synthetic_observation(im_file, expmap_file,
    #                            bgmap_file, maskmap_file, outfile_file)
    # show_in_ds9(outfile)

    ######################################################################
    # composite test - fitting an image including all instrumental
    # effects

    ######################################################################
    # image setup

    ######################################################################
    # image: synthetic test
    # im_file = "cluster-im.fits"
    # xcen = 450
    # ycen = 450
    ######################################################################

    ######################################################################
    # image: 0205
    im_file = "pn-test.fits"

    # ds9 center in ds9 im coords
    xcen_ds9 = 408.61525
    ycen_ds9 = 439.05376

    # the ds9 coordinates have to be transformed (including order
    # switch)
    xcen = ds9imcoord2py(ycen_ds9)
    ycen = ds9imcoord2py(xcen_ds9)
    ######################################################################

    # rest of the input images
    expmap_file = "pn-test-exp.fits"
    bgmap_file  = "pn-test-bg-2cp.fits"
    maskmap_file= "pn-test-mask.fits"

    # test_full_model()

    print "done!"


