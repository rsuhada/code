######################################################################
# script calculating a model background image - 2 component (vignetted
# + unvignetted template)

dir=$1
here=`pwd`
cd $dir

######################################################################
# input parameters

elo=$2
ehi=$3

# original: excesssigma=3 mlmin=1 since it should be run with ps
# alredy masked out the threshold can be increased (even up to point
# to not remove anything additional) mlmin=20 & excesssigma=5 gives
# essentially the esas result, while scut=0.002 is bit more
# conservative (esp. for bright sources) - that's good

mlmin=10.0
excesssigma=5.0
scut=0.002

# this set gives the esas region - might not be enough for the cluster itself!
# mlmin=20.0
# excesssigma=5.0
# scut=0.002

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

# FIXME: add wps bg?
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
	    scut=$scut withootset=no pimin=$elo pimax=$ehi \
	    bkgimageset=$outbg \
	    withcheese=yes withcheesemask=yes \
        excesssigma=$excesssigma \
        mlmin=$mlmin \
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
	    scut=$scut withootset=no pimin=$elo pimax=$ehi \
	    bkgimageset=$outbg \
	    withcheese=yes withcheesemask=yes \
        excesssigma=$excesssigma \
        mlmin=$mlmin \
	    cheesemaskset=$outcheese
done

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0
