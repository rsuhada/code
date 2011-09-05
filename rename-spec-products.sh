######################################################################
# rename extracted products with their analysis_id


dir=$1
here=`pwd`
cd $dir

analysis_id=$ANALYSIS_ID

# FIXME: what is passed is potentially a list - should loop through files

M1_EV_PREFIX=$M1_EV_PREFIX_LIST
M2_EV_PREFIX=$M2_EV_PREFIX_LIST
PN_EV_PREFIX=$PN_EV_PREFIX_LIST


mv mos${M1_EV_PREFIX}-obj.pi mos${M1_EV_PREFIX}-obj-${analysis_id}.pi
mv mos${M1_EV_PREFIX}.rmf mos${M1_EV_PREFIX}-${analysis_id}.rmf
mv mos${M1_EV_PREFIX}.arf mos${M1_EV_PREFIX}-${analysis_id}.arf
mv mos${M1_EV_PREFIX}-back.pi mos${M1_EV_PREFIX}-back-${analysis_id}.pi
mv mos${M1_EV_PREFIX}-obj-im-sp-det.fits mos${M1_EV_PREFIX}-sp-${analysis_id}.fits

mv mos${M2_EV_PREFIX}-obj.pi mos${M2_EV_PREFIX}-obj-${analysis_id}.pi
mv mos${M2_EV_PREFIX}.rmf mos${M2_EV_PREFIX}-${analysis_id}.rmf
mv mos${M2_EV_PREFIX}.arf mos${M2_EV_PREFIX}-${analysis_id}.arf
mv mos${M2_EV_PREFIX}-back.pi mos${M2_EV_PREFIX}-back-${analysis_id}.pi
mv mos${M2_EV_PREFIX}-obj-im-sp-det.fits mos${M2_EV_PREFIX}-sp-${analysis_id}.fits

mv pn${PN_EV_PREFIX}-obj-os.pi pn${PN_EV_PREFIX}-obj-os-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-obj.pi pn${PN_EV_PREFIX}-obj-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-obj-oot.pi pn${PN_EV_PREFIX}-obj-oot-${analysis_id}.pi
mv pn${PN_EV_PREFIX}.rmf pn${PN_EV_PREFIX}-${analysis_id}.rmf
mv pn${PN_EV_PREFIX}.arf pn${PN_EV_PREFIX}-${analysis_id}.arf
mv pn${PN_EV_PREFIX}-back.pi pn${PN_EV_PREFIX}-back-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-obj-im-sp-det.fits pn${PN_EV_PREFIX}-sp-${analysis_id}.fits


######################################################################
# copy over the diagonal response matrices needed for spectral fitting

cp ${esas_caldb}/mos1-diag.rsp.gz .
cp ${esas_caldb}/mos2-diag.rsp.gz .
cp ${esas_caldb}/pn-diag.rsp.gz .



######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0

