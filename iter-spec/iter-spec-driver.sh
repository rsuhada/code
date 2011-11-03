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

instruments=(pn m1 m2)

specdir=../iter-spec            # work dir relative to the analysis directory
bgspecdir=../spec               # quick spectroscopyu dir with the local background

r_init=40                       # [arcsec]
max_iter=10                     # maximum number of iterations
r_tolerance=4.0                 # [arcsec]

EXTRACT_SRC=1
SRC_REGION_ID=cluster-iter-r

MAKE_RMF=1
MAKE_ARF=1
CALCULATE_BACKSCALE=1

LINK_BG=1                       # soft link bg annulus
BG_REGION_ID=bg-ann-01
PS_REGION_ID=ps-man

BG_REGION=${BG_REGION_ID}.phy.reg
PS_REGION=${PS_REGION_ID}.phy.reg

######################################################################
# prepare paths

here=`pwd`
cd $dir

mkdir -p ${specdir}/conf 2> /dev/null


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
    echo "iteration :: " $iter, "current val :: " $r " old val :: " $r_old "diff :: " $r_diff, "tolerance reached :: " $reached_r_tolerance


    ######################################################################
    # write region file

    shape="circle"
    rpad=$(echo $r | bc -l | xargs printf "%1.0f") # round
    rpad=`printf "%03d" $rpad`                     # zero pad

    coordsystem="wcs"
    regname=${specdir}/${SRC_REGION_ID}-${rpad}.wcs.reg
    make_src_reg_file $shape $regname $coordsystem $ra $de $r

    coordsystem="physical"
    regname=${specdir}/${SRC_REGION_ID}-${rpad}.phy.reg
    make_src_reg_file $shape $regname $coordsystem $x_phy $y_phy $r_phy


    ######################################################################
    # do the spectroscopy

    if [[ $EXTRACT_SRC -eq 1 ]]
    then

        for instrument in ${instruments[@]}
        do
            echo "extracting spectra" $instrument $regname
            ${codedir}/extract-source-spect.sh $instrument $regname $PS_REGION
        done

    fi

    r_old=$r
    r=$(echo "scale=6;$r/1.2" | bc)
    r_phy=$(echo "scale=6;$r*20.0" | bc)

    ######################################################################

    iter=$((iter + 1))
    echo "######################################################################"
    echo
done


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0
