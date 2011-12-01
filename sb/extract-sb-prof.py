#!/usr/bin/env python
from sys import argv
import pyfits
from numpy import *
from sb_utils import *
from time import localtime, strftime

if __name__ == '__main__':
    """
    Extract cts/ctr/bg/exp/mask profiles from the input files for further analysis.
    """

    if len(argv) == 9:
        ######################################################################
        # gather arguments

        im_file   = argv[1]
        exp_file  = argv[2]
        bg_file   = argv[3]
        mask_file = argv[4]

        xim = double(argv[5]) - 1.0     # center x coord
        yim = double(argv[6]) - 1.0     # center y coord

        aper = double(argv[7])          # [pix] maximal extraction aperture
        outfile = argv[8]

        ######################################################################
        # start output file
        # FIXME: convert it to fits file output

        f = open(outfile, 'w')

        f.write('# '+strftime('%a %d %b %Y %H:%M:%S', localtime())+'\n')

        f.write('# image '+str(im_file)+'\n')
        f.write('# bg    '+str(bg_file)+'\n')
        f.write('# exp   '+str(exp_file)+'\n')
        f.write('# mask  '+str(mask_file)+'\n')
        f.write('# xim   '+str(xim)+'\n')
        f.write('# yim   '+str(yim)+'\n')
        f.write('# aper  '+str(aper)+'\n')
        f.write('#\n')

        f.write('# r cts_src cts_bg cts_tot exp_time area_correction mask_area geometric_area cts_src_wps cts_bg_wps cts_tot_wps exp_time_wps area_correction_wps mask_area_wps\n')


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
        mask = double(hdu[1].data)
        hdr = hdu[1].header     # get a header for testing purposes

        ######################################################################
        # create images with ps masking

        im  = im_raw  * mask
        bg  = bg_raw  * mask
        exp = exp_raw * mask

        ######################################################################
        # create mask *with* ps regions

        mask_raw = exp_raw.copy()
        mask_raw = (mask_raw>0.0).choose(mask_raw, 1.0)

        ######################################################################
        # precalculate the distance matrix

        print "calculating distance matrix!"

        # FIXME: could be sped up with some mapping tricks?
        distmatrix = sqdist_matrix(im, xim, yim)

        hdu = pyfits.PrimaryHDU(distmatrix, hdr)
        hdulist = pyfits.HDUList([hdu])
        hdulist.writeto('distmatrix.fits', clobber=True)

        print "distance matrix done!"

        ######################################################################
        # do the profile extraction

        for r in range(1.0, aper+1.0, 1):

            ids = where((distmatrix <= r**2.0) & (distmatrix >= (r - 1.0)**2.0))
            geometric_area = len(ids[0])      # [pix]

            ######################################################################
            # with ps (wps), area corrected

            # calculate the missing area correction factor
            mask_area_wps = sum(mask_raw[ids])
            area_correction_wps = 1.0 + (1.0 - mask_area_wps/geometric_area)

            cts_tot_wps   = sum(im_raw[ids])  * area_correction_wps
            cts_bg_wps    = sum(bg_raw[ids])  * area_correction_wps
            exp_time_wps  = sum(exp_raw[ids]) * area_correction_wps

            cts_src_wps = cts_tot_wps - cts_bg_wps

            ######################################################################
            # *withou* ps, area corrected

            # calculate the missing area correction factor
            mask_area = sum(mask[ids])
            area_correction = 1.0 + (1.0 - mask_area/geometric_area)

            cts_tot   = sum(im_raw[ids])  * area_correction
            cts_bg    = sum(bg_raw[ids])  * area_correction
            exp_time  = sum(exp_raw[ids]) * area_correction

            cts_src = cts_tot - cts_bg

            ######################################################################
            # calculate the countrates (area corrected)

            if (exp_time_wps > 0.0):
                # with ps
                ctr_tot_wps = cts_tot/exp_time_wps
                ctr_bg_wps  = cts_bg/exp_time_wps
                ctr_src_wps = cts_src/exp_time_wps

                # without point surces
                ctr_tot = cts_tot/exp_time
                ctr_bg  = cts_bg/exp_time
                ctr_src = cts_src/exp_time
            else:
                ctr_tot_wps = 0.0
                ctr_bg_wps  = 0.0
                ctr_src_wps = 0.0
                ctr_tot = 0.0
                ctr_bg  = 0.0
                ctr_src = 0.0

            ######################################################################
            # write output file

            f.write('%f %f %f %f %f %f %f %f %f %f %f %f %f %f\n' % (r, cts_src, cts_bg, cts_tot, exp_time, area_correction, mask_area, geometric_area, cts_src_wps, cts_bg_wps, cts_tot_wps, exp_time_wps, area_correction_wps, mask_area_wps))
            print "r :: ", r-1.0, r, geometric_area

        f.close()

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
        print "*** ERROR: not enough parameters : ", len(argv),"!"
        print ""
        print "Syntax:"
        print "extract-sb-prof.py <image> <exp map> <bg map> <mask> <center x coord> <center y coord> <output file>"
        print "- coords in ds9 image coordinates"
        print
        print

