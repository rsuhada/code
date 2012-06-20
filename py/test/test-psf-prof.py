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
from sb_plotting_utils import *
from sb_utils import *

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

    ######################################################################
    # stop plot enviroment
    ######################################################################

if __name__ == '__main__':
    print

    energy = 1.5
    theta = 0.3

    instrument=("pn", "m1", "m2")
    # instrument=("m1",)

    plot_king_model_psf(energy, theta, instrument)

    for i in instrument:
        print i
        (rcore, alpha) = get_psf_king_pars(i, energy, theta)
        print rcore, alpha

    print "done"
    # plt.show()
