######################################################################
# rename extracted products with their analysis_id

dir=$1
here=`pwd`
cd $dir

analysis_id=$ANALYSIS_ID
grp=$GRPMIN

grp_script=grp-spec-${analysis_id}-b${$grp}.sh

(

echo "grppha mos1S003-obj-${analysis_id}.pi mos1S003-obj-${analysis_id}-grp.pi \'chkey BACKFILE mos1S003-back-${analysis_id}.pi & chkey RESPFILE mos1S003-${analysis_id}.rmf & chkey ANCRFILE mos1S003-${analysis_id}.arf & group min $grp & exit\'"

echo "grppha mos2S004-obj-${analysis_id}.pi mos2S004-obj-${analysis_id}-grp.pi \'chkey BACKFILE mos2S004-back-${analysis_id}.pi & chkey RESPFILE mos2S004-${analysis_id}.rmf & chkey ANCRFILE mos2S004-${analysis_id}.arf & group min $grp & exit\'"

echo "grppha pnS005-obj-os-${analysis_id}.pi pnS005-obj-os-${analysis_id}-grp.pi \'chkey BACKFILE pnS005-back-${analysis_id}.pi & chkey RESPFILE pnS005-${analysis_id}.rmf & chkey ANCRFILE pnS005-${analysis_id}.arf & group min $grp & exit\'"

) > $grp_script

chmod 744 $grp_script
./$grp_script


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0


