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

print

reload(xspec_utils)

######################################################################
# test calculation for 0559
######################################################################

# TEST_MODEL_NAME = 'none'    # beta, v06mod
TEST_MODEL_NAME = 'beta'    # beta, v06mod
# TEST_MODEL_NAME = 'v06mod'    # beta, v06mod

# cosmology
h_0=70.2
omega_m_0=0.272
omega_de_0=0.728
omega_k_0=0.0

# cluster - 0559
z = 0.6112
r500 = 1043.0                    # [kpc]

# fname='/Users/rs/w/xspt/data/dev/0559/sb/SPT-CL-J0559-5249-run-001-radial-master.tab'

# load the values from XSPEC the table
# 0559
fname='/Users/rs/w/xspt/data/dev/0559/sb/SPT-CL-J0559-5249/SPT-CL-J0559-5249-run-009-radial-master.tab'
fitted_pars_file='/Users/rs/w/xspt/data/dev/0559/sb/SPT-CL-J0559-5249/sb-prof-pn-003.dat.dev.pk'

# 2332
# fname='/Users/rs/w/xspt/data/dev/0559/sb/SPT-CL-J2332-5358/SPT-CL-J2332-5358-run-002-radial-master.tab'
# fitted_pars_file='/Users/rs/w/xspt/data/dev/0559/sb/SPT-CL-J2332-5358/sb-prof-pn-004.dat.dev.pk'

######################################################################
# load in values

data = asciitable.read(table=fname)

rproj2_ang_array = data['r_fit']
rproj1_ang_array = 0.15 * rproj2_ang_array
norm_array       = data['norm']
norm_err_n_array = abs(data['norm_err_n'])
norm_err_p_array = data['norm_err_p']

# SB best fit parameters
pixscale = 2.5       # [arcsec]

# beta = 0.974467
# beta_err =  0.148686
# beta_norm = 0.001095
# beta_norm_err = 0.000145
# rcore = 14.230824 * pixscale         # [arcsec]
# rcore_err = 2.877397 * pixscale

######################################################################
# load in beta fit results

with open(fitted_pars_file, 'rb') as input:
    fitted_pars = pickle.load(input)

beta = fitted_pars['params']['beta']['value']
rcore = fitted_pars['params']['rcore']['value'] * pixscale
beta_norm = fitted_pars['params']['norm']['value']

beta_err = fitted_pars['params']['beta']['stderr']
rcore_err = fitted_pars['params']['rcore']['stderr'] * pixscale
beta_norm_err = fitted_pars['params']['norm']['stderr']

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
    model_pars = (rcore, beta)

    # parameters for the Mgas calculation
    rcore_phy = rcore * pixscale * arcsec_to_radian * da * 1000.0 # [kpc]
    model_pars_phy = (rcore_phy, beta)

elif TEST_MODEL_NAME == 'v06mod':
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

# for i in xrange(len(norm_array)):
for i in xrange(1,):
    rproj2_ang  = rproj2_ang_array[i]
    rproj1_ang  = rproj1_ang_array[i]
    norm_dat  = array((norm_array[i], norm_err_n_array[i], norm_err_p_array[i]))

    ######################################################################
    # calculate the densities and the gas masses

    if VALID_MODEL:

        print rproj2_ang, rproj2_ang * angscale

        # do the integrations
        rho0_dat = spec_norm_to_density(norm_dat, z, da, rproj1_ang, rproj2_ang, model_name, model_pars)

        # number density conversion for A=0.3
        ne0_dat = rho0_dat / (mu_e_feldman92 * mp_cgs)

        # gas mass calculation
        r2 = r500                   # [kpc]
        # r1 = 0.0                    # [kpc]
        r1 = 0.15 * r500            # [kpc]

        mgas_dat = calc_gas_mass(model_name, model_pars_phy, rho0_dat, r1, r2)

        # mgas = mgas_dat[0]

        print '#'*40
        print

        # print r1, r2, model_pars_phy, rho0, mgas

        ######################################################################
        # output

        print
        print "-"*60
        print " z            :: ", z
        print " da           :: ", da , "Mpc"
        print " ang scale    :: ", angscale, "kpc/arcsec"
        print "-"*60
        print " rcore        :: ", rcore, "pix"
        print " rcore phy    :: ", rcore_phy, "kpc"
        print " beta         :: ", beta
        print " proj radius  :: ", rproj1_ang, " - ", rproj2_ang, "arcsec"
        print "-"*60
        print " norm         :: ", norm_dat, " 10**(-14)/((1+z)Da)**2"
        print " rho0 density :: ", rho0_dat, "g cm**-3"
        print " ne0 density  :: ", ne0_dat, "cm**-3"
        print "-"*60
        print " r500         :: ", r500, "kpc"
        print " Mgas         :: ", mgas_dat, "Msol"
        print "-"*60


        ######################################################################
        ######################################################################
        ######################################################################

