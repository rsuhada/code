#!/usr/bin/env python
import sys
import os
import math
import pyfits
from numpy import *
from pylab import rc
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, LogLocator

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

    plt.errorbar(r, c1, [(c1-c1_err<=0.0).choose(c1_err, c1-ymin), c1_err],
        color='black',
        linestyle='',              # -/--/-./:
        linewidth=1,                # linewidth=1
        marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='black',
        markersize=6,               # markersize=6
        label=r"source"               # '__nolegend__'
        )

    plt.errorbar(r, c2, [(c2-c2_err<=0.0).choose(c2_err, c2-ymin), c2_err],
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




if __name__ == '__main__':
    print "This is a library! Use import sb_plotting_utils in your script to call the subrutines"

