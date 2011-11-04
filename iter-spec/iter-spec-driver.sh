######################################################################
# iterative spectroscopy driver script

######################################################################
# libraries

source ${codedir}/utils/util-funcs-lib.sh

######################################################################
# input

dir=$1

######################################################################
# settings

export instruments=(pn m1 m2)
export fitpars="taz"                     # options: t, ta, taz, tz
export fitid="001"
export group_min=1

export specdir=../iter-spec            # work dir relative to the analysis directory
export bgspecdir=../spec               # quick spectroscopyu dir with the local background

export r_init=37.1325                  # [arcsec]   test: 37.1325
export max_iter=1                      # maximum number of iterations
export r_tolerance=4.0                 # [arcsec]

export EXTRACT_SRC=0
export CALCULATE_BACKSCALE=0

export MAKE_RMF=0
export MAKE_ARF=0

export DO_SPECTROSCOPY=1

export SRC_REGION_ID=cluster-iter-r
export BG_REGION_ID=bg-ann-01
export PS_REGION_ID=ps-man
export LINK_BG=0                       # soft link bg annulus

export BG_REGION=${specdir}/${BG_REGION_ID}.phy.reg
export PS_REGION=${specdir}/${PS_REGION_ID}.phy.reg
export parfile=${clname}-par-qspec-001.conf

######################################################################
# prepare paths

here=`pwd`
cd $dir

mkdir -p ${specdir}/conf 2> /dev/null

######################################################################
# create config files if necessary

export config_file=${specdir}/conf/$parfile

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
# get parameters from analysis file

if [[ ! -e $NOTESFILE ]]
then
    echo -e "\n** error: $NOTESFILE does not exists!"
    echo -e "*** error in $0\n"
    cd $startdir
    exit 1
fi

pars=(REDSHIFT NH NAME RA DE X_PHY Y_PHY)

out=`get_cluster_pars $pars`

export redshift=`echo $out | awk '{print $1}'`
export nh=`echo $out | awk '{print $2}'`
export clname=`echo $out | awk '{print $3}'`
export ra=`echo $out | awk '{print $4}'`
export de=`echo $out | awk '{print $5}'`
export x_phy=`echo $out | awk '{print $6}'`
export y_phy=`echo $out | awk '{print $7}'`

echo
echo $clname
echo "redshift :: " $redshift
echo "nH ::       " $nh
echo $ra $de
echo $x_phy $y_phy
echo

######################################################################
# get background spectra (have to be exisiting)

if [[ $LINK_BG -eq 1 ]]
then

    if [[ ! -e ${bgspecdir}/${instruments[0]}-${BG_REGION_ID}.arf ]]
    then
        echo -e "\n** error: ${bgspecdir}/${instruments[0]}-${BG_REGION_ID}.arf does not exists!"
        echo -e "*** error in $0\n"
        cd $startdir
        exit 1
    fi

    ln -s ${bgspecdir}/${BG_REGION_ID}.phy.reg ${specdir}/${BG_REGION_ID}.phy.reg
    ln -s ${bgspecdir}/${PS_REGION_ID}.phy.reg ${specdir}/${PS_REGION_ID}.phy.reg

    for instrument in ${instruments[@]}
    do
        ln -s ${bgspecdir}/${instrument}-${BG_REGION_ID}.im ${specdir}/${instrument}-${BG_REGION_ID}.im
        ln -s ${bgspecdir}/${instrument}-${BG_REGION_ID}.pha ${specdir}/${instrument}-${BG_REGION_ID}.pha
        ln -s ${bgspecdir}/${instrument}-${BG_REGION_ID}.grp.pha ${specdir}/${instrument}-${BG_REGION_ID}.grp.pha
        ln -s ${bgspecdir}/${instrument}-${BG_REGION_ID}.arf ${specdir}/${instrument}-${BG_REGION_ID}.arf
        ln -s ${bgspecdir}/${instrument}-${BG_REGION_ID}.rmf ${specdir}/${instrument}-${BG_REGION_ID}.rmf
    done

fi

######################################################################
# initialize iterations

export r=$r_init
export iter=1
export r_old=10000.0
export reached_r_tolerance=0

export r_phy=$(echo "scale=6;$r*20.0" | bc)

######################################################################
# iterator

while [[ $iter -le $max_iter && $reached_r_tolerance -ne 1 ]]; do

    r_diff=$(echo "scale=6;$r-$r_old" | bc)
    r_diff=`echo ${r_diff#-}`   # get the absolute value
    reached_r_tolerance=`echo "if($r_diff <= $r_tolerance) 1" | bc`

    echo "######################################################################"
    echo "iteration :: " $iter "current val :: " $r " old val :: " $r_old "diff :: " $r_diff, "tolerance reached :: " $reached_r_tolerance

    ######################################################################
    # write region file

    shape="circle"
    rpad=$(echo $r | bc -l | xargs printf "%1.0f") # round
    rpad=`printf "%03d" $rpad`                     # zero pad
    spectrumid="iter-r-$rpad"                      # identifier for spectral products

    coordsystem="wcs"
    regname=${specdir}/${SRC_REGION_ID}-${rpad}.wcs.reg
    make_src_reg_file $shape $regname $coordsystem $ra $de $r

    coordsystem="physical"
    regname=${specdir}/${SRC_REGION_ID}-${rpad}.phy.reg
    make_src_reg_file $shape $regname $coordsystem $x_phy $y_phy $r_phy

    ######################################################################
    # do the extraction of spectra

    if [[ $EXTRACT_SRC -eq 1 ]]
    then
        for instrument in ${instruments[@]}
        do
            echo "extracting spectra: "
            echo ${codedir}/extract-source-spec.sh $instrument $regname $spectrumid $specdir $PS_REGION
            ${codedir}/extract-source-spec.sh $instrument $regname $spectrumid $specdir $PS_REGION
        done
    fi

    ######################################################################
    # do the backscale calculation

    if [[ $CALCULATE_BACKSCALE -eq 1 ]]
    then
        for instrument in ${instruments[@]}
        do
            echo "calculating backscale: "
            echo ${codedir}/calc-backscale.sh $instrument $spectrumid $specdir
            ${codedir}/calc-backscale.sh $instrument $spectrumid $specdir
        done
    fi

    ######################################################################
    # do the rmf extraction

    if [[ $MAKE_RMF -eq 1 ]]
    then
        for instrument in ${instruments[@]}
        do
            echo 'Getting source RMF...'
            echo ${codedir}/extract-rmf.sh $instrument $spectrumid $specdir $ra $de
            ${codedir}/extract-rmf.sh $instrument $spectrumid $specdir $ra $de
        done
    else
        for instrument in ${instruments[@]}
        do
            echo 'Not creating new RMF...'
            if [[ ! -e ${specdir}/${instrument}-${spectrumid}.rmf ]]
            then
                echo -e "${specdir}/${instrument}-${spectrumid}.rmf does not exists - linking it"
                ln -s ${bgspecdir}/${instrument}.rmf ${specdir}/${instrument}-${spectrumid}.rmf
            fi
        done
    fi

    ######################################################################
    # do the arf extraction

    if [[ $MAKE_ARF -eq 1 ]]
    then
        for instrument in ${instruments[@]}
        do
            echo 'Getting source ARF...'
            echo ${codedir}/extract-arf.sh $instrument $spectrumid $specdir $ra $de
            ${codedir}/extract-arf.sh $instrument $spectrumid $specdir $ra $de
        done
    else
        for instrument in ${instruments[@]}
        do
            echo 'Not creating new ARF...'
            if [[ ! -e ${specdir}/${instrument}-${spectrumid}.arf ]]
            then
                echo -e "${specdir}/${instrument}-${spectrumid}.arf does not exists - linking it"
                ln -s ${bgspecdir}/${instrument}.arf ${specdir}/${instrument}-${spectrumid}.arf
            fi
        done
    fi

    ######################################################################
    # do the spectral fit

    instsum=0

    if [[ $DO_SPECTROSCOPY -eq 1 ]]
    then
        cd $specdir
        pwd

        for instrument in ${instruments[@]}
        do
            case $instrument in
                "pn")
                    instsum=$((instsum + 1))
                    ;;
                "m1")
                    instsum=$((instsum + 2))
                    ;;
                "m2")
                    instsum=$((instsum + 4))
                    ;;
                *)
                    echo "unknown instrument"
                    exit 1
            esac
        done

        # FIXME add other instrument setups
        case $instsum in
            1)
                echo "TBD"
                ;;
            2)
                echo "TBD"
                ;;
            3)
                echo "TBD"
                ;;
            4)
                echo "TBD"
                ;;
            5)
                echo "TBD"
                ;;
            6)
                echo "TBD"
                ;;
            7)
                specscript=spec-iter-pnm1m2-${fitpars}.sh

                echo "Running spectroscopy script :: "
                echo ${codedir}/iter-spec/$specscript $clname $fitid conf/$parfile $spectrumid $BG_REGION_ID $group_min
                ${codedir}/iter-spec/$specscript $clname $fitid conf/$parfile $spectrumid $BG_REGION_ID $group_min
                ;;
            *)
                echo "Problem with instruments?"
        esac

        cd $dir
        pwd
    fi

    ######################################################################
    # update the radius

    r_old=$r
    r=$(echo "scale=6;$r*1.2" | bc)
    r_phy=$(echo "scale=6;$r*20.0" | bc)

    ######################################################################
    # finished iteration step

    iter=$((iter + 1))
    echo "######################################################################"
    echo

done

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0
