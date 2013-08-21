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
import asciitable
from xspec_utils import *
import pickle


def print_debug_info():
    print rproj1_ang, rproj2_ang, norm_dat[0], rho0_dat[0], ne0_dat[0], r1, r2, norm_int, mgas_dat[0]

def print_input_info():
    print
    print '='*60
    print 'Input Files'
    print
    print 'XSPEC fit result file:'
    print xspec_fname
    print
    print 'Surface brightness model fitted parameter file:'
    print
    print fitted_pars_file
    print
    print 'MODEL_NAME :: ', TEST_MODEL_NAME
    print
    print '='*60
    print


def output_results():
    ######################################################################
    # output

    print
    print "-"*60
    print " z            :: ", z
    print " da           :: ", da , "Mpc"
    print " ang scale    :: ", angscale, "kpc/arcsec"
    print "-"*60
    print " rcore        :: ", rcore / pixscale, "pix"
    print " rcore        :: ", rcore, "arcsec"
    print " rcore phy    :: ", rcore_phy, "kpc"
    print " beta         :: ", beta
    print " proj radius  :: ", rproj1_ang, " - ", rproj2_ang, "arcsec"
    print "-"*60
    print " norm         :: ", norm_dat, " 10**(-14)/((1+z)Da)**2"
    print " rho0 density :: ", rho0_dat, "g cm**-3"
    print " ne0 density  :: ", ne0_dat, "cm**-3"
    print "-"*60
    print " r500         :: ", r500, "kpc"
    print " r1           :: ", r1, "kpc"
    print " r2           :: ", r2, "kpc"
    print " Mgas         :: ", mgas_dat, "Msol"
    print "-"*60

    return 0


def print_report(fname=None):
    if fname:
        print "result written to file :: "
        print fname
        print

        with open(fname, 'w') as f:
            sys.stdout = f
            # print_debug_info()
            print_input_info()
            output_results()
            sys.stdout = sys.__stdout__
    else:
        # print_debug_info()
        output_results()

    return 0

def tabulate_gas_mass(model_name, model_pars_phy, rho0, rmin, rmax, rstep, mgas_tab):
    """
    Calculate the gas mas between rmin and r_i on grid with stepsize
    rstep out to rmax for this value of rho0 and gas model.

    Arguments:
    - `model_name`: name of the gas model (i.e. beta)
    - `model_pars_phy`: model parameters in physical units (i.e. rcore in [kpc])
    - `rho_0`: central density of the model [g cm**-3]
    - `rmin`: innermost radius [kpc]
    - `rmax`: outermost radius [kpc]
    - `rstep`: step size in radius [kpc]
    - `mgas_tab`: file name where to write the mgas table

    Output:
    Table with:
    r [kpc]   Mgas [Msol]
    """
    # FIXME: add error bars, add full V06 model suport

    rgrid = arange(rmin+rstep, rmax, rstep)
    mgas = []

    # calculate
    for r in rgrid:
        mgas.append(calc_gas_mass(model_name, model_pars_phy, rho0, rmin, r))
        print r, mgas[-1][0], mgas[-1][1], mgas[-1][2]

    # write output
    f = open(mgas_tab, 'w')

    f.write('# r [kpc] \n')
    f.write('# mgas [Msol] \n')
    f.write('# mgas_err_n [Msol] \n')
    f.write('# mgas_err_p [Msol] \n')
    f.write('#\n')
    f.write('# r mgas mgas_err_n mgas_err_p\n')
    for i in range(len(rgrid)):
        f.write('%f %e %f %f\n' % (rgrid[i], mgas[i][0], mgas[i][1], mgas[i][2]))

    f.close()

    print
    print 'Mgas table written to: ', mgas_tab

######################################################################
# main
######################################################################


print

# reload(xspec_utils)

######################################################################
# test calculation for 0559
######################################################################

# cosmology
h_0=70.2
omega_m_0=0.272
omega_de_0=0.728
omega_k_0=0.0

# image/profile pixel scale
pixscale = 2.5       # [arcsec/pix]

# cluster - 0559
z = double(sys.argv[1])
r500 = double(sys.argv[2])
xspec_fname = sys.argv[3]
fitted_pars_file = sys.argv[4]
TEST_MODEL_NAME = sys.argv[5]

# # cluster - 0559
# z = 0.6112
# r500 = 1043.0                    # [kpc]
# xspec_fname='/Users/rs/w/xspt/data/dev/0559/sb/SPT-CL-J0559-5249/SPT-CL-J0559-5249-run-009-radial-master.tab'
# fitted_pars_file='/Users/rs/w/xspt/data/dev/0559/sb/SPT-CL-J0559-5249/sb-prof-pn-003.dat.01.pk'
# TEST_MODEL_NAME = 'beta'    # beta, v06mod

######################################################################
# load in beta fit results

with open(fitted_pars_file, 'rb') as input:
    fitted_pars = pickle.load(input)

beta = fitted_pars['params']['beta']['value']
rcore = fitted_pars['params']['rcore']['value'] * pixscale      # fit is in pix, here converted to [arcsec]
# beta_norm = fitted_pars['params']['norm']['value']

beta_err = fitted_pars['params']['beta']['stderr']
rcore_err = fitted_pars['params']['rcore']['stderr'] * pixscale # fit is in pix, here converted to [arcsec]
# beta_norm_err = fitted_pars['params']['norm']['stderr']

######################################################################
# load in XSPEC norm values

# i put manualyy at he aperture closest to r500 on top of the list
data = asciitable.read(table=xspec_fname, data_start=0)

rproj2_ang_array = data['r_fit']
rproj1_ang_array = 0.15 * rproj2_ang_array
# rproj1_ang_array = 0.0 * rproj2_ang_array
norm_array       = data['norm']
norm_err_n_array = abs(data['norm_err_n'])
norm_err_p_array = data['norm_err_p']

# beta = 0.974467
# beta_err =  0.148686
# beta_norm = 0.001095
# beta_norm_err = 0.000145
# rcore = 14.230824 * pixscale         # [arcsec]
# rcore_err = 2.877397 * pixscale

# output file
mgas_results_fname=fitted_pars_file+'.mgas'
mgas_tab_fname=fitted_pars_file+'.mgas.tab'

######################################################################
# do the calculation

# angular distance
da = dist_ang(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0) # [Mpc]
angscale = arcsec_to_radian * da * 1000.0 # [kpc/arcsec]

# setup the model parameters for the integration
VALID_MODEL = False

if TEST_MODEL_NAME == 'beta':
    model_name = TEST_MODEL_NAME
    VALID_MODEL = True

    # best fit parameters should go here
    model_pars = (rcore, beta)                # rcore in [arcsec]

    # parameters for the Mgas calculation
    # rcore_phy = rcore * pixscale * angscale      # pixscale should not be here !!
    rcore_phy = rcore * angscale
    model_pars_phy = (rcore_phy, beta)

    print_input_info()


elif TEST_MODEL_NAME == 'v06mod':
    # FIXME: need to be fully developed and checked - do not use before!
    model_name = TEST_MODEL_NAME
    VALID_MODEL = True

    rc = 20.0                   # ballpark 0.1 r500, [pix]
    beta = 2.0/3.0
    rs = 20.0                   # ballpark 0.5-1 r500, [pix]
    alpha = 1.5                 # <3
    gamma = 3.0                 # fix = 3
    epsilon = 2.0               # <5

    model_pars = (alpha, beta, gamma, epsilon, rc, rs)

    # parameters for the Mgas calculation
    rc_phy = rc * pixscale * arcsec_to_radian * da * 1000.0 # [kpc]
    rs_phy = rc * pixscale * arcsec_to_radian * da * 1000.0 # [kpc]
    model_pars_phy = (alpha, beta, gamma, epsilon, rc_phy, rs_phy)


######################################################################
#  do the integrations

# print "# xspec_rproj1_ang xspec_rproj2_ang xspec_norm rho0 ne0 mgas_r1 mgas_r2 norm_int mgas" # hdr for debug

# for i in xrange(len(norm_array)):
for i in xrange(1,):
    rproj2_ang  = rproj2_ang_array[i]
    rproj1_ang  = rproj1_ang_array[i]
    norm_dat  = array((norm_array[i], norm_err_n_array[i], norm_err_p_array[i]))

    ######################################################################
    # calculate the densities and the gas masses

    if VALID_MODEL:

        # do the integrations
        rho0_dat, norm_int = spec_norm_to_density(norm_dat, z, da, rproj1_ang, rproj2_ang, model_name, model_pars)

        # number density conversion for A=0.3
        ne0_dat = rho0_dat / (mu_e_feldman92 * mp_cgs)

        # gas mass calculation
        r2 = r500                   # [kpc]
        r1 = 0.0                    # [kpc]
        # r1 = 0.15 * r500            # [kpc]
        rstep = 10              # kpc

        ######################################################################
        #
        # calculate mgas for a range of outer radii
        #
        ######################################################################

        rmin = 0.0            # [kpc]
        rmax = 2.0 * r500     # [kpc]
        rstep = 10.0          # [kpc]

        tabulate_gas_mass(model_name, model_pars_phy, rho0_dat, rmin, rmax, rstep, mgas_tab_fname)

        ######################################################################
        #
        # calculate mgas for given aperture (r1, r2)
        #
        ######################################################################

        mgas_dat = calc_gas_mass(model_name, model_pars_phy, rho0_dat, r1, r2)
        print_report()
        print_report(mgas_results_fname)
