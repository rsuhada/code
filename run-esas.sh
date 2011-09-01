#!/bin/bash

######################################################################
# help

if [[ $# -lt 1 ]]
then
	echo "Runs a esas analysis"
	echo
    echo "Parameters:"
    echo "1. obsid"
    echo ""
    echo "Syntax:"
	echo "run-esas.sh obsid"
    echo
    exit 1
fi

######################################################################
# timing

t="$(date +%s)"
starttime=`date`


######################################################################
# modules and options

export ON_LAPTOP=0

export PREP_ODF_DIR=0
export MAKE_CCF_ODF=0
export RUN_EV_CHAINS=0
export RUN_FILTERS=0
export CHEESE_1B=1
export CHEESE_2B=0


######################################################################
# setup

export obsid=$1
export startdir=`pwd`
# export codedir="/Users/rsuhada/data1/lab/esas/code"
export codedir="/home/rsuhada/data1/sbox/esas/code"
export esas_caldb="/XMM/sas/CCF/esas"
export workdir=${startdir}/${obsid}/analysis


######################################################################
# write start message

echo -e "\n############################################################"
echo -e "start time :: " $starttime
echo -e "directory :: " $startdir
echo -e "obsid :: " $obsid
echo -e "code :: " $codedir
echo -e "############################################################\n"


######################################################################
# catch missing directory

if [[ ! -e $obsid ]]
then

    echo -e "\n** error: obsid $obsid does not exists here: "
    echo -e "*** $startdir\n"
    cd $startdir
    exit 1

fi


######################################################################
# move to obsid directory

cd $obsid
echo "Moved to dir :"
pwd


######################################################################
# prepare odf directory

if [[ $PREP_ODF_DIR -eq 1 ]]
then
    ${codedir}/prep-odf-dir.sh ${startdir}/${obsid}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


######################################################################
# sas setup

if [[ $ON_LAPTOP -eq 1 ]]
then

    export SAS_DIR="/Users/rsuhada/data1/sw/sas.11.0.0/xmmsas_20110223_1803"
    export SAS_PATH="/Users/rsuhada/data1/sw/sas.11.0.0/xmmsas_20110223_1803"
    export SAS_CCFPATH="/xmm/ccf/"
    export SAS_MEMORY_MODEL=high
    export SAS_VERBOSITY=4

    export SAS_ODF=${startdir}/${obsid}/odf
    export SAS_CCF=${startdir}/${obsid}/analysis/ccf.cif

else

    # export SAS_DIR="/utils/xmmsas_11.0.1"
    # export SAS_PATH="/utils/xmmsas_11.0.1"
    # export SAS_CCFPATH="/xmm/ccf/public"
    # export SAS_MEMORY_MODEL=high
    # export SAS_VERBOSITY=4

    export SAS_ODF=${startdir}/${obsid}/odf
    export SAS_CCF=${startdir}/${obsid}/analysis/ccf.cif

fi


echo -e "\n Initial SAS setup : \n"
sasversion


######################################################################
# move to obsid directory

cd analysis
echo "Moved to dir :"
pwd


######################################################################
# make ccf and odf files

if [[ $MAKE_CCF_ODF -eq 1 ]]
then
    ${codedir}/make-ccf-odf.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


######################################################################
# run event calibration chains

if [[ $RUN_EV_CHAINS -eq 1 ]]
then
    ${codedir}/run-ev-chains.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


######################################################################
# run filters

if [[ $RUN_FILTERS -eq 1 ]]
then
    ${codedir}/run-filters.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


######################################################################
# run single band image cheesing

if [[ $CHEESE_1B -eq 1 ]]
then
    ${codedir}/cheese-1b.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


######################################################################
# run two band image cheesing

if [[ $CHEESE_2B -eq 1 ]]
then
    ${codedir}/cheese-2b.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi



######################################################################
# write finish message

cd $startdir

endtime=`date`
t="$(($(date +%s)-t))"

echo -e "\n############################################################"
echo -e "obsid      :: " $obsid
echo -e "start time :: " $starttime
echo -e "end time   :: " $endtime
printf  "runtime    ::  %02dd:%02dh:%02dm:%02ds\n" "$((t/86400))" "$((t/3600%24))" "$((t/60%60))" "$((t%60))"
echo -e "############################################################\n"

echo -e "Done :: $obsid\n"
