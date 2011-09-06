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


######################################################################
# mv essential files

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
# move the rest

mv pn${PN_EV_PREFIX}-obj-im-400-1250.fits pn${PN_EV_PREFIX}-obj-im-400-1250-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-obj-im-400-1250-oot.fits pn${PN_EV_PREFIX}-obj-im-400-1250-oot-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-mask-im-400-1250.fits pn${PN_EV_PREFIX}-mask-im-400-1250-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-exp-im-400-1250.fits pn${PN_EV_PREFIX}-exp-im-400-1250-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-im1-400-1250.fits pn${PN_EV_PREFIX}-im1-400-1250-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-im1-400-1250-oot.fits pn${PN_EV_PREFIX}-im1-400-1250-oot-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-im2-400-1250.fits pn${PN_EV_PREFIX}-im2-400-1250-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-im2-400-1250-oot.fits pn${PN_EV_PREFIX}-im2-400-1250-oot-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-im3-400-1250.fits pn${PN_EV_PREFIX}-im3-400-1250-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-im3-400-1250-oot.fits pn${PN_EV_PREFIX}-im3-400-1250-oot-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-im4-400-1250.fits pn${PN_EV_PREFIX}-im4-400-1250-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-im4-400-1250-oot.fits pn${PN_EV_PREFIX}-im4-400-1250-oot-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-obj-im-2000-7200.fits pn${PN_EV_PREFIX}-obj-im-2000-7200-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-obj-im-2000-7200-oot.fits pn${PN_EV_PREFIX}-obj-im-2000-7200-oot-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-mask-im-2000-7200.fits pn${PN_EV_PREFIX}-mask-im-2000-7200-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-exp-im-2000-7200.fits pn${PN_EV_PREFIX}-exp-im-2000-7200-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-1obj.pi pn${PN_EV_PREFIX}-1obj-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-1obj-oot.pi pn${PN_EV_PREFIX}-1obj-oot-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-1ff.pi pn${PN_EV_PREFIX}-1ff-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-1ff-oot.pi pn${PN_EV_PREFIX}-1ff-oot-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-im1-2000-7200.fits pn${PN_EV_PREFIX}-im1-2000-7200-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-im1-2000-7200-oot.fits pn${PN_EV_PREFIX}-im1-2000-7200-oot-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-2obj.pi pn${PN_EV_PREFIX}-2obj-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-2obj-oot.pi pn${PN_EV_PREFIX}-2obj-oot-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-2ff.pi pn${PN_EV_PREFIX}-2ff-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-2ff-oot.pi pn${PN_EV_PREFIX}-2ff-oot-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-im2-2000-7200.fits pn${PN_EV_PREFIX}-im2-2000-7200-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-im2-2000-7200-oot.fits pn${PN_EV_PREFIX}-im2-2000-7200-oot-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-3obj.pi pn${PN_EV_PREFIX}-3obj-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-3obj-oot.pi pn${PN_EV_PREFIX}-3obj-oot-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-3ff.pi pn${PN_EV_PREFIX}-3ff-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-3ff-oot.pi pn${PN_EV_PREFIX}-3ff-oot-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-im3-2000-7200.fits pn${PN_EV_PREFIX}-im3-2000-7200-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-im3-2000-7200-oot.fits pn${PN_EV_PREFIX}-im3-2000-7200-oot-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-4obj.pi pn${PN_EV_PREFIX}-4obj-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-4obj-oot.pi pn${PN_EV_PREFIX}-4obj-oot-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-4ff.pi pn${PN_EV_PREFIX}-4ff-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-4ff-oot.pi pn${PN_EV_PREFIX}-4ff-oot-${analysis_id}.pi
mv pn${PN_EV_PREFIX}-im4-2000-7200.fits pn${PN_EV_PREFIX}-im4-2000-7200-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-im4-2000-7200-oot.fits pn${PN_EV_PREFIX}-im4-2000-7200-oot-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-obj-im-400-1250.fits mos${M1_EV_PREFIX}-obj-im-400-1250-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-mask-im-400-1250.fits mos${M1_EV_PREFIX}-mask-im-400-1250-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-exp-im-400-1250.fits mos${M1_EV_PREFIX}-exp-im-400-1250-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-obj-im-400-1250-ccd1.fits mos${M1_EV_PREFIX}-obj-im-400-1250-ccd1-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-mask-im-400-1250-ccd1.fits mos${M1_EV_PREFIX}-mask-im-400-1250-ccd1-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-exp-im-400-1250-ccd1.fits mos${M1_EV_PREFIX}-exp-im-400-1250-ccd1-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-im1-400-1250.fits mos${M1_EV_PREFIX}-im1-400-1250-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-im2-400-1250.fits mos${M1_EV_PREFIX}-im2-400-1250-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-im3-400-1250.fits mos${M1_EV_PREFIX}-im3-400-1250-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-im4-400-1250.fits mos${M1_EV_PREFIX}-im4-400-1250-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-im6-400-1250.fits mos${M1_EV_PREFIX}-im6-400-1250-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-im7-400-1250.fits mos${M1_EV_PREFIX}-im7-400-1250-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-obj-im-2000-7200.fits mos${M1_EV_PREFIX}-obj-im-2000-7200-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-mask-im-2000-7200.fits mos${M1_EV_PREFIX}-mask-im-2000-7200-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-exp-im-2000-7200.fits mos${M1_EV_PREFIX}-exp-im-2000-7200-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-1ff.pi mos${M1_EV_PREFIX}-1ff-${analysis_id}.pi
mv mos${M1_EV_PREFIX}-obj-im-2000-7200-ccd1.fits mos${M1_EV_PREFIX}-obj-im-2000-7200-ccd1-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-mask-im-2000-7200-ccd1.fits mos${M1_EV_PREFIX}-mask-im-2000-7200-ccd1-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-exp-im-2000-7200-ccd1.fits mos${M1_EV_PREFIX}-exp-im-2000-7200-ccd1-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-im1-2000-7200.fits mos${M1_EV_PREFIX}-im1-2000-7200-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-1obj.pi mos${M1_EV_PREFIX}-1obj-${analysis_id}.pi
mv mos${M1_EV_PREFIX}-2obj.pi mos${M1_EV_PREFIX}-2obj-${analysis_id}.pi
mv mos${M1_EV_PREFIX}-2ff.pi mos${M1_EV_PREFIX}-2ff-${analysis_id}.pi
mv mos${M1_EV_PREFIX}-im2-2000-7200.fits mos${M1_EV_PREFIX}-im2-2000-7200-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-3obj.pi mos${M1_EV_PREFIX}-3obj-${analysis_id}.pi
mv mos${M1_EV_PREFIX}-3ff.pi mos${M1_EV_PREFIX}-3ff-${analysis_id}.pi
mv mos${M1_EV_PREFIX}-im3-2000-7200.fits mos${M1_EV_PREFIX}-im3-2000-7200-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-4obj.pi mos${M1_EV_PREFIX}-4obj-${analysis_id}.pi
mv mos${M1_EV_PREFIX}-4ff.pi mos${M1_EV_PREFIX}-4ff-${analysis_id}.pi
mv mos${M1_EV_PREFIX}-im4-2000-7200.fits mos${M1_EV_PREFIX}-im4-2000-7200-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-6obj.pi mos${M1_EV_PREFIX}-6obj-${analysis_id}.pi
mv mos${M1_EV_PREFIX}-6ff.pi mos${M1_EV_PREFIX}-6ff-${analysis_id}.pi
mv mos${M1_EV_PREFIX}-im6-2000-7200.fits mos${M1_EV_PREFIX}-im6-2000-7200-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-7obj.pi mos${M1_EV_PREFIX}-7obj-${analysis_id}.pi
mv mos${M1_EV_PREFIX}-7ff.pi mos${M1_EV_PREFIX}-7ff-${analysis_id}.pi
mv mos${M1_EV_PREFIX}-im7-2000-7200.fits mos${M1_EV_PREFIX}-im7-2000-7200-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-obj-im-400-1250.fits mos${M2_EV_PREFIX}-obj-im-400-1250-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-exp-im-400-1250.fits mos${M2_EV_PREFIX}-exp-im-400-1250-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-mask-im-400-1250.fits mos${M2_EV_PREFIX}-mask-im-400-1250-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-obj-im-400-1250-ccd1.fits mos${M2_EV_PREFIX}-obj-im-400-1250-ccd1-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-mask-im-400-1250-ccd1.fits mos${M2_EV_PREFIX}-mask-im-400-1250-ccd1-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-exp-im-400-1250-ccd1.fits mos${M2_EV_PREFIX}-exp-im-400-1250-ccd1-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-im1-400-1250.fits mos${M2_EV_PREFIX}-im1-400-1250-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-im2-400-1250.fits mos${M2_EV_PREFIX}-im2-400-1250-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-im3-400-1250.fits mos${M2_EV_PREFIX}-im3-400-1250-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-im4-400-1250.fits mos${M2_EV_PREFIX}-im4-400-1250-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-im5-400-1250.fits mos${M2_EV_PREFIX}-im5-400-1250-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-im6-400-1250.fits mos${M2_EV_PREFIX}-im6-400-1250-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-im7-400-1250.fits mos${M2_EV_PREFIX}-im7-400-1250-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-obj-im-2000-7200.fits mos${M2_EV_PREFIX}-obj-im-2000-7200-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-mask-im-2000-7200.fits mos${M2_EV_PREFIX}-mask-im-2000-7200-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-exp-im-2000-7200.fits mos${M2_EV_PREFIX}-exp-im-2000-7200-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-1ff.pi mos${M2_EV_PREFIX}-1ff-${analysis_id}.pi
mv mos${M2_EV_PREFIX}-obj-im-2000-7200-ccd1.fits mos${M2_EV_PREFIX}-obj-im-2000-7200-ccd1-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-mask-im-2000-7200-ccd1.fits mos${M2_EV_PREFIX}-mask-im-2000-7200-ccd1-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-exp-im-2000-7200-ccd1.fits mos${M2_EV_PREFIX}-exp-im-2000-7200-ccd1-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-im1-2000-7200.fits mos${M2_EV_PREFIX}-im1-2000-7200-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-1obj.pi mos${M2_EV_PREFIX}-1obj-${analysis_id}.pi
mv mos${M2_EV_PREFIX}-2obj.pi mos${M2_EV_PREFIX}-2obj-${analysis_id}.pi
mv mos${M2_EV_PREFIX}-2ff.pi mos${M2_EV_PREFIX}-2ff-${analysis_id}.pi
mv mos${M2_EV_PREFIX}-im2-2000-7200.fits mos${M2_EV_PREFIX}-im2-2000-7200-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-3obj.pi mos${M2_EV_PREFIX}-3obj-${analysis_id}.pi
mv mos${M2_EV_PREFIX}-3ff.pi mos${M2_EV_PREFIX}-3ff-${analysis_id}.pi
mv mos${M2_EV_PREFIX}-im3-2000-7200.fits mos${M2_EV_PREFIX}-im3-2000-7200-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-4obj.pi mos${M2_EV_PREFIX}-4obj-${analysis_id}.pi
mv mos${M2_EV_PREFIX}-4ff.pi mos${M2_EV_PREFIX}-4ff-${analysis_id}.pi
mv mos${M2_EV_PREFIX}-im4-2000-7200.fits mos${M2_EV_PREFIX}-im4-2000-7200-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-5obj.pi mos${M2_EV_PREFIX}-5obj-${analysis_id}.pi
mv mos${M2_EV_PREFIX}-5ff.pi mos${M2_EV_PREFIX}-5ff-${analysis_id}.pi
mv mos${M2_EV_PREFIX}-im5-2000-7200.fits mos${M2_EV_PREFIX}-im5-2000-7200-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-6obj.pi mos${M2_EV_PREFIX}-6obj-${analysis_id}.pi
mv mos${M2_EV_PREFIX}-6ff.pi mos${M2_EV_PREFIX}-6ff-${analysis_id}.pi
mv mos${M2_EV_PREFIX}-im6-2000-7200.fits mos${M2_EV_PREFIX}-im6-2000-7200-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-7obj.pi mos${M2_EV_PREFIX}-7obj-${analysis_id}.pi
mv mos${M2_EV_PREFIX}-7ff.pi mos${M2_EV_PREFIX}-7ff-${analysis_id}.pi
mv mos${M2_EV_PREFIX}-im7-2000-7200.fits mos${M2_EV_PREFIX}-im7-2000-7200-${analysis_id}.fits
mv filtered.fits filtered-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-back-im-det-400-1250.fits pn${PN_EV_PREFIX}-back-im-det-400-1250-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-spec.qdp pn${PN_EV_PREFIX}-spec-${analysis_id}.qdp
mv pn${PN_EV_PREFIX}-back-im-det-2000-7200.fits pn${PN_EV_PREFIX}-back-im-det-2000-7200-${analysis_id}.fits
mv pn${PN_EV_PREFIX}-aug-spec.qdp pn${PN_EV_PREFIX}-aug-spec-${analysis_id}.qdp
mv pn${PN_EV_PREFIX}-aug-rev-rate.qdp pn${PN_EV_PREFIX}-aug-rev-rate-${analysis_id}.qdp
mv pn${PN_EV_PREFIX}-aug-rev-hard.qdp pn${PN_EV_PREFIX}-aug-rev-hard-${analysis_id}.qdp
mv pn${PN_EV_PREFIX}-aug.qdp pn${PN_EV_PREFIX}-aug-${analysis_id}.qdp
mv mos${M1_EV_PREFIX}-back-im-sky-400-1250.fits mos${M1_EV_PREFIX}-back-im-sky-400-1250-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-back-im-det-400-1250.fits mos${M1_EV_PREFIX}-back-im-det-400-1250-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-spec.qdp mos${M1_EV_PREFIX}-spec-${analysis_id}.qdp
mv mos${M1_EV_PREFIX}-back-im-sky-2000-7200.fits mos${M1_EV_PREFIX}-back-im-sky-2000-7200-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-back-im-det-2000-7200.fits mos${M1_EV_PREFIX}-back-im-det-2000-7200-${analysis_id}.fits
mv mos${M1_EV_PREFIX}-aug.qdp mos${M1_EV_PREFIX}-aug-${analysis_id}.qdp
mv mos${M2_EV_PREFIX}-back-im-det-400-1250.fits mos${M2_EV_PREFIX}-back-im-det-400-1250-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-back-im-sky-400-1250.fits mos${M2_EV_PREFIX}-back-im-sky-400-1250-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-spec.qdp mos${M2_EV_PREFIX}-spec-${analysis_id}.qdp
mv mos${M2_EV_PREFIX}-back-im-sky-2000-7200.fits mos${M2_EV_PREFIX}-back-im-sky-2000-7200-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-back-im-det-2000-7200.fits mos${M2_EV_PREFIX}-back-im-det-2000-7200-${analysis_id}.fits
mv mos${M2_EV_PREFIX}-aug.qdp mos${M2_EV_PREFIX}-aug-${analysis_id}.qdp
mv command.csh command-${analysis_id}.csh



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
