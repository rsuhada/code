#!/usr/bin/env python
from numpy import *
from cosmo_dist import dist_ang
from physconstants import *
from scipy import integrate

def beta_shape_integral(rho, zeta, beta):
    """
    Beta model shape integral for integrating density profile
    (squared) needed for the XSPEC normalization conversion to
    physical units. Integral was validated with Mathematica.

    Arguments:
    - `rho`: dimensionless projected radius (squared)
    - `zeta`: dimensionless LOS distance
    - `beta`: beta power
    """
    return (1 + rho + zeta**2)**(-3*beta)

def beta_shape_integral_3D(x, beta):
    """
    Beta model shape integral for integration of the density profile
    (as function of 3D radius).  To be used for eg Mgas(r<r500)
    integration. Integral was validated with Mathematica.

    Arguments:
    - `x`: 3D radius in rcore units
    - `beta`: beta power
    """
    return x**2 * (1 + x**2)**(-3*beta/2.0)

def v06mod_shape_integral(rho, zeta, a, beta, gamma, epsilon, rbar):
    """
    Modified Vikhlinin06 model shape integral. Integral was validated
    with Mathematica.

    - `rho`: dimensionless projected radius (squared)
    - `zeta`: dimensionless LOS
    - 'a': alpha/2 - power from the profile
    - 'beta', 'gamma', 'epsilon': powers from the profile
    """
    x = rho + zeta**2
    i = x**(-a) * (1 + x)**(a - 3.0*beta) * (1 + x**(gamma/2.0) * rbar)**(-1.0*epsilon/gamma)

    return i

def spec_norm_to_density(norm_dat, z, da, rproj1_ang, rproj2_ang, model_name, model_pars):
    """
    Convert XSPEC normalization to density for a spherical region,
    optionally with excised inner sphere.

    Arguments:
    - `norm`: array XSPEC normalization in XSPEC units
              (10**(-14)/((1+z)Da)**2) with errors
    - `z`: redsihift
    - `da`: angular diameter distance [Mpc]
    - `rproj1_ang`: projected radius of the inner
                    excised spherical region [arcsec]
    - `rproj2_ang`: projected outer radius of the fitted spherical
                    region [arcsec]
    - `model_name`: model identifier: beta, v06
    - 'model_pars': parameter structure - content depends on : on the model

    Output:
    - `density`: array density in cgs [g cm**-3] and associated errors
    """

    # unpack inputs
    norm = norm_dat[0]
    norm_err_n = norm_dat[1]
    norm_err_p = norm_dat[2]

    density_err_n, density_err_p = 0.0, 0.0

    # get relative molecular weights: Feldman 1992, A=0.3
    mu_e = mu_e_feldman92
    mu_h = mu_h_feldman92

    # convert everything to cgs
    da = da * mpc_to_cm

    # the constant factor
    integ_profile = 1.0
    const = norm * 2 * mu_e * mu_h * mp_cgs**2 * (da*(1+z))**2 * 1.0e14

    # is the 2 needed here?
    # 130819: for beta model it is correct - the factor 2 from
    # changing the integral from (-infinity, infinity) to (0,
    # infinity) is used up in the shape integral substitution and does
    # not cancel the remaining factor 2 from the XSPEC normalization

    # FIXME: confirm this for v06 model too

    if model_name == 'beta':
        # print 'Using beta model'

        rcore = model_pars[0]
        beta  = model_pars[1]

        # print 'rcore: ', rcore
        # print 'beta: ', beta
        # print

        # integration bounds
        rho1 = (rproj1_ang / rcore)**2
        rho2 = (rproj2_ang / rcore)**2

        # do the integration
        # for rmax in (1, 1.0e1, 5.0e1, 1.0e2, 1e3, Inf):
        for rmax in (Inf,):
            integ_profile = integrate.dblquad(beta_shape_integral,
                                              0.0, rmax,
                                              lambda rho:rho1, lambda rho:rho2,
                                              args=(beta,))[0]
            print "Integration bound :: ", rmax, 'Shape integral :: ', integ_profile

            integ_profile = integ_profile * (rcore * arcsec_to_radian * da)**3


    elif model_name == 'v06mod':
        # FIXME: DO NOT USE YET - NEEDS REVIEW!!!!        print 'Using modified v06 model'

        # unpack parameters
        alpha   = model_pars[0]
        beta    = model_pars[1]
        gamma   = model_pars[2]
        epsilon = model_pars[3]
        rc      = model_pars[4]
        rs      = model_pars[5]

        a = alpha / 2.0
        rbar = (rc/rs)**gamma

        # integration bounds
        rho1 = (rproj1_ang / rc)**2
        rho2 = (rproj2_ang / rc)**2

        # do the integration
        # for rmax in (1, 1.0e2, 1.0e5, 1.0e6, Inf):
        for rmax in (Inf,):
            integ_profile = integrate.dblquad(v06mod_shape_integral, 0.0, rmax,
                                              lambda rho:rho1, lambda rho:rho2,
                                              args=(a, beta, gamma, epsilon, rbar))[0]
            print "Integration bound :: ", rmax, '   shape integral :: ', integ_profile
            integ_profile = integ_profile * (rc * arcsec_to_radian * da)**3

    try:
	density = sqrt(const / integ_profile)
    except Exception, e:
	raise e

    return array((density, density_err_n, density_err_p))


def calc_gas_mass(model_name, model_pars, rho0_dat, r1, r2):
    """
    Integrate the 3D density profile.

    Arguments:
    - `model_name`: model identifier: beta, v06
    - 'model_pars': parameter structure - content depends on : on the model
    - `rho0`: array - central density from the XSPEC norm [g cm**-3], lower and upper error
    - `r1`: inner 3D radius [kpc],
    - `r2`: outer 3D radius [kpc], e.g. r500

    Output:
    - `Mgas`: gas mass [Msol]
    """

    rho0 = rho0_dat[0]
    rho0_err_n = rho0_dat[1]
    rho0_err_p = rho0_dat[2]

    mgas = 0.0
    mgas_err_n = 0.0
    mgas_err_p = 0.0

    if model_name == 'beta':
        # print 'Using beta model'

        rcore = model_pars[0]
        beta  = model_pars[1]

        # integration bounds
        x1 = r1 / rcore
        x2 = r2 / rcore

        # print 'rcore: ', rcore
        # print 'beta: ', beta
        # print

        integ_profile = 0.0

        # do the integration
        integ_profile = integrate.quad(beta_shape_integral_3D, x1, x2,
                                       args=(beta, ))

        # print 'Integration limits :: ', x1, x2, ' [rcore]'
        # print "integral :: ", integ_profile

        prefactor = 4.0 * pi * (rcore * kpc_to_cm)**3 * (rho0 / msun_cgs)
        mgas =  prefactor * integ_profile[0]
        # mgas_err = prefactor    # need to add error on rho0, beta, rcore

        # print "Mgas :: ", mgas

    # v06mod model

    elif model_name == 'v06mod':
        # FIXME: not done yet
        # print 'Using modified v06 model'

        # unpack parameters
        alpha   = model_pars[0]
        beta    = model_pars[1]
        gamma   = model_pars[2]
        epsilon = model_pars[3]
        rc      = model_pars[4]
        rs      = model_pars[5]

    return array((mgas, mgas_err_n, mgas_err_p))


if __name__ == '__main__':
    print
    ######################################################################
    # test normalization calculation

    TEST_MODEL_NAME = 'beta'    # beta, v06mod
    # TEST_MODEL_NAME = 'v06mod'    # beta, v06mod

    # cosmology
    h_0=70.2
    omega_m_0=0.272
    omega_de_0=0.728
    omega_k_0=0.0

    # cluster parameters - 0559
    z = 0.468
    r500 = 1043.0      # kpc

    rproj1_ang = 0.0     # inner projected radius [arcsec]
    rproj2_ang = 60.0    # outer projected radius [arcsec]
    pixscale = 2.5       # [arcsec]

    # xspec norm
    norm = 1.45738E-03
    norm_err_n = -4.5767e-05
    norm_err_p = +4.53208e-05


    # angular distance
    da = dist_ang(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0) # [Mpc]
    angscale = arcsec_to_radian * da * 1000.0 # [kpc/arcsec]

    # setup the parameters for the integration, somewhat redundant
    # (having 2 rcore units) but for convenience
    if TEST_MODEL_NAME == 'beta':
        model_name = TEST_MODEL_NAME

        # best fit parameters should go here
        rcore = 10.0 * 2.5                # [pix]
        beta  = 2.0/3.0
        model_pars = (rcore, beta)

        # parameters for the Mgas calculation
        rcore_phy = rcore * pixscale * arcsec_to_radian * da * 1000.0 # [kpc]
        model_pars_phy = (rcore_phy, beta)

    elif TEST_MODEL_NAME == 'v06mod':
        model_name = TEST_MODEL_NAME

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
    # do the integrations for the density
    rho0_dat = spec_norm_to_density(norm, z, da, rproj1_ang, rproj2_ang, model_name, model_pars)
    ne0 = rho0 / (mu_e_feldman92 * mp_cgs)

    ######################################################################
    # gas mass calculation
    r1 = 0.0                    # [kpc]
    r2 = r500                   # [kpc]

    mgas_dat = calc_gas_mass(model_name, model_pars_phy, rho0_dat, r1, r2)

    ######################################################################
    # output

    # print
    # print "-"*60
    # print " z            :: ", z
    # print " da           :: ", da , "Mpc"
    # print " ang scale    :: ", angscale, "kpc/arcsec"
    # print "-"*60
    # print " rcore        :: ", rcore, "pix"
    # print " rcore phy    :: ", rcore_phy, "kpc"
    # print " beta         :: ", beta
    # print " proj radius  :: ", rproj1_ang, " - ", rproj2_ang, "arcsec"
    # print "-"*60
    # print " norm         :: ", norm, " 10**(-14)/((1+z)Da)**2"
    # print " rho0 density :: ", rho0, "g cm**-3"
    # print " ne0 density  :: ", ne0, "cm**-3"
    # print "-"*60
    # print " r500         :: ", r500, "kpc"
    # print " Mgas         :: ", mgas, "Msol"
    # print "-"*60


