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

    ######################################################################
    # stop plot enviroment
    ######################################################################

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
    Returns the value of a king profile at given position (relative to
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
    out = 1.0 / ( 1.0 + ( r2/rcore**2 )**alpha
    return out

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

    # # make a list of unique radii, expected factor ~12.5 speedup: actually awful speed
    # imdist = sqrt(sqdist_matrix(im, xcen, ycen))
    # rlist = unique(sort(squeeze(transpose(imdist.reshape((900*900,1))))))
    # for r in rlist:
        # ids = where(imdist == r)
        # print len(ids[0])
        # im[ids] = 1 / ( 1 + (r/rcore)**2 )**alpha

    # the dumb method
    for i in range(imsize[0]):
        for j in range(imsize[1]):
            r2 = sqdistance(xcen, ycen, j , i) # this is already squared
            im[i, j] = 1.0 / ( 1.0 + r2/rcore**2 )**alpha

    # FIXME: needs normalization:
    norm = integrate.quad(psf_2d_model, 0.0, Inf, args=(rcore, alpha))[0]
    print integrate.dblquad(king_2d_model, 0.0, Inf, lambda y:0.0, lambda y:Inf, args=(xcen, ycen, rcore, alpha))[0]

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

def test_psf_creation():
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

def create_dirac():
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

def create_gauss():
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

    # first gauss
    imname = 'gauss-a-100.fits'
    im_gauss = make_2d_uncorr_gauss((xsize, ysize), xcen, ycen, a_sigmax, a_sigmay)

    # make hardcopy
    hdu = pyfits.PrimaryHDU(im_gauss, hdr)    # extension: array, header
    hdulist = pyfits.HDUList([hdu])           # list all extensions here
    hdulist.writeto(imname, clobber=True)

    # second gauss
    imname = 'gauss-b-100.fits'
    im_gauss = make_2d_uncorr_gauss((xsize, ysize), xcen, ycen, b_sigmax, b_sigmay)

    # make hardcopy
    hdu = pyfits.PrimaryHDU(im_gauss, hdr)    # extension: array, header
    hdulist = pyfits.HDUList([hdu])           # list all extensions here
    hdulist.writeto(imname, clobber=True)

    # combined gauss
    imname = 'gauss-c-100.fits'
    im_gauss = make_2d_uncorr_gauss((xsize, ysize), xcen, ycen, c_sigmax, c_sigmay)

    # make hardcopy
    hdu = pyfits.PrimaryHDU(im_gauss, hdr)    # extension: array, header
    hdulist = pyfits.HDUList([hdu])           # list all extensions here
    hdulist.writeto(imname, clobber=True)

def create_psf():
    """
    Create a 2D psf image, save to fits
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

    im_psf = make_2d_king((xsize, ysize), xcen, ycen, instrument, theta, energy)

    # make hardcopy
    hdu = pyfits.PrimaryHDU(im_psf, hdr)    # extension: array, header
    hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    hdulist.writeto(imname, clobber=True)

def create_dirac():
    """
    Create a 2D beta image, save to fits
    """
    # get a header
    fname = 'pn-test.fits'
    hdu = pyfits.open(fname)
    hdr = hdu[0].header

    xsize = 100
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    rcore = 15.0                  # [pix]
    beta = 2.0 / 3.0
    norm = 1.0

    im_beta = make_2d_beta((xsize, ysize), xcen, ycen, rcore, beta)

    # make hardcopy
    hdu = pyfits.PrimaryHDU(im_beta, hdr)# extension: array, header
    hdulist = pyfits.HDUList([hdu])          # list all extensions here
    hdulist.writeto(imname, clobber=True)

def profile_dirac():
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

def profile_psf():
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

def profile_beta():
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

    # the model
    rcore = 15.0                  # [pix]
    beta = 2.0 / 3.0
    norm = 1.0

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

    # do the convolution
    im_conv_gauss = fftconvolve(im_gauss_a.astype(float), im_gauss_b.astype(float), mode = 'same')

    # FIXME: this takes care of the normalization, is it correct?
    im_conv_gauss = im_conv_gauss/im_conv_gauss.max()

    # # FIXME: remove invalid edge
    im_conv_gauss = delete(im_conv_gauss, 0, 0)
    im_conv_gauss = delete(im_conv_gauss, 0, 1)
    im_conv_gauss = delete(im_conv_gauss, im_conv_gauss.shape[1]-1, 0)
    im_conv_gauss = delete(im_conv_gauss, im_conv_gauss.shape[0]-1, 1)

    # print
    # print where(im_gauss_a == im_gauss_a.max())
    # print where(im_conv_gauss == im_conv_gauss.max())

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
        plt.plot(r-0.5, profile_b/geometric_area_b, label=r"$\sigma = $"+str(b_sigmax))
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

def test_convolve_psf_dirac():
    """
    Test convolution: dirac x psf
    """
    im_dirac_psf = fftconvolve(im_dirac.astype(float), im_psf.astype(float), mode = 'same')

    # make hardcopy
    imname='dirac_psf-100.fits'
    hdu = pyfits.PrimaryHDU(im_dirac_psf, hdr)  # extension: array, header
    hdulist = pyfits.HDUList([hdu])             # list all extensions here
    hdulist.writeto(imname, clobber=True)

    max1 = im_dirac_psf.max()
    max2 = im_dirac.max()

    print shape(im_dirac_psf), shape(im_dirac)
    print

    id1 = where(im_dirac_psf==max1)
    id2 = where(im_dirac==max2)

    print id1, id2, im_dirac_psf[id1], im_dirac_psf[id2]

if __name__ == '__main__':
    print

    # setup basic parameters
    theta = 65.8443 / 60.0
    energy = 1.5
    instrument = "pn"

    # setup for the gaussian test
    a_sigmax = 15.0               # [pix]
    a_sigmay = 15.0               # [pix]
    b_sigmax = 9.0               # [pix]
    b_sigmay = 9.0               # [pix]
    c_sigmax = sqrt(a_sigmax**2 + b_sigmax**2)              # [pix]
    c_sigmay = sqrt(a_sigmay**2 + b_sigmay**2)              # [piy]

    # test_psf_creation()

    # create_dirac()
    # create_gauss()
    # create_psf()
    # create_beta()

    # profile_dirac()
    # profile_psf()
    # profile_beta()

    # test_convolve_psf_dirac()

    test_convolve_psf_gauss()

    print "...done!"

######################################################################
# notes
# Fri Jun 29 16:27:04 2012
# - check the center shifting
# - investigate the normalization part (now had to be divided by the
# - maximum... confirm?)
######################################################################





