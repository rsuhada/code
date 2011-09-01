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
# modules
export PREP_ODF_DIR=0
export MAKE_CCF_ODF=0
export RUN_EV_CHAINS=1


######################################################################
# setup
export starttime=`date`
export obsid=$1
export startdir=`pwd`
export codedir="/Users/rsuhada/data1/lab/esas/code"
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
    echo -e "$startdir\n"
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
export SAS_DIR="/Users/rsuhada/data1/sw/sas.11.0.0/xmmsas_20110223_1803"
export SAS_PATH="/Users/rsuhada/data1/sw/sas.11.0.0/xmmsas_20110223_1803"
export SAS_CCFPATH="/xmm/ccf/"
export SAS_MEMORY_MODEL=high
export SAS_VERBOSITY=4

export SAS_ODF=${startdir}/${obsid}/odf
export SAS_CCF=${startdir}/${obsid}/analysis/ccf.cif

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
# write finish message
cd $startdir
export endtime=`date`

echo -e "\n############################################################"
echo -e "obsid :: " $obsid
echo -e "start time :: " $starttime
echo -e "end time :: " $endtime
echo -e "############################################################\n"

echo -e "Done :: $obsid\n"
