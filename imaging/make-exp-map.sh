######################################################################
# script extracting vignetted and unvignetted exposure maps and
# detection masks for the imaging pipe

dir=$1
here=`pwd`
cd $dir

######################################################################
# do the extraction: 0.5-2 keV band

elo=$2
ehi=$3
emask_thresh1=0.01              # [ defailt = 0.1 ]

REMOVE_CLUSTER=0                # should I mask out the cluster?

# FIXME: file names shouldn't be hardcoded!
# MAN_PS_REG_PHYS=ps-man-01.phy.reg
# MAN_PS_REG=ps-man-01.im.reg

MAN_PS_REG_PHYS=${MAN_PS_REG_ID}.phy.reg
MAN_CLUSTER_REG_PHYS=${MAN_CLUSTER_REG_ID}.phy.reg
MAN_PS_REG=${MAN_PS_REG_ID}.im.reg
EMASK_REG=${MAN_PS_REG_ID}-${MAN_CLUSTER_REG_ID}.im.reg

######################################################################
# prepare the region file with the point sources

if [[ -e $MAN_PS_REG_PHYS ]]
then
    image=pn${PN_EV_PREFIX_LIST}-${elo}-${ehi}.im

    if [[ ! -e $image ]]
    then
        echo -e "$image does not exists here! Creating it!"
        ${codedir}/imaging/make-ims.sh .
    fi

    # convert the region in physical coords to image coords
    ${codedir}/utils/convert-wcs2im-ds9.sh $image $MAN_PS_REG_PHYS

    # need to remove the negative sign in front of the shape
    sed 's/-circle/circle/g' $MAN_PS_REG > $EMASK_REG

    # remove also the cluster region if present
    if [[ (-e $MAN_CLUSTER_REG_PHYS) && ($REMOVE_CLUSTER -eq 1)  ]]
    then
        ${codedir}/utils/convert-wcs2im-ds9.sh $image $MAN_CLUSTER_REG_PHYS
        grep circle ${MAN_CLUSTER_REG_ID}.im.reg >> $EMASK_REG
    fi

    ds9tocxc outset=${EMASK_REG}.fits < ${EMASK_REG}

else
    echo -e "\n** error: $MAN_PS_REG_PHYS does not exists here!"
    echo -e "*** error in $0\n"
    cd $startdir
    exit 1
fi

######################################################################
# pn

for prefix in $PN_EV_PREFIX_LIST
do
    image=pn${prefix}-${elo}-${ehi}.im
    evli=pn${prefix}-clean.fits

    outexp=pn${prefix}-${elo}-${ehi}.exp

    eexpmap imageset=${image} attitudeset=atthk.fits \
        eventset=${evli}:EVENTS expimageset=${outexp} \
        withdetcoords=no withvignetting=yes usefastpixelization=no \
        usedlimap=no attrebin=4 pimin=${elo} pimax=${ehi}

    outmask=pn${prefix}-${elo}-${ehi}.mask
	emask expimageset=$outexp detmaskset=$outmask threshold1=$emask_thresh1 regionset=${EMASK_REG}.fits
	emask expimageset=$outexp detmaskset=${outmask}.wps threshold1=$emask_thresh1

    outexp=pn${prefix}-${elo}-${ehi}.uv.exp

    eexpmap imageset=${image} attitudeset=atthk.fits \
        eventset=${evli}:EVENTS expimageset=${outexp} \
        withdetcoords=no withvignetting=no usefastpixelization=no \
        usedlimap=no attrebin=4 pimin=${elo} pimax=${ehi}

done

######################################################################
# m1 + m2

for prefix in $MOS_EV_PREFIX_LIST
do
    image=mos${prefix}-${elo}-${ehi}.im
    evli=mos${prefix}-clean.fits

    if [[ ! -e $image ]]
    then
        echo -e "$image does not exists here! Creating it!"
        ${codedir}/imaging/make-ims.sh .
    fi

    outexp=mos${prefix}-${elo}-${ehi}.exp

    eexpmap imageset=${image} attitudeset=atthk.fits \
        eventset=${evli}:EVENTS expimageset=${outexp} \
        withdetcoords=no withvignetting=yes usefastpixelization=no \
        usedlimap=no attrebin=4 pimin=${elo} pimax=${ehi}

    outmask=mos${prefix}-${elo}-${ehi}.mask
	emask expimageset=$outexp detmaskset=$outmask threshold1=$emask_thresh1 regionset=${EMASK_REG}.fits
	emask expimageset=$outexp detmaskset=${outmask}.wps threshold1=$emask_thresh1

    outexp=mos${prefix}-${elo}-${ehi}.uv.exp

    eexpmap imageset=${image} attitudeset=atthk.fits \
        eventset=${evli}:EVENTS expimageset=${outexp} \
        withdetcoords=no withvignetting=no usefastpixelization=no \
        usedlimap=no attrebin=4 pimin=${elo} pimax=${ehi}

done

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0