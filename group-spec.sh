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


(
echo "grppha mos${M1_EV_PREFIX}-obj-${analysis_id}.pi mos1S003-obj-${analysis_id}-grp.pi 'chkey BACKFILE mos1S003-back-${analysis_id}.pi & chkey RESPFILE mos1S003-${analysis_id}.rmf & chkey ANCRFILE mos1S003-${analysis_id}.arf & group min $grp & exit'"
echo
echo "grppha mos${M2_EV_PREFIX}-obj-${analysis_id}.pi mos2S004-obj-${analysis_id}-grp.pi 'chkey BACKFILE mos2S004-back-${analysis_id}.pi & chkey RESPFILE mos2S004-${analysis_id}.rmf & chkey ANCRFILE mos2S004-${analysis_id}.arf & group min $grp & exit'"
echo
echo "grppha pn${PN_EV_PREFIX}-obj-os-${analysis_id}.pi pnS005-obj-os-${analysis_id}-grp.pi 'chkey BACKFILE pnS005-back-${analysis_id}.pi & chkey RESPFILE pnS005-${analysis_id}.rmf & chkey ANCRFILE pnS005-${analysis_id}.arf & group min $grp & exit'"
) > $grp_script

chmod 744 $grp_script
# ./$grp_script


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0


