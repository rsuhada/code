#!/bin/bash

###########################################################
# XMM-Newton analysis pipeline                            #
# pipeline based on the Snowden & Kuntz analysis method   #
# builds the infrastructure around the runit-image script #
###########################################################


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
# options

export ON_LAPTOP=0

export PN_EV_PREFIX_LIST='S005'                # pn eventlists
export M1_EV_PREFIX_LIST='1S003'               # pn eventlists
export M2_EV_PREFIX_LIST='2S004'               # pn eventlists
export MOS_EV_PREFIX_LIST='1S003 2S004'        # all mos eventlists

export PN_SRC_REGFILE=reg-pn.txt               # source regfile in pn [detector coords]
export M1_SRC_REGFILE=reg-m1.txt               # source regfile in mos [detector coords]
export M2_SRC_REGFILE=reg-m2.txt               # source regfile in mos [detector coords]

export CHEESE_CLOBBER=0         # re-create exposure maps during cheese? [1 - yes, 0 -no]

# export ANALYSIS_ID='full'      # default: full
export ANALYSIS_ID='core'      # default: full
export GRPMIN=100              # esas default: 100

export PN_QUAD1=1                              # use this pn quadrant
export PN_QUAD2=1                              # use this pn quadrant
export PN_QUAD3=1                              # use this pn quadrant
export PN_QUAD4=1                              # use this pn quadrant

export M1_CCD1=1
export M1_CCD2=1
export M1_CCD3=1
export M1_CCD4=1
export M1_CCD5=0
export M1_CCD6=1
export M1_CCD7=1

export M2_CCD1=1
export M2_CCD2=1
export M2_CCD3=1
export M2_CCD4=1
export M2_CCD5=1
export M2_CCD6=1
export M2_CCD7=1


######################################################################
# modules

export PREP_ODF_DIR=0
export MAKE_CCF_ODF=0
export RUN_EV_CHAINS=0
export RUN_FILTERS=0

# MANUAL STEP: inspect light curves
# MANUAL STEP: select eventlist prefixes

export CHEESE_1B=0
export CHEESE_2B=0                              # !!!! not tested yet

# MANUAL STEP: select OK chips/quadrats: ds9 *soft* &
# MANUAL STEP: inspect point source removal, might need updating: ds9 *cheese* & (see notes)

export REMASK=0

# MANUAL STEP: define spectroscopy region in detectro coords - set region names

export EXTRACT_SPEC_ESAS_PN=1
export EXTRACT_SPEC_ESAS_M1=1                   # !!!! not tested yet
export EXTRACT_SPEC_ESAS_M2=1                   # !!!! not tested yet
export EXTRACT_BACK_ESAS_PN=1                   # !!!! not tested yet
export EXTRACT_BACK_ESAS_M1=1                   # !!!! not tested yet
export EXTRACT_BACK_ESAS_M2=1                   # !!!! not tested yet
export RENAME_SPEC_PRODUCTS=0
export GROUP_SPEC=0

# MANUAL STEP: create RASS bg spectrum (see notes)
# MANUAL STEP: spectral fitting: savexspec-${analysis_id}-pow-swcx.xcm

export CORRECT_PROTON=0            # !!!! not finished/tested yet
export COMBINE_SMOOTH=0            # !!!! not finishedtested yet


######################################################################
# setup

export obsid=$1
export startdir=`pwd`
# export codedir="/Users/rsuhada/data1/lab/esas/code"
export codedir="/home/rsuhada/data1/sbox/esas/code"
export esas_caldb="/home/rsuhada/data1/sbox/esas/esas_caldb"
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
# recreate cheese masks after visual inspection

if [[ $REMASK -eq 1 ]]
then
    ${codedir}/remask.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


######################################################################
# run spectrum/image extraction

if [[ $EXTRACT_SPEC_ESAS_PN -eq 1 ]]
then
    ${codedir}/extract-spec-esas-pn.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


######################################################################
# run spectrum/image extraction

if [[ $EXTRACT_SPEC_ESAS_M1 -eq 1 ]]
then
    ${codedir}/extract-spec-esas-m1.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


######################################################################
# run spectrum/image extraction

if [[ $EXTRACT_SPEC_ESAS_M2 -eq 1 ]]
then
    ${codedir}/extract-spec-esas-m2.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


######################################################################
# run background/image extraction

if [[ $EXTRACT_BACK_ESAS_PN -eq 1 ]]
then
    ${codedir}/extract-back-esas-pn.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


######################################################################
# run background/image extraction

if [[ $EXTRACT_BACK_ESAS_M1 -eq 1 ]]
then
    ${codedir}/extract-back-esas-m1.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


######################################################################
# run background/image extraction

if [[ $EXTRACT_BACK_ESAS_M2 -eq 1 ]]
then
    ${codedir}/extract-back-esas-m2.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

######################################################################
# run product renamig

if [[ $RENAME_SPEC_PRODUCTS -eq 1 ]]
then
    ${codedir}/rename-spec-products.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi



######################################################################
# group spectra

if [[ $GROUP_SPEC -eq 1 ]]
then
    ${codedir}/group-spec.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


######################################################################
# group spectra

if [[ $CORRECT_PROTON -eq 1 ]]
then
    ${codedir}/correct-proton.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


######################################################################
# combine and smooth images

if [[ $COMBINE_SMOOTH -eq 1 ]]
then
    ${codedir}/combine-smooth.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


######################################################################
# write finish message

cd $startdir


echo -e "\nAnalysis done. You have been using:\n"
sasversion


endtime=`date`
t="$(($(date +%s)-t))"

echo -e "\n############################################################"
echo -e "obsid      :: " $obsid
echo -e "start time :: " $starttime
echo -e "end time   :: " $endtime
printf  "runtime    ::  %02dd:%02dh:%02dm:%02ds\n" "$((t/86400))" "$((t/3600%24))" "$((t/60%60))" "$((t%60))"
echo -e "############################################################\n"

echo -e "Done :: $obsid\n"
