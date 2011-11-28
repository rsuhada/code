######################################################################
# script calculating a model background image - 2 component (vignetted
# + unvignetted template)

dir=$1
here=`pwd`
cd $dir

######################################################################
# input parameters

elo="500"
ehi="2000"

# emledetextsrclist causes segfault now... so using lower level
# eboxdetect src list
# srclist=emllist-man.fits
# if [[ ! -e $srclist ]]
# then
#     echo -e "\n** warning: $srclist does not exists here!"
#     echo -e "*** Will use the automatic $srclist\n"
#     srclist=emllist.fits
# fi

srclist=boxlist.fits

######################################################################
# do the extraction: 0.5-2 keV band

for prefix in $MOS_EV_PREFIX_LIST
do
    image=mos${prefix}-${elo}-${ehi}.im
    vexp=mos${prefix}-${elo}-${ehi}.exp
    uvexp=mos${prefix}-${elo}-${ehi}.uv.exp
    mask=mos${prefix}-${elo}-${ehi}.mask
    outbg=mos${prefix}-${elo}-${ehi}.bg
    outcheese=mos${prefix}-${elo}-${ehi}.cheese

    if [[ ! -e $vexp ]]
    then
        echo -e "$vexp does not exists here! Creating it!"
        ${codedir}/imaging/make-exp-map.sh .
    fi

    esplinemap boxlistset=$srclist \
	    withdetmask=yes detmaskset=$mask \
	    fitmethod=model withexpimage=yes withexpimage2=yes \
	    expimageset=$vexp expimageset2=$uvexp \
	    imageset=$image \
	    scut=0.002 withootset=no pimin=$elo pimax=$ehi \
	    bkgimageset=$outbg \
	    withcheese=yes withcheesemask=yes \
	    cheesemaskset=$outcheese
done

for prefix in $PN_EV_PREFIX_LIST
do
    image=pn${prefix}-${elo}-${ehi}.im
    vexp=pn${prefix}-${elo}-${ehi}.exp
    uvexp=pn${prefix}-${elo}-${ehi}.uv.exp
    mask=pn${prefix}-${elo}-${ehi}.mask
    outbg=pn${prefix}-${elo}-${ehi}.bg
    outcheese=pn${prefix}-${elo}-${ehi}.cheese

    if [[ ! -e $vexp ]]
    then
        echo -e "$vexp does not exists here! Creating it!"
        ${codedir}/imaging/make-exp-map.sh .
    fi

    esplinemap boxlistset=$srclist \
	    withdetmask=yes detmaskset=$mask \
	    fitmethod=model withexpimage=yes withexpimage2=yes \
	    expimageset=$vexp expimageset2=$uvexp \
	    imageset=$image \
	    scut=0.002 withootset=no pimin=$elo pimax=$ehi \
	    bkgimageset=$outbg \
	    withcheese=yes withcheesemask=yes \
	    cheesemaskset=$outcheese
done

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0
