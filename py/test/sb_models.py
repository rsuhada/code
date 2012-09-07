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
from sb_utils import sqdistance
from test_2d_im import make_2d_beta, extract_profile_generic

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
    model_image = make_2d_beta(imsize, xcen, ycen, norm, rcore, beta)

    (r, profile, geometric_area) = extract_profile_generic(model_image, xcen, ycen)
    model_profile = profile / geometric_area

    if data_profile == None:
        return (r, model_profile)
    else:
        residuals = data_profile - model_profile

        # is this biasing?
        # residuals = residuals / data_profile_err

        return residuals
