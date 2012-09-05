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
from sb_models import beta_2d_lmfit

def test_lmfit_beta():
    """
    Testing simple 2D fit of beta model (no psf)
    """
    fname = 'beta_image_cts.fits'
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

    ######################################################################
    # init model
    pars = lm.Parameters()
    pars.add('imsize' , value=(xsize_obj, ysize_obj), vary=False)
    pars.add('xcen'   , value=xcen_obj, vary=False)
    pars.add('ycen'   , value=ycen_obj, vary=False)
    pars.add('norm'   , value=2.0, vary=True, min=0.0, max=sum(input_im))
    pars.add('rcore'  , value=10.0, vary=True, min=1.0, max=80.0)
    pars.add('beta'   , value=0.8, vary=True, min=0.1, max=1.0)

    # x = beta_2d_lmfit(pars, input_im)
    # print x.shape

    ######################################################################
    # do the fit
    print "starting fit"

    import time
    t1 = time.clock()
    result = lm.minimize(beta_2d_lmfit, pars, args=(data, errors))
    t2 = time.clock()
    print "fitting took: ", t2-t1, " s"

    ######################################################################
    # output
    print
    print "True values:"
    print "norm", normalization
    print "rcore", rcore
    print "beta", beta

    print
    print 'Best-Fit Values:'
    for name, par in pars.items():
        print name, par.value


    ######################################################################
    # get the profiles

    # data
    (r, profile, geometric_area) = extract_profile_generic(data, xcen_obj, ycen_obj)
    profile_norm = profile / geometric_area
    profile_norm_err = sqrt(profile_norm)
    profile_norm_err[profile_norm_err==0.0] = sqrt(profile_norm.max())

    # model
    model = beta_2d_lmfit(pars)
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




    # ######################################################################
    # # extract results
    # norm_fit  = par_fitted["norm"]
    # rcore_fit = par_fitted["rcore"]
    # beta_fit  = par_fitted["beta"]

    # norm_fit_err  = errors_fitted["norm"]
    # rcore_fit_err = errors_fitted["rcore"]
    # beta_fit_err  = errors_fitted["beta"]

    # par_fitted = [model_fit.values["norm"], model_fit.values["rcore"], model_fit.values["beta"]]
    # errors_fitted = model_fit.errors

    # ######################################################################
    # # print results
    # print
    # print "beta true: ", beta
    # print "rcore true: ", rcore
    # print
    # print "beta: ", beta_fit, beta_fit_err
    # print "rcore: ", rcore_fit, rcore_fit_err
    # print "norm: ", norm_fit, norm_fit_err
    # print

    # # build the model
    # model_2d = build_sb_model_beta(xsize, ysize, xsize_obj, ysize_obj, xcen, ycen, norm_fit, rcore_fit, beta_fit, instrument, theta, energy, APPLY_PSF)

    # (r_model, profile_model, geometric_area_model) = extract_profile_generic(model_2d, xcen, ycen)
    # profile_norm_model = profile_model / geometric_area_model

    # ######################################################################
    # # do the plot
    # MAKE_PLOT=True
    # if MAKE_PLOT:
    #     output_figure="fit_beta.png"
    #     plot_data_model_simple(r, profile_norm, r_model, profile_norm_model, output_figure)
    #     print "plotting model"



if __name__ == '__main__':
    print
    DEBUG = True

    ######################################################################
    # devel/debug
    if DEBUG:
        reload(test_2d_im)
        reload(sb_models)
        module_visible()

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
    num_cts       = 2.0e3             # will be the normalization
    rcore         = 10.0               # [pix]
    beta          = 2.0 / 3.0
    normalization = 1.0

    ######################################################################
    # images for fitting tests
    # test_create_beta_im()
    # test_create_cluster_im()

    ######################################################################
    # test lmfit
    test_lmfit_beta()

    print "done!"
