import sys
import os
import math
import pyfits
from numpy import *
from pylab import rc
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, LogLocator, MaxNLocator
from sb_utils import *

def plot_cts_profile(r, c1, c2, fname):
    """
    Generic lin-lin plot for 2 curves no error bars
    plot a cts curve, overplot background

    Arguments:
    - `r`: radius
    - `c1`: curve 1 (source)
    - `c2`: curve 2 (background)
    - 'fname' : figure name
    """

    ######################################################################
    # start plot enviroment
    ######################################################################
    # start figure
    rc('axes', linewidth=1.5)
    fig_obj = plt.figure()
    fig_name=fname
    headline_text = fig_obj.text(0.5, 0.95, '',
                                 horizontalalignment='center',
                                 fontproperties=matplotlib.font_manager.FontProperties(size=16))

    ax1 = fig_obj.add_subplot(111)                         # rows/cols/num of plot
    plt.subplots_adjust(hspace=0.2, wspace=0.2)      # hdefault 0.2, 0.001 for touching

    ######################################################################
    # plot data sets

    plt.plot(r, c1,
        color='black',
        linestyle='-',              # -/--/-./:
        linewidth=1,                # linewidth=1
        marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='black',
        markersize=0,               # markersize=6
        label=r"source"               # '__nolegend__'
        )

    plt.plot(r, c2,
        color='blue',
        linestyle=':',              # -/--/-./:
        linewidth=1,                # linewidth=1
        marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='blue',
        markersize=0,               # markersize=6
        label=r"background"               # '__nolegend__'
        )

    ######################################################################
    # subplot data sets
    ax1.set_xscale('linear')                     # ['linear' | 'log' | 'symlog']
    ax1.set_yscale('linear')                     # ['linear' | 'log' | 'symlog']
    # ax1.set_xlim(xmin=20.0,xmax=50.0)
    ax1.set_ylim(ymin=0.0)

    # subplot text sets
    # ax1.set_title('plot title', fontsize=16, fontweight="bold")  # fontsize=16
    ax1.set_xlabel('r [arcsec]', fontsize=14, fontweight="bold")          # fontsize=12
    ax1.set_ylabel('CTS', fontsize=14, fontweight="heavy")          # fontsize=12

    # legend
    prop = matplotlib.font_manager.FontProperties(size=16)  # size=16
    ax1.legend(loc=0, prop=prop, numpoints=1)

    # x - axis tick labels
    for label in ax1.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)                   # default = 0
        label.set_fontsize(14)                  # default = 12
        label.set_fontweight("normal")          # [ 'normal' | 'normal' | 'heavy' | 'light' | 'ultranormal' | 'ultralight']

    # y - axis tick labels
    for label in ax1.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)                   # default = 0
        label.set_fontsize(14)                  # default = 12
        label.set_fontweight("normal")          # [ 'normal' | 'normal' | 'heavy' | 'light' | 'ultranormal' | 'ultralight']

    # save figure
    plt.savefig(fig_name)

    ######################################################################
    # stop plot enviroment
    ######################################################################


def plot_sb_profile(r, c1, c1_err, c2, c2_err, fname):
    """
    Surface brightness log-log plot for 2 curves with error bars

    Arguments:
    - `r`: radius
    - `c1 + c1_err`: curve 1 (source)
    - `c2 + c2_err`: curve 2 (background)
    - 'fname' : figure name
    """

    ######################################################################
    # start plot enviroment
    ######################################################################
    # start figure
    rc('axes', linewidth=1.5)
    fig_obj = plt.figure()
    fig_name=fname
    headline_text = fig_obj.text(0.5, 0.95, '',
                                 horizontalalignment='center',
                                 fontproperties=matplotlib.font_manager.FontProperties(size=16))

    ax1 = fig_obj.add_subplot(111)                         # rows/cols/num of plot
    plt.subplots_adjust(hspace=0.2, wspace=0.2)      # hdefault 0.2, 0.001 for touching

    c1min = min(c1[where(c1>0.0)])
    c2min = min(c2[where(c2>0.0)])
    ymin  = min(c1min, c2min)/2.0

    ######################################################################
    # plot data sets

    # plt.errorbar(r, c1, [(c1-c1_err<=0.0).choose(c1_err, c1-ymin), c1_err],
    plt.errorbar(r, c1, c1_err,
        color='black',
        linestyle='',              # -/--/-./:
        linewidth=1,                # linewidth=1
        marker='.',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='black',
        markersize=6,               # markersize=6
        label=r"source"               # '__nolegend__'
        )

    # plt.errorbar(r, c2, [(c2-c2_err<=0.0).choose(c2_err, c2-ymin), c2_err],
    plt.errorbar(r, c2, c2_err,
        color='blue',
        linestyle='',              # -/--/-./:
        linewidth=1,                # linewidth=1
        marker='.',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='blue',
        markersize=6,               # markersize=6
        label=r"background"               # '__nolegend__'
        )

    ######################################################################
    # subplot data sets
    ax1.set_xscale('log', nonposx='clip')                     # ['linear' | 'log' | 'symlog']
    ax1.set_yscale('log', nonposy='clip')                     # ['linear' | 'log' | 'symlog']
    # ax1.set_xlim(xmin=20.0,xmax=50.0)
    ax1.set_ylim(ymin=ymin)

    # subplot text sets
    # ax1.set_title('plot title', fontsize=16, fontweight="bold")  # fontsize=16
    ax1.set_xlabel('r [arcsec]', fontsize=14, fontweight="normal")          # fontsize=12
    ax1.set_ylabel('surface brightness [cts/s/pix]', fontsize=14, fontweight="normal")          # fontsize=12

    # legend
    prop = matplotlib.font_manager.FontProperties(size=16)  # size=16
    ax1.legend(loc=0, prop=prop, numpoints=1)

    # x - axis tick labels
    for label in ax1.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)                   # default = 0
        label.set_fontsize(14)                  # default = 12
        label.set_fontweight("normal")          # [ 'normal' | 'normal' | 'heavy' | 'light' | 'ultranormal' | 'ultralight']

    # y - axis tick labels
    for label in ax1.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)                   # default = 0
        label.set_fontsize(14)                  # default = 12
        label.set_fontweight("normal")          # [ 'normal' | 'normal' | 'heavy' | 'light' | 'ultranormal' | 'ultralight']

    plt.get_current_fig_manager().window.wm_geometry("+1100+0")
    # save figure
    plt.savefig(fig_name)

    ######################################################################
    # stop plot enviroment
    ######################################################################

def plot_sb_fit(r, c1, c1_err, beta_pars, fname):
    """
    Surface brightness log-log plot with overplotted betamodel

    Arguments:
    - `r`: radius
    - `c1 + c1_err`: curve 1 (source)
    - 'beta_pars: list of beta mode parameters = [norm, rcore, beta]'
    - 'fname' : figure name
    """

    from sb_utils import beta_model

    ######################################################################
    # start plot enviroment
    ######################################################################
    # start figure
    rc('axes', linewidth=1.5)
    fig_obj = plt.figure()
    fig_name=fname
    headline_text = fig_obj.text(0.5, 0.95, '',
                                 horizontalalignment='center',
                                 fontproperties=matplotlib.font_manager.FontProperties(size=16))

    ax1 = fig_obj.add_subplot(111)                         # rows/cols/num of plot
    plt.subplots_adjust(hspace=0.2, wspace=0.2)      # hdefault 0.2, 0.001 for touching

    ymin = min(c1[where(c1>0.0)])/2.0

    ######################################################################
    # plot data sets

    plt.errorbar(r, c1, [(c1-c1_err<=0.0).choose(c1_err, c1-ymin), c1_err],
        color='black',
        linestyle='',              # -/--/-./:
        linewidth=1,                # linewidth=1
        marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='black',
        markersize=6,               # markersize=6
        label=r"data"               # '__nolegend__'
        )

    beta_mod = beta_model(beta_pars, r)

    plt.plot(r, beta_mod,
        color='black',
        linestyle='-',              # -/--/-./:
            linewidth=1,                # linewidth=1
        marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='black',
        markersize=0,               # markersize=6
        label=r"model"               # '__nolegend__'
        )

    ######################################################################
    # subplot data sets
    ax1.set_xscale('log')                     # ['linear' | 'log' | 'symlog']
    ax1.set_yscale('log')                     # ['linear' | 'log' | 'symlog']
    # ax1.set_xlim(xmin=20.0,xmax=50.0)
    ax1.set_ylim(ymin=ymin)

    # subplot text sets
    # ax1.set_title('plot title', fontsize=16, fontweight="bold")  # fontsize=16
    ax1.set_xlabel('r [arcsec]', fontsize=14, fontweight="bold")          # fontsize=12
    ax1.set_ylabel('surface brightness [cts/s/pix]', fontsize=14, fontweight="heavy")          # fontsize=12

    # legend
    prop = matplotlib.font_manager.FontProperties(size=16)  # size=16
    ax1.legend(loc=0, prop=prop, numpoints=1)

    # x - axis tick labels
    for label in ax1.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)                   # default = 0
        label.set_fontsize(14)                  # default = 12
        label.set_fontweight("normal")          # [ 'normal' | 'normal' | 'heavy' | 'light' | 'ultranormal' | 'ultralight']

    # y - axis tick labels
    for label in ax1.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)                   # default = 0
        label.set_fontsize(14)                  # default = 12
        label.set_fontweight("normal")          # [ 'normal' | 'normal' | 'heavy' | 'light' | 'ultranormal' | 'ultralight']

    # save figure
    plt.savefig(fig_name)

    ######################################################################
    # stop plot enviroment
    ######################################################################


def plot_minuit_err_ellipse(c1, c2, c3, fname):
    """
    Plots beta - rcore 1, 2 , 3 sigma error cipses.

    Arguments:
    - `c1`: 1 sigma cipse as an array converted from minuit output
    - `c2`: 2 sigma cipse as an array converted from minuit output
    - `c3`: 3 sigma cipse as an array converted from minuit output
    """


    ######################################################################
    # start plot enviroment
    ######################################################################
    # start figure
    rc('axes', linewidth=1.5)
    fig_obj = plt.figure()
    fig_name = fname
    headline_text = fig_obj.text(0.5, 0.95, '',
               horizontalalignment='center',
               fontproperties=matplotlib.font_manager.FontProperties(size=16))

    ax1 = fig_obj.add_subplot(111)                         # rows/cols/num of plot
    plt.subplots_adjust(hspace=0.2, wspace=0.2)      # hdefault 0.2, 0.001 for touching

    ######################################################################
    # plot data sets

    plt.plot(c1[:,0], c1[:,1],
        color='red',
        linestyle='-',              # -/--/-./:
            linewidth=1,                # linewidth=1
        marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='red',
        markersize=0,               # markersize=0
        label=r"__nolegend__"               # '__nolegend__'
        )

    # close the ellipse
    plt.plot([c1[0,0], c1[-1,0]], [c1[0,1], c1[-1,1]],
        color='red',
        linestyle='-',              # -/--/-./:
            linewidth=1,                # linewidth=1
        marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='red',
        markersize=0,               # markersize=0
        label=r"__nolegend__"               # '__nolegend__'
        )

    plt.plot(c2[:,0], c2[:,1],
        color='orange',
        linestyle='-',              # -/--/-./:
            linewidth=1,                # linewidth=1
        marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='orange',
        markersize=0,               # markersize=0
        label=r"__nolegend__"               # '__nolegend__'
        )
    # close the ellipse
    plt.plot([c2[0,0], c2[-1,0]], [c2[0,1], c2[-1,1]],
        color='orange',
        linestyle='-',              # -/--/-./:
            linewidth=1,                # linewidth=1
        marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='orange',
        markersize=0,               # markersize=0
        label=r"__nolegend__"               # '__nolegend__'
        )

    # plt.plot(c3[:,0], c3[:,1],
    #     color='green',
    #     linestyle='',              # -/--/-./:
    #         linewidth=1,                # linewidth=1
    #     marker='.',                  # ./o/*/+/x/^/</>/v/s/p/h/H
    #     markerfacecolor='green',
    #     markersize=6,               # markersize=0
    #     label=r"__nolegend__"               # '__nolegend__'
    #     )
    # # close the ellipse
    # plt.plot([c3[0,0], c3[-1,0]], [c3[0,1], c3[-1,1]],
    #     color='green',
    #     linestyle='-',              # -/--/-./:
    #         linewidth=1,                # linewidth=1
    #     marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
    #     markerfacecolor='green',
    #     markersize=0,               # markersize=0
    #     label=r"__nolegend__"               # '__nolegend__'
    #     )

    plt.contour(c3[:,0], c3[:,1],  c3[:,1]/c3[:,1],
                 colors='k', # negative contours will be dashed by default
                 )

    ######################################################################
    # subplot data sets
    ax1.set_xscale('linear')                     # ['linear' | 'log' | 'symlog']
    ax1.set_yscale('linear')                     # ['linear' | 'log' | 'symlog']
    # ax1.set_xlim(xmin=20.0,xmax=50.0)
    # ax1.set_ylim(ymin=20.0,ymax=50.0)

    # subplot text sets
    # ax1.set_title('plot title', fontsize=16, fontweight="bold")  # fontsize=16
    ax1.set_xlabel(r'$\beta$', fontsize=14, fontweight="normal")          # fontsize=12
    # ax1.set_ylabel('r$_{\mathrm{core}}$', fontsize=14, fontweight="bold")          # fontsize=12
    ax1.set_ylabel('r', fontsize=14, fontweight="bold")          # fontsize=12

    # legend
    prop = matplotlib.font_manager.FontProperties(size=16)  # size=16
    ax1.legend(loc=0, prop=prop, numpoints=1)

    # adding minor ticks
    # xminorLocator = plt.MultipleLocator(0.01)           # minor ticks location in absolute units
    # yminorLocator = plt.MultipleLocator(0.5)            # minor ticks location in absolute units
    # xminorLocator = plt.MaxNLocator(20)                 # set minor ticks number - can look weird
    # yminorLocator = plt.MaxNLocator(10)                 # set minor ticks number - can look weird

    # ax1.xaxis.set_minor_locator(xminorLocator)
    # ax1.yaxis.set_minor_locator(yminorLocator)

    # x - axis tick labels
    for label in ax1.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)                   # default = 0
        label.set_fontsize(14)                  # default = 12
        label.set_fontweight("bold")            # [ 'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight']

    # y - axis tick labels
    for label in ax1.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)                   # default = 0
        label.set_fontsize(14)                  # default = 12
        label.set_fontweight("bold")            # [ 'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight']

    # save figure
    plt.savefig(fig_name)

    ######################################################################
    # stop plot enviroment
    ######################################################################


def plot_king_model_psf(energy, theta, instrument):
    """
    Makes a plot of the psf model

    Arguments:
    - `energy`: energy [keV]
    - `theta`: off-axis angle [arcmin]
    - `instrument`: "m1", "m2", "pn", [set]
    """

    numpoints = 1e3
    rmin = 1.0e-1
    rmax = 1.0e3                # [arcsec]

    r = linspace(rmin, rmax, numpoints)

    ######################################################################
    # start plot enviroment
    ######################################################################
    # start figure
    rc('axes', linewidth=1.5)
    fig_obj = plt.figure()
    fig_name='xmm-psf.png'
    headline_text = fig_obj.text(0.5, 0.95, '',
               horizontalalignment='center',
               fontproperties=matplotlib.font_manager.FontProperties(size=16))

    ax1 = fig_obj.add_subplot(111)                         # rows/cols/num of plot
    plt.subplots_adjust(hspace=0.2, wspace=0.2)      # hdefault 0.2, 0.001 for touching

    ######################################################################
    # plot lines

    if ("m1" in instrument):
        instr = "m1"
        (rcore, alpha) = get_psf_king_pars(instr, energy, theta)
        psf = king_profile(r, rcore, alpha)
        print "plotting m1"
        plt.plot(r, psf,
            color='red',
            linestyle='-',              # -/--/-./:
                linewidth=3,                # linewidth=1
            marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
            markerfacecolor='red',
            markersize=0,               # markersize=6
            label=instr               # '__nolegend__'
            )

    if ("m2" in instrument):
        instr = "m2"
        print "plotting m2"
        (rcore, alpha) = get_psf_king_pars(instr, energy, theta)
        psf = king_profile(r, rcore, alpha)
        plt.plot(r, psf,
                 color='orange',
                 linestyle='-',              # -/--/-./:
                 linewidth=3,                # linewidth=1
                 marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
                 markerfacecolor='orange',
                 markersize=0,               # markersize=6
                 label=instr               # '__nolegend__'
                 )

    if ("pn" in instrument):
        instr = "pn"
        print "plotting pn"
        (rcore, alpha) = get_psf_king_pars(instr, energy, theta)
        psf = king_profile(r, rcore, alpha)
        plt.plot(r, psf,
                 color='blue',
                 linestyle='-',              # -/--/-./:
                 linewidth=3,                # linewidth=1
                 marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
                 markerfacecolor='blue',
                 markersize=0,               # markersize=6
                 label=instr               # '__nolegend__'
                 )

    ######################################################################
    # subplot data sets
    ax1.set_xscale('log')                     # ['linear' | 'log' | 'symlog']
    ax1.set_yscale('log')                     # ['linear' | 'log' | 'symlog']
    # ax1.set_xlim(xmin=20.0,xmax=50.0)
    ax1.set_ylim(ymax=2.0)

    title = "XMM-Newton King model PSF, E="+str(energy)+r" keV, $\theta=$"+str(theta)+"'"
    # subplot text sets
    ax1.set_title(title, fontsize=16, fontweight="normal")  # fontsize=16
    ax1.set_xlabel('r [arcsec]', fontsize=14, fontweight="normal")          # fontsize=12
    ax1.set_ylabel('dN/dA', fontsize=14, fontweight="normal")          # fontsize=12

    # legend
    prop = matplotlib.font_manager.FontProperties(size=16)  # size=16
    ax1.legend(loc=0, prop=prop, numpoints=1)

    # x - axis tick labels
    for label in ax1.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)                   # default = 0
        label.set_fontsize(14)                  # default = 12
        label.set_fontweight("normal")            # [ 'normal' | 'normal' | 'heavy' | 'light' | 'ultranormal' | 'ultralight']

    # y - axis tick labels
    for label in ax1.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)                   # default = 0
        label.set_fontsize(14)                  # default = 12
        label.set_fontweight("normal")          # [ 'normal' | 'normal' | 'heavy' | 'light' | 'ultranormal' | 'ultralight']

    # save figure
    plt.savefig(fig_name)


def plot_data_model_simple(r_data, profile_data,
                           r_model=None, profile_model=None,
                           output_figure=None, profile_data_err=None,
                           r_true=None, profile_true=None):
    """
    Simple plot of a profile: data vs model (optionally also error bars)

    Arguments:
    - `r_data`: radial grid for data
    - `profile_data`: profile data
    - `r_model`: radial grid for model
    - `profile_norm_model`: profile model
    - `ouputname`:
    """
    ax1 = plt.figure()
    plt.ion()
    plt.clf()

    if any(profile_data_err):
        plt.errorbar(r_data-0.5, profile_data, profile_data_err,
        color='black',
        linestyle='',              # -/--/-./:
        linewidth=1,                # linewidth=1
        marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='black',
        markersize=6,               # markersize=6
        label=r"source"               # '__nolegend__'
        )
    else:
        plt.plot(r_data-0.5, profile_data,
        color='black',
        linestyle='-',              # -/--/:/-.
        linewidth=1,                # linewidth=1
        marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='black',
        markersize=4,               # markersize=6
        label=r"source"               # '__nolegend__'
        )

    if any(profile_model):
        plt.plot(r_model-0.5, profile_model,
            color='red',
            linestyle='-',              # -/--/:/-.
            linewidth=1,                # linewidth=1
            marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
            markerfacecolor='black',
            markersize=0,               # markersize=6
            label=r"model fit"          # '__nolegend__'
            )

    if any(profile_true):
        plt.plot(r_true-0.5, profile_true,
            color='green',
            linestyle='-',              # -/--/:/-.
            linewidth=1,                # linewidth=1
            marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
            markerfacecolor='black',
            markersize=0,               # markersize=6
            label=r"true model"          # '__nolegend__'
            )

    from pylab import xlabel, ylabel
    xlabel('radius', fontsize=14, fontweight="normal")          # fontsize=12
    ylabel('profile', fontsize=14, fontweight="normal")          # fontsize=12

    # plt.xscale("linear")
    # plt.yscale("linear")

    plt.xscale("log", nonposx='clip')
    plt.yscale("log", nonposy='clip')


    # plt.ylim(ymin=1e-2,ymax=1e4)

    prop = matplotlib.font_manager.FontProperties(size=16)  # size=16
    plt.legend(loc=0, prop=prop, numpoints=1)

    plt.draw()
    plt.get_current_fig_manager().window.wm_geometry("+1100+0")
    plt.show()

    if output_figure:
        plt.savefig(output_figure)


def plot_data_model_resid(r_data, profile_data,
                           r_model=None, profile_model=None,
                           output_figure=None, profile_data_err=None,
                           r_true=None, profile_true=None):
    """
    Simple plot of a profile: data vs model (optionally also error bars)
    just as def plot_data_model_simple but also include residual sublot

    Arguments:
    - `r_data`: radial grid for data
    - `profile_data`: profile data
    - `r_model`: radial grid for model
    - `profile_norm_model`: profile model
    - `ouputname`:
    """
    f = plt.figure()
    plt.subplots_adjust(hspace=0.001)
    plt.ion()
    plt.clf()

    ax1 = plt.subplot(211)
    if any(profile_data_err):
        ax1.errorbar(r_data, profile_data, profile_data_err,
        color='black',
        linestyle='',              # -/--/-./:
        linewidth=1,                # linewidth=1
        marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='black',
        markersize=6,               # markersize=6
        label=r"source"               # '__nolegend__'
        )
    else:
        ax1.plot(r_data, profile_data,
        color='black',
        linestyle='-',              # -/--/:/-.
        linewidth=1,                # linewidth=1
        marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='black',
        markersize=4,               # markersize=6
        label=r"source"               # '__nolegend__'
        )

    if any(profile_model):
        ax1.plot(r_model, profile_model,
            color='red',
            linestyle='-',              # -/--/:/-.
            linewidth=1,                # linewidth=1
            marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
            markerfacecolor='black',
            markersize=0,               # markersize=6
            label=r"model fit"          # '__nolegend__'
            )

    if any(profile_true):
        ax1.plot(r_true, profile_true,
            color='green',
            linestyle='-',              # -/--/:/-.
            linewidth=1,                # linewidth=1
            marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
            markerfacecolor='black',
            markersize=0,               # markersize=6
            label=r"true model"          # '__nolegend__'
            )

    ######################################################################
    # residuals

    PLOT_RESIDUAL = True

    if PLOT_RESIDUAL:

        ax2 = plt.subplot(212)

        # FIXME:
        # res = (profile_data[:-1] - profile_model[1:]) / profile_model[1:]
        # res_err = (profile_data_err[:-1] - profile_model[1:]) / profile_model[1:]
        # ax2.errorbar(r_data[:-1]-1.5, res, res_err,

        res = (profile_data - profile_model) / profile_model
        # res_err = (profile_data_err - profile_model) / profile_model
        res_err = profile_data_err / profile_model

        ax2.errorbar(r_data, res, res_err,
            color='black',
            linestyle='',              # -/--/-./:
            linewidth=1,                # linewidth=1
            marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
            markerfacecolor='black',
            markersize=6,               # markersize=6
            label=r"__nolegend__"               # '__nolegend__'
            )

        ax2.axhline(0.0, color='red')

        # take care of labels and ticks
        ax1.set_xscale("log", nonposx='clip')
        ax1.set_yscale("log", nonposy='clip')
        ax1.set_ylabel('Profile [cts s$^{-1}$ pix$^{-1}$]', fontsize=14, fontweight="normal")          # fontsize=12
        xticklabels = ax1.get_xticklabels()
        plt.setp(xticklabels, visible=False)

        # ax1.yaxis.set_major_locator(MaxNLocator(prune='lower'))  # doesn'the work

        ax2.set_xscale("log", nonposx='clip')
        # ax2.set_yscale("log", nonposy='clip')
        ax2.set_xlabel('Radius', fontsize=14, fontweight="normal")          # fontsize=12
        ax2.set_ylabel('(data-model)/model', fontsize=12, fontweight="normal")          # fontsize=12

        width=std(res)
        ax2.set_ylim(-3*width, 3*width)

        # prop = matplotlib.font_manager.FontProperties(size=16)  # size=16
        # set_legend(loc=0, prop=prop, numpoints=1)

    # plt.draw()
    plt.get_current_fig_manager().window.wm_geometry("+1100+0")
    plt.show()

    if output_figure:
        plt.savefig(output_figure)



if __name__ == '__main__':
    print "This is a library! Use import sb_plotting_utils in your script to call the subrutines"






