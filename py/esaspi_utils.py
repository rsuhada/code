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
import pickle

def show_in_ds9(fits_image):
    """
    Spawn a ds9 process showing fits file(s). Argument can be full ds9
    par string.

    Arguments:
    - `fits_image`: fits to open
    """

    ds9path="/Applications/SAOImage\ DS9.app/Contents/MacOS/ds9"

    print "Opening a ds9 display!"
    os.system(ds9path+" "+fits_image+" &")
    print "Done: Opening a ds9 display!"

def ds9imcoord2py(coord):
    """
    Convert a ds9 image coordinate to a python index

    Arguments:
    - `coord`: ds9 image coordinate
    """
    return round(coord - 1)

def py2ds9imcoord(pyindex):
    """
    Convert a python index to a ds9 image coordinate

    Arguments:
    - `coord`: ds9 image coordinate
    """
    return pyindex + 1

def iplot(x, y):
    """
    A simple no-fuss or features interctive plot for debugging.

    Arguments:
    - `x`: x value
    - `y`: y value
    """
    # interactive quick plot
    plt.figure()
    plt.ion()
    plt.clf()

    plt.plot(x, y,
        color='black',
        linestyle='-',              # -/--/-./:
        linewidth=1,                # linewidth=1
        marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
        markerfacecolor='black',
        markersize=0,               # markersize=6
        label=r"data"               # '__nolegend__'
        )

    plt.xscale("linear")
    plt.yscale("linear")

    plt.show()
    plotPosition="+1100+0"          # large_screen="+1100+0"; lap="+640+0"
    plt.get_current_fig_manager().window.wm_geometry(plotPosition)

def print_lmfit_result_tab(pars_true, pars_fit):
    """
    Print a nice result table for lmfit structures
    """
    print
    print "|"+12*"-"+"|"+12*"-"+"|"+12*"-"+"|"+12*"-"+"|"
    print "| %10s | %10s | %10s | %10s |" % ("name", "true", "fit", "error")
    print "|"+12*"-"+"|"+12*"-"+"|"+12*"-"+"|"+12*"-"+"|"
    for key in pars_true:
        print "| %10s | %10.5f | %10.5f | %10.5f |" % (key, pars_true[key].value, pars_fit[key].value, pars_fit[key].stderr)
    print "|"+12*"-"+"|"+12*"-"+"|"+12*"-"+"|"+12*"-"+"|"
    print

def lmfit_result_to_dict(result_obj, par_obj):
    """
    Flatten lmfit result aa parameter objects to a dictionary,
    removing unpickleable objects and adding a simplre final parameter
    subdictionary.
    """

    d={}
    for key in par_obj:
        d.update({key: {'correl': par_obj[key].correl, 'value': par_obj[key].value, 'stderr': par_obj[key].stderr}})

    outdict = result_obj.__dict__.copy()
    outdict['asteval'] = None
    outdict['namefinder'] = None
    outdict['params'] = d
    outdict['userfcn'] = None

