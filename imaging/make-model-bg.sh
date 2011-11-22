######################################################################
# script calculating a model background image - either a double
# component or s pline background

dir=$1
here=`pwd`
cd $dir

######################################################################
# input parameters

srclist=$2
expvig=$3
expnovig=$4
image=$5
elo=$6
ehi=$7

# export outbg="MOS2_05_20_back.fits"
# export outbg2="MOS2_05_20_back.fits.c5"
# export outcheese="MOS2_05_20_cheese.fits"
# export outcheese2="MOS2_05_20_cheese.fits.c5"


######################################################################
# do the extraction

esplinemap boxlistset=$srclist \
	withdetmask=yes detmaskset=$outmask \
	fitmethod=model withexpimage=yes withexpimage2=yes \
	expimageset=$expvig expimageset2=$expnovig \
	imageset=$image \
	scut=0.002 withootset=no pimin=$elo pimax=$ehi \
	bkgimageset=$outbg \
	withcheese=yes withcheesemask=yes \
	cheesemaskset=$outcheese



######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0
