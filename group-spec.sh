######################################################################
# group extraceted spectra for fitting

dir=$1
here=`pwd`
cd $dir

analysis_id=$ANALYSIS_ID
grp=$GRPMIN

grp_script=grp-spec-${analysis_id}-b${grp}.sh

# FIXME: what is passed is potentially a list - should loop through files

M1_EV_PREFIX=$M1_EV_PREFIX_LIST
M2_EV_PREFIX=$M2_EV_PREFIX_LIST
PN_EV_PREFIX=$PN_EV_PREFIX_LIST

# verion that uses the analysis id: currently deprecated

# (
# echo "grppha mos${M1_EV_PREFIX}-obj-${analysis_id}.pi !mos${M1_EV_PREFIX}-obj-${analysis_id}-grp.pi 'chkey BACKFILE mos${M1_EV_PREFIX}-back-${analysis_id}.pi & chkey RESPFILE mos${M1_EV_PREFIX}-${analysis_id}.rmf & chkey ANCRFILE mos${M1_EV_PREFIX}-${analysis_id}.arf & group min $grp & exit'"
# echo
# echo "grppha mos${M2_EV_PREFIX}-obj-${analysis_id}.pi !mos${M2_EV_PREFIX}-obj-${analysis_id}-grp.pi 'chkey BACKFILE mos${M2_EV_PREFIX}-back-${analysis_id}.pi & chkey RESPFILE mos${M2_EV_PREFIX}-${analysis_id}.rmf & chkey ANCRFILE mos${M2_EV_PREFIX}-${analysis_id}.arf & group min $grp & exit'"
# echo
# echo "grppha pn${PN_EV_PREFIX}-obj-os-${analysis_id}.pi !pn${PN_EV_PREFIX}-obj-os-${analysis_id}-grp.pi 'chkey BACKFILE pn${PN_EV_PREFIX}-back-${analysis_id}.pi & chkey RESPFILE pn${PN_EV_PREFIX}-${analysis_id}.rmf & chkey ANCRFILE pn${PN_EV_PREFIX}-${analysis_id}.arf & group min $grp & exit'"
# ) > $grp_script




(
echo "grppha mos${M1_EV_PREFIX}-obj.pi !mos${M1_EV_PREFIX}-obj-grp.pi 'chkey BACKFILE mos${M1_EV_PREFIX}-back.pi & chkey RESPFILE mos${M1_EV_PREFIX}.rmf & chkey ANCRFILE mos${M1_EV_PREFIX}.arf & group min $grp & exit'"
echo
echo "grppha mos${M2_EV_PREFIX}-obj.pi !mos${M2_EV_PREFIX}-obj-grp.pi 'chkey BACKFILE mos${M2_EV_PREFIX}-back.pi & chkey RESPFILE mos${M2_EV_PREFIX}.rmf & chkey ANCRFILE mos${M2_EV_PREFIX}.arf & group min $grp & exit'"
echo
echo "grppha pn${PN_EV_PREFIX}-obj-os.pi !pn${PN_EV_PREFIX}-obj-os-grp.pi 'chkey BACKFILE pn${PN_EV_PREFIX}-back.pi & chkey RESPFILE pn${PN_EV_PREFIX}.rmf & chkey ANCRFILE pn${PN_EV_PREFIX}.arf & group min $grp & exit'"
) > $grp_script





chmod 744 $grp_script
./$grp_script


if [[ $? -ne 0 ]]
then
    echo -e "\n** error: spectrum grouping failed!"
    echo -e "*** error in script: $0\n"
    cd $here
    exit 1
fi



######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0


