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

######################################################################
# m1

ccd1=$M1_CCD1
ccd2=$M1_CCD2
ccd3=$M1_CCD3
ccd4=$M1_CCD4
ccd5=$M1_CCD5
ccd6=$M1_CCD6
ccd7=$M1_CCD7

proton prefix=${M1_EV_PREFIX} caldb=${esas_caldb} ccd1=$ccd1 ccd2=$ccd2 ccd3=$ccd3 ccd4=$ccd4 ccd5=$ccd5 ccd6=$ccd6 ccd7=$ccd7 elow=400 ehigh=1250 spectrumcontrol=1 pindex=0.972080 pnorm=0.131099

proton prefix=${M1_EV_PREFIX} caldb=${esas_caldb} ccd1=$ccd1 ccd2=$ccd2 ccd3=$ccd3 ccd4=$ccd4 ccd5=$ccd5 ccd6=$ccd6 ccd7=$ccd7 elow=2000 ehigh=7200 spectrumcontrol=1 pindex=0.972080 pnorm=0.131099


######################################################################
# m2

ccd1=$M2_CCD1
ccd2=$M2_CCD2
ccd3=$M2_CCD3
ccd4=$M2_CCD4
ccd5=$M2_CCD5
ccd6=$M2_CCD6
ccd7=$M2_CCD7

proton prefix=${M2_EV_PREFIX} caldb=${esas_caldb} ccd1=$ccd1 ccd2=$ccd2 ccd3=$ccd3 ccd4=$ccd4 ccd5=$ccd5 ccd6=$ccd6 ccd7=$ccd7 elow=400 ehigh=1250 spectrumcontrol=1 pindex=0.972080 pnorm=0.128477

proton prefix=${M2_EV_PREFIX} caldb=${esas_caldb} ccd1=$ccd1 ccd2=$ccd2 ccd3=$ccd3 ccd4=$ccd4 ccd5=$ccd5 ccd6=$ccd6 ccd7=$ccd7 elow=2000 ehigh=7200 spectrumcontrol=1 pindex=0.972080 pnorm=0.128477


######################################################################
# pn

quad1=$PN_QUAD1
quad2=$PN_QUAD2
quad3=$PN_QUAD3
quad4=$PN_QUAD4

proton prefix=${PN_EV_PREFIX} caldb=${esas_caldb} ccd1=$quad1 ccd2=$quad2 ccd3=$quad3 ccd4=$quad4 elow=400 ehigh=1250 spectrumcontrol=1 pindex=1.53003 pnorm=0.361532

proton prefix=${PN_EV_PREFIX} caldb=${esas_caldb} ccd1=$quad1 ccd2=$quad2 ccd3=$quad3 ccd4=$quad4 elow=2000 ehigh=7200 spectrumcontrol=1 pindex=1.53003 pnorm=0.361532


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


