# FIXME: add run-esas interface
# FIXME: install lmgit to 2.7 and use the newer python!
export PYTHONEXEC=/usr/bin/python2.6
export codedir="/Users/rs/data1/sw/esaspi"


# FIXME: add conf file interface ?
# Profile name
prof_fname='/Users/rs/w/xspt/data/dev/0559/sb/SPT-CL-J0559-5249/sb-prof-pn-003.dat'

r500_proj_ang="153.0"      # [arcsec]
instrument="pn"
theta="65.8443"
energy="1.5"                # [keV]

MODEL="beta"
MAKE_CONTROL_PLOT=True

# carry out the fitting

echo $PYTHONEXEC ${codedir}/sb/fit_sb_beta_dev.py $prof_fname $r500_proj_ang $instrument $theta $energy $MODEL $MAKE_CONTROL_PLOT

$PYTHONEXEC ${codedir}/sb/fit_sb_beta_dev.py $prof_fname $r500_proj_ang $instrument $theta $energy $MODEL $MAKE_CONTROL_PLOT