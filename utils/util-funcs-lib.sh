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


function init_tprofile_log_master {
    ######################################################################
    # writes a topcat compliant header line to the master file that
    # tracks the results of each iteration - verision for t profiler

    local __LOG_MASTER_FILE=$1
    echo  "# fitid iter r_fit norm norm_err_n norm_err_p t_fit t_fit_err_n t_fit_err_p z z_err_n z_err_p abund abund_err_n abund_err_p t500 t500_err m500 m500_err r500 r500_ang rcore_ang" > $__LOG_MASTER_FILE
}


function make-im-standard {
    ######################################################################
    # extracts an image: standard settings

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
        ignorelegallimits=no \
        imagebinning=binSize \
        imagedatatype=Real32 \
        imageset=$outim \
        keepfilteroutput=no \
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
        withfilteredset=no \
        withhistogramset=no \
        withhistoranges=no \
        withimagedatatype=yes \
        withimageset=yes \
        withrateset=no \
        withspecranges=no \
        withspectrumset=no \
        withtimeranges=no \
        withxranges=no \
        withyranges=no \
        withzcolumn=no \
        withzerrorcolumn=no \
        writedss=yes \
        xcolumn=X \
        ximagebinsize=80 \
        ximagemax=640 \
        ximagemin=1 \
        ximagesize=600 \
        ycolumn=Y \
        yimagebinsize=80 \
        yimagemax=640 \
        yimagemin=1 \
        yimagesize=600 \
        zcolumn=WEIGHT \
        zerrorcolumn=EWEIGHT

}

function make-im {
    ######################################################################
    # extracts an image: using the esas settings

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

function eval_ccd_pattern {
    ######################################################################
    # returns a pattern string for MOS1 or MOS2 based on good chips
    # note: idiot SAS won't make correct exp maps if you only remove
    # bad chips - instead you have to allow all the good chips

    inst=$1
    outpattern='('

    case $inst in
        m1)
            for ccd in M1_CCD1 M1_CCD2 M1_CCD3 M1_CCD4 M1_CCD5 M1_CCD6 M1_CCD7
            do
                if [[ $ccd -eq 1 ]]
                then
                    ccdnr=${ccd#${ccd%?}}
                    outpattern="${outpattern}(CCDNR == ${ccdnr})||"
                fi
            done
            ;;
        m2)
           for ccd in M2_CCD1 M2_CCD2 M2_CCD3 M2_CCD4 M2_CCD5 M2_CCD6 M2_CCD7
            do
                if [[ $ccd -eq 1 ]]
                then
                    ccdnr=${ccd#${ccd%?}}
                    outpattern="${outpattern}(CCDNR == ${ccdnr})||"
                fi
            done
            ;;
        *)
            echo "** error: unknown instrument"
            cd $startdir
            exit 1
    esac

    # lazy strip the trailing ||
    outpattern=${outpattern%?}
    outpattern="${outpattern%?})"

    echo "$outpattern"
}

function get-oot-scale {
    ######################################################################
    # script to get the oot scale factor for a pn image based on its
    # submode

    image=$1

    submode=`fkeyprint $image SUBMODE | grep = | awk '{print $3}' | sed "s/'//g" | tr '[A-Z]' '[a-z]'` # for extrs safety lowcase everything
    frametime=`fkeyprint $spec FRMTIME | grep = | awk '{print $3}' | sed "s/'//g"`

    case $submode in
        primefullwindow)
            oot_scale=0.063
            ;;
        primefullwindowextended)
            oot_scale=0.0232
            if [[ $frametime -ge 210 ]]
            then
                oot_scale=0.0163
            fi
            ;;
        primelargewindow)
            oot_scale=0.0016
            ;;
        primesmallwindow)
            oot_scale=0.011
            ;;
        *)
            echo "\*\* error: unknown submode: $submode in $image!"
            exit 1
    esac

    # uncomment to temporarily disable oot subtraction
    # oot_scale=0.00

    echo $oot_scale
}

function subtract-oot {
    ######################################################################
    # gets the oot correction factor and subtracts the oot image

    image=$1
    ootimage=$2
    outimage=$3

    # get oot factor
    # it is problematic (but not impossible) to source from within
    # same library - so better repeat myself...
    # oot_scale=$(get-oot-scale $image)   # doesn't have to work

    submode=`fkeyprint $image SUBMODE | grep = | awk '{print $3}' | sed "s/'//g" | tr '[A-Z]' '[a-z]'` # for extrs safety lowcase everything
    frametime=`fkeyprint $image FRMTIME | grep = | awk '{print $3}' | sed "s/'//g"`

    case $submode in
        primefullwindow)
            oot_scale=0.063
            ;;
        primefullwindowextended)
            oot_scale=0.0232
            if [[ $frametime -ge 210 ]]
            then
                oot_scale=0.0163
            fi
            ;;
        primelargewindow)
            oot_scale=0.0016
            ;;
        primesmallwindow)
            oot_scale=0.011
            ;;
        *)
            echo "\*\* error: unknown submode: $submode in $image!"
            exit 1
    esac


    echo $image $ootimage
    echo "scale :: " $oot_scale

    echo farith $ootimage $oot_scale ${ootimage}.tmp MUL clobber=yes
    farith $ootimage $oot_scale ${ootimage}.tmp MUL clobber=yes
    mv ${ootimage}.tmp ${ootimage}

    farith $image $ootimage $outimage SUB clobber=yes

    # copy the original extensions (bintables)
    hdunum=`fstruct ${image} | grep BINTABLE | tail -1 | awk '{print $1}'`
    for ((i=1; i<=$hdunum;i++))
    do
        echo fappend ${image}[$i] ${outimage}
        fappend ${image}[$i] ${outimage}
    done

}


function subtract_oot_spec {
    ######################################################################
    # gets the oot correction factor and subtracts the oot spectrum

    input_spec=$1
    input_ootspec=$2
    RATE_SPACE=1                # 1 - subtraction in rate-space
                                # (STRONGLY RECOMMENDED).
                                # TODO: explore incompatibility with
                                # c-stat (?)

    # backup
    cp ${input_spec} ${input_spec}.orig
    cp ${input_ootspec} ${input_ootspec}.orig

    ######################################################################
    # some ftool tasks can't handle dash in filename

    spec=oot_subtraction_tmp_pn.pha
    ootspec=oot_subtraction_tmp_pn_oot.pha
    outspec=oot_subtraction_tmp_pn_sub.pha

    mv $input_spec $spec
    mv $input_ootspec $ootspec

    ######################################################################
    # get oot factor

    # for extra safety lowcase everything
    submode=`fkeyprint $spec SUBMODE | grep = | awk '{print $3}' | sed "s/'//g" | tr '[A-Z]' '[a-z]'`
    frametime=`fkeyprint $spec FRMTIME | grep = | awk '{print $3}' | sed "s/'//g"`

    case $submode in
        primefullwindow)
            oot_scale=0.063
            ;;
        primefullwindowextended)
            oot_scale=0.0232
            if [[ $frametime -ge 210 ]]
            then
                oot_scale=0.0163
            fi
            ;;
        primelargewindow)
            oot_scale=0.0016
            ;;
        primesmallwindow)
            oot_scale=0.011
            ;;
        *)
            echo "\*\* error: unknown submode: $submode in $spec!"
            echo "\*\*\* error: in script $0"
            exit 1
    esac

    ######################################################################
    # prepare files for oot subtraction

    echo "Subtracting oot with option :: " $RATE_SPACE
    echo "updating spectrum headers and copying oot column"
    echo "spectrum  :: " ${input_spec}
    echo "oot       :: " ${input_ootspec}
    echo "submode   :: " ${submode}
    echo "frametime :: " ${frametime}
    echo "oot scale :: " ${oot_scale}

    if [[ $RATE_SPACE -eq 1 ]]
    then

mathpha <<EOT
${spec}-$oot_scale*${ootspec}
R
$outspec
$spec
1
0
EOT

    ######################################################################
    # move to original filenames

    mv $outspec $input_spec
    mv $ootspec $input_ootspec

    # restore primary header and update keys in first extension
    cphead ${input_spec}.orig+0 ${input_spec}+0
    fkeyprint ${input_spec}.orig+1 BACKSCAL | grep =  > pn-header.tmp.txt
    fkeyprint ${input_spec}.orig+1 EXPOSURE | grep = >> pn-header.tmp.txt
    fmodhead ${input_spec}+1 pn-header.tmp.txt
    rm pn-header.tmp.txt ${spec}

    else

    ######################################################################
    # alternative version in CTS space
    ######################################################################
        echo "subtracting oot now!"

        fparkey value=CTS_OOT_ORIG fitsfile=${ootspec}+1 keyword=TTYPE2
        faddcol infile=${spec}+1 colfile=${ootspec}+1 \
            colname=CTS_OOT_ORIG

        fparkey value=CTS_OOT fitsfile=${ootspec}+1 keyword=TTYPE2
        faddcol infile=${spec}+1 colfile=${ootspec}+1 \
            colname=CTS_OOT

    ######################################################################
    # scale and subtract

    # subtracting oot events
        fcalc clobber=yes infile=${spec}+1 outfile=${spec} \
            clname=CTS_OOT expr=CTS_OOT*${oot_scale} copyall=yes

        fcalc clobber=yes infile=${spec}+1 outfile=${spec} \
            clname=COUNTS expr=COUNTS-CTS_OOT copyall=yes

    ######################################################################
    # remove negative values FIXME: check if this patch is valid wrt
    # esas (though it's typically only few (~5) bins at very high energies,
    # most likely outside fitting range)

        rm remove_neg.tmp.fits 2> /dev/null

        fcopy "${spec}[COUNTS<0.0]" remove_neg.tmp.fits

        fdump infile=remove_neg.tmp.fits+1 outfile=${spec}.ascii clobber=yes \
            columns=CHANNEL rows=- \
            prhead=no showunit=no showrow=no showscale=no showcol=no

        sed '/^$/d' ${spec}.ascii | awk '{print $0+1 " " 0.0}' > ${spec}.ascii2
        fmodtab ${spec}+1 COUNTS ${spec}.ascii2

        rm ${spec}.ascii ${spec}.ascii2 remove_neg.tmp.fits

   ######################################################################
   # move to original filenames

        mv $spec $input_spec
        mv $ootspec $input_ootspec

   ######################################################################
   # alternative version in CTS space
   ######################################################################

fi
}

function arcsec_2_impix_xmm {
    # converts arcseconds to image pixels: for XMM-Newton images
    # uses a hardcoded table
    # FIXME: add python routine that does this generally
    #
    # INPUT:
    # 1 - XMM image fits file
    # 2 - length in arc seconds
    # OUTPUT:
    # length in image pixels

    image=$1
    x=$2

    # get image size
    naxis1=`fkeyprint ${image}+0 NAXIS1 | grep = | awk '{print $3}'`

    case $naxis1 in
        900)
            scale=0.4
            ;;
        648)
            scale=0.25
            ;;
        *)
            echo "\*\* error: image size: $naxis1 in image: $image is not in database"
            echo "\*\*\* error: in script $0"
            exit 1
    esac

    x_im=$(echo "scale=6;$x*$scale" | bc)

    # this the output
    echo $x_im
}
