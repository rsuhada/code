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
DEBUG_CHEESE_IM=1               # creates a masked image for debug checking

echo "** warning: check point source removal condition - currently using esas default!"

######################################################################
# basic source list preselction criterion

# original esas
# expression='(DIST_NN >= 20.0)&&(FLUX >= 0.5e-14)&&(ID_INST == 0)&&(ID_BAND == 0)&&(DET_ML >= 15 )'
# energyfraction=0.5              # doesn't do anything
# bkgfraction=0.5

# relaxed condition: it's ok because the cluster related spurioous are
# hard removed from emllist
# 5.92 -> 3 sigma:, 4: 9.7, 4.5: 11.9
expression='(DIST_NN >= 10.0)&&(FLUX >= 0.5e-15)&&(ID_INST == 0)&&(ID_BAND == 0)&&(DET_ML >= 5.92 )'
energyfraction=0.5              # doesn't do anything
bkgfraction=0.2                 # higher value lower removal radius

######################################################################
# m1

export prefix=$M1_EV_PREFIX_LIST


if [[ $MAKE_NEW_SKY_REG -eq 1 ]]
then

    region eventset=mos${prefix}-clean.fits operationstyle=global srclisttab=emllist-man.fits:SRCLIST expression="$expression" bkgregionset=mos${prefix}-bkg_region-det.fits energyfraction=$energyfraction radiusstyle=enfrac outunit=detxy verbosity=1

    region eventset=mos${prefix}-clean.fits operationstyle=global srclisttab=emllist-man.fits:SRCLIST expression="$expression" bkgregionset=mos${prefix}-bkg_region-sky.fits radiusstyle=contour bkgratestyle=col nosrcellipse=yes bkgfraction=$bkgfraction outunit=xy verbosity=1

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

    region eventset=mos${prefix}-clean.fits operationstyle=global srclisttab=emllist-man.fits:SRCLIST expression="$expression" bkgregionset=mos${prefix}-bkg_region-det.fits energyfraction=$energyfraction radiusstyle=enfrac outunit=detxy verbosity=1

    region eventset=mos${prefix}-clean.fits operationstyle=global srclisttab=emllist-man.fits:SRCLIST expression="$expression" bkgregionset=mos${prefix}-bkg_region-sky.fits radiusstyle=contour bkgratestyle=col nosrcellipse=yes bkgfraction=$bkgfraction outunit=xy verbosity=1

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

    region eventset=pn${prefix}-clean.fits operationstyle=global srclisttab=emllist-man.fits:SRCLIST expression="$expression" bkgregionset=pn${prefix}-bkg_region-det.fits energyfraction=$energyfraction radiusstyle=enfrac outunit=detxy verbosity=1

    region eventset=pn${prefix}-clean.fits operationstyle=global srclisttab=emllist-man.fits:SRCLIST expression="$expression" bkgregionset=pn${prefix}-bkg_region-sky.fits radiusstyle=contour bkgratestyle=col nosrcellipse=yes bkgfraction=$bkgfraction outunit=xy verbosity=1

fi

make_mask inimage=pn${prefix}-obj-im.fits \
inmask=pn${prefix}-mask-im.fits \
outmask=pn${prefix}-cheese.fits \
reglist=pn${prefix}-bkg_region-sky.fits


######################################################################
# create a reg file if you can

# scriptdir=~/data1/sw/scripts/

if [[ -e ${codedir}/utils/fcat2reg.sh  ]]
then
    fcat2reg.sh emllist-man.fits 10.0 ML_ID_SRC
fi

######################################################################
# masked images for debug

if [[ $DEBUG_CHEESE_IM -eq 1 ]]
then
    inimage=pn${prefix}-obj-im.fits
    outmask=pn${prefix}-cheese.fits
    outimage=pn${prefix}-cheeseim.fits

    farith $outmask $inimage $outimage MUL clobber=yes
fi

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0