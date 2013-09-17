#!/bin/bash

###########################################################
# XMM-Newton analysis pipeline                            #
# pipeline based on the Snowden & Kuntz analysis method   #
###########################################################

######################################################################
# help

if [[ $# -lt 2 ]]
then
  echo "Runs a esas analysis"
  echo
    echo "Parameters:"
    echo "1. config file"
    echo "2. module list file"
    echo ""
    echo "Syntax:"
  echo "run-esas.sh 0097820101.conf 0097820101.modules"
    echo
    exit 1
fi

######################################################################
# timing

t="$(date +%s)"
starttime=`date`

######################################################################
# read in arguments

export config_file=$1
export module_list=$2

######################################################################
# catch missing inputs

if [[ ! -e $config_file ]]
then
    echo -e "\n** error: config file $config_file does not exists here: "
    echo -e "*** $startdir\n"
    cd $startdir
    exit 1
fi
source $config_file

if [[ ! -e $module_list ]]
then
    echo -e "\n** error: module list $module_list does not exists here: "
    echo -e "*** $startdir\n"
    cd $startdir
    exit 1
fi
source $module_list

######################################################################
# setup

export obsid=$OBSID
export startdir=`pwd`
export workdir=${startdir}/${ANALYSIS_DIR}/analysis
export NOTESDIR=${startdir}/notes
export NOTESFILE=${NOTESDIR}/analysis-${CLNAME}.txt

######################################################################
# check whether observation is present

if [[ ! -e $ANALYSIS_DIR ]]
then
    echo -e "\n** error: directory $ANALYSIS_DIR does not exists here: "
    echo -e "*** $startdir\n"
    cd $startdir
    exit 1
fi

######################################################################
# sas setup

# ON_LAPTOP can be set in config files, but here it is overriden by
# automatic setting if not commented out

machine=`uname`

if [[ $machine == "Darwin" ]]
then
    export ON_LAPTOP=1
else
    export ON_LAPTOP=0
fi

# CHANGE PATHS HERE DEPENDINGON YOUR INSTALLATIONS
if [[ $ON_LAPTOP -eq 1 ]]
then

    echo "ON_LAPTOP = " $ON_LAPTOP
    echo "machine = " $machine

    export codedir="/Users/rs/data1/sw/esaspi"
    export esas_caldb="/Users/rs/calib/esas"

    export SAS_DIR="/Users/rs/data1/sw/sas-11.0.0/xmmsas_20110223_1803"
    export SAS_PATH="/Users/rs/data1/sw/sas-11.0.0/xmmsas_20110223_1803"
    export SAS_CCFPATH="/Users/rs/calib/xmm/ccf/"
    export SAS_MEMORY_MODEL=high
    export SAS_VERBOSITY=4

    export SAS_ODF=${startdir}/${ANALYSIS_DIR}/odf
    export SAS_CCF=${startdir}/${ANALYSIS_DIR}/analysis/ccf.cif

    export DS9_BINARY="/Users/rs/bin/ds9/ds9"
    export CALC_SCRIPT_DIR="/Users/rs/data1/sw/calc/"

    export PYTHONEXEC=/opt/local/bin/python

else
    # settings are d1 specific at the moment
    echo "ON_LAPTOP = " $ON_LAPTOP
    echo "machine = " $machine

    export codedir="/home/moon/rsuhada/data1/sw/esaspi"
    export esas_caldb="/home/moon/rsuhada/big/sw/xmm_calib/esas"

    export SAS_DIR="/home/moon/rsuhada/big/sw/sas.11.0.0/xmmsas_20110223_1801"
    export SAS_PATH="/home/moon/rsuhada/big/sw/sas.11.0.0/xmmsas_20110223_1801"
    export SAS_CCFPATH="/home/moon/rsuhada/big/sw/xmm_calib/ccf/"
    export SAS_MEMORY_MODEL=high
    export SAS_VERBOSITY=4

    export SAS_ODF=${startdir}/${ANALYSIS_DIR}/odf
    export SAS_CCF=${startdir}/${ANALYSIS_DIR}/analysis/ccf.cif

    export DS9_BINARY="/home/moon/rsuhada/big/sw/ds9/7.0.1/ds9"

    # this is deprecated now - not needed anymore
    # export CALC_SCRIPT_DIR="/home/moon/rsuhada/big/sw/calc/"

    export PYTHONEXEC=/home/moon/rsuhada/big/sw/Python-2.7.3/python

fi

######################################################################
# write start message

echo -e "\n############################################################"
echo -e "start time    :: " $starttime
echo -e "analysis path :: " $startdir
echo -e "analysis dir  :: " $ANALYSIS_DIR
echo -e "obsid         :: " $obsid
echo -e "config        :: " $config_file
echo -e "modules       :: " $module_list
echo -e "code          :: " $codedir
echo -e "############################################################\n"

echo -e "\nInitial SAS setup : \n"
sasversion

######################################################################
# move to obsid directory

cd $ANALYSIS_DIR
echo "Moved to dir :"
pwd

######################################################################
# prepare odf directory

if [[ $PREP_ODF_DIR -eq 1 ]]
then
    ${codedir}/prep-odf-dir.sh ${startdir}/${ANALYSIS_DIR}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

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
# recreate cheese masks after visual inspection - use emllist

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
# evigweight the eventlists

if [[ $DO_EVIGWEIGHT -eq 1 ]]
then
    ${codedir}/do-evigweight.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

######################################################################
# recreate cheese masks after visual inspection - additional src file

if [[ $REMASK_MANUAL_MASK -eq 1 ]]
then
    ${codedir}/remask-manual-mask.sh ${workdir}
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
# run spectrum/image extraction  - custom band (500 - 2000)

elo=500
ehi=2000

if [[ $EXTRACT_SPEC_BAND_PN -eq 1 ]]
then
    ${codedir}/extract-spec-band-pn.sh ${workdir} $elo $ehi
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

######################################################################
# run spectrum/image extraction - custom band (500 - 2000)

elo=500
ehi=2000

if [[ $EXTRACT_SPEC_BAND_M1 -eq 1 ]]
then
    ${codedir}/extract-spec-band-m1.sh ${workdir} $elo $ehi
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

######################################################################
# run spectrum/image extraction  - custom band (500 - 2000)

elo=500
ehi=2000

if [[ $EXTRACT_SPEC_BAND_M2 -eq 1 ]]
then
    ${codedir}/extract-spec-band-m2.sh ${workdir} $elo $ehi
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

######################################################################
# run background/image extraction - custom band (500 - 2000)

elo=500
ehi=2000

if [[ $EXTRACT_BACK_BAND_PN -eq 1 ]]
then
    ${codedir}/extract-back-band-pn.sh ${workdir} $elo $ehi
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

######################################################################
# run background/image extraction - custom band (500 - 2000)

elo=500
ehi=2000

if [[ $EXTRACT_BACK_BAND_M1 -eq 1 ]]
then
    ${codedir}/extract-back-band-m1.sh ${workdir} $elo $ehi
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

######################################################################
# run background/image extraction - custom band (500 - 2000)

elo=500
ehi=2000

if [[ $EXTRACT_BACK_BAND_M2 -eq 1 ]]
then
    ${codedir}/extract-back-band-m2.sh ${workdir} $elo $ehi
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
# imaging pipeline

elo="500"
ehi="2000"

# elo="500"
# ehi="7000"

if [[ $MAKE_IMS -eq 1 ]]
then
    ${codedir}/imaging/make-ims.sh ${workdir} ${elo} ${ehi}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

if [[ $MAKE_EXP_MAP -eq 1 ]]
then
    ${codedir}/imaging/make-exp-map.sh ${workdir} ${elo} ${ehi}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

if [[ $MAKE_MODEL_BG_2COMP -eq 1 ]]
then
    ${codedir}/imaging/make-model-bg-2comp.sh ${workdir} ${elo} ${ehi}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

if [[ $MAKE_MODEL_BG_SPLINE -eq 1 ]]
then
    ${codedir}/imaging/make-model-bg-spline.sh ${workdir} ${elo} ${ehi}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

######################################################################
# sb analyis pipe

if [[ $GET_CTS_STAT_APER -eq 1 ]]
then
    ${codedir}/sb/get-cts-stat-aper.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

if [[ $EXTRACT_SB_PROF -eq 1 ]]
then
    ${codedir}/sb/extract-sb-prof.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

######################################################################
# utilities

if [[ $PIPE_TEST -eq 1 ]]
then
    ${codedir}/pipe-test.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

if [[ $PLT_LC_HIST -eq 1 ]]
then
    ${codedir}/plt-lc-hist.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


if [[ $PLT_DIAGNOSTICS -eq 1 ]]
then
    ${codedir}/plt-diagnostics.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


if [[ $RELINK_SPEC_PRODUCTS -eq 1 ]]
then
    ${codedir}/relink-spec-products.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


if [[ $QUICK_SPEC_LOCBG -eq 1 ]]
then
    ${codedir}/quick-spec-locbg.sh ${workdir} $RA $DE
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi


if [[ $MAKE_QUICK_VIEW_IMS -eq 1 ]]
then
    ${codedir}/make-quick-view-ims.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

if [[ $ITER_SPEC -eq 1 ]]
then
    ${codedir}/iter-spec/iter-spec-driver.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

if [[ $RADIAL_SPEC -eq 1 ]]
then
    ${codedir}/radial-spec/radial-spec-driver.sh ${workdir}
    if [[ $? -ne 0 ]]
    then
        cd $startdir
        exit 1
    fi
fi

######################################################################
# temporary hot-fix

CONVERT_REG_WCS_TO_DET=0
export wcs_region=cluster-man-02.wcs.reg

if [[ $CONVERT_REG_WCS_TO_DET -eq 1 ]]
then
    ${codedir}/utils/convert-reg-wcs-to-det.sh ${workdir} ${wcs_region}
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
echo -e "analysis path :: " $startdir
echo -e "analysis dir  :: " $ANALYSIS_DIR
echo -e "obsid         :: " $obsid
echo -e "config        :: " $config_file
echo -e "modules       :: " $module_list
echo -e "code          :: " $codedir
echo -e "start time    :: " $starttime
echo -e "end time      :: " $endtime
printf  "runtime       ::  %02dd:%02dh:%02dm:%02ds\n" "$((t/86400))" "$((t/3600%24))" "$((t/60%60))" "$((t%60))"
echo -e "############################################################\n"

echo -e "Done :: $obsid\n"