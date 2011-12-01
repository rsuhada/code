#!/usr/bin/env python
from sys import argv
import math
from numpy import *
from pylab import rc
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, LogLocator

def plot_sb_profile(r, c1, c2, fname):
    """
    plot a sb curve, overplot background

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
    # plt.savefig(fig_name)
    ######################################################################
    # stop plot enviroment
    ######################################################################


if __name__ == '__main__':
    """
    Fit the extracted spectrum.
    """

    ######################################################################
    # load in data

    intab = argv[1]
    dat=loadtxt(intab, dtype='string', comments='#', delimiter=None, converters=None,
                skiprows=0, unpack=False,
                # usecols=(0,1)
                )

    r = double(dat[:,0])
    cts_src = double(dat[:,1])
    cts_bg = double(dat[:,2])
    cts_tot = double(dat[:,3])
    exp_time = double(dat[:,4])
    area_correction = double(dat[:,5])
    mask_area = double(dat[:,6])
    geometric_area = double(dat[:,7])
    cts_src_wps = double(dat[:,8])
    cts_bg_wps = double(dat[:,9])
    cts_tot_wps = double(dat[:,10])
    exp_time_wps = double(dat[:,11])
    area_correction_wps = double(dat[:,12])
    mask_area_wps = double(dat[:,13])

    fname = intab+'.ctr.png'
    plot_sb_profile(r, cts_src, cts_bg, fname)


    print "Done!"
