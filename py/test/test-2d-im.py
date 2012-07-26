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
    the center). Function is useful e.g. for  integration.

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

    # this is pretty fast but maybe you want to do it in polar coords
    im = zeros(imsize, dtype=double)
    (rcore, alpha) = get_psf_king_pars(instrument, energy, theta)

    # the dumb method
    for i in range(imsize[0]):
        for j in range(imsize[1]):
            r2 = sqdistance(xcen, ycen, j , i) # this is already squared
            im[i, j] = 1.0 / ( 1.0 + r2/rcore**2 )**alpha

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

def make_2d_beta(imsize, xcen, ycen, rcore, beta):
    """
    Creates a 2D image of a beta model

    Arguments:
    - `imsize`: input 2D array size
    - `xcen`: x coordinate of the function
    - `ycen`: y coordinate of the function
    - 'core': beta model core radius
    - 'beta': beta model slope
    """

    # this is pretty fast but maybe you want to do it in polar coords
    im = zeros(imsize, dtype=double)

    # the dumb method
    for i in range(imsize[0]):
        for j in range(imsize[1]):
            r2 = sqdistance(xcen, ycen, j , i) # this is already squared
            im[i, j] = (1.0 + r2/(rcore)**2)**(-3.0*beta + 0.5)

    return im

def extract_profile_generic(im, xcen, ycen):
    """
    Generic function to extract a 1D profile of a 2D image
    profile[i] plotted at r[i] gives the sum for r[i-1] < r < r[i] ring.
    For plotting and comparison you might want to do r-0.5
    Arguments:
    - `im`: 2D array
    - `xcen`: center x coordinate
    - `ycen`: center y coordinate
    """

    # FIXME: 1. rmax as argument, 2. look at speed improvement in
    # sqdist

    distmatrix = sqrt(sqdist_matrix(im, xcen, ycen))
    # rgrid = arange(1, distmatrix.max()+1, 1.0)  # maximal possible distance (to corner)
    rgrid = arange(1, im.shape[0]/2+1, 1.0)  # maximal possible distance (to side)
    n = len(rgrid)

    x = zeros(n, dtype=float)   # profile
    geometric_area = zeros(n, dtype=float)  # area normalised profile

    # starting bin
    i=0
    ids = where((distmatrix <= rgrid[i]) & (distmatrix >= 0))
    geometric_area[i] = len(ids[0])      # [pix]
    x[i] = sum(im[ids])

    # iterate through the rest
    for i in range(1, n):
        ids = where((distmatrix <= rgrid[i]) & (distmatrix >= (rgrid[i-1])))
        geometric_area[i] = len(ids[0])      # [pix]
        x[i] = sum(im[ids])

    return (rgrid, x, geometric_area)

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
    do_zero_pad = 1
    xsize_obj = 100
    ysize_obj = xsize_obj

     # first gauss - the "source"
    imname = 'gauss-a-100-pad.fits'
    peak_scale = 0.0045         # arbitrary src height - just so that
                                # it can be conveniently plotted

    im_gauss = peak_scale*make_2d_uncorr_gauss((xsize, ysize), xcen, ycen, a_sigmax, a_sigmay)

    if do_zero_pad == 1:
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
    if do_zero_pad == 1:
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
    do_zero_pad = 0
    xsize_obj = 100
    ysize_obj = xsize_obj

    im_psf = make_2d_king((xsize, ysize), xcen, ycen, instrument, theta, energy)
    if do_zero_pad == 1:
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
    do_zero_pad = 0
    xsize_obj = 100
    ysize_obj = xsize_obj

    im_beta = make_2d_beta((xsize, ysize), xcen, ycen, rcore, beta)
    if do_zero_pad == 1:
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

    MAKE_PLOT=1
    if MAKE_PLOT==1:
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

    MAKE_PLOT=1
    if MAKE_PLOT==1:
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

    MAKE_PLOT=1
    if MAKE_PLOT==1:
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
    MAKE_PLOT=1
    if MAKE_PLOT==1:
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
    MAKE_PLOT=1
    if MAKE_PLOT==1:
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

def build_sb_model(xsize, ysize, xsize_obj, ysize_obj, xcen, ycen, rcore, beta, instrument, theta, energy):
    """
    Build a surface brighness model for fitting/plotting.
    """
    APPLY_PSF = True
    DO_ZERO_PAD = True

    print xsize, ysize, xcen, ycen, rcore, beta, instrument, theta, energy

    # create beta
    im_beta = make_2d_beta((xsize, ysize), xcen, ycen, rcore, beta)
    if DO_ZERO_PAD == 1:
        im_beta[:, 0:xsize_obj] = 0.0
        im_beta[:, xsize-xsize_obj:] = 0.0
        im_beta[0:xsize_obj,:] = 0.0
        im_beta[xsize-xsize_obj:,:] = 0.0

    # create psf
    im_psf = make_2d_king((xsize, ysize), xcen, ycen, instrument, theta, energy)
    if DO_ZERO_PAD == 1:
        im_psf[:, 0:xsize_obj] = 0.0
        im_psf[:, xsize-xsize_obj:] = 0.0
        im_psf[0:xsize_obj,:] = 0.0
        im_psf[xsize-xsize_obj:,:] = 0.0

    # FIXME: this needs bit reorganizing so that the proper number of
    # source cts can be assured (while a realistc s/n is kept)
    # note: also needs exp map correction
    # add background model (pre-PSF application)

    # convolve
    im_conv = fftconvolve(im_beta.astype(float), im_psf.astype(float), mode = 'same')
    im_conv = trim_fftconvolve(im_conv)

    return im_conv

def test_create_cluster_im():
    """
    Creates a PSF convolved beta model image with poissonizations
    """
    # settings
    POISSONIZE_IMAGE = True            # poissonize image?
    DO_ZERO_PAD = True
    APPLY_EXPOSURE_MAP = True           # add exposure map
    ADD_BACKGROUND = True

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

    im_conv = build_sb_model(xsize, ysize, xsize_obj, ysize_obj, xcen, ycen, rcore, beta, instrument, theta, energy)

    # write the simple model output, no noise/background
    imname = 'cluster_image_cts_model.fits'
    hdu = pyfits.PrimaryHDU(im_conv, hdr)    # extension - array, header
    hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    hdulist.writeto(imname, clobber=True)

    # normalization and poissonization
    im_conv = num_cts * im_conv/im_conv.sum()

    if POISSONIZE_IMAGE:
        im_conv = poisson.rvs(im_conv)
        print "poisson sum:", im_conv.sum()

    # write the un-masked, no-bg output
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

    image_mask = create_background_mask(background_map)
    im_conv = im_conv * image_mask

    # write the masked output
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

def fit_model_miuit():
    """
    Carry out the fitting using minuit
    """
    ######################################################################
    # simple beta fit

    p0 = [5.0e-5, 10.0, 2.0/3.0]
    rgrid = linspace(0.0, 100.0, 100)

    ######################################################################
    # minuit fit

    data = arrays2minuit(r, sb_src, sb_src_err)

    def minuit_beta_model(r, norm, rcore, beta):
        """
        Return 2D beta model in a minuit compatible way.

        Arguments:
        - 'norm': normalization of the model
        - `rcore`: core radius
        - `beta`: beta exponent
        - `r`: radius
        """

        out = norm * (1.0 + (r/rcore)**2)**(-3.0*beta+0.5)
        return out

    def minuit_beta_model_likelihood(norm, rcore, beta):
        """
        Chi**2 likelihood function for the beta model fitting in a
        minuit compatible way.

        Arguments:
        - 'norm': normalization of the model
        - `rcore`: core radius
        - `beta`: beta exponent
        - `r`: radius
        """
        l = 0.0

        for r, sb_src, sb_src_err in data:
            l += (minuit_beta_model(r, norm, rcore, beta) - sb_src)**2 / sb_src_err**2

        return l

    ######################################################################
    # init parameters and fit limits

    norm0  = median(sb_src)
    rcore0 = 18.0               # [arcsec]
    beta0  = 2.0/3.0

    limit_norm  = (sb_src.min(), sb_src.max())
    limit_rcore = (pixscale, r.max())
    limit_beta  = (0.35, 3.0)         # (0.35, 3.0) - generous bounds
                                      # for uncostrained fit of
                                      # Alshino+10

    ######################################################################
    # the fit

    # setup
    model_fit =  minuit.Minuit(minuit_beta_model_likelihood,
                               norm=norm0, rcore=rcore0, beta=beta0,
                               limit_norm=limit_norm,
                               limit_rcore=limit_rcore,
                               limit_beta=limit_beta,
                               fix_norm=False,
                               fix_rcore=False,
                               fix_beta=False
                               )
    # fit
    model_fit.migrad()

    # model_fit.simplex()      # gradient-independent, but no goodness-of-fit eval/errors - check also starting point dependance

    # errors around best fit
    # model_fit.hesse()
    # model_fit.minos()    # non-linear error estimation if the likelihood is non-parabolic around best-fit (on a ~1 sigma scale)

    par_fitted = [model_fit.values["norm"], model_fit.values["rcore"], model_fit.values["beta"]]
    errors_fitted = model_fit.errors

    print "results: ", model_fit.values
    print "errors:  ", errors_fitted

    # # error ellipses
    # ell_points = 500            # num. of samples for the surface
    # fname = intab+'.err-ellipse.png'

    # ell1 = sort(array(model_fit.contour("beta", "rcore", 1, ell_points)))
    # ell2 = sort(array(model_fit.contour("beta", "rcore", 2, 2*ell_points)))
    # ell3 = sort(array(model_fit.contour("beta", "rcore", 3, 3*ell_points)))

    # sb_plotting_utils.plot_minuit_err_ellipse(ell1, ell2, ell3, fname)


def plot_synthetic_fit():
    """
    Do a simple profile plot of the synthetic image.
    """
    # fname = 'cluster_image_cts_poiss.fits'
    fname = 'cluster_image_cts_poiss.fits'
    hdu = pyfits.open(fname)
    im_conv = hdu[0].data
    hdr = hdu[0].header

    # image setup
    xsize = im_conv.shape[0]
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    xsize_obj = 100
    ysize_obj = xsize_obj

    (r, profile, geometric_area) = extract_profile_generic(im_conv, xcen, ycen)
    profile_norm = profile / geometric_area

    # build the model
    model_2d = build_sb_model(xsize, ysize, xsize_obj, ysize_obj, xcen, ycen, rcore, beta, instrument, theta, energy)

    model_2d = 2000.0 * model_2d/model_2d.sum()

    (r_model, profile_model, geometric_area_model) = extract_profile_generic(model_2d, xcen, ycen)
    profile_norm_model = profile_model / geometric_area_model

    # model = beta_model((1.0, rcore, beta), r_model)
    # # do the fitting

    # do the plot
    MAKE_PLOT=1
    if MAKE_PLOT==1:
        print "plotting psf x beta"
        plt.figure()
        plt.ion()
        plt.clf()

        plt.plot(r-0.5, profile_norm,
            color='black',
            linestyle='',              # -/--/:/-.
            linewidth=0,                # linewidth=1
            marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
            markerfacecolor='black',
            markersize=4,               # markersize=6
            label=r"source"               # '__nolegend__'
            )

        plt.plot(r_model-0.5, profile_norm_model,
            color='red',
            linestyle='-',              # -/--/:/-.
            linewidth=1,                # linewidth=1
            marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
            markerfacecolor='black',
            markersize=0,               # markersize=6
            label=r"model"               # '__nolegend__'
            )

        plt.xscale("log")
        plt.yscale("log")
        # plt.ylim(ymin=1e-3,ymax=5e0)

        prop = matplotlib.font_manager.FontProperties(size=16)  # size=16
        plt.legend(loc=0, prop=prop, numpoints=1)

        plt.draw()
        plt.get_current_fig_manager().window.wm_geometry("+640+0")
        plt.show()

        plt.savefig('model_2d_vs_poi_data.png')


######################################################################
######################################################################
######################################################################

if __name__ == '__main__':
    print

    # setup basic parameters
    theta = 65.8443 / 60.0
    energy = 1.5
    instrument = "pn"

    # setup for the gaussian test
    a_sigmax = 15.0               # [pix]
    a_sigmay = 15.0               # [pix]
    b_sigmax = 20.0               # [pix]
    b_sigmay = 20.0               # [pix]
    c_sigmax = sqrt(a_sigmax**2 + b_sigmax**2)              # [pix]
    c_sigmay = sqrt(a_sigmay**2 + b_sigmay**2)              # [piy]

    # setup for the beta model
    num_cts  = 2.0e3             # will be the normalization
    rcore    = 8.0               # [pix]
    beta     = 2.0 / 3.0
    norm     = 1.0

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


    # the fitting suite
    # test_create_cluster_im()
    plot_synthetic_fit()

    print "...done!"
