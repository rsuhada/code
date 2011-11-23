######################################################################
# script extracting vignetted and unvignetted exposure maps for the
# imaging pipe

dir=$1
here=`pwd`
cd $dir

######################################################################
# do the extraction: 0.5-2 keV band

elo="500"
ehi="2000"


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

    outexp=mos${prefix}-${elo}-${ehi}.uv.exp
    eexpmap imageset=${image} attitudeset=atthk.fits \
        eventset=${evli}:EVENTS expimageset=${outexp} \
        withdetcoords=no withvignetting=no usefastpixelization=no \
        usedlimap=no attrebin=4 pimin=${elo} pimax=${ehi}
done


for prefix in $PN_EV_PREFIX_LIST
do
    image=pn${prefix}-${elo}-${ehi}.im
    evli=pn${prefix}-clean.fits

    if [[ ! -e $image ]]
    then
        echo -e "$image does not exists here! Creating it!"
        ${codedir}/imaging/make-ims.sh .
    fi

    outexp=pn${prefix}-${elo}-${ehi}.exp
    eexpmap imageset=${image} attitudeset=atthk.fits \
        eventset=${evli}:EVENTS expimageset=${outexp} \
        withdetcoords=no withvignetting=yes usefastpixelization=no \
        usedlimap=no attrebin=4 pimin=${elo} pimax=${ehi}

    outexp=pn${prefix}-${elo}-${ehi}.uv.exp
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
