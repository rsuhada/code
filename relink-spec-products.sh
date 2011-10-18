######################################################################
# relinks extracted products to their analysis_id - required for
# rot-det sky

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

ln -s  mos${M1_EV_PREFIX}-obj-${analysis_id}.pi mos${M1_EV_PREFIX}-obj.pi
ln -s  mos${M1_EV_PREFIX}-${analysis_id}.rmf mos${M1_EV_PREFIX}.rmf
ln -s  mos${M1_EV_PREFIX}-${analysis_id}.arf mos${M1_EV_PREFIX}.arf
ln -s  mos${M1_EV_PREFIX}-back-${analysis_id}.pi mos${M1_EV_PREFIX}-back.pi
ln -s  mos${M1_EV_PREFIX}-sp-${analysis_id}.fits mos${M1_EV_PREFIX}-obj-im-sp-det.fits

ln -s  mos${M2_EV_PREFIX}-obj-${analysis_id}.pi mos${M2_EV_PREFIX}-obj.pi
ln -s  mos${M2_EV_PREFIX}-${analysis_id}.rmf mos${M2_EV_PREFIX}.rmf
ln -s  mos${M2_EV_PREFIX}-${analysis_id}.arf mos${M2_EV_PREFIX}.arf
ln -s  mos${M2_EV_PREFIX}-back-${analysis_id}.pi mos${M2_EV_PREFIX}-back.pi
ln -s  mos${M2_EV_PREFIX}-sp-${analysis_id}.fits mos${M2_EV_PREFIX}-obj-im-sp-det.fits

ln -s  pn${PN_EV_PREFIX}-obj-os-${analysis_id}.pi pn${PN_EV_PREFIX}-obj-os.pi
ln -s  pn${PN_EV_PREFIX}-obj-${analysis_id}.pi pn${PN_EV_PREFIX}-obj.pi
ln -s  pn${PN_EV_PREFIX}-obj-oot-${analysis_id}.pi pn${PN_EV_PREFIX}-obj-oot.pi
ln -s  pn${PN_EV_PREFIX}-${analysis_id}.rmf pn${PN_EV_PREFIX}.rmf
ln -s  pn${PN_EV_PREFIX}-${analysis_id}.arf pn${PN_EV_PREFIX}.arf
ln -s  pn${PN_EV_PREFIX}-back-${analysis_id}.pi pn${PN_EV_PREFIX}-back.pi
ln -s  pn${PN_EV_PREFIX}-sp-${analysis_id}.fits pn${PN_EV_PREFIX}-obj-im-sp-det.fits


######################################################################
# move the rest

ln -s  pn${PN_EV_PREFIX}-obj-im-400-1250-${analysis_id}.fits pn${PN_EV_PREFIX}-obj-im-400-1250.fits
ln -s  pn${PN_EV_PREFIX}-obj-im-400-1250-oot-${analysis_id}.fits pn${PN_EV_PREFIX}-obj-im-400-1250-oot.fits
ln -s  pn${PN_EV_PREFIX}-mask-im-400-1250-${analysis_id}.fits pn${PN_EV_PREFIX}-mask-im-400-1250.fits
ln -s  pn${PN_EV_PREFIX}-exp-im-400-1250-${analysis_id}.fits pn${PN_EV_PREFIX}-exp-im-400-1250.fits
ln -s  pn${PN_EV_PREFIX}-im1-400-1250-${analysis_id}.fits pn${PN_EV_PREFIX}-im1-400-1250.fits
ln -s  pn${PN_EV_PREFIX}-im1-400-1250-oot-${analysis_id}.fits pn${PN_EV_PREFIX}-im1-400-1250-oot.fits
ln -s  pn${PN_EV_PREFIX}-im2-400-1250-${analysis_id}.fits pn${PN_EV_PREFIX}-im2-400-1250.fits
ln -s  pn${PN_EV_PREFIX}-im2-400-1250-oot-${analysis_id}.fits pn${PN_EV_PREFIX}-im2-400-1250-oot.fits
ln -s  pn${PN_EV_PREFIX}-im3-400-1250-${analysis_id}.fits pn${PN_EV_PREFIX}-im3-400-1250.fits
ln -s  pn${PN_EV_PREFIX}-im3-400-1250-oot-${analysis_id}.fits pn${PN_EV_PREFIX}-im3-400-1250-oot.fits
ln -s  pn${PN_EV_PREFIX}-im4-400-1250-${analysis_id}.fits pn${PN_EV_PREFIX}-im4-400-1250.fits
ln -s  pn${PN_EV_PREFIX}-im4-400-1250-oot-${analysis_id}.fits pn${PN_EV_PREFIX}-im4-400-1250-oot.fits
ln -s  pn${PN_EV_PREFIX}-obj-im-2000-7200-${analysis_id}.fits pn${PN_EV_PREFIX}-obj-im-2000-7200.fits
ln -s  pn${PN_EV_PREFIX}-obj-im-2000-7200-oot-${analysis_id}.fits pn${PN_EV_PREFIX}-obj-im-2000-7200-oot.fits
ln -s  pn${PN_EV_PREFIX}-mask-im-2000-7200-${analysis_id}.fits pn${PN_EV_PREFIX}-mask-im-2000-7200.fits
ln -s  pn${PN_EV_PREFIX}-exp-im-2000-7200-${analysis_id}.fits pn${PN_EV_PREFIX}-exp-im-2000-7200.fits
ln -s  pn${PN_EV_PREFIX}-1obj-${analysis_id}.pi pn${PN_EV_PREFIX}-1obj.pi
ln -s  pn${PN_EV_PREFIX}-1obj-oot-${analysis_id}.pi pn${PN_EV_PREFIX}-1obj-oot.pi
ln -s  pn${PN_EV_PREFIX}-1ff-${analysis_id}.pi pn${PN_EV_PREFIX}-1ff.pi
ln -s  pn${PN_EV_PREFIX}-1ff-oot-${analysis_id}.pi pn${PN_EV_PREFIX}-1ff-oot.pi
ln -s  pn${PN_EV_PREFIX}-im1-2000-7200-${analysis_id}.fits pn${PN_EV_PREFIX}-im1-2000-7200.fits
ln -s  pn${PN_EV_PREFIX}-im1-2000-7200-oot-${analysis_id}.fits pn${PN_EV_PREFIX}-im1-2000-7200-oot.fits
ln -s  pn${PN_EV_PREFIX}-2obj-${analysis_id}.pi pn${PN_EV_PREFIX}-2obj.pi
ln -s  pn${PN_EV_PREFIX}-2obj-oot-${analysis_id}.pi pn${PN_EV_PREFIX}-2obj-oot.pi
ln -s  pn${PN_EV_PREFIX}-2ff-${analysis_id}.pi pn${PN_EV_PREFIX}-2ff.pi
ln -s  pn${PN_EV_PREFIX}-2ff-oot-${analysis_id}.pi pn${PN_EV_PREFIX}-2ff-oot.pi
ln -s  pn${PN_EV_PREFIX}-im2-2000-7200-${analysis_id}.fits pn${PN_EV_PREFIX}-im2-2000-7200.fits
ln -s  pn${PN_EV_PREFIX}-im2-2000-7200-oot-${analysis_id}.fits pn${PN_EV_PREFIX}-im2-2000-7200-oot.fits
ln -s  pn${PN_EV_PREFIX}-3obj-${analysis_id}.pi pn${PN_EV_PREFIX}-3obj.pi
ln -s  pn${PN_EV_PREFIX}-3obj-oot-${analysis_id}.pi pn${PN_EV_PREFIX}-3obj-oot.pi
ln -s  pn${PN_EV_PREFIX}-3ff-${analysis_id}.pi pn${PN_EV_PREFIX}-3ff.pi
ln -s  pn${PN_EV_PREFIX}-3ff-oot-${analysis_id}.pi pn${PN_EV_PREFIX}-3ff-oot.pi
ln -s  pn${PN_EV_PREFIX}-im3-2000-7200-${analysis_id}.fits pn${PN_EV_PREFIX}-im3-2000-7200.fits
ln -s  pn${PN_EV_PREFIX}-im3-2000-7200-oot-${analysis_id}.fits pn${PN_EV_PREFIX}-im3-2000-7200-oot.fits
ln -s  pn${PN_EV_PREFIX}-4obj-${analysis_id}.pi pn${PN_EV_PREFIX}-4obj.pi
ln -s  pn${PN_EV_PREFIX}-4obj-oot-${analysis_id}.pi pn${PN_EV_PREFIX}-4obj-oot.pi
ln -s  pn${PN_EV_PREFIX}-4ff-${analysis_id}.pi pn${PN_EV_PREFIX}-4ff.pi
ln -s  pn${PN_EV_PREFIX}-4ff-oot-${analysis_id}.pi pn${PN_EV_PREFIX}-4ff-oot.pi
ln -s  pn${PN_EV_PREFIX}-im4-2000-7200-${analysis_id}.fits pn${PN_EV_PREFIX}-im4-2000-7200.fits
ln -s  pn${PN_EV_PREFIX}-im4-2000-7200-oot-${analysis_id}.fits pn${PN_EV_PREFIX}-im4-2000-7200-oot.fits

ln -s  mos${M1_EV_PREFIX}-obj-im-400-1250-${analysis_id}.fits mos${M1_EV_PREFIX}-obj-im-400-1250.fits
ln -s  mos${M1_EV_PREFIX}-mask-im-400-1250-${analysis_id}.fits mos${M1_EV_PREFIX}-mask-im-400-1250.fits
ln -s  mos${M1_EV_PREFIX}-exp-im-400-1250-${analysis_id}.fits mos${M1_EV_PREFIX}-exp-im-400-1250.fits
ln -s  mos${M1_EV_PREFIX}-obj-im-400-1250-ccd1-${analysis_id}.fits mos${M1_EV_PREFIX}-obj-im-400-1250-ccd1.fits
ln -s  mos${M1_EV_PREFIX}-mask-im-400-1250-ccd1-${analysis_id}.fits mos${M1_EV_PREFIX}-mask-im-400-1250-ccd1.fits
ln -s  mos${M1_EV_PREFIX}-exp-im-400-1250-ccd1-${analysis_id}.fits mos${M1_EV_PREFIX}-exp-im-400-1250-ccd1.fits
ln -s  mos${M1_EV_PREFIX}-im1-400-1250-${analysis_id}.fits mos${M1_EV_PREFIX}-im1-400-1250.fits
ln -s  mos${M1_EV_PREFIX}-im2-400-1250-${analysis_id}.fits mos${M1_EV_PREFIX}-im2-400-1250.fits
ln -s  mos${M1_EV_PREFIX}-im3-400-1250-${analysis_id}.fits mos${M1_EV_PREFIX}-im3-400-1250.fits
ln -s  mos${M1_EV_PREFIX}-im4-400-1250-${analysis_id}.fits mos${M1_EV_PREFIX}-im4-400-1250.fits
ln -s  mos${M1_EV_PREFIX}-im5-400-1250-${analysis_id}.fits mos${M1_EV_PREFIX}-im5-400-1250.fits
ln -s  mos${M1_EV_PREFIX}-im6-400-1250-${analysis_id}.fits mos${M1_EV_PREFIX}-im6-400-1250.fits
ln -s  mos${M1_EV_PREFIX}-im7-400-1250-${analysis_id}.fits mos${M1_EV_PREFIX}-im7-400-1250.fits
ln -s  mos${M1_EV_PREFIX}-obj-im-2000-7200-${analysis_id}.fits mos${M1_EV_PREFIX}-obj-im-2000-7200.fits
ln -s  mos${M1_EV_PREFIX}-mask-im-2000-7200-${analysis_id}.fits mos${M1_EV_PREFIX}-mask-im-2000-7200.fits
ln -s  mos${M1_EV_PREFIX}-exp-im-2000-7200-${analysis_id}.fits mos${M1_EV_PREFIX}-exp-im-2000-7200.fits
ln -s  mos${M1_EV_PREFIX}-1ff-${analysis_id}.pi mos${M1_EV_PREFIX}-1ff.pi
ln -s  mos${M1_EV_PREFIX}-obj-im-2000-7200-ccd1-${analysis_id}.fits mos${M1_EV_PREFIX}-obj-im-2000-7200-ccd1.fits
ln -s  mos${M1_EV_PREFIX}-mask-im-2000-7200-ccd1-${analysis_id}.fits mos${M1_EV_PREFIX}-mask-im-2000-7200-ccd1.fits
ln -s  mos${M1_EV_PREFIX}-exp-im-2000-7200-ccd1-${analysis_id}.fits mos${M1_EV_PREFIX}-exp-im-2000-7200-ccd1.fits
ln -s  mos${M1_EV_PREFIX}-im1-2000-7200-${analysis_id}.fits mos${M1_EV_PREFIX}-im1-2000-7200.fits
ln -s  mos${M1_EV_PREFIX}-1obj-${analysis_id}.pi mos${M1_EV_PREFIX}-1obj.pi
ln -s  mos${M1_EV_PREFIX}-2obj-${analysis_id}.pi mos${M1_EV_PREFIX}-2obj.pi
ln -s  mos${M1_EV_PREFIX}-2ff-${analysis_id}.pi mos${M1_EV_PREFIX}-2ff.pi
ln -s  mos${M1_EV_PREFIX}-im2-2000-7200-${analysis_id}.fits mos${M1_EV_PREFIX}-im2-2000-7200.fits
ln -s  mos${M1_EV_PREFIX}-3obj-${analysis_id}.pi mos${M1_EV_PREFIX}-3obj.pi
ln -s  mos${M1_EV_PREFIX}-3ff-${analysis_id}.pi mos${M1_EV_PREFIX}-3ff.pi
ln -s  mos${M1_EV_PREFIX}-im3-2000-7200-${analysis_id}.fits mos${M1_EV_PREFIX}-im3-2000-7200.fits
ln -s  mos${M1_EV_PREFIX}-4obj-${analysis_id}.pi mos${M1_EV_PREFIX}-4obj.pi
ln -s  mos${M1_EV_PREFIX}-4ff-${analysis_id}.pi mos${M1_EV_PREFIX}-4ff.pi
ln -s  mos${M1_EV_PREFIX}-im4-2000-7200-${analysis_id}.fits mos${M1_EV_PREFIX}-im4-2000-7200.fits
ln -s  mos${M1_EV_PREFIX}-5obj-${analysis_id}.pi mos${M1_EV_PREFIX}-5obj.pi
ln -s  mos${M1_EV_PREFIX}-5ff-${analysis_id}.pi mos${M1_EV_PREFIX}-5ff.pi
ln -s  mos${M1_EV_PREFIX}-im5-2000-7200-${analysis_id}.fits mos${M1_EV_PREFIX}-im5-2000-7200.fits
ln -s  mos${M1_EV_PREFIX}-6obj-${analysis_id}.pi mos${M1_EV_PREFIX}-6obj.pi
ln -s  mos${M1_EV_PREFIX}-6ff-${analysis_id}.pi mos${M1_EV_PREFIX}-6ff.pi
ln -s  mos${M1_EV_PREFIX}-im6-2000-7200-${analysis_id}.fits mos${M1_EV_PREFIX}-im6-2000-7200.fits
ln -s  mos${M1_EV_PREFIX}-7obj-${analysis_id}.pi mos${M1_EV_PREFIX}-7obj.pi
ln -s  mos${M1_EV_PREFIX}-7ff-${analysis_id}.pi mos${M1_EV_PREFIX}-7ff.pi
ln -s  mos${M1_EV_PREFIX}-im7-2000-7200-${analysis_id}.fits mos${M1_EV_PREFIX}-im7-2000-7200.fits

ln -s  mos${M2_EV_PREFIX}-obj-im-400-1250-${analysis_id}.fits mos${M2_EV_PREFIX}-obj-im-400-1250.fits
ln -s  mos${M2_EV_PREFIX}-exp-im-400-1250-${analysis_id}.fits mos${M2_EV_PREFIX}-exp-im-400-1250.fits
ln -s  mos${M2_EV_PREFIX}-mask-im-400-1250-${analysis_id}.fits mos${M2_EV_PREFIX}-mask-im-400-1250.fits
ln -s  mos${M2_EV_PREFIX}-obj-im-400-1250-ccd1-${analysis_id}.fits mos${M2_EV_PREFIX}-obj-im-400-1250-ccd1.fits
ln -s  mos${M2_EV_PREFIX}-mask-im-400-1250-ccd1-${analysis_id}.fits mos${M2_EV_PREFIX}-mask-im-400-1250-ccd1.fits
ln -s  mos${M2_EV_PREFIX}-exp-im-400-1250-ccd1-${analysis_id}.fits mos${M2_EV_PREFIX}-exp-im-400-1250-ccd1.fits
ln -s  mos${M2_EV_PREFIX}-im1-400-1250-${analysis_id}.fits mos${M2_EV_PREFIX}-im1-400-1250.fits
ln -s  mos${M2_EV_PREFIX}-im2-400-1250-${analysis_id}.fits mos${M2_EV_PREFIX}-im2-400-1250.fits
ln -s  mos${M2_EV_PREFIX}-im3-400-1250-${analysis_id}.fits mos${M2_EV_PREFIX}-im3-400-1250.fits
ln -s  mos${M2_EV_PREFIX}-im4-400-1250-${analysis_id}.fits mos${M2_EV_PREFIX}-im4-400-1250.fits
ln -s  mos${M2_EV_PREFIX}-im5-400-1250-${analysis_id}.fits mos${M2_EV_PREFIX}-im5-400-1250.fits
ln -s  mos${M2_EV_PREFIX}-im6-400-1250-${analysis_id}.fits mos${M2_EV_PREFIX}-im6-400-1250.fits
ln -s  mos${M2_EV_PREFIX}-im7-400-1250-${analysis_id}.fits mos${M2_EV_PREFIX}-im7-400-1250.fits
ln -s  mos${M2_EV_PREFIX}-obj-im-2000-7200-${analysis_id}.fits mos${M2_EV_PREFIX}-obj-im-2000-7200.fits
ln -s  mos${M2_EV_PREFIX}-mask-im-2000-7200-${analysis_id}.fits mos${M2_EV_PREFIX}-mask-im-2000-7200.fits
ln -s  mos${M2_EV_PREFIX}-exp-im-2000-7200-${analysis_id}.fits mos${M2_EV_PREFIX}-exp-im-2000-7200.fits
ln -s  mos${M2_EV_PREFIX}-1ff-${analysis_id}.pi mos${M2_EV_PREFIX}-1ff.pi
ln -s  mos${M2_EV_PREFIX}-obj-im-2000-7200-ccd1-${analysis_id}.fits mos${M2_EV_PREFIX}-obj-im-2000-7200-ccd1.fits
ln -s  mos${M2_EV_PREFIX}-mask-im-2000-7200-ccd1-${analysis_id}.fits mos${M2_EV_PREFIX}-mask-im-2000-7200-ccd1.fits
ln -s  mos${M2_EV_PREFIX}-exp-im-2000-7200-ccd1-${analysis_id}.fits mos${M2_EV_PREFIX}-exp-im-2000-7200-ccd1.fits
ln -s  mos${M2_EV_PREFIX}-im1-2000-7200-${analysis_id}.fits mos${M2_EV_PREFIX}-im1-2000-7200.fits
ln -s  mos${M2_EV_PREFIX}-1obj-${analysis_id}.pi mos${M2_EV_PREFIX}-1obj.pi
ln -s  mos${M2_EV_PREFIX}-2obj-${analysis_id}.pi mos${M2_EV_PREFIX}-2obj.pi
ln -s  mos${M2_EV_PREFIX}-2ff-${analysis_id}.pi mos${M2_EV_PREFIX}-2ff.pi
ln -s  mos${M2_EV_PREFIX}-im2-2000-7200-${analysis_id}.fits mos${M2_EV_PREFIX}-im2-2000-7200.fits
ln -s  mos${M2_EV_PREFIX}-3obj-${analysis_id}.pi mos${M2_EV_PREFIX}-3obj.pi
ln -s  mos${M2_EV_PREFIX}-3ff-${analysis_id}.pi mos${M2_EV_PREFIX}-3ff.pi
ln -s  mos${M2_EV_PREFIX}-im3-2000-7200-${analysis_id}.fits mos${M2_EV_PREFIX}-im3-2000-7200.fits
ln -s  mos${M2_EV_PREFIX}-4obj-${analysis_id}.pi mos${M2_EV_PREFIX}-4obj.pi
ln -s  mos${M2_EV_PREFIX}-4ff-${analysis_id}.pi mos${M2_EV_PREFIX}-4ff.pi
ln -s  mos${M2_EV_PREFIX}-im4-2000-7200-${analysis_id}.fits mos${M2_EV_PREFIX}-im4-2000-7200.fits
ln -s  mos${M2_EV_PREFIX}-5obj-${analysis_id}.pi mos${M2_EV_PREFIX}-5obj.pi
ln -s  mos${M2_EV_PREFIX}-5ff-${analysis_id}.pi mos${M2_EV_PREFIX}-5ff.pi
ln -s  mos${M2_EV_PREFIX}-im5-2000-7200-${analysis_id}.fits mos${M2_EV_PREFIX}-im5-2000-7200.fits
ln -s  mos${M2_EV_PREFIX}-6obj-${analysis_id}.pi mos${M2_EV_PREFIX}-6obj.pi
ln -s  mos${M2_EV_PREFIX}-6ff-${analysis_id}.pi mos${M2_EV_PREFIX}-6ff.pi
ln -s  mos${M2_EV_PREFIX}-im6-2000-7200-${analysis_id}.fits mos${M2_EV_PREFIX}-im6-2000-7200.fits
ln -s  mos${M2_EV_PREFIX}-7obj-${analysis_id}.pi mos${M2_EV_PREFIX}-7obj.pi
ln -s  mos${M2_EV_PREFIX}-7ff-${analysis_id}.pi mos${M2_EV_PREFIX}-7ff.pi
ln -s  mos${M2_EV_PREFIX}-im7-2000-7200-${analysis_id}.fits mos${M2_EV_PREFIX}-im7-2000-7200.fits

ln -s  filtered-${analysis_id}.fits filtered.fits

ln -s  pn${PN_EV_PREFIX}-back-im-det-400-1250-${analysis_id}.fits pn${PN_EV_PREFIX}-back-im-det-400-1250.fits
ln -s  pn${PN_EV_PREFIX}-spec-${analysis_id}.qdp pn${PN_EV_PREFIX}-spec.qdp
ln -s  pn${PN_EV_PREFIX}-back-im-det-2000-7200-${analysis_id}.fits pn${PN_EV_PREFIX}-back-im-det-2000-7200.fits
ln -s  pn${PN_EV_PREFIX}-aug-spec-${analysis_id}.qdp pn${PN_EV_PREFIX}-aug-spec.qdp
ln -s  pn${PN_EV_PREFIX}-aug-rev-rate-${analysis_id}.qdp pn${PN_EV_PREFIX}-aug-rev-rate.qdp
ln -s  pn${PN_EV_PREFIX}-aug-rev-hard-${analysis_id}.qdp pn${PN_EV_PREFIX}-aug-rev-hard.qdp
ln -s  pn${PN_EV_PREFIX}-aug-${analysis_id}.qdp pn${PN_EV_PREFIX}-aug.qdp

ln -s  mos${M1_EV_PREFIX}-back-im-sky-400-1250-${analysis_id}.fits mos${M1_EV_PREFIX}-back-im-sky-400-1250.fits
ln -s  mos${M1_EV_PREFIX}-back-im-det-400-1250-${analysis_id}.fits mos${M1_EV_PREFIX}-back-im-det-400-1250.fits
ln -s  mos${M1_EV_PREFIX}-spec-${analysis_id}.qdp mos${M1_EV_PREFIX}-spec.qdp
ln -s  mos${M1_EV_PREFIX}-back-im-sky-2000-7200-${analysis_id}.fits mos${M1_EV_PREFIX}-back-im-sky-2000-7200.fits
ln -s  mos${M1_EV_PREFIX}-back-im-det-2000-7200-${analysis_id}.fits mos${M1_EV_PREFIX}-back-im-det-2000-7200.fits
ln -s  mos${M1_EV_PREFIX}-aug-${analysis_id}.qdp mos${M1_EV_PREFIX}-aug.qdp

ln -s  mos${M2_EV_PREFIX}-back-im-det-400-1250-${analysis_id}.fits mos${M2_EV_PREFIX}-back-im-det-400-1250.fits
ln -s  mos${M2_EV_PREFIX}-back-im-sky-400-1250-${analysis_id}.fits mos${M2_EV_PREFIX}-back-im-sky-400-1250.fits
ln -s  mos${M2_EV_PREFIX}-spec-${analysis_id}.qdp mos${M2_EV_PREFIX}-spec.qdp
ln -s  mos${M2_EV_PREFIX}-back-im-sky-2000-7200-${analysis_id}.fits mos${M2_EV_PREFIX}-back-im-sky-2000-7200.fits
ln -s  mos${M2_EV_PREFIX}-back-im-det-2000-7200-${analysis_id}.fits mos${M2_EV_PREFIX}-back-im-det-2000-7200.fits
ln -s  mos${M2_EV_PREFIX}-aug-${analysis_id}.qdp mos${M2_EV_PREFIX}-aug.qdp
ln -s  command-${analysis_id}.csh command.csh



######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0
