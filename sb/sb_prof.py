#!/usr/bin/env python
import sys
import pyfits
from numpy import *

def sqdistance(xcen, ycen, x, y):
    return (xcen - x)**2 + (ycen - y)**2

def dist_matrix(im, xcen, ycen):
    outmatrix = zeros([im.shape[0], im.shape[1]])
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            outmatrix[i, j] = sqdistance(xcen, ycen, j , i)

    return outmatrix

def get_stat(im, distmatrix, xim, yim, r_aper):
    ids = where(distmatrix <= r_aper)
    num_pix = len(ids[0])
    # print im[ids]
    tot_cts = sum(im[ids])
    mean_cts = mean(im[ids])
    stdev_cts =std(im[ids])

    # barring the 0 and less elements
    ids = where((distmatrix <= r_aper) & (im>0))
    num_pix_non0 = len(ids[0])
    tot_cts_non0 = sum(im[ids])
    mean_cts_non0 = mean(im[ids])
    stdev_cts_non0 =std(im[ids])

    maskfrac=double(num_pix_non0)/double(num_pix)

    return (tot_cts, mean_cts, stdev_cts, tot_cts_non0, mean_cts_non0, stdev_cts_non0, num_pix, num_pix-num_pix_non0, double(num_pix-num_pix_non0)/double(num_pix), maskfrac)

if __name__ == '__main__':
    """
    INPUT: input_image xcoord ycoord aperture [bg_image]

    EXAMPLE image.fits 315 324 10 bg.fits
    - coords are in ds9 image coords
    - aperture in im pixels
    """
    if len(sys.argv) > 4:
        ######################################################################
        # gather arguments
        imname = sys.argv[1]
        xim = double(sys.argv[2]) - 1.0
        yim = double(sys.argv[3]) - 1.0
        r_aper = double(sys.argv[4])**2                            # sqare for speedup

        ######################################################################
        # read in data
        fname = imname
        hdu = pyfits.open(fname)
        im = hdu[0].data

        distmatrix = dist_matrix(im, xim, yim)

        answer = get_stat(im, distmatrix, xim, yim, r_aper)

        #############################################################################
        # info output

        print
        print "image :: ", imname
        print "x [im ds9] :: ", xim + 1.0
        print "y [im ds9] :: ", yim + 1.0
        print "r_aper [im pix] :: ", sqrt(r_aper)
        print "----------------------------------"
        print "Center val :: ", im[yim, xim]
        print "Total num. pixels     :: ", answer[6]
        print "Total num. pixels <=0 :: ", answer[7]
        print "pixels <=0 fraction   :: ", answer[8]
        print "maskfrac              :: ", answer[9]
        print "----------------------------------"
        print "mean  > 0 pixels:: ", answer[4]
        print "stdev > 0 pixels:: ", answer[5]
        print "sum   > 0 pixels:: ", answer[3]
        print "----------------------------------"
        print "All pixels in aperture ::"
        print "mean  :: ", answer[1]
        print "stdev :: ", answer[2]
        print "sum   :: ", answer[0]
        print

        if len(sys.argv)==6:
            cts = answer[0]
            bgname = sys.argv[5]
            fname = bgname
            hdu = pyfits.open(fname)
            bg = hdu[0].data
            bgcts = get_stat(bg, distmatrix, xim, yim, r_aper)[0]

            mask = bg / bg

            ids = where(isnan(mask)==True)
            mask[ids] = 0.0
            # hdu = pyfits.PrimaryHDU(mask)
            # hdu.writeto('mask.fits', clobber=True)


            maskcts=get_stat(mask, distmatrix, xim, yim, r_aper)[0]

            areamask = mask + 1.0
            areamask = areamask / areamask
            areamaskcts = get_stat(areamask, distmatrix, xim, yim, r_aper)[0]

            correction=1.0 + (1.0 - maskcts/areamaskcts)

            print "bg image :: ", bgname
            print "BG CTS :: ", bgcts
            print "Source CTS ::", cts-bgcts
            print "mask area :: ", maskcts
            print "geom. area :: ", areamaskcts
            print "Corr. factor :: ", correction
            print "Area corrected BG CTS :: ", correction * bgcts
            print "Area corrected Source CTS ::", correction * (cts-bgcts)
        print

    else:
        print
        print "*** ERROR: not enough parameters : ", len(sys.argv),"!"
        print ""
        print "Syntax:"
        print "ctsaper <image> <center x coord> <center y coord> <aperture> [<bg image>]"
        print "- coords in ds9 image coordinates"
        print "- aperture in image pix"
        print "- bg image optional"
        print
        print "e.g.: ctsaper myimage.fits 325 168 50 mybg.fits"
        print


