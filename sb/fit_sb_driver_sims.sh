# FIXME: add run-esas interface
# FIXME: install lmfit to 2.7 and use the newer python!
export PYTHONEXEC=/usr/bin/python2.6
export codedir="/Users/rs/data1/sw/esaspi"


# FIXME: add conf file interface

# cluster settings
source /Users/rs/w/xspt/data/dev/0559/sb/sb_fit_sims.conf

######################################################################
# model settings
######################################################################

# loop through all instruments


if [[ ${INSTRUMENT_SETUP} == "single" ]]
then

    # fit a set of individual instruments

    for instrument in ${instruments[@]}
    do
        echo "fitting individually :: " $instrument
        # Profile name
        prof_fname="/Users/rs/w/xspt/data/dev/0559/sb/${cluster}/sb-prof-${instrument}-${profile_id}.dat"
        theta="theta_"${instrument}
        theta=${!theta}

        echo $PYTHONEXEC ${codedir}/sb/fit_sb_model_instrument.py $prof_fname $fitid $r500_pix $instrument $theta $energy $MODEL $MAKE_CONTROL_PLOT
        $PYTHONEXEC ${codedir}/sb/fit_sb_model_instrument.py $prof_fname $fitid $r500_pix $instrument $theta $energy $MODEL $MAKE_CONTROL_PLOT
    done

else

      prof_fname_pn="/Users/rs/w/xspt/data/dev/0559/sb/${cluster}/${cluster}-prof-pn-${profile_id}.dat"
    prof_fname_mos1="/Users/rs/w/xspt/data/dev/0559/sb/${cluster}/${cluster}-prof-mos1-${profile_id}.dat"
    prof_fname_mos2="/Users/rs/w/xspt/data/dev/0559/sb/${cluster}/${cluster}-prof-mos2-${profile_id}.dat"

    echo $PYTHONEXEC ${codedir}/sb/fit_sb_model_joint.py $fitid $MODEL $MAKE_CONTROL_PLOT $r500_pix $energy $pn_prof_fname $pn_prof_fname $prof_fname_pn $theta_pn $prof_fname_mos1 $theta_mos1 $prof_fname_mos2 $theta_mos2 $INSTRUMENT_SETUP $instruments

    $PYTHONEXEC ${codedir}/sb/fit_sb_model_joint.py $fitid $MODEL $MAKE_CONTROL_PLOT $r500_pix $energy $pn_prof_fname $pn_prof_fname $prof_fname_pn $theta_pn $prof_fname_mos1 $theta_mos1 $prof_fname_mos2 $theta_mos2 $INSTRUMENT_SETUP "$instruments"

fi