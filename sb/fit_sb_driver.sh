# FIXME: add run-esas interface
# FIXME: install lmgit to 2.7 and use the newer python!
export PYTHONEXEC=/usr/bin/python2.6
export codedir="/Users/rs/data1/sw/esaspi"



fitid=01
r500_proj_ang="153.0"      # [arcsec]
energy="1.5"                # [keV]
MODEL="beta"
MAKE_CONTROL_PLOT=False


# FIXME: add conf file interface

######################################################################
# loop through all instruments

instruments=("pn" "mos1" "mos2")
# instruments=("mos1" "mos2")
# instruments=("pn")

for instrument in ${instruments[@]}
do
    # FIXME: will need to add individual thetas
    theta="65.8443"

    # Profile name
    prof_fname="/Users/rs/w/xspt/data/dev/0559/sb/SPT-CL-J0559-5249/sb-prof-"$instrument"-003.dat"

    echo $PYTHONEXEC ${codedir}/sb/fit_sb_beta_dev.py $prof_fname $fitid $r500_proj_ang $instrument $theta $energy $MODEL $MAKE_CONTROL_PLOT

    $PYTHONEXEC ${codedir}/sb/fit_sb_beta_dev.py $prof_fname $fitid $r500_proj_ang $instrument $theta $energy $MODEL $MAKE_CONTROL_PLOT

done