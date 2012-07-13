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

    distmatrix = sqrt(sqdist_matrix(im, xcen, ycen))
    rgrid = arange(1, distmatrix.max()+1, 1.0)
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
        # print i, rgrid[i-1], rgrid[i], geometric_area[i], profile[i]

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

    xsize = 100
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    # first gauss - the "source"
    imname = 'gauss-a-100.fits'
    peak_scale = 0.0045         # arbitrary src height - just so that
                                # it can be conveniently plotted

    im_gauss = peak_scale*make_2d_uncorr_gauss((xsize, ysize), xcen, ycen, a_sigmax, a_sigmay)
    src_norm = im_gauss.sum()

    # make hardcopy
    hdu = pyfits.PrimaryHDU(im_gauss, hdr)    # extension: array, header
    hdulist = pyfits.HDUList([hdu])           # list all extensions here
    hdulist.writeto(imname, clobber=True)

    # second gauss - "the PSF" - i.e. normed to 1
    imname = 'gauss-b-100.fits'
    im_gauss = make_2d_uncorr_gauss((xsize, ysize), xcen, ycen, b_sigmax, b_sigmay)
    im_gauss = im_gauss / im_gauss.sum()

    # make hardcopy
    hdu = pyfits.PrimaryHDU(im_gauss, hdr)    # extension: array, header
    hdulist = pyfits.HDUList([hdu])           # list all extensions here
    hdulist.writeto(imname, clobber=True)

    # combined gauss - for checking - norm to "source"
    imname = 'gauss-c-100.fits'
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

    imname = 'psf-100.fits'
    xsize = 100
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    im_psf = make_2d_king((xsize, ysize), xcen, ycen, instrument, theta, energy)

    # make hardcopy
    hdu = pyfits.PrimaryHDU(im_psf, hdr)    # extension: array, header
    hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    hdulist.writeto(imname, clobber=True)

def test_create_beta():
    """
    Create a 2D beta image, save to fits
    """
    # get a header
    fname = 'pn-test.fits'
    hdu = pyfits.open(fname)
    hdr = hdu[0].header

    imname = 'beta-100.fits'
    xsize = 100
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    im_beta = make_2d_beta((xsize, ysize), xcen, ycen, rcore, beta)

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
    imname = 'beta-100.fits'
    hdu = pyfits.open(imname)
    im_beta = hdu[0].data
    hdr = hdu[0].header

    xsize = im_beta.shape[0]
    ysize = im_beta.shape[1]
    xcen = xsize/2
    ycen = ysize/2

    (r, profile, geometric_area) = extract_profile_generic(im_beta, xcen, ycen)
    r_model = linspace(0.0, r.max(), 100)

    beta_profile = beta_model((1.0, rcore, beta),r_model)

    MAKE_PLOT=1
    if MAKE_PLOT==1:
        print "plotting beta"
        plt.figure()
        plt.ion()
        plt.clf()
        plt.plot(r - 0.5, profile/geometric_area)
        plt.plot(r_model, beta_profile,
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

def test_convolve_psf_gauss():
    """
    Test gaussian convolution
    """

    imname = 'gauss-a-100.fits'
    hdu = pyfits.open(imname)
    im_gauss_a = hdu[0].data
    hdr = hdu[0].header

    imname = 'gauss-b-100.fits'
    hdu = pyfits.open(imname)
    im_gauss_b = hdu[0].data
    hdr = hdu[0].header

    imname = 'gauss-c-100.fits'
    hdu = pyfits.open(imname)
    im_gauss_c = hdu[0].data
    hdr = hdu[0].header

    xsize = im_gauss_a.shape[0]
    ysize = im_gauss_a.shape[1]
    xcen = xsize/2
    ycen = ysize/2

    # do the convolution: test on gaussian convolution showd
    # normalization conversation to better than 1%, except if PSF is
    # comparable to the source (3%) and increses if PSF is broader
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
    imname = 'beta-100.fits'
    hdu = pyfits.open(imname)
    im_beta = hdu[0].data
    hdr = hdu[0].header

    imname = 'psf-100.fits'
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
    hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    hdulist.writeto(imname, clobber=True)


    print "psf norm : ", im_psf.sum()
    print "norm % diff:", 100.0*(im_psf.sum() - im_beta.sum()) / im_beta.sum()

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

        plt.xscale("linear")
        plt.yscale("linear")
        # plt.ylim(ymin=1e-3,ymax=5e0)

        prop = matplotlib.font_manager.FontProperties(size=16)  # size=16
        plt.legend(loc=0, prop=prop, numpoints=1)

        plt.draw()
        # plt.get_current_fig_manager().window.wm_geometry("+1100+0")
        plt.get_current_fig_manager().window.wm_geometry("+640+0")
        plt.show()

        plt.savefig('psf_conv_test_beta.png')

if __name__ == '__main__':
    print

    # setup basic parameters
    theta = 65.8443 / 60.0
    energy = 1.5
    instrument = "pn"

    # setup for the gaussian test
    a_sigmax = 15.0               # [pix]
    a_sigmay = 15.0               # [pix]
    b_sigmax = 5.0               # [pix]
    b_sigmay = 5.0               # [pix]
    c_sigmax = sqrt(a_sigmax**2 + b_sigmax**2)              # [pix]
    c_sigmay = sqrt(a_sigmay**2 + b_sigmay**2)              # [piy]

    # setup for the beta model
    rcore = 25.0                  # [pix]
    beta = 2.0 / 3.0
    norm = 1.0

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
    test_convolve_psf_beta()
    print "...done!"

    # FIXME:
    # Fri Jul 13 16:41:40 2012
    # - add zero padded borders to trace the counts beyond
    # in beta case - is there a problem with the inverted profiles
