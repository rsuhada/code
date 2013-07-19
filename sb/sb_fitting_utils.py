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
from sb_utils import distance_matrix, optibingrid
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
    # FIXME: refactor to have a unified reading based on topcatformat

    try:
        # old format: headerstart=9
        data = atab.read(table=fname,
                         data_start=0, data_end=None, header_start=9,
                         delimiter=' ', comment='#', quotechar='"')

    except Exception, e:
        # new format: headerstart=11
        data = atab.read(table=fname,
                         data_start=0, data_end=None, header_start=11,
                         delimiter=' ', comment='#', quotechar='"')

    r = data['r']
    sb_src = data['ctr_src']
    sb_bg = data['ctr_bg']
    sb_src_err = data['ctr_src_err']
    sb_bg_err = data['ctr_bg_err']

    return r, sb_src, sb_bg, sb_src_err, sb_bg_err


def print_fit_diagnostics(result, delta_t=-1.0, ndata=None, leastsq_kws=None):
    """
    Print fit diagnostic output

    Arguments:
    - `result`: lmfit result minimizer class
    - `delta_t`: fit time
    - `ndata`: true number of data (differs from the number in result
               if using multiple instruments - it sees only one of them)
    """

    print
    print '='*70
    print 'Diagnostics'
    print '='*70

    print 'nfev          :: ', result.nfev
    print 'message       :: ', result.message

    # not all fitters have it
    if hasattr(result, 'ier'):
        print 'ier           :: ', result.ier
        print 'lmdif_message :: ', result.lmdif_message
        print 'success      :: ', result.success

    if leastsq_kws: print 'leastsq_kws   :: ', leastsq_kws

    print
    print '='*70

    print 'fitting took :: ', delta_t, ' s'
    print 'nfev         :: ', result.nfev
    print 'nvarys       :: ', result.nvarys
    print

    if hasattr(result, 'chisqr'):
        print 'ndata lmfit  :: ', result.ndata
        print 'nfree lmfit  :: ', result.nfree
        print 'residual     :: ', sum(result.residual)
        print 'chisqr       :: ', result.chisqr
        print
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
    FIT_METHOD = 'simplex'
    # FIT_METHOD = 'leastsq'     # 'leastsq' - Levemberg-Markquardt,
                                 # 'simplex' - simplex

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
                   energy, APPLY_PSF, DO_ZERO_PAD, r, sb_src,
                   sb_src_err)

    # fit stop criteria
    if FIT_METHOD == 'leastsq':
        leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+0} # debug set; quickest
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+4} # debug set; some evol
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+7}
        # leastsq_kws={'xtol': 1.0e-8, 'ftol': 1.0e-8, 'maxfev': 1.0e+9}

    if FIT_METHOD == 'simplex':
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfun': 1.0e+0} # debug set; quickest
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfun': 1.0e+4} # debug set; some evol
        leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfun': 1.0e+7}
        # leastsq_kws={'xtol': 1.0e-8, 'ftol': 1.0e-8, 'maxfun': 1.0e+9}

    ######################################################################
    # do the fit: beta

    if DO_FIT:
        print "starting beta fit"
        t1 = time.clock()

        result = lm.minimize(beta_psf_2d_lmfit_profile,
                             pars,
                             args=nonfit_args,
                             method=FIT_METHOD,
                             **leastsq_kws)

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
    FIT_METHOD = 'simplex'
    # FIT_METHOD = 'leastsq'     # 'leastsq' - Levemberg-Markquardt,
                                 # 'simplex' - simplex
    CALC_1D_CI = False           # in most cases standard error is good
                                # enough, this is not needed then
    CALC_2D_CI = False
    PLOT_PROFILE = True
    PRINT_FIT_DIAGNOSTICS = True

    ######################################################################
    # modelling is done in 2D and then projected - setup here the 2D
    # parameters

    # FIXME:
    # 2013-07-11 - lot of vars are deprecated, but it works ok, just
    # redundant

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

    # r contains the start of the innermost bin for integration, but not needed for plotting
    rplt = r[1:]

    ######################################################################
    # scale the data - not really necessary? do val-min/(max-min)

    # scale_sb_src = {}
    # scale_sb_src_err = {}
    ndata = 0

    for instrument in instruments:
        # scale_sb_src[instrument] = median(sb_src[instrument])
        # sb_src[instrument] = sb_src[instrument] / scale_sb_src[instrument]
        # sb_src_err[instrument] = sb_src_err[instrument] / scale_sb_src[instrument]
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


    nonfit_args = (imsize, xsize_obj, ysize_obj, distmatrix, instruments,
                   theta, energy, APPLY_PSF, DO_ZERO_PAD, r, sb_src,
                   sb_src_err)

    # fit stop criteria
    if FIT_METHOD == 'leastsq':
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+0} # debug set; quickest
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+4} # debug set; some evol
        leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+7}
        # leastsq_kws={'xtol': 1.0e-8, 'ftol': 1.0e-8, 'maxfev': 1.0e+9}

    if FIT_METHOD == 'simplex':
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfun': 1.0e+0} # debug set; quickest
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfun': 1.0e+4} # debug set; some evol
        leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfun': 1.0e+7}
        # leastsq_kws={'xtol': 1.0e-8, 'ftol': 1.0e-8, 'maxfun': 1.0e+9}

    ######################################################################
    # do the fit: beta

    if DO_FIT:
        print "starting beta fit"
        t1 = time.clock()

        result = lm.minimize(beta_psf_2d_lmfit_profile_joint,
                             pars,
                             args=nonfit_args,
                             method=FIT_METHOD,
                             **leastsq_kws)

        t2 = time.clock()

        print
        print
        print "fitting took: ", t2-t1, " s"
        print
        print

        ######################################################################
        # scale the data back

        # for instrument in instruments:
        #     sb_src[instrument] = sb_src[instrument] * scale_sb_src[instrument]
        #     sb_src_err[instrument] = sb_src_err[instrument] * scale_sb_src[instrument]

        #     # scale also the fitted norm
        #     pars['norm_'+instrument].value = pars['norm_'+instrument].value * scale_sb_src[instrument]
        #     pars['norm_'+instrument].stderr = pars['norm_'+instrument].stderr * scale_sb_src[instrument]
        #     pars['norm_'+instrument].max = pars['norm_'+instrument].max * scale_sb_src[instrument]
        #     pars['norm_'+instrument].min = pars['norm_'+instrument].min * scale_sb_src[instrument]

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
            print_fit_diagnostics(result, t2-t1, ndata, leastsq_kws)

        # print_result_tab(pars_true, pars)
        lm.printfuncs.report_errors(result.params)

        with open(results_pickle+'.txt', 'w') as f:
            sys.stdout = f

            if PRINT_FIT_DIAGNOSTICS:
                print_fit_diagnostics(result, t2-t1, ndata, leastsq_kws)

            print
            print
            lm.printfuncs.report_errors(result.params)
            print
            print

            sys.stdout = sys.__stdout__

        print
        print "fitting subroutine done!"

    ######################################################################
    # plot beta fit and detcprofiles

    if DO_FIT and PLOT_PROFILE:
        for instrument in instruments:
            output_figure = results_pickle+'.'+instrument+'.beta_psf.png'

            print "result plot :: ", output_figure

            # FIXME: implement plotter for joint fits
            plot_data_model_resid(rplt, sb_src[instrument],
                              r_model, profile_norm_model[instrument],
                              output_figure, sb_src_err[instrument])

    ######################################################################
    # FIXME: not yet ported, confidence intervals

    if DO_FIT and CALC_1D_CI:
        print "Calculating 1D confidence intervals"
        # sigmas = [0.682689492137, 0.954499736104, 0.997300203937]
        # sigmas = [0.682689492137, 0.954499736104]
        # sigmas = [0.997300203937]
        sigmas = [0.954499736104]
        # sigmas = [0.682689492137]
        # ci_pars = ['rc', 'beta']
        # ci_pars = ['rc']
        # ci_pars = ['norm_pn', 'rc']
        ci_pars = ['norm_'+instruments[0]]

        t1 = time.clock()
        ci, trace = lm.conf_interval(result, p_names=ci_pars, sigmas=sigmas,
                                     trace=True, verbose=True, maxiter=1e3)

        t2 = time.clock()

        # save to file
        with open(results_pickle+'.ci', 'wb') as output:
            pickle.dump(ci, output, pickle.HIGHEST_PROTOCOL)

        print
        print "Confidence interval calculation took : ", t2 - t1

        lm.printfuncs.report_ci(ci)

    return 0


def fit_v06_model_joint(r, sb_src, sb_src_err, instruments, theta, energy, results_pickle=None):
    """
    Fit a v06 x psf model to any combination of instruments via joint
    likelihood

    Arguments:
    """

    # settings
    APPLY_PSF = True
    DO_ZERO_PAD = True
    DO_FIT = True
    # FIT_METHOD = 'simplex'
    FIT_METHOD = 'leastsq'     # 'leastsq' - Levemberg-Markquardt,
                              # 'simplex' - simplex
    CALC_1D_CI = False         # in most cases standard error is good
                              # enough, this is not needed then
    CALC_2D_CI = False
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

    # r contains the start of the innermost bin for integration, but not needed for plotting
    rplt = r[1:]

    ######################################################################
    # scale the data

    scale_sb_src = {}
    scale_sb_src_err = {}
    ndata = 0

    for instrument in instruments:
        ndata += len(sb_src[instrument])

    ######################################################################
    # init beta model

    n0 = 1e+0
    rc = 20.0
    beta = 4.0/3.0
    rs = 20.0
    alpha = 1.5
    gamma = 3.0
    epsilon = 1.5
    r500_pix = r.max()

    # v06 pars lmfit structure
    pars = lm.Parameters()
    pars.add('rc'      , value=rc, vary=True, min=0.05, max=r.max())
    pars.add('beta'    , value=beta, vary=True, min=0.05, max=2.0)
    pars.add('rs'      , value=rs, vary=True, min=0.05, max=2*r.max())
    pars.add('alpha'   , value=alpha, vary=True, min=0.01, max=3.0)
    pars.add('epsilon' , value=epsilon, vary=True, min=0.0, max=5.0)
    pars.add('gamma'   , value=gamma, vary=False)

    # FIXME: reasonable initial value and bounds!
    for instrument in instruments:
        pars.add('n0_'+instrument, value=n0, #value=mean(sb_src[instrument]),
                 vary=True, min=1.0e-9, max=1.0e3)

    # set the ancilarry parameters
    # +1 bc of the central divergence
    data = empty(imsize)
    distmatrix_input = distance_matrix(data, xcen_obj, ycen_obj).astype('int') + 1
    bgrid = unique(distmatrix_input.flat)

    # non-fit arguments
    nonfit_args = (distmatrix_input, bgrid, r500_pix, instruments, theta, energy,
                   xcen_obj, ycen_obj, r, sb_src, sb_src_err)

    # fit stop criteria
    if FIT_METHOD == 'leastsq':
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+0} # debug set; quickest
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+4} # debug set; some evol
        leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+7}
        # leastsq_kws={'xtol': 1.0e-8, 'ftol': 1.0e-8, 'maxfev': 1.0e+9}

    if FIT_METHOD == 'simplex':
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfun': 1.0e+1} # debug set; quickest
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfun': 1.0e+4} # debug set; some evol
        leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfun': 1.0e+7}
        # leastsq_kws={'xtol': 1.0e-8, 'ftol': 1.0e-8, 'maxfun': 1.0e+9}

    ######################################################################
    # do the fit: beta

    if DO_FIT:
        print "starting v06 fit with method :: ", FIT_METHOD
        t1 = time.clock()

        result = lm.minimize(v06_psf_2d_lmfit_profile_joint,
                             pars,
                             args=nonfit_args,
                             method=FIT_METHOD,
                             **leastsq_kws)

        t2 = time.clock()

        print
        print
        print "fitting took: ", t2-t1, " s"
        print
        print

        ######################################################################
        # get the output model

        (r_model, profile_norm_model) = \
            v06_psf_2d_lmfit_profile_joint(pars, distmatrix_input, bgrid,
                                           r500_pix, instruments, theta, energy,
                                           xcen_obj, ycen_obj)

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
            print_fit_diagnostics(result, t2-t1, ndata, leastsq_kws)

        # print_result_tab(pars_true, pars)
        lm.printfuncs.report_errors(result.params)

        with open(results_pickle+'.txt', 'w') as f:
            sys.stdout = f

            if PRINT_FIT_DIAGNOSTICS:
                print_fit_diagnostics(result, t2-t1, ndata, leastsq_kws)

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
            plot_data_model_resid(rplt, sb_src[instrument],
                              r_model, profile_norm_model[instrument],
                              output_figure, sb_src_err[instrument])

    ######################################################################
    # calculate confidence intervals

    if DO_FIT and CALC_1D_CI:
        print "Calculating 1D confidence intervals"
        sigmas = [0.682689492137, 0.954499736104, 0.997300203937]
        # sigmas = [0.682689492137, 0.954499736104]
        # sigmas = [0.997300203937]
        # sigmas = [0.954499736104]
        # sigmas = [0.682689492137]
        # ci_pars = ['rc', 'beta']
        # ci_pars = ['rc']
        # ci_pars = ['n0_pn', 'rc']
        ci_pars = ['n0_'+instruments[0]]

        t1 = time.clock()
        ci, trace = lm.conf_interval(result, p_names=ci_pars, sigmas=sigmas,
                                     trace=True, verbose=True, maxiter=1e3)

        t2 = time.clock()

        # save to file
        with open(results_pickle+'.ci', 'wb') as output:
            pickle.dump(ci, output, pickle.HIGHEST_PROTOCOL)

        print
        print "Confidence interval calculation took : ", t2 - t1

        lm.printfuncs.report_ci(ci)

    ######################################################################
    # FIXME: not done yet: Calculate 2D confidence intervals

    if DO_FIT and  CALC_2D_CI:
        output_figure = results_pickle+'.2d_like_beta_psf.png'
        from timer import Timer

        with Timer() as t:
            print "Calculating 2D confidence intervals"
            x, y, likelihood = lm.conf_interval2d(result,'rcore','beta', 10, 10)
            plt_like_surface(x, y, likelihood, output_figure, 'rcore', 'beta')

        print "elasped time:", t.secs, " s"

    return 0


def fit_v06_model(r, sb_src, sb_src_err, instrument, theta, energy, results_pickle=None):
    """
    Fit of v06 model with psf convolution
    """
    # settings
    APPLY_PSF = True
    DO_ZERO_PAD = True
    DO_FIT = True
    FIT_METHOD = 'simplex'
    # FIT_METHOD = 'leastsq'     # 'leastsq' - Levemberg-Markquardt,
                                 # 'simplex' - simplex
    CALC_1D_CI = True           # in most cases standard error is good
                                # enough, this is not needed then
    CALC_2D_CI = False
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
    # imsize = input_im.shape     # FIXME: is this necessary? I could just use it inside the model
    imsize = (size, size)         # FIXME: is this necessary? I could just use it inside the model

    xsize_obj = xsize # 100             # if running t1.fits set to 100 else xsize
    ysize_obj = xsize_obj
    xcen_obj = xsize_obj / 2
    ycen_obj = ysize_obj / 2
    r_aper = xsize_obj  / 2        # aperture for the fitting

    ######################################################################
    # init model

    n0 = 1.0
    rc = 20.0
    beta = 4.0/3.0
    rs = 20.0
    alpha = 1.5
    gamma = 3.0
    epsilon = 1.5

    # rmax = 2*r500_pix
    r500_pix = r.max()
    ndata = len(sb_src)

    # v06 pars lmfit structure
    pars = lm.Parameters()
    pars.add('n0_'+instrument, value=n0, vary=True, min=1.0e-9, max=1.0e3)
    pars.add('rc'      , value=rc, vary=True, min=0.05, max=r.max())
    pars.add('beta'    , value=beta, vary=True, min=0.05, max=2.0)
    pars.add('rs'      , value=rs, vary=True, min=0.05, max=2*r.max())
    pars.add('alpha'   , value=alpha, vary=True, min=0.01, max=3.0)
    pars.add('epsilon' , value=epsilon, vary=True, min=0.0, max=5.0)
    pars.add('gamma'   , value=gamma, vary=False)

    # set the ancilarry parameters
    # +1 bc of the central divergence
    data = empty(imsize)
    distmatrix_input = distance_matrix(data, xcen_obj, ycen_obj).astype('int') + 1
    bgrid = unique(distmatrix_input.flat)

    ######################################################################
    # do the fit: v06

    nonfit_args = (distmatrix_input, bgrid, r500_pix, instrument, theta, energy,
                   xcen_obj, ycen_obj, r, sb_src, sb_src_err)

    # fit stop criteria
    if FIT_METHOD == 'leastsq':
        leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+0} # debug set; quickest
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+4} # debug set; some evol
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+7}
        # leastsq_kws={'xtol': 1.0e-8, 'ftol': 1.0e-8, 'maxfev': 1.0e+9}

    if FIT_METHOD == 'simplex':
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfun': 1.0e+0} # debug set; quickest
        # leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfun': 1.0e+4} # debug set; some evol
        leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfun': 1.0e+7}
        # leastsq_kws={'xtol': 1.0e-8, 'ftol': 1.0e-8, 'maxfun': 1.0e+9}

    ######################################################################
    # do the actual fitting

    if DO_FIT:
        print "starting v06 fit with method :: ", FIT_METHOD
        t1 = time.clock()

        result = lm.minimize(v06_psf_2d_lmfit_profile,
                             pars,
                             args=nonfit_args,
                             method=FIT_METHOD,
                             **leastsq_kws)

        t2 = time.clock()
        print "fitting took: ", t2-t1, " s"

        # get the output model
        (r_model, profile_norm_model) = v06_psf_2d_lmfit_profile(pars,
                                                                 distmatrix_input,
                                                                 bgrid,
                                                                 r500_pix,
                                                                 instrument, theta, energy,
                                                                 xcen_obj,
                                                                 ycen_obj)

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
            print_fit_diagnostics(result, t2-t1, ndata, leastsq_kws)

        # print_result_tab(pars_true, pars)
        lm.printfuncs.report_errors(result.params)

        with open(results_pickle+'.txt', 'w') as f:
            sys.stdout = f

            if PRINT_FIT_DIAGNOSTICS:
                print_fit_diagnostics(result, t2-t1, ndata, leastsq_kws)

            print
            print
            lm.printfuncs.report_errors(result.params)
            print
            print

            sys.stdout = sys.__stdout__

        print
        print "fitting subroutine done!"

    ######################################################################
    # plot v06 fit and data profiles

    if DO_FIT and PLOT_PROFILE:
        output_figure = results_pickle+'.'+instrument+'.v06_psf.png'

        print "result plot :: ", output_figure

        # FIXME: implement plotter for joint fits
        plot_data_model_resid(r, sb_src,
                              r_model, profile_norm_model,
                              output_figure, sb_src_err)

    ######################################################################
    # FIXME: not yet ported, confidence intervals

    if DO_FIT and CALC_1D_CI:
        print "Calculating 1D confidence intervals"
        # sigmas = [0.682689492137, 0.954499736104, 0.997300203937]
        sigmas = [0.682689492137, 0.954499736104]
        # just an example
        ci_pars = ['rc', 'beta']

        ci, trace = lm.conf_interval(result, p_names=ci_pars, sigmas=sigmas,
                              trace=True, verbose=True, maxiter=1e3)

        lm.printfuncs.report_ci(ci)

    # FIXME: this seems to fail for beta and rc (i think problem is
    # due to parameter degeneracy no code issue)
    if DO_FIT and  CALC_2D_CI:
        output_figure = results_pickle+'.2d_like_v06_psf.png'
        from timer import Timer

        with Timer() as t:
            print "Calculating 2D confidence intervals"
            x, y, likelihood = lm.conf_interval2d(result,'rc','beta', 10, 10)
            plt_like_surface(x, y, likelihood, output_figure, 'rc', 'beta')

        print "elasped time:", t.secs, " s"


    # import IPython
    # IPython.embed()

    return 0




