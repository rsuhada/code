######################################################################
# library of utility functions

function get_cluster_pars {

    ######################################################################
    # looks through an analysis notebook file returning the requested
    # parameters. Input is an array, e.g.  pars=(RA DE RA60
    # DE60 X_IM Y_IM X_PHY Y_PHY NH REDSHIFT), output is a string

    if [[ -e $NOTESFILE ]]
    then

        pars=$1
        declare -a values

        for i in ${!pars[@]}
        do
            val=`grep ${pars[i]} $NOTESFILE | head -1 | awk '{print $2}'`
            values=( "${values[@]}" "$val" )
            # echo ${pars[i]} ${values[i]}
        done

        # this is the output
        echo ${values[@]}

    else
        echo "$NOTESFILE does not exist, not returning parameters!"
    fi
}

