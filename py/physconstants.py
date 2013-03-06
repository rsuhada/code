"""
Library of physical and astrophysical constants and convenience unit
conversion constatns.
"""
import math


######################################################################
# physical constatnts

cc_cgs = 2.99792458e10                        # Speed of light [cgs]
bk_cgs = 1.3806503e-16                        # Boltzmann's constant [cgs]
hp_cgs = 6.62606876e-27                       # Planck's constant [cgs]

# mass
mp_cgs = 1.67262158e-24                   # Proton rest mass [cgs]
me_cgs = 9.10938188e-28                       # Electron rest mass [cgs]


######################################################################
# astrophysical

# mass
msun_cgs = 1.989e33                           # Solar Mass [cgs]

# distance
mpc_to_cm = 3.085677582e24                # megaparsec [cgs]
kpc_to_cm = 3.085677582e21                # megaparsec [cgs]
cm_to_mpc = 1.0 / mpc_to_cm
cm_to_kpc = 1.0 / kpc_to_cm


######################################################################
# composition

# relative molecular weights: Feldman 1992, A=0.3
mu_e_feldman92 = 1.167
mu_h_feldman92 = 1.400


######################################################################
# angles

degree_to_radian = math.pi/(180.0)
arcmin_to_radian = math.pi/(180.0 * 60.0)
arcsec_to_radian = math.pi/(180.0 * 3600.0)

radian_to_degree = 1.0 / degree_to_radian
radian_to_arcmin = 1.0 / arcmin_to_radian
radian_to_arcsec = 1.0 / arcsec_to_radian

######################################################################
# radio

jy_to_si = 1.0e-26              # [W m**-2 Hz**-1]
jy_to_cgs = 1.0e-23             # [erg s**-1 cm**-2 Hz**-1]
