#!/usr/bin/env python
import sys
import os
import math
from numpy import *
from pylab import rc
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, LogLocator


def plot_r_t(r, t, t_err_p, t_err_n, figname):
    """
    Plot the cumulative temperature as function of extraction radius.
    """
    ######################################################################
    # start plot enviroment
    ######################################################################
    # start figure
    rc('axes', linewidth=1.5)
    fig_obj = plt.figure()
    headline_text = fig_obj.text(0.5, 0.95, '',
               horizontalalignment='center',
               fontproperties=matplotlib.font_manager.FontProperties(size=16))

    ax1 = fig_obj.add_subplot(111)                   # rows/cols/num of plot
    plt.subplots_adjust(hspace=0.2, wspace=0.2)      # hdefault=0.2, 0.001 for touching

    ######################################################################
    # plot data sets

    plt.errorbar(r, t, [t_err_n, t_err_p], fmt='o')      # both mixed

    ######################################################################
    # subplot data sets
    ax1.set_xscale('linear')                     # linear/log/symlog
    ax1.set_yscale('linear')                     # linear/log/symlog
    ax1.set_xlim(0.0, 1.1*r.max())

    # subplot text sets
    # ax1.set_title('plot title', fontsize=16, fontweight="normal")  # fontsize=16
    ax1.set_xlabel('Radius [arcsec]', fontsize=14, fontweight="normal")          # fontsize=12
    ax1.set_ylabel('T$_{\mathrm{X}}$ [keV]', fontsize=14, fontweight="normal")          # fontsize=12

    # legend
    prop = matplotlib.font_manager.FontProperties(size=16)  # size=16
    ax1.legend(loc=0, prop=prop, numpoints=1)

    # x - axis tick labels
    for label in ax1.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)                   # default = 0
        label.set_fontsize(14)                  # default = 12
        label.set_fontweight("normal")          # normal/heavy/light/ultranormal/ultralight

    # y - axis tick labels
    for label in ax1.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)                   # default = 0
        label.set_fontsize(14)                  # default = 12
        label.set_fontweight("normal")          # normal/heavy/light/ultranormal/ultralight

    # save figure
    plt.savefig(figname)

    ######################################################################
    # stop plot enviroment
    ######################################################################


if __name__ == '__main__':
    intab = sys.argv[1]

    ######################################################################
    # load data
    figname = intab+'.png'

    dat=loadtxt(intab, dtype='string', comments='#', delimiter=None, converters=None,
                skiprows=0, unpack=False,
                usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
                )

    fitid = double(dat[:,0])
    iter = double(dat[:,1])
    r_fit = double(dat[:,2])
    norm = double(dat[:,3])
    norm_err_n = -1.0*double(dat[:,4])
    norm_err_p = double(dat[:,5])
    t_fit = double(dat[:,6])
    t_fit_err_n = -1.0*double(dat[:,7])
    t_fit_err_p = double(dat[:,8])
    z = double(dat[:,9])
    z_err_n = -1.0*double(dat[:,10])
    z_err_p = double(dat[:,11])
    abund = double(dat[:,12])
    abund_err_n = -1.0*double(dat[:,13])
    abund_err_p = double(dat[:,14])


    ######################################################################
    # plot

    plot_r_t(r_fit, t_fit, t_fit_err_p, t_fit_err_n, figname)

    print "Plot created:"
    print figname
