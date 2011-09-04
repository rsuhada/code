######################################################################
# do the calculations required for soft-proton contamination
# correction

dir=$1
here=`pwd`
cd $dir

analysis_id=$ANALYSIS_ID


# FIXME: what is passed is potentially a list - should loop through files
M1_EV_PREFIX=$M1_EV_PREFIX_LIST
M2_EV_PREFIX=$M2_EV_PREFIX_LIST
PN_EV_PREFIX=$PN_EV_PREFIX_LIST


######################################################################
# Snowden & Kuntz, 2011:
# proton-scale finds the solid angle for the region to include in the
# spectral fitting.  The solid angle which is in units of square arc
# minutes is added as a constant in the spectral model.  This scales
# the fitted parameters to per square arc minutes, which is also the
# units for the ROSAT data.

proton_scale caldb=${esas_caldb} mode=1 detector=1 maskfile=mos${M1_EV_PREFIX}-sp-${analysis_id}.fits specfile=mos${M1_EV_PREFIX}-obj-${analysis_id}.pi

proton_scale caldb=${esas_caldb} mode=1 detector=2 maskfile=mos${M2_EV_PREFIX}-sp-${analysis_id}.fits specfile=mos${M2_EV_PREFIX}-obj-${analysis_id}.pi

proton_scale caldb=${esas_caldb} mode=1 detector=3 maskfile=pn${PN_EV_PREFIX}-sp-${analysis_id}.fits specfile=pn${PN_EV_PREFIX}-obj-os-${analysis_id}.pi


######################################################################
# Snowden & Kuntz, 2011:
# proton uses the fitted soft proton parameters to create images of
# the soft proton contamination in detector coordinates.

# FIXME: ccd passing
# Sun Sep  4 09:41:45 2011

proton prefix=${M1_EV_PREFIX} caldb=${esas_caldb} ccd1=1 ccd2=1 ccd3=1 ccd4=1 ccd5=1 ccd6=1 ccd7=1 elow=400 ehigh=1250 spectrumcontrol=1 pindex=0.972080 pnorm=0.131099

proton prefix=${M1_EV_PREFIX} caldb=${esas_caldb} ccd1=1 ccd2=1 ccd3=1 ccd4=1 ccd5=1 ccd6=1 ccd7=1 elow=2000 ehigh=7200 spectrumcontrol=1 pindex=0.972080 pnorm=0.131099

proton prefix=${M2_EV_PREFIX} caldb=${esas_caldb} ccd1=1 ccd2=1 ccd3=1 ccd4=1 ccd5=1 ccd6=1 ccd7=1 elow=400 ehigh=1250 spectrumcontrol=1 pindex=0.972080 pnorm=0.128477

proton prefix=${M2_EV_PREFIX} caldb=${esas_caldb} ccd1=1 ccd2=1 ccd3=1 ccd4=1 ccd5=1 ccd6=1 ccd7=1 elow=2000 ehigh=7200 spectrumcontrol=1 pindex=0.972080 pnorm=0.128477

proton prefix=${PN_EV_PREFIX} caldb=${esas_caldb} ccd1=1 ccd2=1 ccd3=1 ccd4=1 elow=400 ehigh=1250 spectrumcontrol=1 pindex=1.53003 pnorm=0.361532

proton prefix=${PN_EV_PREFIX} caldb=${esas_caldb} ccd1=1 ccd2=1 ccd3=1 ccd4=1 elow=2000 ehigh=7200 spectrumcontrol=1 pindex=1.53003 pnorm=0.361532


######################################################################
# Snowden & Kuntz, 2011:
# rot-im-det-sky uses information in a previously created count image
# in sky coordinates to rotate the detector coordinate background
# images into images in sky coordinates.

elow='400'            # detection bands minima [eV]
ehigh='1250'          # detection bands maxima [eV]

rot-im-det-sky prefix=${M1_EV_PREFIX} mask=0 elow=$elow ehigh=$ehigh mode=2
rot-im-det-sky prefix=${M2_EV_PREFIX} mask=0 elow=$elow ehigh=$ehigh mode=2
rot-im-det-sky prefix=${PN_EV_PREFIX} mask=0 elow=$elow ehigh=$ehigh mode=2


elow='2000'            # detection bands minima [eV]
ehigh='7200'          # detection bands maxima [eV]

rot-im-det-sky prefix=${M1_EV_PREFIX} mask=0 elow=$elow ehigh=$ehigh mode=2
rot-im-det-sky prefix=${M2_EV_PREFIX} mask=0 elow=$elow ehigh=$ehigh mode=2
rot-im-det-sky prefix=${PN_EV_PREFIX} mask=0 elow=$elow ehigh=$ehigh mode=2


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0


