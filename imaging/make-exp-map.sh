######################################################################
# script extracting vignetted and unvignetted exposure maps and
# detection masks for the imaging pipe

dir=$1
here=`pwd`
cd $dir

######################################################################
# do the extraction: 0.5-2 keV band

elo="500"
ehi="2000"

MAN_PS_REG_PHYS=ps-man.phy.reg
MAN_PS_REG=ps-man.im.reg

######################################################################
# prepare the region file with the point sources

if [[ -e $MAN_PS_REG_PHYS ]]
then

    if [[ ! -e $image ]]
    then
        echo -e "$image does not exists here! Creating it!"
        ${codedir}/imaging/make-ims.sh .
    fi

    # convert the region in physical coords to image coords
    image=pn${PN_EV_PREFIX_LIST}-${elo}-${ehi}.im
    ${codedir}/utils/convert-wcs2im-ds9.sh $image $MAN_PS_REG_PHYS

    # need to remove the negative sign in front of the shape
    sed -i .sed.bk 's/-circle/circle/g' $MAN_PS_REG
    rm ${MAN_PS_REG}.sed.bk
    ds9tocxc outset=${MAN_PS_REG}.fits < ${MAN_PS_REG}

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
	emask expimageset=$outexp detmaskset=$outmask threshold1=0.1 regionset=${MAN_PS_REG}.fits

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
    image=mos${prefix}-obj-im-400-1250-full.fits
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
	emask expimageset=$outexp detmaskset=$outmask threshold1=0.1 regionset=${MAN_PS_REG}.fits

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
