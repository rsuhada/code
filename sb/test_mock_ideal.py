#!/usr/bin/env python
from fit_sb_beta_dev import *

if __name__ == '__main__':

    ######################################################################
    # settings
    fname = '/Users/rs/w/xspt/data/dev/0559/sb/profile-lmfit-ideal-beta.tmp'
    outfig = fname+'.dev.png'

    # r_500_proj_ang = 153.0   # projected radius [arcsec]
    r_500_proj_ang = 100.0   # projected radius [arcsec]

    # PSF parameters
    theta = 65.8443 / 60.0
    energy = 1.5
    instrument = "pn"
    psf_pars = (instrument, theta, energy)

    # module settings
    MAKE_CONTROL_PLOT = False
    FIT_BETA_MODEL = True
    FIT_V06_MODEL = False

    ######################################################################
    # loading the data
    (r, sb_src, sb_bg, sb_src_err, sb_bg_err) = sanitize_sb_curve(load_sb_curve(fname))

    # sb_bg = zeros(len(sb_src))
    # sb_src_err = sqrt(sb_src)
    # sb_bg_err = 0.01 * sb_src_err

    ids = where(r<=r_500_proj_ang)

    r = r[ids]
    sb_src = sb_src[ids]
    sb_bg = sb_bg[ids]
    sb_src_err = sb_src_err[ids]
    sb_bg_err = sb_bg_err[ids]
    n = len(r)

    ######################################################################
    # control plot

    if MAKE_CONTROL_PLOT:
        plot_sb_profile(r, sb_src, sb_src_err, sb_bg, sb_bg_err, outfig)
        os.system("open "+outfig)

    if FIT_BETA_MODEL:
        fit_beta_model(r, sb_src, sb_src_err)

    if FIT_V06_MODEL:
        fit_v06_model(r, sb_src, sb_src_err)


    print "done!"
