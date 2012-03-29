######################################################################
# very simple script for pipe testing (export of variables,
# unit/integrated testing)

dir=$1
here=`pwd`
cd $dir

######################################################################
# do all the sourceing here

source ${codedir}/utils/util-funcs-lib.sh

######################################################################
# run the test

testlogfile=pipe_test.log

if [[ -e $testlogfile ]]
then
    rm $testlogfile
fi


(
echo "Options:"
echo ON_LAPTOP $ON_LAPTOP
echo PN_EV_PREFIX_LIST $PN_EV_PREFIX_LIST
echo M1_EV_PREFIX_LIST $M1_EV_PREFIX_LIST
echo M2_EV_PREFIX_LIST $M2_EV_PREFIX_LIST
echo MOS_EV_PREFIX_LIST $MOS_EV_PREFIX_LIST
echo PN_SRC_REGFILE $PN_SRC_REGFILE
echo M1_SRC_REGFILE $M1_SRC_REGFILE
echo M2_SRC_REGFILE $M2_SRC_REGFILE
echo CHEESE_CLOBBER $CHEESE_CLOBBER
echo ANALYSIS_ID $ANALYSIS_ID
echo GRPMIN $GRPMIN
echo PN_QUAD1 $PN_QUAD1
echo PN_QUAD2 $PN_QUAD2
echo PN_QUAD3 $PN_QUAD3
echo PN_QUAD4 $PN_QUAD4
echo M1_CCD1 $M1_CCD1
echo M1_CCD2 $M1_CCD2
echo M1_CCD3 $M1_CCD3
echo M1_CCD4 $M1_CCD4
echo M1_CCD5 $M1_CCD5
echo M1_CCD6 $M1_CCD6
echo M1_CCD7 $M1_CCD7
echo M2_CCD1 $M2_CCD1
echo M2_CCD2 $M2_CCD2
echo M2_CCD3 $M2_CCD3
echo M2_CCD4 $M2_CCD4
echo M2_CCD5 $M2_CCD5
echo M2_CCD6 $M2_CCD6
echo M2_CCD7 $M2_CCD7

echo
echo "Modules:"
echo PREP_ODF_DIR $PREP_ODF_DIR
echo MAKE_CCF_ODF $MAKE_CCF_ODF
echo RUN_EV_CHAINS $RUN_EV_CHAINS
echo RUN_FILTERS $RUN_FILTERS
echo CHEESE_1B $CHEESE_1B
echo CHEESE_2B $CHEESE_2B
echo REMASK $REMASK
echo EXTRACT_SPEC_ESAS_PN $EXTRACT_SPEC_ESAS_PN
echo EXTRACT_SPEC_ESAS_M1 $EXTRACT_SPEC_ESAS_M1
echo EXTRACT_SPEC_ESAS_M2 $EXTRACT_SPEC_ESAS_M2
echo EXTRACT_BACK_ESAS_PN $EXTRACT_BACK_ESAS_PN
echo EXTRACT_BACK_ESAS_M1 $EXTRACT_BACK_ESAS_M1
echo EXTRACT_BACK_ESAS_M2 $EXTRACT_BACK_ESAS_M2
echo RENAME_SPEC_PRODUCTS $RENAME_SPEC_PRODUCTS
echo GROUP_SPEC $GROUP_SPEC
echo CORRECT_PROTON $CORRECT_PROTON
echo COMBINE_SMOOTH $COMBINE_SMOOTH
echo PIPE_TEST $PIPE_TEST

) > $testlogfile

if [[ ! -e $testlogfile ]]
then
    echo -e "\n** error: ${dir}/$testlogfile was not created!"
    echo -e "*** error in $0\n"
    cd $startdir
    exit 1
else
    echo
    echo "Pipeline test succesful!"
    echo "Log file: ${dir}/$testlogfile"
    echo
    cat $testlogfile
    echo
fi

######################################################################
# unit testing

echo "######################################################################"
echo UNIT TEST
echo "######################################################################"

echo "current dir:"
pwd
echo

####################
# # image converter
# # image=pnS003-obj-image-sky.fits
# image=test.im
# x_wcs="83.99"
# x_im=`arcsec_2_impix_xmm $image $x_wcs`
# echo "Conversion: $x_wcs [\"] is $x_im [pix]"

# ####################
# # get_cts_stat_annul
# image=mos1S001-500-2000.exp
# bgmap=mos1S001-500-2000.exp
# aperture1_im=1
# aperture2_im=2
# pars=(X_IM Y_IM)
# xim=409.99769
# yim=439.99936
# # out=`get_cluster_pars $pars`
# # xim=`echo $out | awk '{print $1}'`
# # yim=`echo $out | awk '{print $2}'`
# ${codedir}/sb/get_cts_stat_aper_annul.py $image $xim $yim $aperture1_im $aperture2_im $bgmap > test.txt
# cat test.txt


echo "######################################################################"
echo UNIT TEST
echo "######################################################################"

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0
