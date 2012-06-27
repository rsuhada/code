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
            im[i, j] = 1 / ( 1 + r2/(rcore)**2 )**alpha

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


if __name__ == '__main__':
    print

    theta = 65.8443 / 60.0
    energy = 1.5
    instrument = "pn"

    ######################################################################
    # PSF testing

    # energy = 1.5
    # theta = 0.3

    # instrument=("pn", "m1", "m2")

    # plot_king_model_psf(energy, theta, instrument)

    # for i in instrument:
    #     print i
    #     (rcore, alpha) = get_psf_king_pars(i, energy, theta)
    #     print rcore, alpha

    # print "done"

    # ######################################################################
    # # create dirac function image
    #
    # imname = 'dirac.fits'
    # xsize = 900
    # ysize = xsize
    # xcen = xsize/2
    # ycen = ysize/2

    # im_dirac = make_2d_dirac((xsize, ysize), xcen, ycen)

    # # make hardcopy
    # hdu = pyfits.PrimaryHDU(im_dirac, hdr)    # extension: array, header
    # hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    # hdulist.writeto(imname, clobber=True)

    # ######################################################################
    # # create PSF function image
    #
    # imname = 'dirac.fits'
    # xsize = 900
    # ysize = xsize
    # xcen = xsize/2
    # ycen = ysize/2

    # im_psf = make_2d_king((xsize, ysize), xcen, ycen, instrument, theta, energy)

    # # make hardcopy
    # hdu = pyfits.PrimaryHDU(im_psf, hdr)    # extension: array, header
    # hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    # hdulist.writeto(imname, clobber=True)

    ######################################################################
    # create beta function image

    imname = 'beta-100.fits'
    xsize = 100
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2

    rcore = 15.0                  # [pix]
    beta = 2.0 / 3.0
    norm = 1.0
    beta_pars = [norm, rcore, beta]

    im_beta = make_2d_beta((xsize, ysize), xcen, ycen, rcore, beta)

    # make hardcopy
    hdu = pyfits.PrimaryHDU(im_beta, hdr)    # extension: array, header
    hdulist = pyfits.HDUList([hdu])          # list all extensions here
    hdulist.writeto(imname, clobber=True)

    ######################################################################
    # load from disc

    # fname = 'psf.fits'
    fname = 'psf-100.fits'
    hdu = pyfits.open(fname)
    im_psf = hdu[0].data
    hdr = hdu[0].header

    xsize = im_psf.shape[0]
    ysize = im_psf.shape[1]
    xcen = xsize/2
    ycen = ysize/2

    ######################################################################
    # profile extractor

    (r, profile, geometric_area) = extract_profile_generic(im_psf, xcen, ycen)

    # model check
    (rcore_model, alpha_model) = get_psf_king_pars(instrument, energy, theta)

    r_model = linspace(0.0, r.max(), 100)
    psf_model = king_profile(r_model, rcore_model, alpha_model)

    print "plotting"
    # plt.loglog(r, profile/geometric_area)
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
    # plt.get_current_fig_manager().window.wm_geometry("+640+0")

    print "...done!"


