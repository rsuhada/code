from numpy import *
import pyfits

######################################################################
# library collecting misc. utility functions for the surface
# brightness pipeline
######################################################################

def zero_pad_image(image, keep_radius):
    """
    Zero pad image - remove borders of a 2D array
    # FIXME: currently assumes image centered (maybe want to have a general approach?)

    Arguments:
    - `image`: 2d numpy array
    - `keep_radius`:
    """
    xsize = image.shape[0]

    image[:, 0:keep_radius]      = 0.0
    image[:, xsize-keep_radius:] = 0.0
    image[0:keep_radius,:]       = 0.0
    image[xsize-keep_radius:,:]  = 0.0

    return image


def load_fits_im(file_name='', extension=None):
    """
    Load an image from fits file extension, return also header.
    Only really useful if you want an image from single extension.

    Arguments:
    - 'file_name': fits file name
    - 'extension': number of extension to get image from
    """
    if not extension: extension = 0 # tmp fix until see below
    hdu   = pyfits.open(file_name)
    image = hdu[extension].data
    hdr   = hdu[extension].header
    return image, hdr


    # # FIXME: add file existence check and no image extension handling
    # # if no extension specified find the first image
    # if not extension:   # switch to extension = None in function def not "0" (which is a valid extension)
    #     for table in hdu:
    #         hdr = table.header
    #         print "header", hdu
    #         # this is not correct - there can be IMAGE in a non-IMAGE
    #         # extension, try nacis
    #         if 'IMAGE' in hdr.values():
    #             image = table.data
    #             return image, hdr
    # else:
    #     image = hdu[extension].data
    #     hdr   = hdu[extension].header
    #     return image, hdr

    # # error
    # return 1, 1


def sqdistance(xcen, ycen, x, y):
    """
    Calculate the squared Euclidean distance.
    """
    return (xcen - x)**2 + (ycen - y)**2

def sqdist_matrix(im, xcen, ycen):
    """
    Create a matrix given the squared Euclidean distance of each point
    wrt the input center.
    """
    outmatrix = zeros([im.shape[0], im.shape[1]])
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            outmatrix[i, j] = sqdistance(xcen, ycen, j , i)

    return outmatrix

def distance_matrix(im, xcen, ycen):
    """
    Return distance matrix. This can be used in bincount (after
    recasting to int). Solution from stackoverflow, should be really
    fast.
    """
    outmatrix = sqrt(arange(-xcen, im.shape[0]-xcen, dtype=float)[:,None]**2
          + arange(-ycen, im.shape[1]-ycen, dtype=float)[None,:]**2)
    return outmatrix

def distance_matrix_bin(im, xcen, ycen, rgrid):
    """
    Return binned distance matrix using the input radii,

    Arguments:
    - `im`: 2D array - image
    - `xcen`: x coordinate [pix]
    - `ycen`: y coordinate [pix]
    - `rgrid`: radius grid array [pix]
    """
    outmatrix = sqrt(arange(-xcen, im.shape[0]-xcen, dtype=float)[:,None]**2
          + arange(-ycen, im.shape[1]-ycen, dtype=float)[None,:]**2)
    return outmatrix

def get_cts_stat(im, distmatrix, xim, yim, r_aper):
    """
    Provide basic statistics (total/mean cts etc.) for an input image
    in an aperture around the chosen center.
    """
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

def get_cts_stat_annul(im, distmatrix, xim, yim, r_min, r_max):
    """
    Provide basic statistics (total/mean cts etc.) for an input image
    in an annulus (r_min<r<=r_max) aperture around the chosen center.
    """
    ids = where((distmatrix <= r_max) & (r_min < distmatrix))
    num_pix = len(ids[0])
    # print im[ids]
    tot_cts = sum(im[ids])
    mean_cts = mean(im[ids])
    stdev_cts =std(im[ids])

    # barring the 0 and less elements
    ids = where((distmatrix <= r_max) & (r_min < distmatrix) & (im>0))
    num_pix_non0 = len(ids[0])
    tot_cts_non0 = sum(im[ids])
    mean_cts_non0 = mean(im[ids])
    stdev_cts_non0 =std(im[ids])

    maskfrac=double(num_pix_non0)/double(num_pix)

    return (tot_cts, mean_cts, stdev_cts, tot_cts_non0, mean_cts_non0, stdev_cts_non0, num_pix, num_pix-num_pix_non0, double(num_pix-num_pix_non0)/double(num_pix), maskfrac)

def cal_aper_sum(im, distmatrix, xim, yim, r_aper):
    """
    NOTE: not used atm.
    Return the sum af all input image pixels within the aperture.
    This is th stripped down version of get_cts_stat.
    """
    ids = where(distmatrix <= r_aper)
    num_pix = len(ids[0])
    tot_cts = sum(im[ids])

    return (tot_cts)

def beta_model(pars, r):
    """
    Return 2D beta model.

    Arguments:
    - 'pars': parameter list containg:
        - 'norm': normalization of the model
        - `rcore`: core radius
        - `beta`: beta exponent
    - `r`: radius
    """

    [norm, rcore, beta] = pars

    out = norm * (1.0 + (r/rcore)**2)**(-3.0*beta+0.5)
    return out


def beta_model_likelihood(r, data, data_err, beta_pars):
    """
    Likelihood function for the beta model fitting

    Arguments:
    - `r`: radius
    - `data`: curve (surface brightnes) -> data
    - `data_err`: error on curve (surface brightnes) -> data
    - 'beta_pars: list of beta mode parameters = [norm, rcore, beta]'
    """
    from sb_utils import beta_model

    model = beta_model(beta_pars, r)
    l = sum(((data-model)/data_err)**2.0)

    return l


def arrays2minuit(x, y, y_err):
    """
    Convert the three numpy input arrays into a minuit compatible input data
    structure (list of tuples, where each tuple has 3 element: x[i], y[i],
    y_err[i])
    """

    minuit_data = []

    for i in range(len(x)):
        minuit_data.append((x[i],y[i],y_err[i]))

    return minuit_data

def get_psf_king_pars(instrument, energy, theta):
    """
    Provides the rcore and alpha (slope) of a King profile of the PSF
    for the given instrument based on Ghizzardi 2001 (MOS1 + MOS2,
    CAL-TN-22) and (PN, CAL-TN-29) from inflight calibration
    available:

    http://xmm.vilspa.esa.es/external/xmm_sw_cal/calib/documentation.shtml

    Arguments:
    - 'instrument': "pn", "m1", "m2"
    - 'energy': energy [keV]
    - 'theta': offaxis angle [arcmin]

    Output:
    - 'rcore': King model core radius [arcsec]
    - 'alpha': King model slope
    """

    if (instrument == "m1"):
        # rcore pars
        a     =  5.074
        a_err =  0.001
        b     = -0.236
        b_err =  0.001
        c     =  0.002
        c_err =  0.001
        d     = -0.0180
        d_err =  0.0006

        # alpha pars
        x     =  1.472
        x_err =  0.003
        y     = -0.010
        y_err =  0.001
        z     = -0.001
        z_err =  0.002
        w     = -0.0016
        w_err =  0.0013

    elif (instrument == "m2"):
        # rcore pars
        a     =  4.759
        a_err =  0.018
        b     = -0.203
        b_err =  0.010
        c     =  0.014
        c_err =  0.017
        d     = -0.0229
        d_err =  0.0133

        # alpha pars
        x     =  1.411
        x_err =  0.001
        y     = -0.005
        y_err =  0.001
        z     = -0.001
        z_err =  0.002
        w     = -0.0002
        w_err =  0.0011

    elif (instrument == "pn"):
        # rcore pars
        a     =  6.636
        a_err =  0.020
        b     = -0.305
        b_err =  0.032
        c     = -0.175
        c_err =  0.010
        d     = -0.0067
        d_err =  0.0185

        # alpha pars
        x     =  1.525
        x_err =  0.001
        y     = -0.015
        y_err =  0.001
        z     = -0.012
        z_err =  0.001
        w     = -0.0010
        w_err =  0.0004

    else:
        print "*** Error: unknown instrument for PSF King model parameter calculation"

    # rcore = 1.0
    # alpha = 1.0

    rcore = a + b * energy + c * theta + d * energy * theta
    alpha = x + y * energy + z * theta + w * energy * theta

    return (rcore, alpha)

def king_profile(r, rcore, alpha):
    """
    Returns a king profile on the input grid

    Arguments:
    - `r`: input radii [arcsec]
    - 'rcore': King model core radius [arcsec]
    - 'alpha': King model slope
    """

    y = 1 / ( 1 + (r/rcore)**2 )**alpha

    return y

# def lmfit_get_ci(fit, sigmas=(0.67400000000000004, 0.94999999999999996, 0.997)):
#     """
#     Calculate the 2D confidence intervals for a lmfit results

#     Arguments:
#     - `fit`: lmfit minimizer (containg results)
#     """

#     ci, trace = lm.conf_interval(result,sigmas=sigmas, trace=True, verbose=0, maxiter=1)
#     lmfit.printfuncs.report_ci(ci)



def optibingrid(binnum=20, rmax=100, c=1.2):
    """
    Calculate the profile grid using the "optimal" binning (see
    Andersson et al. 2011)

    Arguments:
    - 'binnum': total number of bins [20]
    - 'rmax': maximal radius [100 pix, recommended 1.5r500]
    """
    r = array([(i * rmax**(1.0/c)/binnum)**c for i in range(binnum)])

    return r

def optibin(im, xcen, ycen, rgrid):
    """
    Extract from the image a profile using the optimal binning (see
    Andersson et al. 2011)

    Arguments:
    - 'im': 2d array
    - 'xcen': x coordinate of the center [pix]
    - 'ycen': x coordinate of the center [pix]
    - 'rgrid': radii grid (recommendation: 1.5r500) [pix]
    """

    return 0

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

    t1 = time.clock()

    distmatrix = sqrt(sqdist_matrix(im, xcen, ycen))

    t2 = time.clock()
    print "dist matrix took: ", t2-t1, " s"

    # rgrid = arange(1, distmatrix.max()+1, 1.0)  # maximal possible distance (to corner)
    rgrid = arange(1, im.shape[0]/2+1, 1.0)  # maximal possible distance (to side)
    n = len(rgrid)

    x = zeros(n, dtype=float)   # profile
    geometric_area = zeros(n, dtype=float)  # area normalised profile

    t1 = time.clock()

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

    t2 = time.clock()
    print "extraction took: ", t2-t1, " s"

    return (rgrid, x, geometric_area)

def extract_profile_fast(im, distmatrix, xcen, ycen):
    """
    Improved function to extract a 1D profile of a 2D image profile[i]
    plotted at r[i] gives the sum for r[i-1] < r < r[i] ring.  For
    plotting and comparison you might want to do r-1 (central pixel is
    r=0). Note that this is slightly different from the
    extract_profile_generic, where there is only a 0.5 pix shift.

    Arguments:
    - `im`: 2D array
    - `distmatrix`: 2D array distmatrix - has to be int type
    - `xcen`: center x coordinate
    - `ycen`: center y coordinate
    """
    geometric_area = bincount(distmatrix.flat)
    profile = bincount(distmatrix.flat, weights=im.flat)

    return (profile, geometric_area)

def extract_binned_sb_profiles(distmatrix, rgrid, im, expmap, bgmap, maskmap):
    """
    Extract cts, ctr and surface brightness radial profiles.
    - `distmatrix`: distance matrix wrt the desired center
    - `rgrid`: grid with aperture boundaries [pix]
    - `im`: cluster image [cts]
    - `expmap`: exposure map [s]
    - `bgmap`: background map [cts]
    - `maskmap`: detector mask map
    """
    # use the histogram trick to extract profiles
    cts_tot = array(histogram(distmatrix, bins=rgrid, weights=im)[0])
    cts_bg = array(histogram(distmatrix, bins=rgrid, weights=bgmap)[0])
    expt = array(histogram(distmatrix, bins=rgrid, weights=expmap)[0])
    mask_area = array(histogram(distmatrix, bins=rgrid, weights=maskmap)[0]) # mask area
    geo_area = array(histogram(distmatrix, bins=rgrid)[0]) # geometric area

    # area correction due to point sources
    geo_area = geo_area.astype('float')
    mask_area = mask_area.astype('float')
    ps_area_corr = 1.0 + (1.0 - mask_area/geo_area)

    # correct for are missing in removed ps
    cts_tot = cts_tot * ps_area_corr
    cts_bg = cts_bg * ps_area_corr

    ctr_tot = 0.0 * cts_tot
    ctr_bg  = 0.0 * cts_bg

    # calculate the count rates
    idx = where(expt>0.0)
    ctr_tot[idx] = cts_tot[idx]/expt[idx]
    ctr_bg[idx]  = cts_bg[idx]/expt[idx]

    # calculate the surface brightness (already corrected for missing
    # ps - use geo_area not mask_area)
    sb_tot          = ctr_tot/geo_area
    sb_bg           = ctr_bg/geo_area

    # poisson errors
    cts_tot_err = sqrt(cts_tot)
    cts_bg_err  = sqrt(cts_bg)
    # cts_src_err = sqrt(cts_tot_err**2.0 + cts_bg_err**2.0)

    ctr_tot_err = cts_tot_err/expt
    ctr_bg_err  = cts_bg_err/expt
    # ctr_src_err = sqrt(ctr_tot_err**2.0 + ctr_bg_err**2.0)

    sb_tot_err  = ctr_tot_err/geo_area
    sb_bg_err   = ctr_bg_err/geo_area
    # sb_src_err  = ctr_src_err/mask_area

    # return just the surface brightnesses for speed/handling ease
    return sb_tot, sb_tot_err, sb_bg, sb_bg_err

    # extended return
    # return cts_tot, cts_tot_err, ctr_tot, ctr_tot_err, sb_tot, sb_tot_err, \
           # cts_bg, cts_bg_err, ctr_bg, ctr_bg_err, sb_bg, sb_bg_err
