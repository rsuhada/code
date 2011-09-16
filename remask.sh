######################################################################
# run masking software to updated cheese masks after CHEESE_1B/2B
# after manual inspection

dir=$1
here=`pwd`
cd $dir


echo "** warning: check point source removal condition - currently using esas default!"


######################################################################
# m1

export prefix=$M1_EV_PREFIX_LIST

region eventset=mos${prefix}-clean.fits operationstyle=global srclisttab=emllist.fits:SRCLIST expression='(DIST_NN >= 15.0)&&(FLUX >= 0.5e-14)&&(ID_INST == 0)&&(ID_BAND == 0)&&(DET_ML >= 15)' bkgregionset=mos${prefix}-bkg_region-det.fits energyfraction=0.5 radiusstyle=enfrac outunit=detxy verbosity=1

region eventset=mos${prefix}-clean.fits operationstyle=global srclisttab=emllist.fits:SRCLIST expression='(DIST_NN >= 15.0)&&(FLUX >= 0.5e-14)&&(ID_INST == 0)&&(ID_BAND == 0)&&(DET_ML >= 15)' bkgregionset=mos${prefix}-bkg_region-sky.fits radiusstyle=contour bkgratestyle=col nosrcellipse=yes bkgfraction=0.5 outunit=xy verbosity=1

make_mask inimage=mos${prefix}-obj-im.fits \
inmask=mos${prefix}-mask-im.fits \
outmask=mos${prefix}-cheese.fits \
reglist=mos${prefix}-bkg_region-sky.fits


######################################################################
# m2

export prefix=$M2_EV_PREFIX_LIST

region eventset=mos${prefix}-clean.fits operationstyle=global srclisttab=emllist.fits:SRCLIST expression='(DIST_NN >= 15.0)&&(FLUX >= 0.5e-14)&&(ID_INST == 0)&&(ID_BAND == 0)&&(DET_ML >= 15)' bkgregionset=mos${prefix}-bkg_region-det.fits energyfraction=0.5 radiusstyle=enfrac outunit=detxy verbosity=1

region eventset=mos${prefix}-clean.fits operationstyle=global srclisttab=emllist.fits:SRCLIST expression='(DIST_NN >= 15.0)&&(FLUX >= 0.5e-14)&&(ID_INST == 0)&&(ID_BAND == 0)&&(DET_ML >= 15)' bkgregionset=mos${prefix}-bkg_region-sky.fits radiusstyle=contour bkgratestyle=col nosrcellipse=yes bkgfraction=0.5 outunit=xy verbosity=1

make_mask inimage=mos${prefix}-obj-im.fits \
inmask=mos${prefix}-mask-im.fits \
outmask=mos${prefix}-cheese.fits \
reglist=mos${prefix}-bkg_region-sky.fits


######################################################################
# pn

export prefix=$PN_EV_PREFIX_LIST

region eventset=pn${prefix}-clean.fits operationstyle=global srclisttab=emllist.fits:SRCLIST expression='(DIST_NN >= 15.0)&&(FLUX >= 0.5e-14)&&(ID_INST == 0)&&(ID_BAND == 0)&&(DET_ML >= 15)' bkgregionset=pn${prefix}-bkg_region-det.fits energyfraction=0.5 radiusstyle=enfrac outunit=detxy verbosity=1

region eventset=pn${prefix}-clean.fits operationstyle=global srclisttab=emllist.fits:SRCLIST expression='(DIST_NN >= 15.0)&&(FLUX >= 0.5e-14)&&(ID_INST == 0)&&(ID_BAND == 0)&&(DET_ML >= 15)' bkgregionset=pn${prefix}-bkg_region-sky.fits radiusstyle=contour bkgratestyle=col nosrcellipse=yes bkgfraction=0.5 outunit=xy verbosity=1

make_mask inimage=pn${prefix}-obj-im.fits \
inmask=pn${prefix}-mask-im.fits \
outmask=pn${prefix}-cheese.fits \
reglist=pn${prefix}-bkg_region-sky.fits


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0