######################################################################
# script calculating a model background image - spline version using
# the setup emplyed by the 2xmm team - well tested but not necessarily
# optimal for faint clusters
#
# NOTE: scut=0.002 (2xmmi default) makes huge exclusion radia, leaving
# little are for fit. 0.01 is default for esas, which seems to make
# bit too small holes. Truth somewhere between?

dir=$1
here=`pwd`
cd $dir

######################################################################
# input parameters

elo="500"
ehi="2000"

USE_OOT=0                       # use the oot correction for pn? using
                                # it causes some small (maybe
                                # negligible) artefacts

srclist=emllist-man.fits

if [[ ! -e $srclist ]]
then
    echo -e "\n** warning: $srclist does not exists here!"
    echo -e "*** Will use the automatic $srclist\n"
    srclist=emllist.fits
fi

    srclist=boxlist.fits

######################################################################
# do the extraction: 0.5-2 keV band

for prefix in $MOS_EV_PREFIX_LIST
do
    image=mos${prefix}-${elo}-${ehi}.im
    vexp=mos${prefix}-${elo}-${ehi}.exp
    uvexp=mos${prefix}-${elo}-${ehi}.uv.exp
    mask=mos${prefix}-${elo}-${ehi}.mask
    outbg=mos${prefix}-${elo}-${ehi}.spl.bg
    outcheese=mos${prefix}-${elo}-${ehi}.spl.cheese

    if [[ ! -e $vexp ]]
    then
        echo -e "$vexp does not exists here! Creating it!"
        ${codedir}/imaging/make-exp-map.sh .
    fi

    esplinemap boxlistset=$srclist \
	    withdetmask=yes detmaskset=$mask \
	    withexpimage=yes withexpimage2=no \
        expimageset=$uvexp \
	    imageset=$image \
	    pimin=$elo pimax=$ehi \
	    bkgimageset=$outbg \
	    withcheese=yes withcheesemask=yes \
	    cheesemaskset=$outcheese \
        withootset=false \
        scut=0.002 \
        fitmethod=spline \
        nsplinenodes=13 \
        excesssigma=3.0 \
        nfitrun=4

        # 2xmm uses the flat exposure map here
        # not used:
        #    nsplinenodes=12 \
        #    excesssigma=2.5 \
        #    withootset='true' \
        #    mlmin=1.0 \

done

for prefix in $PN_EV_PREFIX_LIST
do

    ooteventset=pn${prefix}-clean-oot.fits
    image=pn${prefix}-${elo}-${ehi}.im
    vexp=pn${prefix}-${elo}-${ehi}.exp
    uvexp=pn${prefix}-${elo}-${ehi}.uv.exp
    mask=pn${prefix}-${elo}-${ehi}.mask
    outbg=pn${prefix}-${elo}-${ehi}.spl.bg
    outcheese=pn${prefix}-${elo}-${ehi}.spl.cheese

    if [[ ! -e $vexp ]]
    then
        echo -e "$vexp does not exists here! Creating it!"
        ${codedir}/imaging/make-exp-map.sh .
    fi

    if [[ $USE_OOT -eq 1 ]]
    then

        # 2xmm use oot here, but it leaves strange residuals - some
        # can be masked out but still the bg has visible tiny stripy
        # artefacts
        esplinemap boxlistset=$srclist \
	        withdetmask=yes detmaskset=$mask \
	        withexpimage=yes withexpimage2=no \
	        expimageset=$uvexp \
	        imageset=$image \
	        pimin=$elo pimax=$ehi \
	        bkgimageset=$outbg \
	        withcheese=yes withcheesemask=yes \
	        cheesemaskset=$outcheese \
            withootset=true \
            ooteventset=$ooteventset \
            scut=0.002 \
            fitmethod=spline \
            nsplinenodes=13 \
            excesssigma=3.0 \
            nfitrun=4

        # SAS leaves some residuals pixels that shouldn't be there
        farith $outbg ${mask}\[1\] farith-tmp.fits \* clobber=yes
        mv farith-tmp.fits $outbg

    else

        esplinemap boxlistset=$srclist \
	        withdetmask=yes detmaskset=$mask \
	        withexpimage=yes withexpimage2=no \
	        expimageset=$uvexp \
	        imageset=$image \
	        pimin=$elo pimax=$ehi \
	        bkgimageset=$outbg \
	        withcheese=yes withcheesemask=yes \
	        cheesemaskset=$outcheese \
            scut=0.002 \
            fitmethod=spline \
            nsplinenodes=13 \
            excesssigma=3.0 \
            nfitrun=4

    fi

    # withootset=true \
    #     ooteventset=$ooteventset \

    # 2xmm uses the flat exposure map here also uses oot - this makes
    # strage stripe residuals - tiny but look arficial
    #
    # not used:
    #    nsplinenodes=12 \
    #    excesssigma=2.5 \
    #    withootset='true' \
    #    mlmin=1.0 \

done

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0
