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
        # start output file for profiles
        # FIXME: convert it to fits file output?

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

        f.write('# r sb_src sb_bg sb_tot sb_src_err sb_bg_err sb_tot_err ctr_src ctr_bg ctr_tot ctr_src_err ctr_bg_err ctr_tot_err cts_src cts_bg cts_tot cts_src_err cts_bg_err cts_tot_err exp_time area_correction mask_area geometric_area sb_src_wps sb_bg_wps sb_tot_wps sb_src_wps_err sb_bg_wps_err sb_tot_wps_err ctr_src_wps ctr_bg_wps ctr_tot_wps ctr_src_wps_err ctr_bg_wps_err ctr_tot_wps_err cts_src_wps cts_bg_wps cts_tot_wps cts_src_wps_err cts_bg_wps_err cts_tot_wps_err  exp_time_wps area_correction_wps mask_area_wps\n')

        ######################################################################
        # start output file for cumulative profiles
        # FIXME: convert it to fits file output

        g = open(outfile+'.cumul', 'w')

        g.write('# '+strftime('%a %d %b %Y %H:%M:%S', localtime())+'\n')

        g.write('# image '+str(im_file)+'\n')
        g.write('# bg    '+str(bg_file)+'\n')
        g.write('# exp   '+str(exp_file)+'\n')
        g.write('# mask  '+str(mask_file)+'\n')
        g.write('# xim   '+str(xim)+'\n')
        g.write('# yim   '+str(yim)+'\n')
        g.write('# aper  '+str(aper)+'\n')
        g.write('#\n')

        g.write('# r cumul_sb_src cumul_sb_bg cumul_sb_tot cumul_sb_src_err cumul_sb_bg_err cumul_sb_tot_err cumul_ctr_src cumul_ctr_bg cumul_ctr_tot cumul_ctr_src_err cumul_ctr_bg_err cumul_ctr_tot_err cumul_cts_src cumul_cts_bg cumul_cts_tot cumul_cts_src_err cumul_cts_bg_err cumul_cts_tot_err exp_time area_correction mask_area geometric_area cumul_sb_src_wps cumul_sb_bg_wps cumul_sb_tot_wps cumul_sb_src_wps_err cumul_sb_bg_wps_err cumul_sb_tot_wps_err cumul_ctr_src_wps cumul_ctr_bg_wps cumul_ctr_tot_wps cumul_ctr_src_wps_err cumul_ctr_bg_wps_err cumul_ctr_tot_wps_err cumul_cts_src_wps cumul_cts_bg_wps cumul_cts_tot_wps cumul_cts_src_wps_err cumul_cts_bg_wps_err cumul_cts_tot_wps_err  exp_time_wps area_correction_wps mask_area_wps\n')

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

        # trim sizes if necessary (should be needed only in case of
        # manual testing)

        if im_raw.shape[0] == exp_raw.shape[0]-2:
            exp_raw = trim_fftconvolve(exp_raw)
        if im_raw.shape[0] == bg_raw.shape[0]-2:
            bg_raw = trim_fftconvolve(bg_raw)
        if im_raw.shape[0] == mask.shape[0]-2:
            mask = trim_fftconvolve(mask)

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

        distmatrix = sqdist_matrix(im, xim, yim)

        hdu = pyfits.PrimaryHDU(distmatrix, hdr)
        hdulist = pyfits.HDUList([hdu])
        hdulist.writeto('distmatrix.fits', clobber=True)

        print "distance matrix done!"

        ######################################################################
        # initialize cumulative curves

        cumul_cts_tot_wps     = 0.0
        cumul_cts_bg_wps      = 0.0
        cumul_cts_src_wps     = 0.0
        cumul_cts_tot         = 0.0
        cumul_cts_bg          = 0.0
        cumul_cts_src         = 0.0
        cumul_ctr_tot_wps     = 0.0
        cumul_ctr_bg_wps      = 0.0
        cumul_ctr_src_wps     = 0.0
        cumul_ctr_tot         = 0.0
        cumul_ctr_bg          = 0.0
        cumul_ctr_src         = 0.0
        cumul_sb_tot_wps      = 0.0
        cumul_sb_bg_wps       = 0.0
        cumul_sb_src_wps      = 0.0
        cumul_sb_tot          = 0.0
        cumul_sb_bg           = 0.0
        cumul_sb_src          = 0.0

        cumul_cts_tot_wps_err = 0.0
        cumul_cts_bg_wps_err  = 0.0
        cumul_cts_src_wps_err = 0.0
        cumul_cts_tot_err     = 0.0
        cumul_cts_bg_err      = 0.0
        cumul_cts_src_err     = 0.0
        cumul_ctr_tot_wps_err = 0.0
        cumul_ctr_bg_wps_err  = 0.0
        cumul_ctr_src_wps_err = 0.0
        cumul_ctr_tot_err     = 0.0
        cumul_ctr_bg_err      = 0.0
        cumul_ctr_src_err     = 0.0
        cumul_sb_tot_wps_err  = 0.0
        cumul_sb_bg_wps_err   = 0.0
        cumul_sb_src_wps_err  = 0.0
        cumul_sb_tot_err      = 0.0
        cumul_sb_bg_err       = 0.0
        cumul_sb_src_err      = 0.0

        cts_tot_wps     = 0.0
        cts_bg_wps      = 0.0
        cts_src_wps     = 0.0
        cts_tot         = 0.0
        cts_bg          = 0.0
        cts_src         = 0.0
        ctr_tot_wps     = 0.0
        ctr_bg_wps      = 0.0
        ctr_src_wps     = 0.0
        ctr_tot         = 0.0
        ctr_bg          = 0.0
        ctr_src         = 0.0
        sb_tot_wps      = 0.0
        sb_bg_wps       = 0.0
        sb_src_wps      = 0.0
        sb_tot          = 0.0
        sb_bg           = 0.0
        sb_src          = 0.0

        cts_tot_wps_err = 0.0
        cts_bg_wps_err  = 0.0
        cts_src_wps_err = 0.0
        cts_tot_err     = 0.0
        cts_bg_err      = 0.0
        cts_src_err     = 0.0
        ctr_tot_wps_err = 0.0
        ctr_bg_wps_err  = 0.0
        ctr_src_wps_err = 0.0
        ctr_tot_err     = 0.0
        ctr_bg_err      = 0.0
        ctr_src_err     = 0.0
        sb_tot_wps_err  = 0.0
        sb_bg_wps_err   = 0.0
        sb_src_wps_err  = 0.0
        sb_tot_err      = 0.0
        sb_bg_err       = 0.0
        sb_src_err      = 0.0

        ######################################################################
        # do the profile extraction

        radii = arange(1.0, aper+1.0, 1.0)
        for r in radii:

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
            # *without* ps, area corrected

            # calculate the missing area correction factor
            mask_area = sum(mask[ids])
            area_correction = 1.0 + (1.0 - mask_area/geometric_area)

            cts_tot   = sum(im_raw[ids])  * area_correction
            cts_bg    = sum(bg_raw[ids])  * area_correction
            exp_time  = sum(exp_raw[ids]) * area_correction

            cts_src = cts_tot - cts_bg


            print  "area:", r, mask_area, mask_area_wps
            ######################################################################
            # calculate the counts/countrates/surface brightness (area corrected)

            # if (exp_time_wps > 0.0):
            if (mask_area_wps > 0.0):
                # with ps
                ctr_tot_wps     = cts_tot_wps/exp_time_wps
                ctr_bg_wps      = cts_bg_wps/exp_time_wps
                ctr_src_wps     = cts_src_wps/exp_time_wps

                sb_tot_wps      = ctr_tot_wps/mask_area_wps
                sb_bg_wps       = ctr_bg_wps/mask_area_wps
                sb_src_wps      = ctr_src_wps/mask_area_wps

                # poisson errors
                cts_tot_wps_err = sqrt(cts_tot)
                cts_bg_wps_err  = sqrt(cts_bg)
                cts_src_wps_err = sqrt(cts_tot_wps_err**2.0 + cts_bg_wps_err**2.0)

                ctr_tot_wps_err = cts_tot_wps_err/exp_time_wps
                ctr_bg_wps_err  = cts_bg_wps_err/exp_time_wps
                ctr_src_wps_err = sqrt(ctr_tot_wps_err**2.0 + ctr_bg_wps_err**2.0)

                sb_tot_wps_err  = ctr_tot_wps_err/mask_area_wps
                sb_bg_wps_err   = ctr_bg_wps_err/mask_area_wps
                sb_src_wps_err  = ctr_src_wps_err/mask_area_wps

            else:
                ######################################################################
                # ring missing

                ctr_tot_wps     = 0.0
                ctr_bg_wps      = 0.0
                ctr_src_wps     = 0.0
                sb_tot_wps      = 0.0
                sb_bg_wps       = 0.0
                sb_src_wps      = 0.0
                ctr_tot_wps_err = -1.0
                ctr_bg_wps_err  = -1.0
                ctr_src_wps_err = -1.0
                sb_tot_wps_err  = -1.0
                sb_bg_wps_err   = -1.0
                sb_src_wps_err  = -1.0

            # if (exp_time > 0.0):
            if (mask_area > 0.0):
                # without point surces
                ctr_tot         = cts_tot/exp_time
                ctr_bg          = cts_bg/exp_time
                ctr_src         = cts_src/exp_time

                sb_tot          = ctr_tot/mask_area
                sb_bg           = ctr_bg/mask_area
                sb_src          = ctr_src/mask_area

                # poisson errors
                cts_tot_err = sqrt(cts_tot)
                cts_bg_err  = sqrt(cts_bg)
                cts_src_err = sqrt(cts_tot_err**2.0 + cts_bg_err**2.0)

                ctr_tot_err = cts_tot_err/exp_time
                ctr_bg_err  = cts_bg_err/exp_time
                ctr_src_err = sqrt(ctr_tot_err**2.0 + ctr_bg_err**2.0)

                sb_tot_err  = ctr_tot_err/mask_area
                sb_bg_err   = ctr_bg_err/mask_area
                sb_src_err  = ctr_src_err/mask_area

            else:
                ######################################################################
                # ring missing

                ctr_tot         = 0.0
                ctr_bg          = 0.0
                ctr_src         = 0.0
                sb_tot          = 0.0
                sb_bg           = 0.0
                sb_src          = 0.0
                ctr_tot_err     = -1.0
                ctr_bg_err      = -1.0
                ctr_src_err     = -1.0
                sb_tot_err      = -1.0
                sb_bg_err       = -1.0
                sb_src_err      = -1.0

            ######################################################################
            # cumulative curves

            cumul_cts_tot_wps     = cumul_cts_tot_wps + cts_tot_wps
            cumul_cts_bg_wps      = cumul_cts_bg_wps + cts_bg_wps
            cumul_cts_src_wps     = cumul_cts_src_wps + cts_src_wps
            cumul_cts_tot         = cumul_cts_tot + cts_tot
            cumul_cts_bg          = cumul_cts_bg + cts_bg
            cumul_cts_src         = cumul_cts_src + cts_src
            cumul_ctr_tot_wps     = cumul_ctr_tot_wps + ctr_tot_wps
            cumul_ctr_bg_wps      = cumul_ctr_bg_wps + ctr_bg_wps
            cumul_ctr_src_wps     = cumul_ctr_src_wps + ctr_src_wps
            cumul_ctr_tot         = cumul_ctr_tot + ctr_tot
            cumul_ctr_bg          = cumul_ctr_bg + ctr_bg
            cumul_ctr_src         = cumul_ctr_src + ctr_src
            cumul_sb_tot_wps      = cumul_sb_tot_wps + sb_tot_wps
            cumul_sb_bg_wps       = cumul_sb_bg_wps + sb_bg_wps
            cumul_sb_src_wps      = cumul_sb_src_wps + sb_src_wps
            cumul_sb_tot          = cumul_sb_tot + sb_tot
            cumul_sb_bg           = cumul_sb_bg + sb_bg
            cumul_sb_src          = cumul_sb_src + sb_src

            #  formal errors - bins are not independent
            cumul_cts_tot_wps_err = (cumul_cts_tot_wps_err**2 + cts_tot_wps_err**2)**0.5
            cumul_cts_bg_wps_err  = (cumul_cts_bg_wps_err**2 + cts_bg_wps_err**2)**0.5
            cumul_cts_src_wps_err = (cumul_cts_src_wps_err**2 + cts_src_wps_err**2)**0.5
            cumul_cts_tot_err     = (cumul_cts_tot_err**2 + cts_tot_err**2)**0.5
            cumul_cts_bg_err      = (cumul_cts_bg_err**2 + cts_bg_err**2)**0.5
            cumul_cts_src_err     = (cumul_cts_src_err**2 + cts_src_err**2)**0.5
            cumul_ctr_tot_wps_err = (cumul_ctr_tot_wps_err**2 + ctr_tot_wps_err**2)**0.5
            cumul_ctr_bg_wps_err  = (cumul_ctr_bg_wps_err**2 + ctr_bg_wps_err**2)**0.5
            cumul_ctr_src_wps_err = (cumul_ctr_src_wps_err**2 + ctr_src_wps_err**2)**0.5
            cumul_ctr_tot_err     = (cumul_ctr_tot_err**2 + ctr_tot_err**2)**0.5
            cumul_ctr_bg_err      = (cumul_ctr_bg_err**2 + ctr_bg_err**2)**0.5
            cumul_ctr_src_err     = (cumul_ctr_src_err**2 + ctr_src_err**2)**0.5
            cumul_sb_tot_wps_err  = (cumul_sb_tot_wps_err**2 + sb_tot_wps_err**2)**0.5
            cumul_sb_bg_wps_err   = (cumul_sb_bg_wps_err**2 + sb_bg_wps_err**2)**0.5
            cumul_sb_src_wps_err  = (cumul_sb_src_wps_err**2 + sb_src_wps_err**2)**0.5
            cumul_sb_tot_err      = (cumul_sb_tot_err**2 + sb_tot_err**2)**0.5
            cumul_sb_bg_err       = (cumul_sb_bg_err**2 + sb_bg_err**2)**0.5
            cumul_sb_src_err      = (cumul_sb_src_err**2 + sb_src_err**2)**0.5

            ######################################################################
            # write output profile file

            f.write('%f %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e\n' % (r, sb_src, sb_bg, sb_tot, sb_src_err, sb_bg_err, sb_tot_err, ctr_src, ctr_bg, ctr_tot, ctr_src_err, ctr_bg_err, ctr_tot_err, cts_src, cts_bg, cts_tot, cts_src_err, cts_bg_err, cts_tot_err, exp_time, area_correction, mask_area, geometric_area, sb_src_wps, sb_bg_wps, sb_tot_wps, sb_src_wps_err, sb_bg_wps_err, sb_tot_wps_err, ctr_src_wps, ctr_bg_wps, ctr_tot_wps, ctr_src_wps_err, ctr_bg_wps_err, ctr_tot_wps_err, cts_src_wps, cts_bg_wps, cts_tot_wps, cts_src_wps_err, cts_bg_wps_err, cts_tot_wps_err, exp_time_wps, area_correction_wps, mask_area_wps))


            ######################################################################
            # write output cumulative profile file

            g.write('%f %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e\n' % (r, cumul_sb_src, cumul_sb_bg, cumul_sb_tot, cumul_sb_src_err, cumul_sb_bg_err, cumul_sb_tot_err, cumul_ctr_src, cumul_ctr_bg, cumul_ctr_tot, cumul_ctr_src_err, cumul_ctr_bg_err, cumul_ctr_tot_err, cumul_cts_src, cumul_cts_bg, cumul_cts_tot, cumul_cts_src_err, cumul_cts_bg_err, cumul_cts_tot_err, exp_time, area_correction, mask_area, geometric_area, cumul_sb_src_wps, cumul_sb_bg_wps, cumul_sb_tot_wps, cumul_sb_src_wps_err, cumul_sb_bg_wps_err, cumul_sb_tot_wps_err, cumul_ctr_src_wps, cumul_ctr_bg_wps, cumul_ctr_tot_wps, cumul_ctr_src_wps_err, cumul_ctr_bg_wps_err, cumul_ctr_tot_wps_err, cumul_cts_src_wps, cumul_cts_bg_wps, cumul_cts_tot_wps, cumul_cts_src_wps_err, cumul_cts_bg_wps_err, cumul_cts_tot_wps_err, exp_time_wps, area_correction_wps, mask_area_wps))

            print "r :: ", r-1.0, r, geometric_area

        f.close()
        g.close()

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
