######################################################################
# iterative spectroscopy driver script

source ${codedir}/utils/util-funcs-lib.sh

dir=$1
here=`pwd`
cd $dir

specdir=../spec

######################################################################
# settings

ra=$2
de=$3

EXTRACT_SRC=1
EXTRACT_BG=1

MAKE_RMF=1
MAKE_ARF=1
CALCULATE_BACKSCALE=1

SRC_REGION=cluster-iter-01.phy.reg
BG_REGION=bg-ann-01.phy.reg
PS_REGION=ps-man.phy.reg


######################################################################
# get parameters from analysis file

if [[ ! -e $NOTESFILE ]]
then
    echo -e "\n** error: $NOTESFILE does not exists here!"
    echo -e "*** error in $0\n"
    cd $startdir
    exit 1
fi

pars=(REDSHIFT NH CLNAME)

out=`get_cluster_pars $pars`
export redshift=`echo $out | awk '{print $1}'`
export nh=`echo $out | awk '{print $2}'`

echo $out
echo "redshift :: " $redshift
echo "nH ::       " $nh


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0
