######################################################################
# iterative spectroscopy driver script

######################################################################
# libraries

source ${codedir}/utils/util-funcs-lib.sh

######################################################################
# input and basic file name setup

dir=$1

export specdir=../radial-spec            # work dir relative to the analysis directory
export bgspecdir=../spec               # quick spectroscopyu dir with the local background
export parfile=${CLNAME}-par-rspec-001.conf
n
######################################################################
# prepare paths

here=`pwd`
cd $dir

mkdir -p ${specdir}/conf 2> /dev/null

######################################################################
# create config and result files if necessary

export config_file=${specdir}/conf/$parfile

if [[ ! -e $config_file ]]
then
    cp ${codedir}/templates/template-par-rspec-001.conf $config_file

    if [[ -e $NOTESFILE ]]
    then
        pars=(REDSHIFT NH)
        out=`get_cluster_pars $pars`
        tmp_redshift=`echo $out | awk '{print $1}'`
        tmp_nh=`echo $out | awk '{print $2}'`

        sed -i.sed.bk "s/PLACEHOLDER_REDSHIFT/${tmp_redshift}/g" $config_file
        sed -i.sed.bk "s/PLACEHOLDER_NH/${tmp_nh}/g" $config_file
        rm ${config_file}.sed.bk
    fi
fi

if [[ ! -e ${specdir}/conf/${CLNAME}-par-rspec-001.results ]]
then
    cp ${codedir}/templates/template-par-ispec-001.results ${specdir}/conf/${CLNAME}-par-rspec-001.results
fi

######################################################################
# MANUAL: uncomment this part if you want only to pre-create the dirs
# and config files

# echo "configs written!"
# sleep 1
# exit 0

######################################################################
# load in the config

source $config_file

######################################################################
# prepare needed file

export BG_REGION=${specdir}/${BG_REGION_ID}.phy.reg
export PS_REGION=${specdir}/${PS_REGION_ID}.phy.reg
export bgid=${BG_REGION_ID}            # FIXME: refactor redundancy

export LOG_MASTER_FILE="${dir}/${specdir}/conf/${CLNAME}-run-${fitid}-radial-master.tab"

# will need image coordinate point source directory
cp ${startdir}/${ANALYSIS_DIR}/analysis/${PS_REGION_ID}.im.reg ${specdir}/

echo $LOG_MASTER_FILE

######################################################################
# check whether we have a non-conflicting run

if [[ -e $LOG_MASTER_FILE ]]
then
    echo -e "\n** error: $LOG_MASTER_FILE exists here!"
    echo -e "*** error: Consider changing fitid: $fitid, or delete the master to force overwrite"
    echo -e "*** error: in $0\n"
    cd $startdir
    exit 1
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
export CLNAME=`echo $out | awk '{print $3}'`
export ra=`echo $out | awk '{print $4}'`
export de=`echo $out | awk '{print $5}'`
export x_phy=`echo $out | awk '{print $6}'`
export y_phy=`echo $out | awk '{print $7}'`

echo
echo $CLNAME
echo "redshift :: " $redshift
echo "nH ::       " $nh
echo $ra $de
echo $x_phy $y_phy
echo

######################################################################
# get background spectra (link it - have to be already pre-exisiting)

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

export iter=1
export r_old=0.0

export r=$r_min
export r_phy=$(echo "scale=6;$r*20.0" | bc)

export rcore=$(echo "scale=6;$core_frac*$r" | bc)
export rcore_phy=$(echo "scale=6;$rcore*20.0" | bc)
reached_r_max=`echo "if($r > $r_max) 1" | bc`

echo "initial radius: " $r
echo "core radius: " $rcore $rcore_phy
echo "max radius: " $r_max
echo "r step: " $r_step
echo "reached r_max: " $reached_r_max
init_tprofile_log_master $LOG_MASTER_FILE

######################################################################
# iterator

while [[ $reached_r_max -ne 1 ]]; do

    echo "######################################################################"
    echo "iteration :: " $iter "current val :: " $r "step :: " $r "maximal :: " $r_max

    ######################################################################
    # write region files

    shape="circle"

    export rcore=$(echo "scale=6;$core_frac*$r" | bc)
    rpad=$(echo $r | bc -l | xargs printf "%1.0f") # round
    export rpad=`printf "%03d" $rpad`              # zero pad, need export
    spectrumid="run-$fitid-iter-r-$rpad"           # identifier for spectral products

    export r_phy=$(echo "scale=6;$r*20.0" | bc)    # current rad in phy units
    export rcore_phy=$(echo "scale=6;$rcore*20.0" | bc)    # current rad in phy units

    coordsystem="wcs"
    regname=${specdir}/${SRC_REGION_ID}-${rpad}.wcs.reg
    make_src_reg_file $shape $regname $coordsystem $ra $de $r

    coordsystem="physical"
    regname=${specdir}/${SRC_REGION_ID}-${rpad}.phy.reg
    make_src_reg_file $shape $regname $coordsystem $x_phy $y_phy $r_phy
    SRC_REGION=$regname

    coordsystem="wcs"
    regname=${specdir}/${CORE_REGION_ID}-${rpad}.wcs.reg
    make_src_reg_file $shape $regname $coordsystem $ra $de $rcore

    coordsystem="physical"
    regname=${specdir}/${CORE_REGION_ID}-${rpad}.phy.reg
    make_src_reg_file $shape $regname $coordsystem $x_phy $y_phy $rcore_phy
    CORE_REGION=$regname

    ######################################################################
    # do the extraction of spectra

    if [[ $EXTRACT_SRC_SPEC -eq 1 ]]
    then
        for instrument in ${instruments[@]}
        do
            echo "extracting spectra: "

            if [[ $EXCLUDE_CORE -eq 0 ]]
            then
                echo "Not excising the core:"
                echo ${codedir}/extract-source-spec.sh $instrument $SRC_REGION $spectrumid $specdir $PS_REGION
                ${codedir}/extract-source-spec.sh $instrument $SRC_REGION $spectrumid $specdir $PS_REGION
            else
                echo "Excising the core:"
                echo ${codedir}/extract-source-spec.sh $instrument $SRC_REGION $spectrumid $specdir $PS_REGION $CORE_REGION
                ${codedir}/extract-source-spec.sh $instrument $SRC_REGION $spectrumid $specdir $PS_REGION $CORE_REGION
            fi
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

    # detmaptype="dataset"        # flat/psf/dataset
    detmaptype="psf"        # flat/psf/dataset - psf default for SAS and ESAS

    if [[ $MAKE_RMF -eq 1 ]]
    then
        for instrument in ${instruments[@]}
        do
            echo 'Getting source RMF...'
            detmaparray=${specdir}/${instrument}-${spectrumid}-detmap.ds
            echo ${codedir}/extract-rmf.sh $instrument $spectrumid $specdir $ra $de $detmaptype $detmaparray
            ${codedir}/extract-rmf.sh $instrument $spectrumid $specdir $ra $de $detmaptype $detmaparray
        done
    else
        for instrument in ${instruments[@]}
        do
            # FIXME: linking currently broken
            echo 'Not creating new RMF...'
            if [[ ! -e ${specdir}/${instrument}-${spectrumid}.rmf ]]
            then
                echo -e "${specdir}/${instrument}-${spectrumid}.rmf does not exists - linking it to preexisting"

                rmfile=${bgspecdir}/${instrument}-cluster-man-01.rmf # use a backup rmf
                if [[ ! -e $rmfile ]]
                then
                    echo -e "\n** error: $rmfile does not exists here!"
                    echo -e "*** error in $0\n"
                    cd $startdir
                    exit 1
                fi
                ln -s $rmfile ${specdir}/${instrument}-${spectrumid}.rmf
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
                echo -e "${specdir}/${instrument}-${spectrumid}.arf does not exists - linking it to preexisting"

                arfile=${bgspecdir}/${instrument}-cluster-man-01.arf # use a backup arf
                if [[ ! -e $arfile ]]
                then
                    echo -e "\n** error: $arfile does not exists here!"
                    echo -e "*** error in $0\n"
                    cd $startdir
                    exit 1
                fi
                ln -s $arfile ${specdir}/${instrument}-${spectrumid}.arf
            fi
        done
    fi

    ######################################################################
    # do the oot subtraction

    if [[ $EXTRACT_SRC_SPEC -eq 1 ]]
    then
        echo "Running oot subtraction: "
        export here=`pwd`
        cd $specdir
        echo "doing oot subtraction"
        subtract_oot_spec ${instrument}-${spectrumid}.pha ${instrument}-${spectrumid}-oot.pha

    # comment for debugging
        rm ${instrument}-${spectrumid}-oot.pha ${instrument}-${spectrumid}-oot.im ${instrument}-${spectrumid}-oot.pha.orig

        cd $here
    fi

    ######################################################################
    # do the spectral fit

    instsum=0

    if [[ $DO_SPECTROSCOPY -eq 1 ]]
    then
        cd $specdir
        pwd

        # determine the combination of present instruments
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

        # select the script given the combination of instruments
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
                ;;
            *)
                echo "Problem with instruments?"
        esac


        echo "Running spectroscopy script :: "
        echo ${codedir}/iter-spec/$specscript $CLNAME conf/$parfile $spectrumid $BG_REGION_ID $group_min
        ${codedir}/iter-spec/$specscript $CLNAME conf/$parfile $spectrumid $BG_REGION_ID $group_min
        ${codedir}/quick-spec/gather-quickspec-results.sh ${spectrumid} 1 # overwrites if exists

    fi

    ######################################################################
    # write into the master

    if [[ $DO_SPECTROSCOPY -eq 1 ]]
    then
        echo "writing into the master log"
        # sort of dummy here - if current r were r500 what would be the pars be (required for further output)
        $PYTHONEXEC ${codedir}/py/t_to_r.py ${spectrumid}/${CLNAME}-${spectrumid}.result | tee ${spectrumid}/${CLNAME}-${spectrumid}.aper
        aper_results=`read_aper_result_file ${spectrumid}/${CLNAME}-${spectrumid}.aper`

        echo $fitid $iter $r $aper_results >> $LOG_MASTER_FILE
        mv formated_pars.out ${CLNAME}-${spectrumid}.fpars
    else
        echo $fitid $iter $r >> $LOG_MASTER_FILE
    fi

    ######################################################################
    # prepare new aperture
    iter=$((iter + 1))
    r_old=$r
    r=$(echo "scale=6;$r+$r_step" | bc)
    echo $r_old $r_step $r "@@@@@@@@@@@@@@@@@@@@"

    reached_r_max=`echo "if($r > $r_max) 1" | bc`

    ######################################################################
    # finished iteration step

    ${codedir}/iter-spec/clean-up-spec.sh ${spectrumid} 2>/dev/null

    cd $dir                     # returns to analysis subdir
    pwd

    echo "Done:"
    echo "iteration :: " $iter " for r val :: " $r_old " r for the next iteration :: " $r >>  ${specdir}/${spectrumid}/${CLNAME}-${spectrumid}.aper
    echo "######################################################################" >> ${specdir}/${spectrumid}/${CLNAME}-${spectrumid}.aper
    echo

done                            # iteration end
######################################################################


######################################################################
# plot

echo "Creating radial temperature plot!"
$PYTHONEXEC ${codedir}/radial-spec/plt_radial_t.py $LOG_MASTER_FILE



######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0