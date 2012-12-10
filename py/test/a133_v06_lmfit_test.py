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
from scipy import integrate


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


# def fit_a133_sb():
#     """
#     Fit a133 digitized profile
#     """

#     ######################################################################
#     # load data
#     intab = '/Users/rs/data1/sw/esaspi/py/test/a133-sprof.dat'
#     dat=loadtxt(intab, dtype='string', comments='#', delimiter=None, converters=None,
#                 skiprows=0, unpack=False,
#                 usecols=(0,1,2,3)
#                 )

#     r_data = double(dat[:,0])
#     profile_norm_data = double(dat[:,1])
#     profile_norm_data_err_d = profile_norm_data - double(dat[:,2])
#     profile_norm_data_err_u = double(dat[:,3]) - profile_norm_data

#     # erorrs
#     profile_norm_data_err = (profile_norm_data_err_d + profile_norm_data_err_u)/2.0
#     # profile_norm_data_err = profile_norm_data_err

#     plot_data_model_simple(r_data, profile_norm_data, None, None, None, profile_norm_data_err,
#                            None, None)

#     n0 = 7e+0
#     rc = 20.0
#     beta = 4.0/3.0
#     rs = 20.0
#     alpha = 1.5
#     gamma = 3.0
#     epsilon = 1.5

#     # convert pars to lmfit structure
#     pars = lm.Parameters()
#     pars.add('n0'      , value=n0, vary=True, min=1.0e-9, max=1.0e3)
#     pars.add('rc'      , value=rc, vary=True, min=0.05, max=r500_pix)
#     pars.add('beta'    , value=beta, vary=True, min=0.05, max=2.0)
#     pars.add('rs'      , value=rs, vary=True, min=0.05, max=2*r500_pix)
#     pars.add('alpha'   , value=alpha, vary=True, min=0.01, max=3.0)
#     pars.add('epsilon' , value=epsilon, vary=True, min=0.0, max=5.0)
#     pars.add('gamma'   , value=gamma, vary=False)

#     nonfit_args = (distmatrix_input, bgrid, r500_pix, psf_pars,
#                    xcen_obj, ycen_obj)

#     (r_true, profile_norm_true) = v06_psf_2d_lmfit_profile(pars_true,
#                                                            *nonfit_args)





def fit_a133_sb(fname='cluster-im-v06-psf.fits'):
    """
    Testing simple 1D fit of v06 model with psf convolution
    """
    APPLY_PSF = True
    DO_ZERO_PAD = True

    input_im, hdr = load_fits_im(fname)

    ######################################################################
    # image setup

    xsize = input_im.shape[0]
    ysize = xsize
    xcen = xsize/2 #+ 1
    ycen = ysize/2 #+ 1

    imsize = input_im.shape

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

    # normalize and get errors
    profile_norm_data_err = sqrt(profile_norm_data)
    profile_norm_data_err[profile_norm_data_err==0.0] = sqrt(profile_norm_data.max())

    ######################################################################
    ######################################################################
    ######################################################################
    # insert the a133 data

    intab = '/Users/rs/data1/sw/esaspi/py/test/a133-sprof.dat'
    dat=loadtxt(intab, dtype='string', comments='#', delimiter=None, converters=None,
                skiprows=0, unpack=False,
                usecols=(0,1,2,3)
                )

    r_data = double(dat[:,0])
    profile_norm_data = double(dat[:,1])
    profile_norm_data_err_d = profile_norm_data - double(dat[:,2])
    profile_norm_data_err_u = double(dat[:,3]) - profile_norm_data

    # erorrs
    profile_norm_data_err = (profile_norm_data_err_d + profile_norm_data_err_u)/2.0

    ######################################################################
    ######################################################################
    ######################################################################

    # plot_data_model_simple(r_data, profile_norm_data, None, None,
    #                        None, profile_norm_data_err,
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


        t2 = time.clock()
        print "fitting took: ", t2-t1, " s"

    ######################################################################
    # output

    if DO_FIT:
        lm.printfuncs.report_errors(result.params)
        print_result_tab(pars_true, pars)

    ######################################################################
    # plot profiles

    PLOT_PROFILE = True

    if DO_FIT and PLOT_PROFILE:

        print 30*'#'
        print

        output_figure = 'lmfit_v06_psf_1d.png'

        # plot_data_model_simple(r_data, profile_norm_data, None, None,

        plot_data_model_simple(r_fit_model, profile_norm_data[:len(r_fit_model)],
                               r_fit_model, profile_norm_fit_model,
                               output_figure, profile_norm_data_err[:len(r_fit_model)],
                               None, None)


######################################################################
# setup basic parameters
theta = 65.8443 / 60.0
energy = 1.5
instrument = "pn"

psf_pars = (instrument, theta, energy)

# setup for the beta model
num_cts       = 2.0e5             # Will be the normalization

# model pars
r500 = 1.0e3                # r500 [kpc]
r500_pix = 30              # r500 in im pixels

n0 = 7e+0
rc = 20.0                   # ballpark 0.1 r500
beta = 2.0/3.0
rs = 20.0                   # ballpark 0.5-1 r500
alpha = 1.5                 # <3
gamma = 3.0                 # fix = 3
epsilon = 2.0               # <5

pars_true = lm.Parameters()
pars_true.add('n0', value=n0, vary=False)
pars_true.add('rc', value=rc, vary=False)
pars_true.add('beta', value=beta, vary=False)
pars_true.add('rs', value=rs, vary=False)
pars_true.add('alpha', value=alpha, vary=False)
pars_true.add('gamma', value=gamma, vary=False)
pars_true.add('epsilon', value=epsilon, vary=False)

im_file = 'v06_image_cts.fits'

import test_2d_im
reload(test_2d_im)
fit_a133_sb(im_file)

