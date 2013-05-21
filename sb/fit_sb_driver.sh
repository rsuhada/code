# FIXME: add run-esas interface
# FIXME: install lmgit to 2.7 and use the newer python!
export PYTHONEXEC=/usr/bin/python2.6
export codedir="/Users/rs/data1/sw/esaspi"


# FIXME: add conf file interface

# cluster settings

source /Users/rs/w/xspt/data/dev/0559/sb/sb_fit.conf

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
        theta="theta"${instrument}
        theta=${!theta}

        echo $PYTHONEXEC ${codedir}/sb/fit_sb_model_instrument.py $prof_fname $fitid $r500_proj_ang $instrument $theta $energy $MODEL $MAKE_CONTROL_PLOT
        # $PYTHONEXEC ${codedir}/sb/fit_sb_model_instrument.py $prof_fname $fitid $r500_proj_ang $instrument $theta $energy $MODEL $MAKE_CONTROL_PLOT

    done


else

    echo "fitting jointly :: " $instruments


    for instrument in ${instruments[@]}
    do
        echo "fitting individually :: " $instrument
        # Profile name
        prof_fname="/Users/rs/w/xspt/data/dev/0559/sb/${cluster}/sb-prof-${instrument}-${profile_id}.dat"
        theta="theta"${instrument}
        theta=${!theta}

        echo $PYTHONEXEC ${codedir}/sb/fit_sb_model_instrument.py $prof_fname $fitid $r500_proj_ang $instrument $theta $energy $MODEL $MAKE_CONTROL_PLOT
        # $PYTHONEXEC ${codedir}/sb/fit_sb_model_instrument.py $prof_fname $fitid $r500_proj_ang $instrument $theta $energy $MODEL $MAKE_CONTROL_PLOT

fi