#!/usr/bin/env python
import sys
import os
import math
import pyfits
import time
from numpy import *
from scipy.signal import fftconvolve
from pylab import rc
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, LogLocator
from sb_utils import sqdistance, distance_matrix, load_fits_im, extract_profile_fast, extract_profile_fast2
from test_2d_im import make_2d_beta, extract_profile_generic, make_2d_king, make_2d_king_old, trim_fftconvolve, zero_pad_image
from scipy import integrate
from scipy.stats import poisson


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

    r2 = zeros(imsize, dtype=double)

    # I've tested a version with list comprehension and was a tiny bit
    # *slower*

    for i in range(round(imsize[0])):
        for j in range(round(imsize[1])):
            r2[i, j] = sqdistance(xcen, ycen, j , i) # this is already squared

    model = norm * (1.0 + r2/(rcore)**2)**(-3.0*beta + 0.5)


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
    t1 = time.clock()
    model_image = make_2d_beta(imsize, xcen, ycen, norm, rcore, beta)
    t2 = time.clock()
    print "beta inside minimize took: ", t2-t1, " s"

    ######################################################################
    # original extraction
    # t1 = time.clock()
    # (r, profile, geometric_area) = extract_profile_generic(model_image, xcen, ycen)
    # model_profile = profile / geometric_area
    # t2 = time.clock()
    # print "extract inside minimize took: ", t2-t1, " s"
    ######################################################################


    #ADDED SPEED#####################################################################
    # setup data for the profile extraction - for speedup
    t1 = time.clock()
    distmatrix = distance_matrix(data, xcen_obj, ycen_obj).astype(int) # need int for bincount
    r_length = data.shape[0]/2 + 1
    r = arange(0, r_length, 1.0)
    (profile, geometric_area) = extract_profile_fast(data, distmatrix, xcen_obj, ycen_obj)
    model_profile = profile[0:r_length] / geometric_area[0:r_length]    # trim the corners
    t2 = time.clock()
    print "extract inside minimize took: ", t2-t1, " s"
    #ADDED SPEED#####################################################################

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
    # FIXME: the _object coordinates are not needed anymore

    # hdr = pyfits.getheader('pn-test.fits') # FIXME: would be better to create a fits header from scratch

    xcen  = pars['xcen'].value
    ycen  = pars['ycen'].value
    norm  = pars['norm'].value
    rcore = pars['rcore'].value
    beta  = pars['beta'].value

    t1 = time.clock()

    im_beta = make_2d_beta(imsize, xcen, ycen, norm, rcore, beta)

    # hdu = pyfits.PrimaryHDU(im_beta, hdr)    # extension - array, header
    # hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    # hdulist.writeto('tmpa.fits', clobber=True)

    # if DO_ZERO_PAD: im_beta = zero_pad_image(im_beta, xsize_obj)

    # hdu = pyfits.PrimaryHDU(im_beta, hdr)    # extension - array, header
    # hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    # hdulist.writeto('tmp0.fits', clobber=True)

    im_output = im_beta

    if APPLY_PSF:
        # create PSF
        im_psf = make_2d_king_old(imsize, xcen, ycen, instrument, theta, energy)

        # convolve
        im_output = fftconvolve(im_beta.astype(float), im_psf.astype(float), mode = 'same')
        im_output = trim_fftconvolve(im_output)

    return im_output

def v06_funct(r, rc, rs, n0, alpha, beta, gamma, epsilon):
    """
    The integration kernel of the vikhlinin06 model (i.e. the n_p *
    n_e) as a function of 3D radius. Following andersson11 does not
    include the central beta model.
    """
    rn = r / rc                 # normed radius

    denominator = (1.0 + rn**2)**(3*beta - alpha/2.0) * (1.0 + (r/rs)**gamma)**(epsilon/gamma)
    f = n0**2 * rn**(-1*alpha) / denominator

    return f

def v06_funct_los(l, b, rc, rs, n0, alpha, beta, gamma, epsilon):
    """
    The integration kernel of the vikhlinin06 model (i.e. the n_p *
    n_e) as a function of LOS depth at fixed projected
    distance. Following andersson11 does not include the central beta
    model.

    Arguments:
    - 'l': LOS depth
    - 'b': projected distance ("impact" parameter)
    """

    r = sqrt(l**2 + b**2)       # convert (l, b) -> r (3D radius)
    rn = r / rc                 # normed radius

    denominator = (1.0 + rn**2)**(3*beta - alpha/2.0) * (1.0 + (r/rs)**gamma)**(epsilon/gamma)
    f = n0**2 * rn**(-1*alpha) / denominator

    return f

def v06_full_funct(r, rc, rs, n0, alpha, beta, gamma, epsilon, n02, rc2, beta2):
    """
    The integration kernel of the vikhlinin06 model (i.e. the n_p *
    n_e) as a function of 3D distance. Includes the central beta
    model.
    """
    rn = r / rc                 # normed radius

    denominator = (1.0 + rn**2)**(3*beta - alpha/2.0) * (1.0 + (r/rs)**gamma)**(epsilon/gamma)
    f = n0**2 * rn**(-1*alpha) / denominator + n02**2 / (1.0 + (r/rc2)**2)**(3.0*beta2)

    return f

def v06_full_funct_los(l, b, rc, rs, n0, alpha, beta, gamma, epsilon, n02, rc2, beta2):
    """
    The integration kernel of the vikhlinin06 model (i.e. the n_p *
    n_e) as a function of LOS depth at fixed projected
    distance. Includes the central beta model.

    Arguments:
    - 'l': LOS depth
    - 'b': projected distance ("impact" parameter)
    """

    r = sqrt(l**2 + b**2)       # convert (l, b) -> r (3D radius)
    rn = r / rc                 # normed radius

    denominator = (1.0 + rn**2)**(3*beta - alpha/2.0) * (1.0 + (r/rs)**gamma)**(epsilon/gamma)
    f = n0**2 * rn**(-1*alpha) / denominator + n02**2 / (1.0 + (r/rc2)**2)**(3.0*beta2)

    return f

def make_2d_v06(distmatrix, bgrid, r500, rc, rs, n0, alpha, beta, gamma, epsilon):
    """
    Creates a 2D image of a projected v06 model (cylindrical
    projection)

    Arguments:
    """

    rmin = 1    # minimal radius seems to be 10kpc need only for
                # plotting

    lmin = 0
    lmax = 3.0 * r500

    # do the LOS integration
    dens_prof_los = [integrate.quad(v06_funct_los, lmin, lmax,
                             args=(b, rc, rs, n0, alpha, beta, gamma, epsilon))[0]
              for b in bgrid]

    # create the 2d image
    im = zeros(distmatrix.shape)
    for i, b in enumerate(bgrid):
        im[where(distmatrix==b)] =  dens_prof_los[i]

    return im

def make_2d_v06_psf(pars, distmatrix, bgrid, r500, psf_pars):
    """
    Creates a 2D image of a vikhlinin et al. 2006 model convolved with psf.
    """
    APPLY_PSF = True

    rc = pars['rc'].value
    rs = pars['rs'].value
    n0 = pars['n0'].value
    alpha = pars['alpha'].value
    beta = pars['beta'].value
    gamma = pars['gamma'].value
    epsilon = pars['epsilon'].value

    im_output = make_2d_v06(distmatrix, bgrid, r500, rc, rs, n0,
                            alpha, beta, gamma, epsilon)

    if APPLY_PSF:
        # create PSF
        im_psf = make_2d_king(distmatrix, psf_pars[0], psf_pars[1],
                              psf_pars[2])

        # convolve
        im_output = fftconvolve(im_output.astype(float),
                                im_psf.astype(float), mode = 'same')
        im_output = trim_fftconvolve(im_output)

    return im_output


def beta_psf_2d_lmfit_profile(pars, imsize, xsize_obj, ysize_obj,
                              instrument, theta, energy, APPLY_PSF,
                              DO_ZERO_PAD, data_profile=None,
                              data_profile_err=None):
    """
    Fits the surface brightness profile by creating a 2D model of the
    image - beta model x psf
    No bg.
    Also allows to return directly residuals.
    """
    USE_ERROR=True             # debug option

    # model in 2d image beta x PSF = and extract profile
    model_image = make_2d_beta_psf(pars, imsize, xsize_obj, ysize_obj,
                                   instrument, theta, energy,
                                   APPLY_PSF, DO_ZERO_PAD)

    # this is the new version
    xcen_obj = xsize_obj / 2
    ycen_obj = ysize_obj / 2
    # we want just the relevant part of the image
    # data = model_image[ycen-ysize_obj/2:ycen+ysize_obj/2, xcen-xsize_obj/2:xcen+xsize_obj/2]
    data = model_image

    # setup data for the profile extraction - for speedup
    distmatrix = distance_matrix(data, xcen_obj, ycen_obj).astype(int) # need int for bincount
    r_length = data.shape[0]/2 + 1

    # r = arange(0, r_length, 1.0)   # original line: before 2013-03-13
    r = arange(1.0, r_length+1, 1.0)

    (profile, geometric_area) = extract_profile_fast(data, distmatrix, xcen_obj, ycen_obj)
    model_profile = profile[0:r_length] / geometric_area[0:r_length]    # trim the corners

    if data_profile == None:
        return (r, model_profile)
    else:
        residuals = data_profile - model_profile
        # is this biasing?
        if USE_ERROR: residuals = residuals / data_profile_err

        return residuals


def v06_psf_2d_lmfit_profile(pars,distmatrix,bgrid,r500,psf_pars,
                             xcen_obj,ycen_obj,data_profile=None,
                             data_profile_err=None):
    """
    Fits the surface brightness profile by creating a 2D model of the
    image - v06 model (without the central beta model) x psf
    No bg.
    Also allows to return directly residuals.
    """
    USE_ERROR=True             # debug option

    # make first a 2D image
    model_image = make_2d_v06_psf(pars, distmatrix, bgrid, r500,
                                  psf_pars)

    # FIXME: is this necessary for each step?
    # trim distmatrix size to image post convolution
    distmatrix = roll(roll(distmatrix,2,axis=0),2,axis=1)
    distmatrix = trim_fftconvolve(distmatrix)

    # profile extraction
    r_length = r500             # factor out r500
    r = arange(0, r_length, 1.0)

    (profile, geometric_area) = extract_profile_fast2(model_image, distmatrix, bgrid)
    model_profile = profile[0:r_length] / geometric_area[0:r_length]    # trim the corners

    # print '*'*30
    # print len(r), len(model_profile)
    # print len(profile[0:r_length]), r_length
    # # print len(data_profile[0:r_length]), len(model_profile), r500, r_length
    # print '*'*30
    # # from time import sleep
    # # sleep(100)


    if data_profile == None:
        # return (r, model_profile, geometric_area)
        return (r, model_profile)
    else:
        residuals = data_profile[0:r_length] - model_profile
        # is this biasing?
        if USE_ERROR: residuals = residuals / data_profile_err[0:r_length]

        # return residuals
        return residuals


def make_synthetic_observation(srcmodel_file, expmap_file, bgmap_file, maskmap_file, outfile):
    """
    Take a synthetic sb model and turn it into a "observation" by
    applying an exposure map, bg image and mask.

    'srcmodel' - model of the source poissonized in units [cts],
                 normed to required total cts
    'expmap' - exposure map
    'bgmap' - background map (smooth, units cts)
    'maskmap' - mask
    """
    POISSONIZE_IMAGE = False

    # load images
    srcmodel, hdr = load_fits_im(srcmodel_file)
    expmap, hdr = load_fits_im(expmap_file)
    bgmap, hdr = load_fits_im(bgmap_file)
    maskmap, hdr = load_fits_im(maskmap_file, 1) # mask is in ext1


    # trim sizes if necessary (should be needed only in case of
        # manual testing)

    if srcmodel.shape[0] == expmap.shape[0]-2:
        expmap = trim_fftconvolve(expmap)
    if srcmodel.shape[0] == bgmap.shape[0]-2:
        bgmap = trim_fftconvolve(bgmap)
    if srcmodel.shape[0] == maskmap.shape[0]-2:
        maskmap = trim_fftconvolve(maskmap)

    # # do the rescaling to the fft image
    # expmap = trim_fftconvolve(expmap)
    # bgmap = trim_fftconvolve(bgmap)
    # maskmap = trim_fftconvolve(maskmap)

    # do the transforms
    bgmap_poi = bgmap * maskmap     # get rid of artifacts
    ids = where(bgmap_poi != 0.0)

    if POISSONIZE_IMAGE:
        bgmap_poi[ids] = poisson.rvs(bgmap[ids])

    output_im = srcmodel * expmap + bgmap_poi # output is in cts (cts/pix in each pixel)
    output_im = output_im * maskmap

    # save output
    hdu = pyfits.PrimaryHDU(output_im, hdr)    # extension - array, header
    hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    hdulist.writeto(outfile, clobber=True)
