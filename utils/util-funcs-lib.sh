######################################################################
# library of utility functions

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


function make_src_reg_file {
    ######################################################################
    # write a ds9 region file
    # supports wcs and physical coords
    # supports circle and annnulus shapes (easily extensible to other)

    shape=$1
    regname=$2
    coords=$3
    x=$4
    y=$5
    radius=$6
    radius2=$7

    echo $shape
    echo $regname
    echo $coords
    echo $x
    echo $y
    echo $radius
    echo $radius2

    ######################################################################
    # resolve coordinate system

    if [[ "$coords" == "phy" || "$coords" == "physical" ]]
    then
        coords="physical"
        units=''
    fi

    if [[ "$coords" == "wcs" || "$coords" == "fk5" ]]
    then
        coords="fk5"
        units='"'
    fi

    ######################################################################
    # resolve region shape

    case $shape in
        "annulus")
            regionexpression="${shape}($x,$y,${radius}${units},${radius2}${units})"
            ;;
        "circle")
            regionexpression="${shape}($x,$y,${radius}${units})"
            ;;
        *)
            regionexpression="${shape}($x,$y,${radius}${units})"
            echo "Unknown shape, using circle"
    esac

    ######################################################################
    # write the region file

    (
    echo "# Region file format: DS9 version 4.1"
    echo global color=green dashlist=8 3 width=1 font=\"helvetica 10 normal\" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1
    echo $coords
    echo $regionexpression

    ) > $regname

    echo "Written region file: " $regname

}


function ds9reg_to_sasdesc {
    ######################################################################
    # parse a ds9 region file to create a SAS descriptor file

    inreg=$1                    # ds9 region file
    remove=$2                   # [ 0/1 ] should I remove these regions?

    if [[ $# != 2 ]]
    then
        echo "missing second parameter! 1 = this should be an active region, 0 = remove these regions"
        exit 1
    fi

    # if [[ -e ${inreg}.desc ]]
    # then
    #     echo "backuping region file ${inreg}.desc"
    #     mv ${inreg}.desc ${inreg}.desc.bk
    # fi

    if [[ $remove -eq 0 ]]
    then

        egrep "circle" $inreg | tr -d "\-circle(" | tr -d ")" | awk '{print "&&! circle("$1",X,Y)"}' | tr '\n' ' ' > ${inreg}.desc

    else

        egrep "circle" $inreg | tr -d "\-circle(" | tr -d ")" | awk '{print "circle("$1",X,Y)"}' | tr '\n' ' ' > ${inreg}.desc

        egrep "annulus" $inreg | tr -d "\-annulus(" | tr -d ")" | awk '{print "annulus("$1",X,Y)"}' | tr '\n' ' ' >> ${inreg}.desc

    fi

    echo "Done parsing file $inreg"

    ls ${inreg}.desc
}


function read_aper_result_file {
    ######################################################################
    # reads in the physical parameters for the give aperture file
    # written by t_to_r.py

    infile=$1

    norm=`egrep "\bnorm\b" ${infile} | awk '{print $2}'`
    norm_err_n=`egrep "\bnorm_err_n\b" ${infile} | awk '{print $2}'`
    norm_err_p=`egrep "\bnorm_err_p\b" ${infile} | awk '{print $2}'`
    t_fit=`egrep "\bt_fit\b" ${infile} | awk '{print $2}'`
    t_fit_err_n=`egrep "\bt_fit_err_n\b" ${infile} | awk '{print $2}'`
    t_fit_err_p=`egrep "\bt_fit_err_p\b" ${infile} | awk '{print $2}'`
    t500=`egrep "\bt500\b" ${infile} | awk '{print $2}'`
    t500_err=`egrep "\bt500_err\b" ${infile} | awk '{print $2}'`
    z=`egrep "\bz\b" ${infile} | awk '{print $2}'`
    z_err_n=`egrep "\bz_err_n\b" ${infile} | awk '{print $2}'`
    z_err_p=`egrep "\bz_err_p\b" ${infile} | awk '{print $2}'`
    abund=`egrep "\babund\b" ${infile} | awk '{print $2}'`
    abund_err_n=`egrep "\babund_err_n\b" ${infile} | awk '{print $2}'`
    abund_err_p=`egrep "\babund_err_p\b" ${infile} | awk '{print $2}'`

    m500=`egrep "\bm500\b" ${infile} | awk '{print $2}'`
    m500_err=`egrep "\bm500_err\b" ${infile} | awk '{print $2}'`
    r500=`egrep "\br500\b" ${infile} | awk '{print $2}'`
    rcore_ang=`egrep "\b0.15r500_ang\b" ${infile} | awk '{print $2}'`
    r500_ang=`egrep "\br500_ang\b" ${infile} | awk '{print $2}'`

    echo $norm $norm_err_n $norm_err_p $t_fit $t_fit_err_n $t_fit_err_p $z $z_err_n $z_err_p $abund $abund_err_n $abund_err_p $t500 $t500_err $m500 $m500_err $r500 $r500_ang $rcore_ang
}


function init_log_master {
    ######################################################################
    # writes a topcat compliant header line to the master file that
    # tracks the results of each iteration

    local __LOG_MASTER_FILE=$1
    echo  "# fitid iter r_fit r_fit_next r_diff norm norm_err_n norm_err_p t_fit t_fit_err_n t_fit_err_p z z_err_n z_err_p abund abund_err_n abund_err_p t500 t500_err m500 m500_err r500 r500_ang rcore_ang" > $__LOG_MASTER_FILE
}


function make-im {
    ######################################################################
    # extracts an image

    inevli=$1
    outim=$2
    elo=$3
    ehi=$4
    expression=$5

    evselect \
        attributestocopy='' \
        blockstocopy='' \
        cleandss=no \
        decimagecenter=0 \
        destruct=yes \
        dssblock='' \
        energycolumn=PHA \
        expression="(PI in [${elo}:${ehi}]) && (FLAG .eq. 0) $expression" \
        filteredset=filtered.fits \
        filterexposure=yes \
        filtertype=expression \
        flagbit=-1 \
        flagcolumn=EVFLAG \
        histogrambinsize=1 \
        histogramcolumn=TIME \
        histogrammax=1000 \
        histogrammin=0 \
        histogramset=histo.fits \
        ignorelegallimits=yes \
        imagebinning=imageSize \
        imagedatatype=Int32 \
        imageset=$outim \
        keepfilteroutput=yes \
        makeratecolumn=no \
        maketimecolumn=no \
        raimagecenter=0 \
        rateset=rate.fits \
        specchannelmax=4095 \
        specchannelmin=0 \
        spectralbinsize=10 \
        spectrumset=spectrum.fits \
        squarepixels=yes \
        table=${inevli}:EVENTS \
        timebinsize=1 \
        timecolumn=TIME \
        timemax=1000 \
        timemin=0 \
        updateexposure=yes \
        withcelestialcenter=no \
        withfilteredset=yes \
        withhistogramset=no \
        withhistoranges=no \
        withimagedatatype=yes \
        withimageset=yes \
        withrateset=no \
        withspecranges=no \
        withspectrumset=no \
        withtimeranges=no \
        withxranges=yes \
        withyranges=yes \
        withzcolumn=no \
        withzerrorcolumn=no \
        writedss=yes \
        xcolumn=X \
        ximagebinsize=1 \
        ximagemax=48400 \
        ximagemin=3401 \
        ximagesize=900 \
        ycolumn=Y \
        yimagebinsize=1 \
        yimagemax=48400 \
        yimagemin=3401 \
        yimagesize=900 \
        zcolumn=WEIGHT \
        zerrorcolumn=EWEIGHT

}
