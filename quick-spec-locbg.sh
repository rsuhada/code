######################################################################
# preliminary script for extraction of files for spectral analysis
# uses very standard and simple local bg approach
# requires double cleaned eventlist and defined extraction regions

dir=$1
here=`pwd`
cd $dir

specdir=../spec

# FIXME: available in a standalone script - this function is redundant
function get_cluster_pars {

    ######################################################################
    # looks through an analysis notebook file returning the requested
    # parameters. Input is an array, e.g.  pars=(RA DE RA60
    # DE60 X_IM Y_IM X_PHY Y_PHY NH REDSHIFT), output is a string

    if [[ -e $NOTESFILE ]]
    then

        pars=$1
        declare -a values

        for i in ${!pars[@]}
        do
            val=`grep ${pars[i]} $NOTESFILE | head -1 | awk '{print $2}'`
            values=( "${values[@]}" "$val" )
            # echo ${pars[i]} ${values[i]}
        done

        # this is the output
        echo ${values[@]}

    else
        echo "$NOTESFILE does not exist, not returning parameters!"
    fi
}

######################################################################
# settings

ra=$2
de=$3

EXTRACT_SRC=0
EXTRACT_BG=1

MAKE_RMF=0
MAKE_ARF=0

MAKE_RMF_BG=0
MAKE_ARF_BG=0

CALCULATE_BACKSCALE=1

# # 0205
# SRC_REGION=cluster-man-01.phy.reg
# BG_REGION=bg-ann-06.phy.reg
# PS_REGION=ps-man-02.phy.reg

# 0559
SRC_REGION=cluster-man-02.phy.reg
BG_REGION=bg-ann-03.phy.reg
PS_REGION=ps-man-03.phy.reg

######################################################################
# create the spectroscopy dir if it does not exists

mkdir -p ${specdir}/conf 2> /dev/null

config_file=${specdir}/conf/${CLNAME}-par-qspec-001.conf

if [[ ! -e $config_file ]]
then
    cp ${codedir}/templates/template-par-qspec-001.conf $config_file

    if [[ -e $NOTESFILE ]]
    then

        pars=(REDSHIFT NH)
        out=`get_cluster_pars $pars`
        tmp_redshift=`echo $out | awk '{print $1}'`
        tmp_nh=`echo $out | awk '{print $2}'`

        sed -i .sed.bk "s/PLACEHOLDER_REDSHIFT/${tmp_redshift}/g" $config_file
        sed -i .sed.bk "s/PLACEHOLDER_NH/${tmp_nh}/g" $config_file
        rm ${config_file}.sed.bk

    fi
fi

if [[ ! -e ${specdir}/conf/${CLNAME}-par-qspec-001.results ]]
then
    cp ${codedir}/templates/template-par-qspec-001.results ${specdir}/conf/${CLNAME}-par-qspec-001.results
fi

######################################################################
# check existence of region files

if [[ ! -e $SRC_REGION ]]
then
    echo -e "\n** error: $SRC_REGION does not exists here!"
    echo -e "*** error in $0\n"
    cd $startdir
    exit 1
fi

if [[ ! -e $BG_REGION ]]
then
    echo -e "\n** error: $BG_REGION does not exists here!"
    echo -e "*** error in $0\n"
    cd $startdir
    exit 1
fi

if [[ ! -e $PS_REGION ]]
then
    echo -e "\n** error: $PS_REGION does not exists here!"
    echo -e "*** error in $0\n"
    cd $startdir
    exit 1
fi

cp $SRC_REGION $BG_REGION $PS_REGION $specdir
bgid=`echo $BG_REGION | sed 's/\..*//g'`

######################################################################
# parse the region files, second parameter equals 0 means region file
# will be removed

# FIXME: available as a util function
parse-spec-reg.sh $SRC_REGION 1
parse-spec-reg.sh $BG_REGION 1
parse-spec-reg.sh $PS_REGION 0

######################################################################
# prepare the region descriptors

inpattern=`cat ${PS_REGION}.desc`
psreg="$inpattern"

inpattern=`cat ${SRC_REGION}.desc`
srcreg="$inpattern"

inpattern=`cat ${BG_REGION}.desc`
bgreg="$inpattern"

# original

# mospattern="#XMMEA_EM && ((FLAG & 0x10000) == 0) && (FLAG == 0) && (PATTERN<=12) && (PI in [100:10000])"
# pnpattern="((FLAG & 0x10000) == 0) && (FLAG == 0) && (PATTERN<=4) && (PI in [100:10000])"

# esas

mospattern="(FLAG == 0) && (PATTERN<=12) && (PI in [100:10000])"
pnpattern="(FLAG == 0) && (PATTERN<=4) && (PI in [100:10000])"

if [[ $EXTRACT_SRC -ne 0 ]]
then

######################################################################
#  get m1 spectra

    echo -e '\nGetting m1 spectra...'

    mosexpr="$mospattern && $srcreg $psreg"
    prefix=$M1_EV_PREFIX_LIST
    evlist=mos${prefix}-clean.fits

    evselect table=${evlist} withimageset=yes imageset=${specdir}/m1.im \
        xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
        yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
        withspectrumset=true spectrumset=${specdir}/m1.pha \
        withspecranges=true energycolumn=PI specchannelmin=0 \
        specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
        writedss=Y expression="$mosexpr"

    # detector map file for arfgen
    evselect table=${evlist} withimageset=yes imageset=m1-detmap.ds \
        xcolumn=DETX ycolumn=DETY imagebinning=binSize ximagebinsize=80 \
        yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
        withspectrumset=true spectrumset=${specdir}/m1.pha \
        withspecranges=true energycolumn=PI specchannelmin=0 \
        specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
        writedss=Y expression="$mosexpr"

######################################################################
#  get m2 spectra

    echo -e '\nGetting m2 spectra...'

    mosexpr="$mospattern && $srcreg $psreg"
    prefix=$M2_EV_PREFIX_LIST
    evlist=mos${prefix}-clean.fits

    evselect table=${evlist} withimageset=yes imageset=${specdir}/m2.im \
        xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
        yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
        withspectrumset=true spectrumset=${specdir}/m2.pha \
        withspecranges=true energycolumn=PI specchannelmin=0 \
        specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
        writedss=Y expression="$mosexpr"

    # detector map file for arfgen
    evselect table=${evlist} withimageset=yes imageset=m2-detmap.ds \
        xcolumn=DETX ycolumn=DETY imagebinning=binSize ximagebinsize=80 \
        yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
        withspectrumset=true spectrumset=${specdir}/m2.pha \
        withspecranges=true energycolumn=PI specchannelmin=0 \
        specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
        writedss=Y expression="$mosexpr"

######################################################################
#  get pn spectra

    echo -e '\nGetting pn spectra...'

    pnexpr="$pnpattern && $srcreg $psreg"
    prefix=$PN_EV_PREFIX_LIST
    evlist=pn${prefix}-clean.fits

    evselect table=${evlist} withimageset=yes imageset=${specdir}/pn.im \
        xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
        yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
        withspectrumset=true spectrumset=${specdir}/pn.pha \
        withspecranges=true energycolumn=PI specchannelmin=0 \
        specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
        writedss=Y expression="$pnexpr"

    # detector map file for arfgen
    evselect table=${evlist} withimageset=yes imageset=pn-detmap.ds \
        xcolumn=DETX ycolumn=DETY imagebinning=binSize ximagebinsize=80 \
        yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
        withspectrumset=true spectrumset=${specdir}/pn.pha \
        withspecranges=true energycolumn=PI specchannelmin=0 \
        specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
        writedss=Y expression="$pnexpr"

######################################################################
#  get pn oot spectra

    echo -e '\nGetting pn spectra...'

    pnexpr="$pnpattern && $srcreg $psreg"
    prefix=$PN_EV_PREFIX_LIST
    evlist=pn${prefix}-clean-oot.fits

    evselect table=${evlist} withimageset=yes imageset=${specdir}/pn-oot.im \
        xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
        yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
        withspectrumset=true spectrumset=${specdir}/pn-oot.pha \
        withspecranges=true energycolumn=PI specchannelmin=0 \
        specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
        writedss=Y expression="$pnexpr"

    # # detector map file for arfgen
    # evselect table=${evlist} withimageset=yes imageset=pn-oot-detmap.ds \
    #     xcolumn=DETX ycolumn=DETY imagebinning=binSize ximagebinsize=80 \
    #     yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
    #     withspectrumset=true spectrumset=${specdir}/pn-oot.pha \
    #     withspecranges=true energycolumn=PI specchannelmin=0 \
    #     specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
    #     writedss=Y expression="$pnexpr"

fi

if [[ $EXTRACT_BG -ne 0 ]]
then

######################################################################
#  get m1 background spectra

    echo -e '\nGetting m1 background spectra...'

    mosexpr="$mospattern && $bgreg $psreg"
    prefix=$M1_EV_PREFIX_LIST
    evlist=mos${prefix}-clean.fits

    evselect table=${evlist} withimageset=yes imageset=${specdir}/m1-${bgid}.im \
        xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
        yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
        withspectrumset=true spectrumset=${specdir}/m1-${bgid}.pha \
        withspecranges=true energycolumn=PI specchannelmin=0 \
        specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
        writedss=Y expression="$mosexpr"

    # detector map file for arfgen
    evselect table=${evlist} withimageset=yes imageset=m1-${bgid}-detmap.ds \
        xcolumn=DETX ycolumn=DETY imagebinning=binSize ximagebinsize=80 \
        yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
        withspectrumset=true spectrumset=${specdir}/m1-${bgid}.pha \
        withspecranges=true energycolumn=PI specchannelmin=0 \
        specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
        writedss=Y expression="$mosexpr"

######################################################################
#  get m2 background spectra

    echo -e '\nGetting m2 background spectra...'

    mosexpr="$mospattern && $bgreg $psreg"
    prefix=$M2_EV_PREFIX_LIST
    evlist=mos${prefix}-clean.fits

    evselect table=${evlist} withimageset=yes imageset=${specdir}/m2-${bgid}.im \
        xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
        yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
        withspectrumset=true spectrumset=${specdir}/m2-${bgid}.pha \
        withspecranges=true energycolumn=PI specchannelmin=0 \
        specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
        writedss=Y expression="$mosexpr"

    # detector map file for arfgen
    evselect table=${evlist} withimageset=yes imageset=m2-${bgid}-detmap.ds \
        xcolumn=DETX ycolumn=DETY imagebinning=binSize ximagebinsize=80 \
        yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
        withspectrumset=true spectrumset=${specdir}/m2-${bgid}.pha \
        withspecranges=true energycolumn=PI specchannelmin=0 \
        specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
        writedss=Y expression="$mosexpr"


######################################################################
#  get pn background spectra

    echo -e '\nGetting pn background spectra...'

    pnexpr="$pnpattern && $bgreg $psreg"
    prefix=$PN_EV_PREFIX_LIST
    evlist=pn${prefix}-clean.fits

    evselect table=${evlist} withimageset=yes imageset=${specdir}/pn-${bgid}.im \
        xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
        yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
        withspectrumset=true spectrumset=${specdir}/pn-${bgid}.pha \
        withspecranges=true energycolumn=PI specchannelmin=0 \
        specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
        writedss=Y expression="$pnexpr"

    # detector map file for arfgen
    evselect table=${evlist} withimageset=yes imageset=pn-${bgid}-detmap.ds \
        xcolumn=DETX ycolumn=DETY imagebinning=binSize ximagebinsize=80 \
        yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
        withspectrumset=true spectrumset=${specdir}/pn-${bgid}.pha \
        withspecranges=true energycolumn=PI specchannelmin=0 \
        specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
        writedss=Y expression="$pnexpr"

######################################################################
#  get pn oot background spectra

    echo -e '\nGetting pn background spectra...'

    pnexpr="$pnpattern && $bgreg $psreg"
    prefix=$PN_EV_PREFIX_LIST
    evlist=pn${prefix}-clean-oot.fits

    evselect table=${evlist} withimageset=yes imageset=${specdir}/pn-${bgid}-oot.im \
        xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
        yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
        withspectrumset=true spectrumset=${specdir}/pn-${bgid}-oot.pha \
        withspecranges=true energycolumn=PI specchannelmin=0 \
        specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
        writedss=Y expression="$pnexpr"

    # # detector map file for arfgen
    # evselect table=${evlist} withimageset=yes imageset=pn-${bgid}-oot-detmap.ds \
    #     xcolumn=DETX ycolumn=DETY imagebinning=binSize ximagebinsize=80 \
    #     yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
    #     withspectrumset=true spectrumset=${specdir}/pn-${bgid}-oot.pha \
    #     withspecranges=true energycolumn=PI specchannelmin=0 \
    #     specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
    #     writedss=Y expression="$pnexpr"

fi

######################################################################
# GETTING RMF:

export detmaptype=psf             # sas for ext sources: flat; esas: psf

if [[ $MAKE_RMF -ne 0 ]]
then

    echo -e '\nGetting source RMF...'

    rmfgen spectrumset=${specdir}/pn.pha rmfset=${specdir}/pn.rmf detmaptype=${detmaptype} # withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}
    # rmfgen spectrumset=${specdir}/m1.pha rmfset=${specdir}/m1.rmf detmaptype=${detmaptype} # withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}
    # rmfgen spectrumset=${specdir}/m2.pha rmfset=${specdir}/m2.rmf detmaptype=${detmaptype} # withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}

fi

if [[ $MAKE_RMF_BG -ne 0 ]]
then

    echo -e '\nGetting background RMF...'
    rmfgen spectrumset=${specdir}/pn-${bgid}.pha rmfset=${specdir}/pn-${bgid}.rmf detmaptype=${detmaptype} # withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}
    # rmfgen spectrumset=${specdir}/m1-${bgid}.pha rmfset=${specdir}/m1-${bgid}.rmf detmaptype=${detmaptype} # withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}
    # rmfgen spectrumset=${specdir}/m2-${bgid}.pha rmfset=${specdir}/m2-${bgid}.rmf detmaptype=${detmaptype} # withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}

fi


######################################################################
# GETTING ARF:

# export set="withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de} withrmfset=true withdetbounds=yes extendedsource=yes detmaptype=flat filterdss=no detxbins=10 detybins=10 modelee=N withbadpixcorr=N modeleffarea=Y modelquantumeff=Y modelfiltertrans=Y modelootcorr=no"

export set="badpixelresolution=2 crossregionarf=no detmaptype=dataset extendedsource=yes filterdss=yes filteredset=filteredpixellist.ds ignoreoutoffov=yes keeparfset=yes modelee=no modeleffarea=yes modelfiltertrans=yes modelootcorr=no modelquantumeff=yes psfenergy=2 setbackscale=no sourcecoords=eqpos sourcex=0 sourcey=0 useodfatt=no withbadpixcorr=yes withdetbounds=no withfilteredset=no withrmfset=yes withsourcepos=no"


if [[ $MAKE_ARF -ne 0 ]]
then

    # WITH VIG CORR!!!!!!!!!!!! -> special purpose  - if you use: 1. local bg & 2. zcolumn of spectra is "NO"
    # export set="withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de} withrmfset=true withdetbounds=yes extendedsource=yes detmaptype=flat filterdss=no detxbins=10 detybins=10 modelee=N withbadpixcorr=N modeleffarea=Y modelquantumeff=Y modelfiltertrans=Y"

    #export set="withsourcepos=yes sourcecoords="det" sourcex=3320.25 sourcey=8438.24 withrmfset=true withdetbounds=yes extendedsource=yes detmaptype=flat filterdss=no detxbins=10 detybins=10 modelee=N withbadpixcorr=N modeleffarea=Y modelquantumeff=Y modelfiltertrans=Y"

    echo -e '\nGetting source ARFs...'

    arfgen spectrumset=${specdir}/pn.pha  $set rmfset=${specdir}/pn.rmf  arfset=${specdir}/pn.arf badpixlocation=pn${PN_EV_PREFIX_LIST}-clean.fits detmaparray=pn-detmap.ds
    # arfgen spectrumset=${specdir}/m1.pha  $set rmfset=${specdir}/m1.rmf  arfset=${specdir}/m1.arf badpixlocation=mos${M1_EV_PREFIX_LIST}-clean.fits detmaparray=m1-detmap.ds
    # arfgen spectrumset=${specdir}/m2.pha  $set rmfset=${specdir}/m2.rmf  arfset=${specdir}/m2.arf badpixlocation=mos${M2_EV_PREFIX_LIST}-clean.fits detmaparray=m2-detmap.ds

fi

if [[ $MAKE_ARF_BG -ne 0 ]]
then

    # WITH VIG CORR!!!!!!!!!!!! -> special purpose  - if you use: 1. local bg & 2. zcolumn of spectra is "NO"
    # export set="withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de} withrmfset=true withdetbounds=yes extendedsource=yes detmaptype=flat filterdss=no detxbins=10 detybins=10 modelee=N withbadpixcorr=N modeleffarea=Y modelquantumeff=Y modelfiltertrans=Y"

    #export set="withsourcepos=yes sourcecoords="det" sourcex=3320.25 sourcey=8438.24 withrmfset=true withdetbounds=yes extendedsource=yes detmaptype=flat filterdss=no detxbins=10 detybins=10 modelee=N withbadpixcorr=N modeleffarea=Y modelquantumeff=Y modelfiltertrans=Y"

    echo -e '\nGetting background ARFs...'

    arfgen spectrumset=${specdir}/pn-${bgid}.pha  $set rmfset=${specdir}/pn-${bgid}.rmf  arfset=${specdir}/pn-${bgid}.arf badpixlocation=pn${PN_EV_PREFIX_LIST}-clean.fits detmaparray=pn-${bgid}-detmap.ds
    # arfgen spectrumset=${specdir}/m1-${bgid}.pha  $set rmfset=${specdir}/m1-${bgid}.rmf  arfset=${specdir}/m1-${bgid}.arf badpixlocation=mos${M1_EV_PREFIX_LIST}-clean.fits detmaparray=m1-${bgid}-detmap.ds
    # arfgen spectrumset=${specdir}/m2-${bgid}.pha  $set rmfset=${specdir}/m2-${bgid}.rmf  arfset=${specdir}/m2-${bgid}.arf badpixlocation=mos${M2_EV_PREFIX_LIST}-clean.fits detmaparray=m2-${bgid}-detmap.ds

fi

######################################################################
# backscale

if [[ $CALCULATE_BACKSCALE -ne 0 ]]
then

    if [[ $EXTRACT_SRC -ne 0 ]]
    then

        echo "Backscaling source spectra"

        prefix=$M1_EV_PREFIX_LIST
        evlist=mos${prefix}-clean.fits
        backscale spectrumset=${specdir}/m1.pha badpixlocation=$evlist useodfatt=yes

        prefix=$M2_EV_PREFIX_LIST
        evlist=mos${prefix}-clean.fits
        backscale spectrumset=${specdir}/m2.pha badpixlocation=$evlist useodfatt=yes

        prefix=$PN_EV_PREFIX_LIST
        evlist=pn${prefix}-clean.fits
        backscale spectrumset=${specdir}/pn.pha badpixlocation=$evlist useodfatt=yes

    fi

    if [[ $EXTRACT_BG -ne 0 ]]
    then

        echo "Backscaling background spectra"

        prefix=$M1_EV_PREFIX_LIST
        evlist=mos${prefix}-clean.fits
        backscale spectrumset=${specdir}/m1-${bgid}.pha badpixlocation=$evlist useodfatt=yes

        prefix=$M2_EV_PREFIX_LIST
        evlist=mos${prefix}-clean.fits
        backscale spectrumset=${specdir}/m2-${bgid}.pha badpixlocation=$evlist useodfatt=yes

        prefix=$PN_EV_PREFIX_LIST
        evlist=pn${prefix}-clean.fits
        backscale spectrumset=${specdir}/pn-${bgid}.pha badpixlocation=$evlist useodfatt=yes

    fi

fi

######################################################################
# do the OOT subtraction moved past the rmfgen/arfgen/backscale tasks
# - if subtracting before them there were sometime problems (e.g. with
# mathpha, updating keywords could fix it but this seems to be
# standard enough (i.e. to do rmfgen/arfgen on pre-oot subtraction))

# FIXME: unfortunately needs to jump between dirs...
cd $specdir
source ${codedir}/utils/util-funcs-lib.sh

if [[ $EXTRACT_SRC -eq 1  ]]
then
    echo "oot subtraction - source"
    pn.pha
    subtract_oot_spec pn.pha pn-oot.pha
fi

if [[ $EXTRACT_BG -eq 1 ]]
then
    echo "oot subtraction - background"
    subtract_oot_spec pn-${bgid}.pha pn-${bgid}-oot.pha
fi

cd $dir

######################################################################
# EXIT

cd $here
echo -e "\n$0 in $obsid done!"
exit 0
