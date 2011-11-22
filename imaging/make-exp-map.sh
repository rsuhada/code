######################################################################
# script extracting vignetted and unvignetted exposure maps for the
# imaging pipe

dir=$1
here=`pwd`
cd $dir

######################################################################
# do the extraction

prefix=$MOS_EV_PREFIX_LIST

inevli=$2
image=$3
expmap=$4
elo=$5
ehi=$6
vignetting=$7



prefix=$PN_EV_PREFIX_LIST
elow='500'     # detection bands minima [eV]
ehigh='2000'    # detection bands maxima [eV]
regfile=$PN_SRC_REGFILE
pattern=4
quad1=$PN_QUAD1
quad2=$PN_QUAD2
quad3=$PN_QUAD3
quad4=$PN_QUAD4
evselect table=pnS003-clean.fits:EVENTS withfilteredset=yes expression='(PATTERN <= 4)&&(FLAG == 0)&&((CCDNR == 1)||(CCDNR == 2)||(CCDNR == 3)||(CCDNR == 4)||(CCDNR == 5)||(CCDNR == 6)||(CCDNR == 7)||(CCDNR == 8)||(CCDNR == 9)||(CCDNR == 10)||(CCDNR == 11)||(CCDNR == 12))&&((DETX,DETY) in BOX(-2196,-1110,16060,15510,0)) &&region(pnS003-bkg_region-sky.fits)&&((DETX,DETY) IN circle(-2200,-1110,17980))&&(PI in [400:1250])' filtertype=expression imagebinning='imageSize' imagedatatype='Int32' imageset=pnS003-obj-im-400-1250.fits squarepixels=yes withxranges=yes withyranges=yes xcolumn='X' ximagesize=900 ximagemax=48400 ximagemin=3401 ycolumn='Y' yimagesize=900 yimagemax=48400  yimagemin=3401 updateexposure=yes filterexposure=yes ignorelegallimits=yes


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0
