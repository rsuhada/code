######################################################################
# run masking software to updated cheese masks after CHEESE_1B/2B
# after manual inspection

source ${codedir}/utils/util-funcs-lib.sh

dir=$1
here=`pwd`
cd $dir

######################################################################
# option for manual reduction

MAKE_NEW_SKY_REG=1              # if you modify the region-sky.fits

echo "** warning: check point source removal condition - currently using esas default!"

######################################################################
# basic source list preselction criterion

expression='(DIST_NN >= 20.0)&&(FLUX >= 0.5e-14)&&(ID_INST == 0)&&(ID_BAND == 0)&&(DET_ML >= 15)'

######################################################################
# add manually adjusted ps to the exclusion

REMOVE_MAN_PS=1
MAN_PS_REG=ps-man.phy.reg

if [[ $REMOVE_MAN_PS -eq 1 ]]
then
    ds9reg_to_sasdesc $MAN_PS_REG 0
    inpattern=`cat ${MAN_PS_REG}.desc`
    expression="$expression $inpattern"
fi

######################################################################
# m1

export prefix=$M1_EV_PREFIX_LIST


if [[ $MAKE_NEW_SKY_REG -eq 1 ]]
then

    region eventset=mos${prefix}-clean.fits operationstyle=global srclisttab=emllist-man.fits:SRCLIST expression="$expression" bkgregionset=mos${prefix}-bkg_region-det.fits energyfraction=0.5 radiusstyle=enfrac outunit=detxy verbosity=1

    region eventset=mos${prefix}-clean.fits operationstyle=global srclisttab=emllist-man.fits:SRCLIST expression="$expression" bkgregionset=mos${prefix}-bkg_region-sky.fits radiusstyle=contour bkgratestyle=col nosrcellipse=yes bkgfraction=0.5 outunit=xy verbosity=1

fi

make_mask inimage=mos${prefix}-obj-im.fits \
inmask=mos${prefix}-mask-im.fits \
outmask=mos${prefix}-cheese.fits \
reglist=mos${prefix}-bkg_region-sky.fits


######################################################################
# m2

export prefix=$M2_EV_PREFIX_LIST

if [[ $MAKE_NEW_SKY_REG -eq 1 ]]
then

    region eventset=mos${prefix}-clean.fits operationstyle=global srclisttab=emllist-man.fits:SRCLIST expression="$expression" bkgregionset=mos${prefix}-bkg_region-det.fits energyfraction=0.5 radiusstyle=enfrac outunit=detxy verbosity=1

    region eventset=mos${prefix}-clean.fits operationstyle=global srclisttab=emllist-man.fits:SRCLIST expression="$expression" bkgregionset=mos${prefix}-bkg_region-sky.fits radiusstyle=contour bkgratestyle=col nosrcellipse=yes bkgfraction=0.5 outunit=xy verbosity=1

fi

make_mask inimage=mos${prefix}-obj-im.fits \
inmask=mos${prefix}-mask-im.fits \
outmask=mos${prefix}-cheese.fits \
reglist=mos${prefix}-bkg_region-sky.fits


######################################################################
# pn

export prefix=$PN_EV_PREFIX_LIST

if [[ $MAKE_NEW_SKY_REG -eq 1 ]]
then

    region eventset=pn${prefix}-clean.fits operationstyle=global srclisttab=emllist-man.fits:SRCLIST expression="$expression" bkgregionset=pn${prefix}-bkg_region-det.fits energyfraction=0.5 radiusstyle=enfrac outunit=detxy verbosity=1

    region eventset=pn${prefix}-clean.fits operationstyle=global srclisttab=emllist-man.fits:SRCLIST expression="$expression" bkgregionset=pn${prefix}-bkg_region-sky.fits radiusstyle=contour bkgratestyle=col nosrcellipse=yes bkgfraction=0.5 outunit=xy verbosity=1

fi

make_mask inimage=pn${prefix}-obj-im.fits \
inmask=pn${prefix}-mask-im.fits \
outmask=pn${prefix}-cheese.fits \
reglist=pn${prefix}-bkg_region-sky.fits


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0