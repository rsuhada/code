from sys import argv
import math
from numpy import *
from pylab import rc
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, LogLocator
from scipy import optimize
# from sb_utils import beta_model, beta_model_likelihood
from sb_utils import arrays2minuit
import minuit
import sb_plotting_utils


if __name__ == '__main__':
    """
    Fit the extracted spectrum.
    """

    reload(sb_plotting_utils)

    # FIXME: 4.0 for 648x648, 2.5 for 900x900 binning
    pixscale = 4.0               # [arcsec/pix]

    ######################################################################
    # load in data

    intab = argv[1]
    dat=loadtxt(intab, dtype='string', comments='#', delimiter=None, converters=None,
                skiprows=0, unpack=False,
                # usecols=(0,1)
                )

    r = double(dat[:,0])
    sb_src = double(dat[:,1])
    sb_bg = double(dat[:,2])
    sb_tot = double(dat[:,3])
    sb_src_err = double(dat[:,4])
    sb_bg_err = double(dat[:,5])
    sb_tot_err = double(dat[:,6])
    ctr_src = double(dat[:,7])
    ctr_bg = double(dat[:,8])
    ctr_tot = double(dat[:,9])
    ctr_src_err = double(dat[:,10])
    ctr_bg_err = double(dat[:,11])
    ctr_tot_err = double(dat[:,12])
    cts_src = double(dat[:,13])
    cts_bg = double(dat[:,14])
    cts_tot = double(dat[:,15])
    cts_src_err = double(dat[:,16])
    cts_bg_err = double(dat[:,17])
    cts_tot_err = double(dat[:,18])
    exp_time = double(dat[:,19])
    area_correction = double(dat[:,20])
    mask_area = double(dat[:,21])
    geometric_area = double(dat[:,22])
    sb_src_wps = double(dat[:,23])
    sb_bg_wps = double(dat[:,24])
    sb_tot_wps = double(dat[:,25])
    sb_src_wps_err = double(dat[:,26])
    sb_bg_wps_err = double(dat[:,27])
    sb_tot_wps_err = double(dat[:,28])
    ctr_src_wps = double(dat[:,29])
    ctr_bg_wps = double(dat[:,30])
    ctr_tot_wps = double(dat[:,31])
    ctr_src_wps_err = double(dat[:,32])
    ctr_bg_wps_err = double(dat[:,33])
    ctr_tot_wps_err = double(dat[:,34])
    cts_src_wps = double(dat[:,35])
    cts_bg_wps = double(dat[:,36])
    cts_tot_wps = double(dat[:,37])
    cts_src_wps_err = double(dat[:,38])
    cts_bg_wps_err = double(dat[:,39])
    cts_tot_wps_err = double(dat[:,40])
    exp_time_wps = double(dat[:,41])
    area_correction_wps = double(dat[:,42])
    mask_area_wps = double(dat[:,43])

    ######################################################################
    # transform data

    r = r * pixscale                 # [acsec]

    ######################################################################
    # do the plots

    fname = intab+'.ctr.png'
    # sb_plotting_utils.plot_cts_profile(r, cts_src, cts_bg, fname)
    # sb_plotting_utils.plot_sb_profile(r, sb_src, sb_src_err, sb_bg, sb_bg_err, fname)

    ######################################################################
    # simple beta fit

    p0 = [5.0e-5, 10.0, 2.0/3.0]
    rgrid = linspace(0.0, 100.0, 100)

    ######################################################################
    # minuit fit

    data = arrays2minuit(r, sb_src, sb_src_err)

    def minuit_beta_model(r, norm, rcore, beta):
        """
        Return 2D beta model in a minuit compatible way.

        Arguments:
        - 'norm': normalization of the model
        - `rcore`: core radius
        - `beta`: beta exponent
        - `r`: radius
        """

        out = norm * (1.0 + (r/rcore)**2)**(-3.0*beta+0.5)
        return out

    def minuit_beta_model_likelihood(norm, rcore, beta):
        """
        Chi**2 likelihood function for the beta model fitting in a
        minuit compatible way.

        Arguments:
        - 'norm': normalization of the model
        - `rcore`: core radius
        - `beta`: beta exponent
        - `r`: radius
        """
        l = 0.0

        for r, sb_src, sb_src_err in data:
            l += (minuit_beta_model(r, norm, rcore, beta) - sb_src)**2 / sb_src_err**2

        return l

    ######################################################################
    # init parameters and fit limits

    norm0  = median(sb_src)
    rcore0 = 18.0               # [arcsec]
    beta0  = 2.0/3.0

    limit_norm  = (sb_src.min(), sb_src.max())
    limit_rcore = (pixscale, r.max())
    limit_beta  = (0.35, 3.0)         # (0.35, 3.0) - generous bounds
                                      # for uncostrained fit of
                                      # Alshino+10

    ######################################################################
    # the fit

    # setup
    model_fit =  minuit.Minuit(minuit_beta_model_likelihood,
                               norm=norm0, rcore=rcore0, beta=beta0,
                               limit_norm=limit_norm,
                               limit_rcore=limit_rcore,
                               limit_beta=limit_beta,
                               fix_norm=False,
                               fix_rcore=False,
                               fix_beta=False
                               )
    # fit
    model_fit.migrad()

    # model_fit.simplex()      # gradient-independent, but no goodness-of-fit eval/errors - check also starting point dependance

    # errors around best fit
    # model_fit.hesse()
    # model_fit.minos()    # non-linear error estimation if the likelihood is non-parabolic around best-fit (on a ~1 sigma scale)

    par_fitted = [model_fit.values["norm"], model_fit.values["rcore"], model_fit.values["beta"]]
    errors_fitted = model_fit.errors

    print "results: ", model_fit.values
    print "errors:  ", errors_fitted

    # error ellipses
    ell_points = 500            # num. of samples for the surface
    fname = intab+'.err-ellipse.png'

    ell1 = sort(array(model_fit.contour("beta", "rcore", 1, ell_points)))
    ell2 = sort(array(model_fit.contour("beta", "rcore", 2, 2*ell_points)))
    ell3 = sort(array(model_fit.contour("beta", "rcore", 3, 3*ell_points)))

    sb_plotting_utils.plot_minuit_err_ellipse(ell1, ell2, ell3, fname)

    ######################################################################
    # plot result

    # par_fitted = p0
    fname = intab+'.fit.png'
    sb_plotting_utils.plot_sb_fit(r, sb_src, sb_src_err, par_fitted, fname)

    plt.show()
    print "Done!"

    # run ~/data1/sw/esaspi/sb/sb-prof-fitter.py sb-prof-pn-111205-001.dat
