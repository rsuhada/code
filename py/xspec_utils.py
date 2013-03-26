#!/usr/bin/env python
from numpy import *
from cosmo_dist import dist_ang
from physconstants import *


def spec_norm_to_density(norm, z, da, rproj1_ang=0.0, rproj2_ang, model_name, model_pars):
    """
    Convert XSPEC normalization to density for a spherical region,
    optionally with excised inner sphere.

    Arguments:
    - `norm`: XSPEC normalization in XSPEC units
    - `z`: redsihift
    - `da`: angular diameter distance [Mpc]
    - `r_proj_inner_ang`: [default=0] projected radius of the inner
                          excised spherical region [arcsec]
    - `rproj2_ang`: projected outer radius of the fitted spherical
      region [arcsec]
    - `model_name`: model identifier: beta, v06
    - 'model_pars': parameter structure - content depends on : on the model

    Output:
    - `density`: density in cgs [g cm**-3]
    """

    # get relative molecular weights: Feldman 1992, A=0.3
    mu_e = mu_e_feldman92
    mu_h = mu_h_feldman92

    # convert everything to cgs
    da = da * mpc_to_cm
    r_proj = r_proj_ang * arcsec_to_radian * da       # [cm]
    r_proj_inner = r_proj_inner_ang  * arcsec_to_radian * da

    # the constant factor
    const = norm * 2 * mu_e * mu_h * mp_cgs**2 * (da*(1+z))**2 * 1.0e14

    return density


if __name__ == '__main__':
    print
    ######################################################################
    # test normalization calculation

    # cosmology
    h_0=70.2
    omega_m_0=0.272
    omega_de_0=0.728
    omega_k_0=0.0

    # cluster
    z = 0.468
    r_proj_ang = 60.0   # projected radius [arcsec]

    norm = 1.45738E-03
    norm_err_n = -4.5767e-05
    norm_err_p = +4.53208e-05

    # angular distance
    da = dist_ang(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0) # [Mpc]
    angscale = arcsec_to_radian * da * 1000.0 # [kpc/arcsec]

    density = spec_norm_to_density(norm, z, da, r_proj_ang)
    ne = density / (mu_e_feldman92 * mp_cgs)


    print
    print " z          :: ", z
    print " da         :: ", da
    print " ang scale  :: ", angscale
    print " r_proj_ang :: ", r_proj_ang
    print " r_proj     :: ", r_proj
    print " norm       :: ", norm
    print " density    :: ", density
    print " ne density :: ", ne





