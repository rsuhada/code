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
from sb_plotting_utils import *
from sb_utils import *
from scipy.signal import fftconvolve
from scipy import delete
from scipy import integrate
from scipy.stats import poisson
import minuit
import time

def get_instrument_id(instrument):
    """
    Return an instrument id number. Needed because of minuit.

    Arguments:
    - `instrument`: string
    """

    instrument_list = {
        'pn':0,
        'm1':1,
        'm2':2,
        'chandra':3
        }

    return instrument_list[instrument]

def resolve_instrument_id(instrument_id):
    """
    Return an instrument given the id number. Needed because of minuit.

    Arguments:
    - `instrument`: string
    """

    instrument_list = (
        "pn",
        "m1",
        "m2",
        "chandra"
        )

    return instrument_list[instrument_id]

def make_2d_dirac(imsize, xcen, ycen):
    """
    Creates a 2D image of a Dirac funtion

    Arguments:
    - `imsize`: input 2D array size
    - `xcen`: x coordinate of the function
    - `ycen`: y coordinate of the function
    """

    im = zeros(imsize, dtype=double)
    im[xcen, ycen] = 1.0

    return im

def make_2d_uncorr_gauss(imsize, xcen, ycen, sigmax, sigmay):
    """
    Creates a 2D Gaussian (no correlation)

    Arguments:
    - `imsize`: input 2D array size
    - `xcen`: x coordinate of the function
    - `ycen`: y coordinate of the function
    - 'sigmax': sigma in x direction
    - 'sigmay': sigma in y direction
    """

    im = zeros(imsize, dtype=double)
    for i in range(imsize[0]):
        for j in range(imsize[1]):
            im[i, j] = exp(-1.0 * ((j - xcen)**2/(2.0*sigmax**2))) * exp(-1.0 * ((i - ycen)**2/(2.0*sigmay**2)))

    return im

def king_2d_model(x, y, xcen, ycen, rcore, alpha):
    """
    Returns the value of a King profile at given position (relative to
    the center). Function is useful e.g. for integration.

    Arguments:
    - `x`: x coordinate
    - `y`: y coordinate
    - `xcen`: x coordinate of the function
    - `ycen`: y coordinate of the function
    - `rcore`: King core radius
    - `alpha`: King alpha slope
    """
    r2 = sqdistance(xcen, ycen, x , y) # this is already squared
    out = 1.0 / ( 1.0 + ( r2/rcore**2 )**alpha )
    return out

def trim_fftconvolve(image):
    """
    Removes invalid rows and columns from a convolved image after
    fftconvolve with the "same" option.

    Arguments:
    - `image`: input image for trimming
    """

    # remove invalid edge
    image = delete(image, 0, 0)
    image = delete(image, 0, 1)
    image = delete(image, image.shape[1]-1, 0)
    image = delete(image, image.shape[0]-1, 1)

    return image

def make_2d_king(imsize, xcen, ycen, instrument, theta, energy):
    """
    Creates a 2D image of the PSF

    Arguments:
    - `imsize`: input 2D array size
    - `xcen`: x coordinate of the function
    - `ycen`: y coordinate of the function
    - 'energy': energy [keV]
    - 'theta': offaxis angle [arcmin]
    """

    # see notes at make_2d_beta
    r2 = zeros(imsize, dtype=double)
    (rcore, alpha) = get_psf_king_pars(instrument, energy, theta)

    # the dumb method
    for i in range(imsize[0]):
        for j in range(imsize[1]):
            r2[i, j] = sqdistance(xcen, ycen, j , i) # this is already squared

    im = 1.0 / ( 1.0 + r2/rcore**2 )**alpha

    # normalization calculation
    # from model: to inf converges slowly
    # norm = integrate.dblquad(king_2d_model, 0.0, Inf, lambda y:0.0, lambda y:Inf, args=(xcen, ycen, rcore, alpha))[0]    # to inf - not recommended
    # print norm
    #
    # norm = integrate.dblquad(king_2d_model, 0.0, imsize[0], lambda y:0.0, lambda y:imsize[1], args=(xcen, ycen, rcore, alpha))[0] # to image size
    # print norm

    # simpler version using the data itself - probably the most
    # appropriate in this case
    norm = im.sum()

    im = im / norm
    return im

def make_2d_beta(imsize, xcen, ycen, norm, rcore, beta):
    """
    Creates a 2D image of a beta model

    Arguments:
    - `imsize`: input 2D array size
    - `xcen`: x coordinate of the function
    - `ycen`: y coordinate of the function
    - 'core': beta model core radius
    - 'beta': beta model slope
    """
    r2 = zeros(imsize, dtype=double)
    # FIXME: refactor to pass distmatrix

    for i in range(imsize[0]):
        for j in range(imsize[1]):
            r2[i, j] = sqdistance(xcen, ycen, j , i) # this is already squared

    im = norm * (1.0 + r2/(rcore)**2)**(-3.0*beta + 0.5)

    return im

def test_psf_parameter():
    """
    Test psf parameter calculation for all the instruments
    """

    ######################################################################
    # PSF testing
    energy = 1.5
    theta = 0.3

    instrument=("pn", "m1", "m2")

    plot_king_model_psf(energy, theta, instrument)

    for i in instrument:
        print i
        (rcore, alpha) = get_psf_king_pars(i, energy, theta)
        print rcore, alpha

    print "done"

def test_create_dirac():
    """
    Create a dirac 2D, save to fits
    """
    # get a header
    fname = 'pn-test.fits'
    hdu = pyfits.open(fname)
    hdr = hdu[0].header

    imname = 'dirac.fits'
    xsize = 900
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    im_dirac = make_2d_dirac((xsize, ysize), xcen, ycen)

    # make hardcopy
    hdu = pyfits.PrimaryHDU(im_dirac, hdr)    # extension: array, header
    hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    hdulist.writeto(imname, clobber=True)

def test_create_gauss():
    """
    Create two test 2D gauss, save to fits.
    """

    # get a header
    fname = 'pn-test.fits'
    hdu = pyfits.open(fname)
    hdr = hdu[0].header

    xsize = 300
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    # if zero padded image for testing - this to check normalizations
    DO_ZERO_PAD = True
    xsize_obj = 100
    ysize_obj = xsize_obj

     # first gauss - the "source"
    imname = 'gauss-a-100-pad.fits'
    peak_scale = 0.0045         # arbitrary src height - just so that
                                # it can be conveniently plotted

    im_gauss = peak_scale*make_2d_uncorr_gauss((xsize, ysize), xcen, ycen, a_sigmax, a_sigmay)

    if DO_ZERO_PAD:
        im_gauss[:, 0:xsize_obj] = 0.0
        im_gauss[:, xsize-xsize_obj:] = 0.0
        im_gauss[0:xsize_obj,:] = 0.0
        im_gauss[xsize-xsize_obj:,:] = 0.0

    src_norm = im_gauss.sum()

    # make hardcopy
    hdu = pyfits.PrimaryHDU(im_gauss, hdr)    # extension: array, header
    hdulist = pyfits.HDUList([hdu])           # list all extensions here
    hdulist.writeto(imname, clobber=True)

    # second gauss - "the PSF" - i.e. normed to 1
    imname = 'gauss-b-100-pad.fits'
    im_gauss = make_2d_uncorr_gauss((xsize, ysize), xcen, ycen, b_sigmax, b_sigmay)
    if DO_ZERO_PAD:
        im_gauss[:, 0:xsize_obj] = 0.0
        im_gauss[:, xsize-xsize_obj:] = 0.0
        im_gauss[0:xsize_obj,:] = 0.0
        im_gauss[xsize-xsize_obj:,:] = 0.0

    im_gauss = im_gauss / im_gauss.sum()

    # make hardcopy
    hdu = pyfits.PrimaryHDU(im_gauss, hdr)    # extension: array, header
    hdulist = pyfits.HDUList([hdu])           # list all extensions here
    hdulist.writeto(imname, clobber=True)

    # combined gauss - for checking - norm to "source"
    imname = 'gauss-c-100-pad.fits'
    im_gauss = make_2d_uncorr_gauss((xsize, ysize), xcen, ycen, c_sigmax, c_sigmay)
    im_gauss = src_norm * im_gauss / im_gauss.sum()

    # make hardcopy
    hdu = pyfits.PrimaryHDU(im_gauss, hdr)    # extension: array, header
    hdulist = pyfits.HDUList([hdu])           # list all extensions here
    hdulist.writeto(imname, clobber=True)

def test_create_psf():
    """
    Create a 2D psf image, save to fits.
    """
    # get a header
    fname = 'pn-test.fits'
    hdu = pyfits.open(fname)
    hdr = hdu[0].header

    imname = 'psf-100-pad.fits'
    xsize = 900
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    # if zero padded image for testing - this to check normalizations
    DO_ZERO_PAD = False
    xsize_obj = 100
    ysize_obj = xsize_obj

    im_psf = make_2d_king((xsize, ysize), xcen, ycen, instrument, theta, energy)
    if DO_ZERO_PAD:
        im_psf[:, 0:xsize_obj] = 0.0
        im_psf[:, xsize-xsize_obj:] = 0.0
        im_psf[0:xsize_obj,:] = 0.0
        im_psf[xsize-xsize_obj:,:] = 0.0

    # make hardcopy
    hdu = pyfits.PrimaryHDU(im_psf, hdr)    # extension: array, header
    hdulist = pyfits.HDUList([hdu])         # list all extensions here
    hdulist.writeto(imname, clobber=True)

def test_create_beta():
    """
    Create a 2D beta image, save to fits
    """
    # get a header
    fname = 'pn-test.fits'
    hdu = pyfits.open(fname)
    hdr = hdu[0].header

    imname = 'beta-100-pad.fits'
    xsize = 900
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    # if zero padded image for testing - this to check normalizations
    # - works fine
    DO_ZERO_PAD = False
    xsize_obj = 100
    ysize_obj = xsize_obj

    im_beta = make_2d_beta((xsize, ysize), xcen, ycen, norm, rcore, beta)
    if DO_ZERO_PAD:
        im_beta[:, 0:xsize_obj] = 0.0
        im_beta[:, xsize-xsize_obj:] = 0.0
        im_beta[0:xsize_obj,:] = 0.0
        im_beta[xsize-xsize_obj:,:] = 0.0

    # make hardcopy
    hdu = pyfits.PrimaryHDU(im_beta, hdr)# extension: array, header
    hdulist = pyfits.HDUList([hdu])          # list all extensions here
    hdulist.writeto(imname, clobber=True)

def test_profile_dirac():
    """
    Load and plot a 2D dirac
    """
    imname = 'dirac-100.fits'
    hdu = pyfits.open(imname)
    im_dirac = hdu[0].data
    hdr = hdu[0].header

    xsize = im_dirac.shape[0]
    ysize = im_dirac.shape[1]
    xcen = xsize/2
    ycen = ysize/2

    (r, profile, geometric_area) = extract_profile_generic(im_dirac, xcen, ycen)

    MAKE_PLOT=True
    if MAKE_PLOT:
        print "plotting dirac"
        plt.figure()
        plt.ion()
        plt.clf()
        plt.plot(r-0.5, profile/geometric_area)

        plt.xscale("linear")
        plt.yscale("linear")
        plt.draw()
        plt.show()
        plt.get_current_fig_manager().window.wm_geometry("+1100+0")
        plt.show()

def test_profile_psf():
    """
    Load and plot a 2D psf
    """
    ######################################################################
    # model check - PSF

    imname = 'psf-100.fits'
    hdu = pyfits.open(imname)
    im_psf = hdu[0].data
    hdr = hdu[0].header

    xsize = im_psf.shape[0]
    ysize = im_psf.shape[1]
    xcen = xsize/2
    ycen = ysize/2

    (r, profile, geometric_area) = extract_profile_generic(im_psf, xcen, ycen)
    (rcore_model, alpha_model) = get_psf_king_pars(instrument, energy, theta)
    r_model = linspace(0.0, r.max(), 100)
    psf_model = king_profile(r_model, rcore_model, alpha_model)

    MAKE_PLOT=True
    if MAKE_PLOT:
        print "plotting psf"
        plt.figure()
        plt.ion()
        plt.clf()
        plt.plot(r-0.5, profile/geometric_area)
        plt.plot(r_model, psf_model,
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
        plt.draw()
        plt.show()
        plt.get_current_fig_manager().window.wm_geometry("+1100+0")
        plt.show()

def test_profile_beta():
    """
    Load and plot a 2D beta
    """
    imname = 'beta-100-pad.fits'
    hdu = pyfits.open(imname)
    im_beta = hdu[0].data
    hdr = hdu[0].header

    xsize = im_beta.shape[0]
    ysize = im_beta.shape[1]
    xcen = xsize/2
    ycen = ysize/2

    (r, profile, geometric_area) = extract_profile_generic(im_beta, xcen, ycen)
    r_model = linspace(0.0, r.max(), 1000)

    beta_profile = beta_model((1.0, rcore, beta),r_model)

    MAKE_PLOT=True
    if MAKE_PLOT:
        print "plotting beta"
        plt.figure()
        plt.ion()
        plt.clf()
        plt.plot(r - 0.5, profile/geometric_area, marker='o')
        plt.plot(r_model, beta_profile,
            color='black',
            linestyle='-',              # -/--/-./:
            linewidth=1,                # linewidth=1
            marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
            markerfacecolor='black',
            markersize=0,               # markersize=6
            label=r"data"               # '__nolegend__'
            )
        plt.xscale("log")
        plt.yscale("log")
        plt.draw()
        plt.show()
        plt.get_current_fig_manager().window.wm_geometry("+1100+0")

def test_convolve_psf_gauss():
    """
    Test gaussian convolution
    """

    imname = 'gauss-a-100-pad.fits'
    hdu = pyfits.open(imname)
    im_gauss_a = hdu[0].data
    hdr = hdu[0].header

    imname = 'gauss-b-100-pad.fits'
    hdu = pyfits.open(imname)
    im_gauss_b = hdu[0].data
    hdr = hdu[0].header

    imname = 'gauss-c-100-pad.fits'
    hdu = pyfits.open(imname)
    im_gauss_c = hdu[0].data
    hdr = hdu[0].header

    xsize = im_gauss_a.shape[0]
    ysize = im_gauss_a.shape[1]
    xcen = xsize/2
    ycen = ysize/2

    print "size:", xsize

    # do the convolution: test on gaussian convolution, works very
    # good assuming large enough aperture/trimming
    # NOTE: "valid" range is not working for me

    im_conv_gauss = fftconvolve(im_gauss_a.astype(float), im_gauss_b.astype(float), mode = 'same')
    print "norm % diff:", 100.0*(im_gauss_a.sum() - im_conv_gauss.sum()) / im_conv_gauss.sum()

    im_conv_gauss = trim_fftconvolve(im_conv_gauss)

    # save to a file
    imname = 'conv-gauss-ab-100.fits'
    hdu = pyfits.PrimaryHDU(im_conv_gauss, hdr)    # extension - array, header
    hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    hdulist.writeto(imname, clobber=True)

    # extract profile
    (r, profile_a, geometric_area_a)       = extract_profile_generic(im_gauss_a, xcen, ycen)
    (r, profile_b, geometric_area_b)       = extract_profile_generic(im_gauss_b, xcen, ycen)
    (r, profile_c, geometric_area_c)       = extract_profile_generic(im_gauss_c, xcen, ycen)
    (r, profile_conv, geometric_area_conv) = extract_profile_generic(im_conv_gauss, xcen, ycen)

    # do the plot
    MAKE_PLOT=True
    if MAKE_PLOT:
        print "plotting gauss"
        plt.figure()
        plt.ion()
        plt.clf()

        plt.plot(r-0.5, profile_a/geometric_area_a, label=r"$\sigma = $"+str(a_sigmax))
        plt.plot(r-0.5, profile_b/geometric_area_b, label=r"$\sigma = $"+str(b_sigmax)+ " (psf)")
        plt.plot(r-0.5, profile_conv/geometric_area_conv, label=r"conv-data")

        plt.plot(r[::10]-0.5, profile_c[::10]/geometric_area_c[::10],
            color='black',
            linestyle='',              # -/--/:/-.
            linewidth=0,                # linewidth=1
            marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
            markerfacecolor='orange',
            markersize=6,               # markersize=6
            label="$\sigma = $"+str(c_sigmax)               # '__nolegend__'
            )

        plt.xscale("linear")
        plt.yscale("linear")

        prop = matplotlib.font_manager.FontProperties(size=16)  # size=16
        plt.legend(loc=0, prop=prop, numpoints=1)

        plt.draw()
        plt.get_current_fig_manager().window.wm_geometry("+1100+0")
        plt.show()

        plt.savefig('psf_conv_test_gauss.png')

def test_convolve_psf_beta():
    """
    Test convolution: beta x psf
    """
    imname = 'beta-100-pad.fits'
    hdu = pyfits.open(imname)
    im_beta = hdu[0].data
    hdr = hdu[0].header

    imname = 'psf-100-pad.fits'
    hdu = pyfits.open(imname)
    im_psf = hdu[0].data
    hdr = hdu[0].header

    xsize = im_beta.shape[0]
    ysize = im_beta.shape[1]
    xcen = xsize/2
    ycen = ysize/2

    im_conv = fftconvolve(im_beta.astype(float), im_psf.astype(float), mode = 'same')
    im_conv = trim_fftconvolve(im_conv)

    # save into a file
    imname = 'conv-beta-psf-100.fits'
    hdu = pyfits.PrimaryHDU(im_conv, hdr)    # extension - array, header
    hdulist = pyfits.HDUList([hdu])          # list all extensions here
    hdulist.writeto(imname, clobber=True)

    ######################################################################
    # test part
    print "psf norm : ", im_psf.sum()
    print "norm % diff:", 100.0*(im_beta.sum() - im_conv.sum()) / im_beta.sum()

    ######################################################################
    # extract profile
    (r, profile_source, geometric_area_source) = extract_profile_generic(im_beta, xcen, ycen)
    (r, profile_psf, geometric_area_psf)       = extract_profile_generic(im_psf, xcen, ycen)
    (r, profile_conv, geometric_area_conv)     = extract_profile_generic(im_conv, xcen, ycen)

    profile_source_norm = profile_source/geometric_area_source
    profile_psf_norm    = profile_psf/geometric_area_psf
    profile_conv_norm   = profile_conv/geometric_area_conv

    profile_psf_norm = profile_psf_norm * profile_source_norm.max() / profile_psf_norm.max()

    # do the plot
    MAKE_PLOT=True
    if MAKE_PLOT:
        print "plotting psf x beta"
        plt.figure()
        plt.ion()
        plt.clf()

        plt.plot(r-0.5, profile_source_norm, label=r"source")
        plt.plot(r-0.5, profile_psf_norm, label=r"psf")
        plt.plot(r-0.5, profile_conv_norm, label=r"conv-data")

        plt.xscale("log")
        plt.yscale("log")
        # plt.ylim(ymin=1e-3,ymax=5e0)

        prop = matplotlib.font_manager.FontProperties(size=16)  # size=16
        plt.legend(loc=0, prop=prop, numpoints=1)

        plt.draw()
        plt.get_current_fig_manager().window.wm_geometry("+1100+0")
        # plt.get_current_fig_manager().window.wm_geometry("+640+0")
        plt.show()

        plt.savefig('psf_conv_test_beta.png')

def load_exposure_map():
    """
    Auxiliarly map to load an exposure map
    """
    fname = 'pn-test-exp.fits'
    hdu = pyfits.open(fname)
    exp_map = trim_fftconvolve(hdu[0].data)

    # remove too low exp regions (max/10)
    exp_thresh_factor = 10.0
    ids_trim = (exp_map<exp_map.max()/exp_thresh_factor)
    exp_map[ids_trim] = 0.0

    return exp_map

def load_background_map():
    """
    Auxiliarly map to load an background map
    """
    fname = 'pn-test-bg-2cp.fits'
    hdu = pyfits.open(fname)
    background_map = trim_fftconvolve(hdu[0].data)

    return background_map

def create_background_mask(background_map):
    """
    Creates a background mask with ps and artifacts removed
    """
    # create mask - need to remove all kinds of articats
    # getting rid of an artifact value - only at this ste because
    # there is a bug in poisson that crashes on 0 valued input
    artifact=1.0e-5
    background_map[background_map==artifact] = 0.0
    image_mask = background_map / background_map
    image_mask[where(negative(isfinite(image_mask)))] = 0.0
    return image_mask

def build_sb_model_beta(xsize, ysize, xsize_obj, ysize_obj, xcen, ycen, norm, rcore, beta, instrument, theta, energy, APPLY_PSF):
    """
    Build a surface brighness model for fitting/plotting.
    """
    DO_ZERO_PAD = False

    # create beta
    im_beta = make_2d_beta((xsize, ysize), xcen, ycen, norm, rcore, beta)

    if DO_ZERO_PAD: im_beta = zero_pad_image(im_beta, xsize_obj)
    im_output = im_beta

    if APPLY_PSF:
    # create psf
        im_psf = make_2d_king((xsize, ysize), xcen, ycen, instrument, theta, energy)
        # if DO_ZERO_PAD: im_psf = zero_pad_image(im_psf, xsize_obj)

    # FIXME: this needs bit reorganizing so that the proper number of
    # source cts can be assured (while a realistc s/n is kept)
    # note: also needs exp map correction
    # add background model (pre-PSF application)

        # convolve
        im_output = fftconvolve(im_beta.astype(float), im_psf.astype(float), mode = 'same')
        im_output = trim_fftconvolve(im_output)

    return im_output

def test_create_beta_im():
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
    imname = 'beta_image_cts.fits'
    hdu = pyfits.PrimaryHDU(im_beta, hdr)    # extension - array, header
    hdulist = pyfits.HDUList([hdu])          # list all extensions here
    hdulist.writeto(imname, clobber=True)

def test_create_cluster_im():
    """
    Creates a PSF convolved beta model image with poissonizations
    """
    # settings
    APPLY_PSF = True
    POISSONIZE_IMAGE = True            # poissonize image?
    DO_ZERO_PAD = True
    APPLY_EXPOSURE_MAP = False           # add exposure map
    ADD_BACKGROUND = False

    # FIXME: add background, realistic exposure map + decide how to
    # treat for modeling work

    # get a header
    fname = 'pn-test.fits'
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

    im_conv = build_sb_model_beta(xsize, ysize, xsize_obj, ysize_obj, xcen, ycen, normalization, rcore, beta, instrument, theta, energy, APPLY_PSF)

    # smooth model - beta x PSF, no noise/background/mask
    imname = 'cluster_image_cts_model.fits'
    hdu = pyfits.PrimaryHDU(im_conv, hdr)    # extension - array, header
    hdulist = pyfits.HDUList([hdu])          # list all extensions here
    hdulist.writeto(imname, clobber=True)

    # normalization and poissonization
    im_conv = num_cts * im_conv/im_conv.sum()

    if POISSONIZE_IMAGE:
        im_conv = poisson.rvs(im_conv)
        print "poisson sum:", im_conv.sum()

    # poissonized model -  beta x PSF, poissonized, no background/mask
    imname = 'cluster_image_cts_poiss.fits'
    hdu = pyfits.PrimaryHDU(im_conv, hdr)    # extension - array, header
    hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    hdulist.writeto(imname, clobber=True)

    # add background - preliminary approach with bit fudging
    # (background not psf-ized)
    if ADD_BACKGROUND:
        background_map = load_background_map()
        exp_map = load_exposure_map()

        # poissonize
        print "poisson sum:", background_map.sum()
        if POISSONIZE_IMAGE:
            background_map_poi = poisson.rvs(background_map)

            # add to the image
            im_conv = im_conv + background_map_poi
        else:
            im_conv = im_conv + background_map

        image_mask = create_background_mask(background_map)
        im_conv = im_conv * image_mask

    # poissonized model with masking and background -  beta x PSF, poissonized, has background and masked ps
    imname = 'cluster_image_cts.fits'
    hdu = pyfits.PrimaryHDU(im_conv, hdr)    # extension - array, header
    hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    hdulist.writeto(imname, clobber=True)

    # hdu = pyfits.PrimaryHDU(image_mask, hdr)    # extension - array, header
    # hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    # hdulist.writeto('mask.fits', clobber=True)

    # apply exposure map
    if APPLY_EXPOSURE_MAP:
        if not(ADD_BACKGROUND):
            exp_map = load_exposure_map()

        im_conv_ctr = im_conv / exp_map           # create an ctr image
        im_conv_ctr[where(negative(isfinite(im_conv_ctr)))] = 0.0

        # write the output
        imname = 'cluster_image_ctr.fits'
        hdu = pyfits.PrimaryHDU(im_conv_ctr, hdr)    # extension - array, header
        hdulist = pyfits.HDUList([hdu])                  # list all extensions here
        hdulist.writeto(imname, clobber=True)


def plot_data_model_simple(r_data, profile_data,
                           r_model, profile_model,
                           output_figure, profile_data_err=None,
                           r_true=None, profile_true=None):
    """
    Simple plot of a profile: data vs model (optionally also error bars)

    Arguments:
    - `r_data`: radial grid for data
    - `profile_data`: profile data
    - `r_model`: radial grid for model
    - `profile_norm_model`: profile model
    - `ouputname`:
    """
    plt.figure()
    plt.ion()
    plt.clf()

    if any(profile_data_err):
        plt.errorbar(r_data-0.5, profile_data, profile_data_err,
        color='black',
        linestyle='',              # -/--/-./:
        linewidth=1,                # linewidth=1
        marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='black',
        markersize=6,               # markersize=6
        label=r"source"               # '__nolegend__'
        )
    else:
        plt.plot(r_data-0.5, profile_data,
        color='black',
        linestyle='',              # -/--/:/-.
        linewidth=0,                # linewidth=1
        marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='black',
        markersize=4,               # markersize=6
        label=r"source"               # '__nolegend__'
        )

    plt.plot(r_model-0.5, profile_model,
        color='red',
        linestyle='-',              # -/--/:/-.
        linewidth=1,                # linewidth=1
        marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='black',
        markersize=0,               # markersize=6
        label=r"model fit"          # '__nolegend__'
        )

    plt.plot(r_true-0.5, profile_true,
        color='green',
        linestyle='-',              # -/--/:/-.
        linewidth=1,                # linewidth=1
        marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='black',
        markersize=0,               # markersize=6
        label=r"true model"          # '__nolegend__'
        )

    plt.xscale("linear")
    plt.yscale("linear")
    # plt.ylim(ymin=1e-3,ymax=5e0)

    prop = matplotlib.font_manager.FontProperties(size=16)  # size=16
    plt.legend(loc=0, prop=prop, numpoints=1)

    plt.draw()
    plt.get_current_fig_manager().window.wm_geometry("+1100+0")
    # plt.get_current_fig_manager().window.wm_geometry("+640+0")
    plt.show()
    plt.savefig(output_figure)

def minuit_beta_model(r, norm, rcore, beta):
    """
    Return 1D beta model in a minuit compatible way.

    Arguments:
    - 'norm': normalization of the model
    - `rcore`: core radius
    - `beta`: beta exponent
    - `r`: radius
    """

    out = norm * (1.0 + (r/rcore)**2)**(-3.0*beta+0.5)
    return out

def fit_model_minuit_beta(r, sb_src, sb_src_err, instrument, theta, energy):
    """
    Carry out the fitting using minuit: beta model, optionally with
    psf convolution. Please note: the fits itself is done on 1D arrays
    - this is a limitation imposed by pymiuit (i.e. 2D model is
    constantly being refolded to a profile)
    """

    ######################################################################
    # minuit fit
    data = arrays2minuit(r, sb_src, sb_src_err)

    ######################################################################
    # init parameters and fit limits

    norm0  = median(sb_src)
    rcore0 = 10.0               # [pix]
    beta0  = 2.0/3.0

    limit_norm  = (sb_src.min(), sb_src.max())
    limit_rcore = (1.0, r.max())
    limit_beta  = (0.35, 3.0)         # (0.35, 3.0) - generous bounds
                                      # for uncostrained fit of
                                      # Alshino+10

    def minuit_beta_model_likelihood(norm, rcore, beta):
        """
        Chi**2 likelihood function for the beta model fitting in a
        minuit compatible way.
        Model: beta model

        Arguments:
        - 'norm': normalization of the model
        - `rcore`: core radius
        - `beta`: beta exponent
        """
        l = 0.0
        for r, sb_src, sb_src_err in data:
            l += (minuit_beta_model(r, norm, rcore, beta) - sb_src)**2 / sb_src_err**2

        return l

    # fit simple beta
    model_fit =  minuit.Minuit(minuit_beta_model_likelihood,
                               norm=norm0, rcore=rcore0, beta=beta0,
                               limit_norm=limit_norm,
                               limit_rcore=limit_rcore,
                               limit_beta=limit_beta,
                               fix_norm=False,
                               fix_rcore=False,
                               fix_beta=False
                               )

    # fit model
    model_fit.migrad()
    return (model_fit.values, model_fit.errors)


def fit_model_minuit_beta_psf(r, sb_src, sb_src_err, xsize, ysize, xsize_obj, ysize_obj, xcen, ycen, instid, theta, energy):
    """
    Carry out the fitting using minuit: beta model, optionally with
    psf convolution. Please note: the fits itself is done on 1D arrays
    - this is a limitation imposed by pymiuit (i.e. 2D model is
    constantly being refolded to a profile)
    """
    ######################################################################
    # minuit fit
    data = arrays2minuit(r, sb_src, sb_src_err)

    ######################################################################
    # init parameters and fit limits
    norm0  = median(sb_src)
    rcore0 = 10.0               # [pix]
    beta0  = 2.0/3.0

    limit_norm  = (sb_src.min(), sb_src.max())
    limit_rcore = (1.0, r.max())
    limit_beta  = (0.35, 3.0)         # (0.35, 3.0) - generous bounds
                                      # for uncostrained fit of
                                      # Alshino+10

    ######################################################################
    # the fit likelihood
    # FIXME: get this working

    def minuit_sb_model_likelihood(xsize, ysize, xsize_obj, ysize_obj, xcen, ycen, norm, rcore, beta, instid, theta, energy):
        """
        Chi**2 likelihood function for the surface brightness model
        fitting in a minuit compatible way (psf x beta).

        Model: beta x psf

        Arguments:
        See arguments of build_sb_model_beta. The data is passed
        implicitely (and therefore likelihood calucalation and the
        fitting have to be at the same level/namespace).
        """
        l = 0.0
        APPLY_PSF = False

        # build the model
        print xsize, ysize, xsize_obj, ysize_obj, xcen, ycen, norm, rcore, beta, instid, theta, energy, APPLY_PSF
        model_2d = build_sb_model_beta(xsize, ysize, xsize_obj, ysize_obj, xcen, ycen, norm, rcore, beta, instid, theta, energy, APPLY_PSF)
        (r_model, profile_model, geometric_area_model) = extract_profile_generic(model_2d, xcen, ycen)
        profile_norm_model = profile_model / geometric_area_model

        for r, sb_src, sb_src_err in data:
            # calculate the likelihood
            l += (profile_norm_model - sb_src)**2 / sb_src_err**2
        return l

    def minuit_sb_model_likelihood_debug(xsize, ysize, xsize_obj, ysize_obj, xcen, ycen, norm, rcore, beta, instid, theta, energy):
        """
        Simple debug: 1d beta no psf
        """
        l = 0.0
        # print instid
        for r, sb_src, sb_src_err in data:
            l += (minuit_beta_model(r, norm, rcore, beta) - sb_src)**2 / sb_src_err**2
        return l

# fixme
# Thu Aug 23 17:09:06 2012
# now replace the likelihood calculation with the PSF version
# needs: propagate the instid parameter upstrem where the SPF is
# calculated (make minimal change i.e. at root keep string parameter)
# also: don'the forget that plotting has PSF turned of

    # setup sb model
    # model_fit =  minuit.Minuit(minuit_sb_model_likelihood_debug,
    model_fit =  minuit.Minuit(minuit_sb_model_likelihood,
                               #
                               norm=norm0,
                               fix_norm=False,
                               limit_norm=limit_norm,
                               #
                               rcore=rcore0,
                               fix_rcore=False,
                               limit_rcore=limit_rcore,
                               #
                               beta=beta0,
                               fix_beta=False,
                               limit_beta=limit_beta,
                               #
                               xsize=xsize,
                               fix_xsize=True,
                               # limit_xsize=None,
                               #
                               ysize=ysize,
                               fix_ysize=True,
                               # limit_ysize=None,
                               #
                               xsize_obj=xsize_obj,
                               fix_xsize_obj=True,
                               # limit_xsize_obj=None,
                               #
                               ysize_obj=ysize_obj,
                               fix_ysize_obj=True,
                               # limit_ysize_obj=None,
                               #
                               xcen=xcen,
                               fix_xcen=True,
                               # limit_xcen=None,
                               #
                               ycen=ycen,
                               fix_ycen=True,
                               # limit_ycen=None,
                               #
                               instid=instid,
                               fix_instid=True,
                               # limit_instid=None,
                               #
                               theta=theta,
                               fix_theta=True,
                               # limit_theta=None,
                               #
                               energy=energy,
                               fix_energy=False,
                               # limit_energy=None
                               )


                               # instid=instid,
                               # fix_instid=True,
                               # # limit_instid=None,

    # fit model
    model_fit.migrad()

    # model_fit.simplex()      # gradient-independent, but no goodness-of-fit eval/errors - check also starting point dependance

    # # errors around best fit
    # model_fit.hesse()
    # model_fit.minos()    # non-linear error estimation if the likelihood is non-parabolic around best-fit (on a ~1 sigma scale)

    # # error ellipses
    # ell_points = 100            # num. of samples for the surface
    # fname = 'beta-rcore-err-ellipse.png'

    # ell1 = sort(array(model_fit.contour("beta", "rcore", 1, ell_points)))
    # ell2 = sort(array(model_fit.contour("beta", "rcore", 2, 2*ell_points)))
    # ell3 = sort(array(model_fit.contour("beta", "rcore", 3, 3*ell_points)))

    # plot_minuit_err_ellipse(ell1, ell2, ell3, fname)

    return (model_fit.values, model_fit.errors)

def test_fit_beta():
    """
    Simple fit to the data using a simple beta model (no psf/bg)
    """
    fname = 'beta_image_cts.fits'
    APPLY_PSF = False

    input_im, hdr = load_fits_im(fname)

    # image setup
    xsize = input_im.shape[0]
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    xsize_obj = 100
    ysize_obj = xsize_obj
    r_aper = xsize_obj          # aperture for the fitting

    (r, profile, geometric_area) = extract_profile_generic(input_im, xcen, ycen)
    profile_norm = profile / geometric_area
    profile_norm_err = sqrt(profile_norm)
    profile_norm_err[profile_norm_err==0.0] = sqrt(profile_norm.max())

    ######################################################################
    # do the fitting - fit 1d profile
    # remoe useless passes
    (par_fitted, errors_fitted) = fit_model_minuit_beta(r, profile_norm, profile_norm_err, instrument, theta, energy)

    ######################################################################
    # extract results
    norm_fit  = par_fitted["norm"]
    rcore_fit = par_fitted["rcore"]
    beta_fit  = par_fitted["beta"]

    norm_fit_err  = errors_fitted["norm"]
    rcore_fit_err = errors_fitted["rcore"]
    beta_fit_err  = errors_fitted["beta"]

    # par_fitted = [model_fit.values["norm"], model_fit.values["rcore"], model_fit.values["beta"]]
    # errors_fitted = model_fit.errors

    ######################################################################
    # print results
    print
    print "beta true: ", beta
    print "rcore true: ", rcore
    print
    print "beta: ", beta_fit, beta_fit_err
    print "rcore: ", rcore_fit, rcore_fit_err
    print "norm: ", norm_fit, norm_fit_err
    print

    # build the model
    model_2d = build_sb_model_beta(xsize, ysize, xsize_obj, ysize_obj, xcen, ycen, norm_fit, rcore_fit, beta_fit, instrument, theta, energy, APPLY_PSF)

    (r_model, profile_model, geometric_area_model) = extract_profile_generic(model_2d, xcen, ycen)
    profile_norm_model = profile_model / geometric_area_model

    ######################################################################
    # do the plot
    MAKE_PLOT=True
    if MAKE_PLOT:
        output_figure="fit_beta.png"
        plot_data_model_simple(r, profile_norm, r_model, profile_norm_model, output_figure)
        print "plotting model"

def test_fit_beta_psf():
    """
    Simple fit to the data using a simple beta model x psf
    """
    # fname = 'cluster_image_cts_poiss.fits'
    fname = 'beta_image_cts.fits'
    APPLY_PSF = True

    input_im, hdr = load_fits_im(fname)

    # image setup
    xsize = input_im.shape[0]
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    xsize_obj = 100
    ysize_obj = xsize_obj
    r_aper = xsize_obj          # aperture for the fitting

    (r, profile, geometric_area) = extract_profile_generic(input_im, xcen, ycen)
    profile_norm = profile / geometric_area
    profile_norm_err = sqrt(profile_norm)
    profile_norm_err[profile_norm_err==0.0] = sqrt(profile_norm.max())

    ######################################################################
    # do the fitting - fit 1d profile
    (par_fitted, errors_fitted) = fit_model_minuit_beta_psf(r, profile_norm, profile_norm_err, xsize, ysize, xsize_obj, ysize_obj, xcen, ycen, instid, theta, energy)

    ######################################################################
    # extract results
    norm_fit  = par_fitted["norm"]
    rcore_fit = par_fitted["rcore"]
    beta_fit  = par_fitted["beta"]

    norm_fit_err  = errors_fitted["norm"]
    rcore_fit_err = errors_fitted["rcore"]
    beta_fit_err  = errors_fitted["beta"]

    # par_fitted = [model_fit.values["norm"], model_fit.values["rcore"], model_fit.values["beta"]]
    # errors_fitted = model_fit.errors

    ######################################################################
    # print results
    print
    print "beta true: ", beta
    print "rcore true: ", rcore
    print
    print "beta: ", beta_fit, beta_fit_err
    print "rcore: ", rcore_fit, rcore_fit_err
    print "norm: ", norm_fit, norm_fit_err
    print

    ######################################################################
    # build the model
    APPLY_PSF = False            # just for debug!!

    model_2d = build_sb_model_beta(xsize, ysize, xsize_obj, ysize_obj, xcen, ycen, norm_fit, rcore_fit, beta_fit, instrument, theta, energy, APPLY_PSF)

    (r_model, profile_model, geometric_area_model) = extract_profile_generic(model_2d, xcen, ycen)
    profile_norm_model = profile_model / geometric_area_model

    ######################################################################
    # do the plot
    MAKE_PLOT=False
    if MAKE_PLOT:
        print "plotting model"
        output_figure="fit_beta_psf.png"
        plot_data_model_simple(r, profile_norm, r_model, profile_norm_model, output_figure)

def module_visible():
    print "module visible!"
    return 0

######################################################################
######################################################################
######################################################################


if __name__ == '__main__':
    print

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
    c_sigmay = sqrt(a_sigmay**2 + b_sigmay**2)              # [piy]

    # setup for the beta model
    num_cts       = 2.0e3             # will be the normalization
    rcore         = 10.0               # [pix]
    beta          = 2.0 / 3.0
    normalization = 1.0

    # parameter calculation test
    # test_psf_parameter()

    # fits image creation tests
    # test_create_dirac()
    # test_create_gauss()
    # test_create_psf()
    # test_create_beta()

    # profile extration tests
    # test_profile_dirac()
    # test_profile_psf()
    # test_profile_beta()

    # convolution tests
    # test_convolve_psf_gauss()
    # test_convolve_psf_beta()

    ######################################################################
    # images for fitting tests
    # test_create_beta_im()
    test_create_cluster_im()

    ######################################################################
    # fit and plot
    # test_fit_beta()
    # test_fit_beta_psf()

    print "...done!"

    # FIXME:
    # refactor code using load_fits_im
    # refactor code using zero_pad_image



