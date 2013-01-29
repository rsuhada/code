######################################################################
# calculate area correction factors due to point source removal,
# chipgaps etc. for given existing EPIC image.

source ${codedir}/utils/util-funcs-lib.sh

######################################################################
# setup SAS

here=`pwd`                      # should be cluster/iter-spec/iteration
MAKE_EXP_MAP=1                  # create exposure maps? 0 - no they
                                # already exist (debugging)

aperture1="$1"
aperture2="$2"                  # for annulus (EXCLUDE_CORE = 1)

######################################################################
# satup parameterss

elo="500"                       # band is not crucial for our purposes
ehi="2000"
emask_thresh1=0.01              # [ defailt = 0.1 ]
areacorrection_file=area_correction.txt

MAN_PS_REG=`ls ps-man*.im.reg`

if [[ ! -e $MAN_PS_REG ]]
then
    echo -e "\n** error: region $MAN_PS_REG does not exists in $here!"
    echo -e "*** error in $0\n"
    cd $startdir
    exit 1
fi

rm $areacorrection_file 2>/dev/null

######################################################################
# get the exposure maps

for instrument in m1 m2 pn
do
    echo "working on instrument : " $instrument

    # FIXME: assumes that the keyword is on a single line (should be OK)
    image=`ls ${instrument}-*.im | grep -v specband`
    evli=`fkeyprint ${image}+0 XPROC0 | grep -o "table=[^ ]*" | sed 's/table=//g'`
    evli=${startdir}/${ANALYSIS_DIR}/analysis/${evli##*/}   # strips possible path and adds the correct one

    if [[ ! -e $evli ]]
    then
        echo -e "\n** error: $evli does not exists!"

        echo -e "\n* Either path is set wronly or check ${image}"
        echo -e "whether table= is not split to several lines. If yes edit $0"
        echo -e "and hardcode evenlist path"

        echo -e "*** error in $0\n"

        exit 1
    fi

    outexp=${image%.*}.exp
    outexp_wps=${image%.*}.wps.exp

    ######################################################################
    # make exposure map
    if [[ $MAKE_EXP_MAP -eq 1 ]]
    then
        eexpmap imageset=${image} attitudeset=${startdir}/${ANALYSIS_DIR}/analysis/atthk.fits \
            eventset=${evli}:EVENTS expimageset=${outexp_wps} \
            withdetcoords=no withvignetting=yes usefastpixelization=no \
            usedlimap=no attrebin=4 pimin=${elo} pimax=${ehi}
    fi

    ######################################################################
    # create a fits reg file for ps-masking
    # need to remove the negative sign in front of the shape
    sed -i.sed.bk 's/-circle/circle/g' $MAN_PS_REG
    rm ${MAN_PS_REG}.sed.bk
    ds9tocxc outset=${MAN_PS_REG}.fits < ${MAN_PS_REG}

    ######################################################################
    # create the mask
    outmask=${image%.*}.mask
    emask expimageset=$outexp_wps detmaskset=$outmask threshold1=$emask_thresh1 regionset=${MAN_PS_REG}.fits

    ######################################################################
    # exposure maps are not strictly needed here, but its easier to
    # supply them to python then the mask (where data is in
    # 2. extension)

    # ftools can't handle dash in file name
    cp $outexp_wps exp.tmp.fits
    cp $outmask mask.tmp.fits

    farith exp.tmp.fits mask.tmp.fits+1 out.tmp.fits MUL clobber=yes

    mv out.tmp.fits $outexp
    rm exp.tmp.fits mask.tmp.fits

    ######################################################################
    # get the correcton factors

    image=${image}
    bgmap=${outexp}            # irrelevant here - just need the
                               # correct mask area

    pars=(X_IM Y_IM)
    out=`get_cluster_pars $pars`
    xim=`echo $out | awk '{print $1}'`
    yim=`echo $out | awk '{print $2}'`


    if [[ $EXCLUDE_CORE -eq 0 ]]
    then

        aperture1_im=`arcsec_2_impix_xmm $image $aperture1`

        echo "Getting area correction for non-core excised image"
        ${PYTHONEXEC} ${codedir}/sb/get_cts_stat_aper.py $image $xim $yim $aperture1_im $bgmap > ${image%.*} > ${image%.*}-areacorr.txt

    else

        aperture1_im=`arcsec_2_impix_xmm $image $aperture1`
        aperture2_im=`arcsec_2_impix_xmm $image $aperture2`

        echo "Getting area correction for core excised image"
        ${PYTHONEXEC} ${codedir}/sb/get_cts_stat_aper_annul.py $image $xim $yim $aperture1_im $aperture2_im $bgmap > ${image%.*} > ${image%.*}-areacorr.txt

    fi

    acorr=`grep -i "area correction factor" ${image%.*}-areacorr.txt | awk '{print $5}'`
    echo $instrument $acorr >> ${areacorrection_file}
done

######################################################################
# exit

echo -e "\n$0 in $obsid done!"
exit 0

