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

def extract_profile_generic(im, xcen, ycen):
    """
    Generic function to extract a 1D profile of a 2D image

    Arguments:
    - `im`: 2D array
    - `xcen`: center x coordinate
    - `ycen`: center y coordinate
    """

    distmatrix = sqrt(sqdist_matrix(im, xcen, ycen))
    rgrid = arange(0.0, distmatrix.max(), 1.0)
    n = len(rgrid)

    x = zeros(n, dtype=float)   # profile
    geometric_area = zeros(n, dtype=float)  # area normalised profile

    i = 0
    for i in range(n-1):
        ids = where((distmatrix <= rgrid[i+1]) & (distmatrix >= (rgrid[i])))
        geometric_area[i] = len(ids[0])      # [pix]
        x[i] = sum(im[ids])

    return (rgrid, x, geometric_area)


if __name__ == '__main__':
    print

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

    ######################################################################
    # 2D baseimage

    fname = 'pn-test.im'
    hdu = pyfits.open(fname)
    hdr = hdu[0].header
    dat = hdu[0].data

    # setup image
    # xsize = 900
    # ysize = 900

    xsize = dat.shape[0]
    ysize = dat.shape[1]

    print "Image size:", xsize, ysize

    # ######################################################################
    # # create dirac function image
    # xcen = 450
    # ycen = 450

    # im_dirac = make_2d_dirac((xsize, ysize), xcen, ycen)

    # # make hardcopy
    # hdu = pyfits.PrimaryHDU(im_dirac, hdr)    # extension: array, header
    # hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    # hdulist.writeto('dirac.fits', clobber=True)

    # ######################################################################
    # # create PSF function image
    # xcen = 450
    # ycen = 450
    # theta = 65.8443 / 60.0
    # energy = 1.5
    # instrument = "pn"

    # im_psf = make_2d_king((xsize, ysize), xcen, ycen, instrument, theta, energy)

    # # make hardcopy
    # hdu = pyfits.PrimaryHDU(im_psf, hdr)    # extension: array, header
    # hdulist = pyfits.HDUList([hdu])                  # list all extensions here
    # hdulist.writeto('psf.fits', clobber=True)


    ######################################################################
    # load from disc

    fname = 'psf.fits'
    hdu = pyfits.open(fname)
    im_psf = hdu[0].data
    hdr = hdu[0].header
    xcen = 450
    ycen = 450

    ######################################################################
    # profile extractor

    (r, profile, geometric_area) = extract_profile_generic(im_psf, xcen, ycen)

    print "plotting"
    plt.loglog(r, profile/geometric_area)
    plt.show()
