#!/usr/bin/env python
import sys
import pyfits
from numpy import *
from sb_utils import *

if __name__ == '__main__':
    """
    Extract cts/ctr/bg/exp/mask profiles from the input files for further analysis.
    """

    if len(sys.argv) == 8:
        ######################################################################
        # gather arguments

        im_file   = sys.argv[1]
        exp_file  = sys.argv[2]
        bg_file   = sys.argv[3]
        mask_file = sys.argv[4]

        xim = double(sys.argv[5]) - 1.0     # center x coord
        yim = double(sys.argv[6]) - 1.0     # center y coord

        aper = double(sys.argv[7])          # [pix] maximal extraction aperture


        ######################################################################
        # load in the fits file

        fname = im_file
        hdu = pyfits.open(fname)
        im_raw = hdu[0].data

        fname = exp_file
        hdu = pyfits.open(fname)
        exp_raw = hdu[0].data

        fname = bg_file
        hdu = pyfits.open(fname)
        bg_raw = hdu[0].data

        fname = mask_file
        hdu = pyfits.open(fname)
        # mask = int(hdu[1].data)
        mask = hdu[1].data
        hdr = hdu[1].header     # get a header for testing purposes

        ######################################################################
        # create images with ps masking

        im  = im_raw  * mask
        bg  = bg_raw  * mask
        exp = exp_raw * mask

        ######################################################################
        # create mask *with* ps regions

        # mask_raw = exp_raw/exp_raw

        mask_raw = exp_raw.copy()
        mask_raw = (mask_raw>0.0).choose(mask_raw, 1.0)

        # hdu = pyfits.PrimaryHDU(mask_raw, hdr)
        # hdulist = pyfits.HDUList([hdu])
        # hdulist.writeto('new.fits')

        ######################################################################
        # precalculate the distance matrix

        distmatrix = sqdist_matrix(im, xim, yim)

        # hdu = pyfits.PrimaryHDU(distmatrix, hdr) # extension: array, header
        # hdulist = pyfits.HDUList([hdu])                  # list all extensions here
        # hdulist.writeto('dist.fits', clobber=True)

        ######################################################################
        # do the profile extraction

        for r in range(1.0, aper+1.0, 1):
            ids = where((distmatrix <= r**2.0) & (distmatrix >= (r - 1.0)**2.0))

            num_pix = len(ids[0])

            # with ps
            cts_wps_raw = sum(im_raw[ids])
            cts_wps_bg  = sum(bg_raw[ids])
            expt_wps    = sum(exp_raw[ids])
            # mask_raw    = sum(mask_raw[ids])

            # without ps
            cts_raw = sum(im[ids])
            cts_bg  = sum(bg[ids])
            expt    = sum(exp[ids])
            mask    = sum(mask[ids])

            print "r :: ", r-1.0, r, num_pix

        ######################################################################
        # write report

        print
        print "#"*70
        print "image :: ", im_file
        print "bg    :: ", bg_file
        print "exp   :: ", exp_file
        print "mask  :: ", mask_file
        print "#"*70
        print "xim   :: ", xim
        print "yim   :: ", yim
        print "aper  :: ", aper
        print "#"*70
        print

    ######################################################################
    # bad input bailout

    else:
        print
        print "*** ERROR: not enough parameters : ", len(sys.argv),"!"
        print ""
        print "Syntax:"
        print "extract-sb-prof.py <image> <exp map> <bg map> <mask> <center x coord> <center y coord>"
        print "- coords in ds9 image coordinates"
        print
        print

