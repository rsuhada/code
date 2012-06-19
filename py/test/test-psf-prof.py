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

def plot_model_psf(energy, theta, instrument):
    """
    Makes a plot of the psf model

    Arguments:
    - `energy`: energy [keV]
    - `theta`: off-axis angle [arcmin]
    - `instrument`: "m1", "m2", "pn", [set]
    """

    if ("m1" in instrument):
        print "plotting m1"

    if ("m2" in instrument):
        print "plotting m2"

    if ("pn" in instrument):
        print "plotting pn"

    # get_psf_prof(instrument, energy, theta)


if __name__ == '__main__':
    print

    energy = 1.5
    theta = 1.0
    # instrument=("pn", "m1", "m2")
    instrument=("m1")

    plot_model_psf(energy, theta, instrument)

    print "done"
