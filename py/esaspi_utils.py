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


def show_in_ds9(fits_image):
    """
    Spawn a ds9 process showing a file

    Arguments:
    - `fits_image`: fits to open
    """

    ds9path="/Applications/SAOImage\ DS9.app/Contents/MacOS/ds9"

    print "Opening a ds9 display!"
    os.system(ds9path+" "+fits_image+" &")
    print "Done: Opening a ds9 display!"
