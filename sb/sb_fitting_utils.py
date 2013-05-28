import sys
import os
import math
from numpy import *
from pylab import rc
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, LogLocator
from sb_plotting_utils import plot_sb_profile, plot_cts_profile, plot_data_model_simple, plot_data_model_resid, plt_like_surface
from esaspi_utils import *
from sb_utils import distance_matrix
from sb_models import *
import lmfit as lm
import time
import asciitable as atab
import pickle

def load_sb_curve(fname):
    """
    Loads the surface brightness curve from file.

    Arguments:
    - `fname`: file name
    """

    data = atab.read(table=fname,
                     data_start=0, data_end=None, header_start=9,
                     delimiter=' ', comment='#', quotechar='"')

    r = data['r']
    sb_src = data['ctr_src']
    sb_bg = data['ctr_bg']
    sb_src_err = data['ctr_src_err']
    sb_bg_err = data['ctr_bg_err']

    # dat=loadtxt(fname, dtype='string', comments='#', delimiter=None, converters=None,
    #         skiprows=0, unpack=False,
    #         # usecols=(0,1,2,4,5)
    #         usecols=(0,1,2,4,5,6,7,10,11)
    #         )

    # r = double(dat[:,0])
    # sb_src = double(dat[:,1])
    # sb_bg = double(dat[:,2])
    # sb_src_err = double(dat[:,3])
    # sb_bg_err = double(dat[:,4])

    return r, sb_src, sb_bg, sb_src_err, sb_bg_err


def print_fit_diagnostics(result, delta_t=-1.0, ndata=None):
    """
    Print fit diagnostic output

    Arguments:
    - `result`: lmfit result minimizer class
    - `delta_t`: fit time
    - `nfree_true`: tru number of degrees of freedom (differs from the
      number in result if using multiple instruments - it sees only
      one of them)
    """

    print
    print '='*70
    print 'Diagnostics'
    print '='*70

    print
    print 'nfev          :: ', result.nfev
    print 'message       :: ', result.message
    print 'ier           :: ', result.ier
    print 'lmdif_message :: ', result.lmdif_message

    print
    print
    print '='*70

    print 'fitting took :: ', delta_t, ' s'
    print 'success      :: ', result.success
    print 'nfev         :: ', result.nfev
    print 'nvarys       :: ', result.nvarys
    print 'residual     :: ', sum(result.residual)
    print 'chisqr       :: ', result.chisqr
    print
    print 'ndata lmfit  :: ', result.ndata
    print 'nfree lmfit  :: ', result.nfree
    print 'redchi lmfit :: ', result.redchi
    print

    if ndata:
        print 'ndata        :: ', ndata
        print 'nfree        :: ', ndata - result.nvarys
        print 'redchi       :: ', result.chisqr / (ndata - result.nvarys)
    else:
        print 'ndata        :: ', result.ndata
        print 'nfree        :: ', result.nfree
        print 'redchi       :: ', result.redchi


    print '='*70
    print



def sanitize_sb_curve(sb_curve_tuple):
    """
    Clean the curves by removing bins with negative values.

    Arguments: sb_curve_tuple containing:
    - `r`:
    - `sb_src`:
    - `sb_bg`:
    - `sb_src_err`:
    - `sb_bg_err`:
    """
    (r, sb_src, sb_bg, sb_src_err, sb_bg_err) = sb_curve_tuple

    # non-0 and non-NaN
    ids1 = where(sb_src>0.0)
    ids2 = where(negative(isnan(sb_src)))

    # ids = unique(hstack((ids1, ids2)))
    ids = ids2

    r = r[ids]
    sb_src = sb_src[ids]
    sb_bg = sb_bg[ids]
    sb_src_err = sb_src_err[ids]
    sb_bg_err = sb_bg_err[ids]

    return (r, sb_src, sb_bg, sb_src_err, sb_bg_err)


def fit_beta_model(r, sb_src, sb_src_err, instrument, theta, energy, results_pickle=None):
    """
    Fit a beta x psf model

    Arguments:
    - `r`:
    - `sb_src`:
    - `sb_src_err`:
    """

    # settings
    APPLY_PSF = True
    DO_ZERO_PAD = True
    DO_FIT = True
    PLOT_PROFILE = True

    ######################################################################
    # modelling is done in 2D and then projected - setup here the 2D
    # parameters

    size = 2.0 * r.max()
    xsize = size
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2
    # imsize = input_im.shape         # FIXME: is this necessary? I could just use it inside the model
    imsize = (size, size)         # FIXME: is this necessary? I could just use it inside the model

    xsize_obj = xsize # 100             # if running t1.fits set to 100 else xsize
    ysize_obj = xsize_obj
    xcen_obj = xsize_obj / 2
    ycen_obj = ysize_obj / 2
    r_aper = xsize_obj  / 2        # aperture for the fitting

    ######################################################################
    # create the distance matrix for speedup

    distmatrix = distance_matrix(zeros((imsize[0]-2, imsize[1]-2)), xcen_obj, ycen_obj).astype(int) # need int for bincount

    ######################################################################
    # init beta model

    pars = lm.Parameters()
    pars.add('norm_'+instrument, value=mean(sb_src), vary=True, min=0.0, max=sum(abs(sb_src)))
    pars.add('rcore', value=5.0, vary=True, min=0.05, max=80.0)
    pars.add('beta', value=0.8, vary=True, min=0.1, max=10.0)
    pars.add('xcen', value=xcen_obj, vary=False)
    pars.add('ycen', value=ycen_obj, vary=False)

    # sb_src = sb_src * r

    nonfit_args = (imsize, xsize_obj, ysize_obj, distmatrix, instrument, theta,
                   energy, APPLY_PSF, DO_ZERO_PAD, sb_src,
                   sb_src_err)

    # leastsq_kws={'xtol': 1.0e7, 'ftol': 1.0e7, 'maxfev': 1.0e+0} # debug set
    leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+7}

    ######################################################################
    # do the fit: beta

    if DO_FIT:
        print "starting beta fit"
        t1 = time.clock()

        result = lm.minimize(beta_psf_2d_lmfit_profile,
                             pars,
                             args=nonfit_args,
                             **leastsq_kws)

        result.leastsq()

        t2 = time.clock()
        print "fitting took: ", t2-t1, " s"

        # get the output model
        (r_model, profile_norm_model) = beta_psf_2d_lmfit_profile(pars,
                                                                  imsize,
                                                                  xsize_obj,
                                                                  ysize_obj,
                                                                  distmatrix,
                                                                  instrument,
                                                                  theta,
                                                                  energy,
                                                                  APPLY_PSF,
                                                                  DO_ZERO_PAD)

    ######################################################################
    # save structures

    if DO_FIT and results_pickle:
        outstrct = lmfit_result_to_dict(result, pars)

        with open(results_pickle, 'wb') as output:
            pickle.dump(outstrct, output, pickle.HIGHEST_PROTOCOL)

        ######################################################################
        # output

    if DO_FIT:
        # print_result_tab(pars_true, pars)
        lm.printfuncs.report_errors(result.params)

        with open(results_pickle+'.txt', 'w') as f:
            sys.stdout = f
            lm.printfuncs.report_errors(result.params)
            print "fitting took: "+str(t2-t1)+" s"
            sys.stdout = sys.__stdout__

        print "fitting subroutine done!"

    ######################################################################
    # plot beta fit and data profiles

    if DO_FIT and PLOT_PROFILE:

        output_figure = results_pickle+'.beta_psf.png'

        print "result plot :: ", output_figure

        plot_data_model_resid(r, sb_src,
                              r_model, profile_norm_model,
                              output_figure, sb_src_err)

    print "results written to:: ", results_pickle
    return 0


def fit_beta_model_joint(r, sb_src, sb_src_err, instruments, theta, energy, results_pickle=None):
    """
    Fit a beta x psf model to any combination of instruments via joint
    likelihood

    Arguments:
    """

    # settings
    APPLY_PSF = True
    DO_ZERO_PAD = True
    DO_FIT = True
    CALC_1D_CI = False           # in most cases standard error is good
                                # enough, this is not needed then
    CALC_2D_CI = True
    PLOT_PROFILE = True
    PRINT_FIT_DIAGNOSTICS = True


    ######################################################################
    # modelling is done in 2D and then projected - setup here the 2D
    # parameters

    size = 2.0 * r.max()
    xsize = size
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2
    # imsize = input_im.shape         # FIXME: is this necessary? I could just use it inside the model
    imsize = (size, size)         # FIXME: is this necessary? I could just use it inside the model

    xsize_obj = xsize # 100             # if running t1.fits set to 100 else xsize
    ysize_obj = xsize_obj
    xcen_obj = xsize_obj / 2
    ycen_obj = ysize_obj / 2
    r_aper = xsize_obj  / 2        # aperture for the fitting

    # pre-calculate distmatrix for speedup - it is same for all
    # instruments
    distmatrix = distance_matrix(zeros((imsize[0]-2, imsize[1]-2)), xcen_obj, ycen_obj).astype(int) # need int for bincount

    ######################################################################
    # scale the data

    scale_sb_src = {}
    scale_sb_src_err = {}
    ndata = 0

    for instrument in instruments:
        scale_sb_src[instrument] = median(sb_src[instrument])
        sb_src[instrument] = sb_src[instrument] / scale_sb_src[instrument]
        sb_src_err[instrument] = sb_src_err[instrument] / scale_sb_src[instrument]
        ndata += len(sb_src[instrument])

    ######################################################################
    # init beta model

    pars = lm.Parameters()
    pars.add('rcore', value=5.0, vary=True, min=0.05, max=80.0)
    pars.add('beta', value=0.67, vary=True, min=0.1, max=10.0)
    pars.add('xcen', value=xcen_obj, vary=False)
    pars.add('ycen', value=ycen_obj, vary=False)

    for instrument in instruments:
        pars.add('norm_'+instrument, value=mean(sb_src[instrument]),
                 vary=True, min=min(sb_src[instrument]),
                 max=sum(abs(sb_src[instrument])))

    # sb_src = sb_src * r

    nonfit_args = (imsize, xsize_obj, ysize_obj, distmatrix, instruments,
                   theta, energy, APPLY_PSF, DO_ZERO_PAD, sb_src,
                   sb_src_err)

    # leastsq_kws={'xtol': 1.0e7, 'ftol': 1.0e7, 'maxfev': 1.0e+0} # debug set; quickest
    # leastsq_kws={'xtol': 1.0e7, 'ftol': 1.0e7, 'maxfev': 1.0e+4} # debug set; some evol

    leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+7}
    # leastsq_kws={'xtol': 1.0e-8, 'ftol': 1.0e-8, 'maxfev': 1.0e+9}

    ######################################################################
    # do the fit: beta

    if DO_FIT:
        print "starting beta fit"
        t1 = time.clock()

        result = lm.minimize(beta_psf_2d_lmfit_profile_joint,
                             pars,
                             args=nonfit_args,
                             **leastsq_kws)

        result.leastsq()

        t2 = time.clock()

        print
        print
        print "fitting took: ", t2-t1, " s"
        print
        print

        ######################################################################
        # scale the data back

        for instrument in instruments:
            sb_src[instrument] = sb_src[instrument] * scale_sb_src[instrument]
            sb_src_err[instrument] = sb_src_err[instrument] * scale_sb_src[instrument]

            # scale also the fitted norm
            pars['norm_'+instrument].value = pars['norm_'+instrument].value * scale_sb_src[instrument]
            pars['norm_'+instrument].stderr = pars['norm_'+instrument].stderr * scale_sb_src[instrument]
            pars['norm_'+instrument].max = pars['norm_'+instrument].max * scale_sb_src[instrument]
            pars['norm_'+instrument].min = pars['norm_'+instrument].min * scale_sb_src[instrument]

        ######################################################################
        # get the output model
        (r_model, profile_norm_model) = \
            beta_psf_2d_lmfit_profile_joint(pars, imsize,
                                            xsize_obj, ysize_obj,
                                            distmatrix,
                                            instruments, theta,
                                            energy,
                                            APPLY_PSF, DO_ZERO_PAD)


        ######################################################################
        # save structures

        if results_pickle:
            outstrct = lmfit_result_to_dict(result, pars)

            with open(results_pickle, 'wb') as output:
                pickle.dump(outstrct, output, pickle.HIGHEST_PROTOCOL)

                print "results written to:: ", results_pickle

        ######################################################################
        # output

        if PRINT_FIT_DIAGNOSTICS:
            print_fit_diagnostics(result, t2-t1, ndata)

        # print_result_tab(pars_true, pars)
        lm.printfuncs.report_errors(result.params)

        with open(results_pickle+'.txt', 'w') as f:
            sys.stdout = f

            if PRINT_FIT_DIAGNOSTICS:
                print_fit_diagnostics(result, t2-t1, ndata)

            print
            print
            lm.printfuncs.report_errors(result.params)
            print
            print

            sys.stdout = sys.__stdout__

        print
        print "fitting subroutine done!"

    ######################################################################
    # plot beta fit and data profiles

    if DO_FIT and PLOT_PROFILE:
        for instrument in instruments:
            output_figure = results_pickle+'.'+instrument+'.beta_psf.png'

            print "result plot :: ", output_figure

            # FIXME: implement plotter for joint fits
            plot_data_model_resid(r, sb_src[instrument],
                              r_model, profile_norm_model[instrument],
                              output_figure, sb_src_err[instrument])

    ######################################################################
    # FIXME: not yet ported, confidence intervals

    if DO_FIT and CALC_1D_CI:
        print "Calculating 1D confidence intervals"
        # sigmas = [0.682689492137, 0.954499736104, 0.997300203937]
        sigmas = [0.682689492137, 0.954499736104]
        ci_pars = ['rcore', 'beta']

        ci, trace = lm.conf_interval(result, p_names=ci_pars, sigmas=sigmas,
                              trace=True, verbose=True, maxiter=1)

        lm.printfuncs.report_ci(ci)

    if DO_FIT and  CALC_2D_CI:
        output_figure = results_pickle+'.2d_like_beta_psf.png'
        from timer import Timer

        with Timer() as t:
            print "Calculating 2D confidence intervals"
            x, y, likelihood = lm.conf_interval2d(result,'rcore','beta', 30, 30)
            plt_like_surface(x, y, likelihood, output_figure, 'rcore', 'beta')

        print "elasped time:", t.secs, " s"


    # import IPython
    # IPython.embed()

    return 0


# FIXME: implement outpickle
def fit_v06_model(r, sb_src, sb_src_err, instrument, theta, energy, results_pickle=None):
    """
    Testing simple 1D fit of v06 model with psf convolution
    """
    APPLY_PSF = True
    DO_ZERO_PAD = True
    DO_FIT = True
    PLOT_PROFILE = True
    CALC_1D_CI = False
    CALC_2D_CI = False

    ######################################################################
    # modelling is done in 2D and then projected - setup here the 2D
    # parameters

    size = 2.0 * r.max()
    xsize = size
    ysize = xsize
    xcen = xsize/2
    ycen = ysize/2
    # imsize = input_im.shape     # FIXME: is this necessary? I could just use it inside the model
    imsize = (size, size)         # FIXME: is this necessary? I could just use it inside the model

    xsize_obj = xsize # 100             # if running t1.fits set to 100 else xsize
    ysize_obj = xsize_obj
    xcen_obj = xsize_obj / 2
    ycen_obj = ysize_obj / 2
    r_aper = xsize_obj  / 2        # aperture for the fitting

    ######################################################################
    # init model

    n0 = 7e+0
    rc = 20.0
    beta = 4.0/3.0
    rs = 20.0
    alpha = 1.5
    gamma = 3.0
    epsilon = 1.5

    rmax = 100.0
    r500_pix = rmax

    # v06 pars lmfit structure
    pars = lm.Parameters()
    pars.add('n0'      , value=n0, vary=True, min=1.0e-9, max=1.0e3)
    pars.add('rc'      , value=rc, vary=True, min=0.05, max=rmax)
    pars.add('beta'    , value=beta, vary=True, min=0.05, max=2.0)
    pars.add('rs'      , value=rs, vary=True, min=0.05, max=2*rmax)
    pars.add('alpha'   , value=alpha, vary=True, min=0.01, max=3.0)
    pars.add('epsilon' , value=epsilon, vary=True, min=0.0, max=5.0)
    pars.add('gamma'   , value=gamma, vary=False)

    # set the ancilarry parameters
    # +1 bc of the central divergence
    data = empty(imsize)
    distmatrix_input = distance_matrix(data, xcen_obj, ycen_obj).astype('int') + 1
    bgrid = unique(distmatrix_input.flat)

    # gather all non-fit arguments
    nonfit_args = (distmatrix_input, bgrid, r500_pix, psf_pars,
                   xcen_obj, ycen_obj)

    ######################################################################
    # do the fit: v06

    nonfit_args = (distmatrix_input, bgrid, r500_pix, psf_pars,
                   xcen_obj, ycen_obj, sb_src, sb_src_err)

    # leastsq_kws={'xtol': 1.0e7, 'ftol': 1.0e7, 'maxfev': 1.0e+0} # debug set
    leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+7}

    if DO_FIT:
        print "starting v06 fit"
        t1 = time.clock()

        result = lm.minimize(v06_psf_2d_lmfit_profile,
                             pars,
                             args=nonfit_args,
                             **leastsq_kws)
        result.leastsq()

        t2 = time.clock()
        print "fitting took: ", t2-t1, " s"

        # get the output model
        (r_model, profile_norm_model) = v06_psf_2d_lmfit_profile(pars,
                                                                 distmatrix_input,
                                                                 bgrid,
                                                                 r500_pix,
                                                                 psf_pars,
                                                                 xcen_obj,
                                                                 ycen_obj)

    ######################################################################
    # output

    if DO_FIT:
        lm.printfuncs.report_errors(result.params)
        # print_result_tab(pars_true, pars)

    ######################################################################
    # FIXME: not yet ported, confidence intervals

    if CALC_1D_CI:
        print "Calculating 1D confidence intervals"
        # sigmas = [0.682689492137, 0.954499736104, 0.997300203937]
        sigmas = [0.682689492137, 0.954499736104]
        ci_pars = ['rcore', 'beta']

        ci, trace = lm.conf_interval(result, p_names=ci_pars, sigmas=sigmas,
                              trace=True, verbose=True, maxiter=1)

        lm.printfuncs.report_ci(ci)

    if CALC_2D_CI:
        from timer import Timer

        with Timer() as t:
            print "Calculating 2D confidence intervals"
            x, y, prob = lm.conf_interval2d(result,'rcore','beta',20,20)
            plt.contourf(x,y,prob)

        print "elasped time:", t.secs, " s"

    ######################################################################
    # plot v06 profiles

    if DO_FIT and PLOT_PROFILE:

        # output_figure = '/Users/rs/w/xspt/data/dev/0559/sb/lmfit_v06_psf.png'
        output_figure = fname+'.beta_fit.png'

        print len(r), len( sb_src), len( r_model), len( profile_norm_model)

        # plot_data_model_resid(r, sb_src,
        #                       r_model, profile_norm_model,
        #                       output_figure, sb_src_err)

        print r[0], r_model[0]
