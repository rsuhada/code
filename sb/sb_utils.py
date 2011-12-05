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
