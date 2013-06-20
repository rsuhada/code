#!/usr/bin/env python2.6
import lmfit as lm
from numpy import *
import time
from sb_fitting_utils import print_fit_diagnostics
import matplotlib.pylab as plt


def do_fit():
    """
    Run the fitter region
    """

    print "starting fit with method :: ", FIT_METHOD
    t1 = time.clock()

    result = lm.minimize(residual,
                         pars,
                         method=FIT_METHOD,
                         **leastsq_kws)

    t2 = time.clock()

    #  outputs
    # print "fitting took: ", t2-t1, " s"
    # print

    lm.printfuncs.report_errors(result.params)
    print_fit_diagnostics(result, t2-t1, len(y), leastsq_kws)

    return result

# FIXME: not working at the moment
# plot contours
def plot_conf(result):
    x, y, grid=lm.conf_interval2d(result,'a','b',30,30)
    plt.contourf(x,y,grid,np.linspace(0,1,11))
    plt.xlabel('a');
    plt.colorbar();
    plt.ylabel('b');



# model
def funct(a, b):
    return 1/(a*x) + b

# create data
a_true = 0.1
b_true = 2.0
x=linspace(0.3,10,100)
y=funct(a_true, b_true) + 0.1*random.randn(x.size)

#  use stock data for repeatability
a_true = 0.1
b_true = 2.0
y = array(( 35.31974891,  27.2502685,   22.14511225,  18.72513472,  16.38344418 ,
  14.6186514   , 13.29029116  ,  11.97833455  ,  11.23311135 ,  10.48015721  ,
   9.7801057   ,  9.30701759  ,   9.05237106  ,   8.23312357 ,   8.02829518  ,
   7.6847496   ,  7.36974537  ,   7.08993438  ,   6.75707617 ,   6.56856683  ,
   6.48669963  ,  6.23568942  ,   6.03088916  ,   5.72145744 ,   5.89779252  ,
   5.7115539   ,  5.35471713  ,   5.49938213  ,   5.35135295 ,   5.20705134  ,
   5.10471319  ,  4.88997229  ,   4.8337169   ,   4.58619614 ,   4.75046407  ,
   4.91269666  ,  4.50934007  ,   4.52298432  ,   4.38245226 ,   4.46151934  ,
   4.41267316  ,  4.39704596  ,   4.21335614  ,   4.40512179 ,   4.10374354  ,
   4.29663358  ,  4.06263362  ,   3.97267681  ,   3.96472531 ,   3.96596165  ,
   3.94348777  ,  3.85519797  ,   3.91071778  ,   3.93010838 ,   3.7532274   ,
   3.71082321  ,  3.77967646  ,   3.66220168  ,   3.72396648 ,   3.67528294  ,
   3.5375727   ,  3.642105    ,   3.30227959  ,   3.54779342 ,   3.56336371  ,
   3.44142536  ,  3.61007951  ,   3.42485707  ,   3.58399346 ,   3.34521551  ,
   3.52451734  ,  3.27799557  ,   3.3963908   ,   3.47793105 ,   3.42875748  ,
   3.46917475  ,  3.37105327  ,   3.06481685  ,   3.13251597 ,   3.10162521  ,
   3.24343277  ,  3.21489026  ,   3.18315609  ,   3.39679822 ,   3.14424304  ,
   3.05763955  ,  3.24517363  ,   3.19023368  ,   3.24204155 ,   3.10077281  ,
   3.1740611   ,  3.22062324  ,   3.08989742  ,   3.00693678 ,   3.04278766  ,
   3.01443441  ,  3.03154234  ,   3.13141617  ,   3.11017908 ,   2.94036625      ))

##################################################################
# results for this data set with leastsq at leastsq_kws={'xtol': #
# 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+7}:                     #
#                                                                #
# fitting took:  0.001944  s                                     #
#                                                                #
# a_true 0.1                                                     #
# b_true 2.0                                                     #
#   a:     0.100109 +/- 0.000200 (0.20%) initial =  2.000000     #
#   b:     2.009682 +/- 0.012503 (0.62%) initial =  3.000000     #
# Correlations:                                                  #
#    C(a, b)                      =  0.601 #                     #
##################################################################


# residuals for titing
def residual(pars):
    a=pars['a'].value
    b=pars['b'].value
    return funct(a, b) - y

# create parameter container
pars=lm.Parameters()
pars.add_many(('a', 2.0),('b', 3.0))

print
print 'a_true = ', a_true
print 'b_true = ', b_true
print

######################################################################
# do the fitting: leastsq

print
print
print '='*70
print '='*70

# create parameter container
pars=lm.Parameters()
pars.add_many(('a', 2.0),('b', 3.0))

FIT_METHOD='leastsq'
leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfev': 1.0e+7}
result = do_fit()

# confidence interval
# sigmas = [0.682689492137]
sigmas = [0.682689492137, 0.954499736104, 0.997300203937]
ci_pars = ['a', 'b']
ci, trace = lm.conf_interval(result, p_names=ci_pars, sigmas=sigmas,
                      trace=True, verbose=True, maxiter=1e3)
lm.printfuncs.report_ci(ci)

print

######################################################################
# do the fitting: simplex

print
print
print '='*70
print '='*70

# create parameter container
pars_simplex=lm.Parameters()
pars_simplex.add_many(('a', 2.0),('b', 3.0))

FIT_METHOD='simplex'
leastsq_kws={'xtol': 1.0e-7, 'ftol': 1.0e-7, 'maxfun': 1.0e+7} # debug set; quickest
result_simplex = do_fit()

# confidence interval
# sigmas = [0.682689492137]
sigmas = [0.682689492137, 0.954499736104, 0.997300203937]
ci_pars = ['a', 'b']
ci, trace = lm.conf_interval(result_simplex, p_names=ci_pars, sigmas=sigmas,
                      trace=True, verbose=True, maxiter=1e3)
lm.printfuncs.report_ci(ci)

# plot_conf(result_simplex)
# plot_conf(result)



import IPython
IPython.embed()



###########################################################################
# TEST RESULTS                                                            #
# for fixed data set                                                      #
#                                                                         #
# a_true =  0.1                                                           #
# b_true =  2.0                                                           #
#                                                                         #
# ======================================================================  #
# starting fit with method ::  leastsq                                    #
#   a:     0.100109 +/- 0.000200 (0.20%) initial =  2.000000              #
#   b:     2.009682 +/- 0.012503 (0.62%) initial =  3.000000              #
# Correlations:                                                           #
#     C(a, b)                      =  0.601                               #
# Calculating CI for a                                                    #
# Calculating CI for b                                                    #
#      99.73%    95.45%    68.27%     0.00%    68.27%    95.45%    99.73% #
# a   0.09931   0.09931   0.09931   0.10011   0.10091   0.10091   0.10091 #
# b   1.97154   1.98450   1.99739   2.00968   2.02198   2.03486   2.04783 #
#                                                                         #
# ======================================================================  #
# starting fit with method ::  simplex                                    #
#   a:     0.100109 initial =  2.000000                                   #
#   b:     2.009682 initial =  3.000000                                   #
# Correlations:                                                           #
# Calculating CI for a                                                    #
# Calculating CI for b                                                    #
#      99.73%    95.45%    68.27%     0.00%    68.27%    95.45%    99.73% #
# a   0.09887   0.09898   0.09840   0.10011   0.10182   0.10123   0.10134 #
# b   1.97086   1.98480   1.99738   2.00968   2.02199   2.03456   2.04851 #
###########################################################################





