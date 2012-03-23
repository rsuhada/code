######################################################################
# calculate area correction factors due to point source removal,
# chipgaps etc. for given existing EPIC image.

######################################################################
# setup

here=`pwd`                      # should be cluster/iter-spec/iteration

SETUP_SAS=1                     # should I set SAS path? 0 - no, use
                                # current setting

EVLI_DIR=${workdir}             # dir with filtered eventlists

if [[ $# == 1 ]]
then
    SETUP_SAS=$2
fi

if [[ ${SETUP_SAS} -eq 1 ]]
then
    echo "setting custom paths..."
    # this part might need manual settings!
    export EVLI_DIR=../../analysis
    export SAS_ODF=../../analysis/odf
    export SAS_CCF=../../analysis/ccf.cif

    export codedir="/Users/rs/data1/sw/esaspi"
    export esas_caldb="/Users/rs/calib/esas"

    export SAS_DIR="/Users/rs/data1/sw/sas-11.0.0/xmmsas_20110223_1803"
    export SAS_PATH="/Users/rs/data1/sw/sas-11.0.0/xmmsas_20110223_1803"
    export SAS_CCFPATH="/Users/rs/calib/xmm/ccf/"
    export SAS_MEMORY_MODEL=high
    export SAS_VERBOSITY=4
fi

sasversion

elo="500"                       # band is not crucial for our purposes
ehi="2000"

######################################################################
# get the exposure maps

for instrument in m1 m2 pn
do
    echo "working on instrument : " $instrument

    # FIXME: assumes that the keyword is on a single line (should be OK)
    image=`ls ${instrument}-*.im`
    evli=`fkeyprint ${image}+0 XPROC0 | grep -o "table=[^ ]*" | sed 's/table=//g'`
    evli=${EVLI_DIR}/${evli##*/}   # strips possible path and adds the correct one

    if [[ ! -e $evli ]]
    then
        echo -e "\n** error: $evli does not exists!"

        echo -e "\n* Either path is set wronly or check ${image}"
        echo -e "whether table= is not split to several lines. If yes edit $0"
        echo -e "and hardcode evenlist path"

        echo -e "*** error in $0\n"

        exit 1
    fi


    outexp=${image%.*},exp

    eexpmap imageset=${image} attitudeset=${EVLI_DIR}/atthk.fits \
        eventset=${evli}:EVENTS expimageset=${outexp} \
        withdetcoords=no withvignetting=yes usefastpixelization=no \
        usedlimap=no attrebin=4 pimin=${elo} pimax=${ehi}
done

######################################################################
# exit

echo -e "\n$0 in $obsid done!"
exit 0
