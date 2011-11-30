from numpy import *

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
