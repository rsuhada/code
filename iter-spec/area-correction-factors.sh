######################################################################
# calculate area correction factors due to point source removal,
# chipgaps etc. for given existing EPIC image.

source ${codedir}/utils/util-funcs-lib.sh

######################################################################
# setup SAS

here=`pwd`                      # should be cluster/iter-spec/iteration

SETUP_SAS=1                     # should I set SAS path? 0 - no, use
                                # current setting
aperture=80.0                   # [ pix ]
MAKE_EXP_MAP=1                  # create exposure maps? 0 - no they
                                # already exist (debugging)

EVLI_DIR=${workdir}             # dir with filtered eventlists

if [[ $# -ge 1 ]]
then
    SETUP_SAS=$2
    aperture=$3
fi

if [[ ${SETUP_SAS} -eq 1 ]]
then
    echo "setting custom paths..."
    # this part might need manual settings!
    export EVLI_DIR=../../analysis
    export SAS_ODF=../../analysis/odf
    export SAS_CCF=../../analysis/ccf.cif

    export codedir="/Users/rs/data1/sw/esaspi"
    export esas_caldb="/Users/rs/calib/esas"

    export SAS_DIR="/Users/rs/data1/sw/sas-11.0.0/xmmsas_20110223_1803"
    export SAS_PATH="/Users/rs/data1/sw/sas-11.0.0/xmmsas_20110223_1803"
    export SAS_CCFPATH="/Users/rs/calib/xmm/ccf/"
    export SAS_MEMORY_MODEL=high
    export SAS_VERBOSITY=4
fi

sasversion

######################################################################
# satup parameterss

elo="500"                       # band is not crucial for our purposes
ehi="2000"
emask_thresh1=0.01              # [ defailt = 0.1 ]
MAN_PS_REG=`ls ps-man*.im.reg`

if [[ ! -e $MAN_PS_REG ]]
then
    echo -e "\n** error: $MAN_PS_REG does not exists in $here!"
    echo -e "*** error in $0\n"
    cd $startdir
    exit 1
fi

######################################################################
# get the exposure maps

for instrument in m1 m2 pn
do
    echo "working on instrument : " $instrument

    # FIXME: assumes that the keyword is on a single line (should be OK)
    image=`ls ${instrument}-*.im`
    evli=`fkeyprint ${image}+0 XPROC0 | grep -o "table=[^ ]*" | sed 's/table=//g'`
    evli=${EVLI_DIR}/${evli##*/}   # strips possible path and adds the correct one

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
    outexp_wps=${image%.*}.wps,exp

    ######################################################################
    # make exposure map
    if [[ $MAKE_EXP_MAP -eq 1 ]]
    then
        eexpmap imageset=${image} attitudeset=${EVLI_DIR}/atthk.fits \
            eventset=${evli}:EVENTS expimageset=${outexp_wps} \
            withdetcoords=no withvignetting=yes usefastpixelization=no \
            usedlimap=no attrebin=4 pimin=${elo} pimax=${ehi}
    fi

    ######################################################################
    # create a fits reg file for ps-masking
    # need to remove the negative sign in front of the shape
    sed -i .sed.bk 's/-circle/circle/g' $MAN_PS_REG
    rm ${MAN_PS_REG}.sed.bk
    ds9tocxc outset=${MAN_PS_REG}.fits < ${MAN_PS_REG}

    ######################################################################
    # create the mask
    outmask=${image%.*},mask
    emask expimageset=$outexp_wps detmaskset=$outmask threshold1=$emask_thresh1 regionset=${MAN_PS_REG}.fits

    farith $outexp $outexp_wps $outmask MUL clobber=yes

    ######################################################################
    # get the correcton factors

    image=${image}
    expmap=${outexp}
    bgmap=${outmask}            # irrelevant here: dummy

    pars=(X_IM Y_IM)
    out=`get_cluster_pars $pars`
    xim=`echo $out | awk '{print $1}'`
    yim=`echo $out | awk '{print $2}'`

    ${codedir}/sb/get_cts_stat_aper.py $image $xim $yim $aperture $bgmap


done

######################################################################
# exit

echo -e "\n$0 in $obsid done!"
exit 0
