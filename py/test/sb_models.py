#!/usr/bin/env python
import sys
import os
import math
import pyfits
from numpy import *
from scipy.signal import fftconvolve
from pylab import rc
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, LogLocator
from sb_utils import sqdistance, distance_matrix, load_fits_im
from test_2d_im import make_2d_beta, extract_profile_generic, extract_profile_fast, make_2d_king, trim_fftconvolve, zero_pad_image

def beta_2d_lmfit(pars, data=None, errors=None):
    """
    Creates a 2D image of a beta model.
    Function is exactly same as make_2d_beta, but has a lmfit
    interface.
    Also allows to return directly residuals

    Arguments:
    - `imsize`: input 2D array size
    - `xcen`: x coordinate of the function
    - `ycen`: y coordinate of the function
    - 'core': beta model core radius
    - 'beta': beta model slope
    """

    # unpack parameters
    imsize = pars['imsize'].value
    xcen   = pars['xcen'].value
    ycen   = pars['ycen'].value
    norm   = pars['norm'].value
    rcore  = pars['rcore'].value
    beta   = pars['beta'].value

    model = zeros(imsize, dtype=double)

    # this is pretty fast but maybe you want to do it in polar coordinates
    # the dumb method
    for i in range(round(imsize[0])):
        for j in range(round(imsize[1])):
            r2 = sqdistance(xcen, ycen, j , i) # this is already squared
            model[i, j] = norm * (1.0 + r2/(rcore)**2)**(-3.0*beta + 0.5)

    # model = map(lambda x, y:   range(round(imsize[1])), range(round(imsize[0])))
    # L2 = map(lambda x: round(x, 1), L)
    # try this - need arg passing
    # theta = map(math.atan2, y, x)
    # is equivalent to cycling through theta = math.atan2(y[i], x[i]])
    # (the y/x order here is atan2 specific, simply supply arrays as needed!)

    if data == None:
        return model
    else:
        residuals = data - model

        # is this biasing?
        residuals = residuals / errors

        # residuals[where(negative(isfinite(residuals)))] = 1.0e15
        # residuals[where(negative(isfinite(residuals)))] = 0.0

    SAVE_DEBUG=False
    if SAVE_DEBUG:
        ######################################################################
        # get a header
        fname='pn-test.fits'
        hdu = pyfits.open(fname)
        hdr = hdu[0].header

        hdu = pyfits.PrimaryHDU(residuals, hdr)    # extension - array, header
        hdulist = pyfits.HDUList([hdu])                  # list all extensions here
        hdulist.writeto('resids.fits', clobber=True)

        hdu = pyfits.PrimaryHDU(model, hdr)    # extension - array, header
        hdulist = pyfits.HDUList([hdu])                  # list all extensions here
        hdulist.writeto('model.fits', clobber=True)

        hdu = pyfits.PrimaryHDU(data, hdr)    # extension - array, header
        hdulist = pyfits.HDUList([hdu])                  # list all extensions here
        hdulist.writeto('data.fits', clobber=True)

        hdu = pyfits.PrimaryHDU(errors, hdr)    # extension - array, header
        hdulist = pyfits.HDUList([hdu])                  # list all extensions here
        hdulist.writeto('errors.fits', clobber=True)
        ######################################################################

    return ravel(residuals)


def beta_1d_lmfit(pars, r, data_profile=None, data_profile_err=None):
    """
    Fits a 1D profile of a beta model (model created in 1D).
    Also allows to return directly residuals.

    Arguments:
    """

    # unpack parameters
    norm   = pars['norm'].value
    rcore  = pars['rcore'].value
    beta   = pars['beta'].value

    model = norm * (1.0 + (r/rcore)**2)**(-3.0*beta+0.5)

    if data_profile == None:
        return model
    else:
        residuals = data_profile - model

        # is this biasing?
        residuals = residuals / data_profile_err

        return residuals


def beta_2d_lmfit_profile(pars, imsize=None, data_profile=None, data_profile_err=None):
    """
    Fits the surface brightness profile by creating a 2D model of the
    image.
    No psf, or bg.
    Also allows to return directly residuals.

    Arguments:
    """

    # unpack parameters
    norm   = pars['norm'].value
    rcore  = pars['rcore'].value
    beta   = pars['beta'].value
    xcen   = pars['xcen'].value
    ycen   = pars['ycen'].value

    # model in 2d and extract profile
    import time
    t1 = time.clock()
    model_image = make_2d_beta(imsize, xcen, ycen, norm, rcore, beta)
    t2 = time.clock()
    print "beta inside minimize took: ", t2-t1, " s"

    t1 = time.clock()
    (r, profile, geometric_area) = extract_profile_generic(model_image, xcen, ycen)
    model_profile = profile / geometric_area
    t2 = time.clock()
    print "extract inside minimize took: ", t2-t1, " s"


    if data_profile == None:
        return (r, model_profile)
    else:
        residuals = data_profile - model_profile

        # is this biasing?
        residuals = residuals / data_profile_err
        # print xcen, ycen, rcore

        return residuals

def make_2d_beta_psf(pars, imsize, xsize_obj, ysize_obj, instrument, theta, energy, APPLY_PSF, DO_ZERO_PAD):
    """
    Creates a 2D image of a beta model convolved with psf
    Arguments:
    """

    print 30*"#"
    print "pars:"
    print pars, imsize, xsize_obj, ysize_obj, instrument, theta, energy, APPLY_PSF, DO_ZERO_PAD
    print 30*"#"

    xcen  = pars['xcen'].value
    ycen  = pars['ycen'].value
    norm  = pars['norm'].value
    rcore = pars['rcore'].value
    beta  = pars['beta'].value

    im = zeros(imsize, dtype=double)

    import time
    t1 = time.clock()

    im_beta = make_2d_beta(imsize, xcen, ycen, norm, rcore, beta)
    # FIXME: CRITICAL  - verify if this is where you want to have it
    # in case of convolution you'd like to have a 0 border to avoid edge effects

    t2 = time.clock()
    print "1. beta took: ", t2-t1, " s"

    if DO_ZERO_PAD: im_beta = zero_pad_image(im_beta, xsize_obj)

    im_output = im_beta

    if APPLY_PSF:
    # create PSF
        t1 = time.clock()
        im_psf = make_2d_king(imsize, xcen, ycen, instrument, theta, energy)
        t2 = time.clock()
        print "psf took: ", t2-t1, " s"

        # convolve
        t1 = time.clock()
        im_output = fftconvolve(im_beta.astype(float), im_psf.astype(float), mode = 'same')
        im_output = trim_fftconvolve(im_output)
        t2 = time.clock()
        print "convolve took: ", t2-t1, " s"

    return im_output


def beta_psf_2d_lmfit_profile(pars, imsize, xsize_obj, ysize_obj, instrument, theta, energy, APPLY_PSF, DO_ZERO_PAD, data_profile=None, data_profile_err=None):
    """
    Fits the surface brightness profile by creating a 2D model of the
    image - beta model x psf
    No bg.
    Also allows to return directly residuals.
    """

    # unpack parameters
    xcen   = pars['xcen'].value
    ycen   = pars['ycen'].value
    norm   = pars['norm'].value
    rcore  = pars['rcore'].value
    beta   = pars['beta'].value

    import time
    t1 = time.clock()

    # model in 2d image beta x PSF = and extract profile
    model_image = make_2d_beta_psf(pars, imsize, xsize_obj, ysize_obj,
                                   instrument, theta, energy,
                                   APPLY_PSF, DO_ZERO_PAD)

    input_im, hdr = load_fits_im("t1.fits")
    hdu = pyfits.PrimaryHDU(model_image, hdr)    # extension - array, header
    hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    hdulist.writeto('test.fits', clobber=True)

    t2 = time.clock()
    print "beta inside minimize took: ", t2-t1, " s"

    # # extract the profile
    # (r, profile, geometric_area) = extract_profile_generic(model_image, xcen, ycen)
    # model_profile = profile / geometric_area

    # this is the new version
    xcen_obj = xsize_obj / 2
    ycen_obj = ysize_obj / 2
    # we want just the relevant part of the image
    # data = model_image[ycen-ysize_obj/2:ycen+ysize_obj/2, xcen-xsize_obj/2:xcen+xsize_obj/2]
    data = model_image

    # (r, profile, geometric_area) = extract_profile_generic(data, xcen_obj, ycen_obj)
    # model_profile = profile / geometric_area

    #ADDED SPEED#####################################################################
    # setup data for the profile extraction - for speedup
    distmatrix = distance_matrix(data, xcen_obj, ycen_obj).astype(int) # need int for bincount
    r_length = data.shape[0]/2 + 1
    r = arange(0, r_length, 1.0)
    (profile, geometric_area) = extract_profile_fast(data, distmatrix, xcen_obj, ycen_obj)
    model_profile = profile[0:r_length] / geometric_area[0:r_length]    # trim the corners
    #ADDED SPEED#####################################################################

    if data_profile == None:
        return (r, model_profile)
    else:
        residuals = data_profile - model_profile
        # is this biasing?
        # residuals = residuals / data_profile_err
        # print norm, xcen, ycen, rcore

        return residuals
