######################################################################
# converts a wcs ds9 region to detector coordinates
#
# writes out region descriptors needed for the pipeline
# writes out for convenience also standard ds9 region files in
# detector coords
# also added a handy output of offaxis and position angles
#
# NOTES:
# 1. only circle supported atm
# 2. only a single prefix - it is not required by the script as input

dir=$1                          # e.g. bla/analysis
region_file=$2
here=`pwd`
cd $dir

######################################################################
# converting the region file

if [[ ! -e $region_file ]]
then
    echo -e "\n** error: missing region file: $region_file"
    echo -e "*** error in script: $0\n"
    cd $startdir
    exit 1
fi

# remove previous files
rm ${region_file}.reg-pn.txt
rm ${region_file}.reg-m1.txt
rm ${region_file}.reg-m2.txt


# prepare detector coordiante region file
regheader="# Region file format: DS9 version 4.1\n# Filename: pnS005-obj-im-det-2000-7200.fits\nglobal color=green dashlist=8 3 width=1 font=\"helvetica 10 normal\" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\nphysical"

pn_det_reg=`basename ${region_file} .reg`-det-pn.reg
m1_det_reg=`basename ${region_file} .reg`-det-m1.reg
m2_det_reg=`basename ${region_file} .reg`-det-m2.reg

echo -e $regheader > $pn_det_reg
echo -e $regheader > $m1_det_reg
echo -e $regheader > $m2_det_reg


######################################################################
# read and parse the region file
exec 6<&0
exec < $region_file
read
until [ -z "$REPLY" ]
do
    line=`echo $REPLY | grep "circle"`

    if [[ $? -eq 0 ]]
    then
        line=`echo $line | sed 's/[(,),"]/,/g'`

        # parse information
        shape=`echo $line | awk -F, '{print $1}'`
        ra=`echo $line | awk -F, '{print $2}'`
        de=`echo $line | awk -F, '{print $3}'`
        radius=`echo $line | awk -F, '{print $4}'`

        # convert radius
        radius=$(echo "scale=2;20.0*$radius" | bc)

        echo $shape
        echo $ra
        echo $de
        echo $radius
        echo

        echo "###########################################" > ${region_file}.ecoords
        echo "# ${region_file}" >> ${region_file}.ecoords
        echo "###########################################" >> ${region_file}.ecoords
        echo "RA " $ra >> ${region_file}.ecoords
        echo "DE " $de >> ${region_file}.ecoords

        # RUN coordinate conversion: pn
        ecoordconv_image=`ls -1 pnS???-obj-im.fits`
        tmp=${region_file}.pn.ecoordconv

        if [[ -e $ecoordconv_image ]]
        then
            ecoordconv imageset=$ecoordconv_image x=$ra y=$de coordtype=EQPOS > $tmp

            # parse output
            detx=`grep DETX ${region_file}.pn.ecoordconv | awk '{print $3}'`
            dety=`grep DETX ${region_file}.pn.ecoordconv | awk '{print $4}'`
            theta=`grep Theta ${region_file}.pn.ecoordconv | awk '{print $3}'` # [ arcsec ]
            phi=`grep Theta ${region_file}.pn.ecoordconv | awk '{print $4}'`
            phyx=`grep "X: Y:" ${region_file}.pn.ecoordconv | awk '{print $3}'`
            phyy=`grep "X: Y:" ${region_file}.pn.ecoordconv | awk '{print $4}'`
            rawx=`grep RAWX ${region_file}.pn.ecoordconv | awk '{print $3}'`
            rawy=`grep RAWX ${region_file}.pn.ecoordconv | awk '{print $4}'`
            ccds=`grep CCD\(s\) ${region_file}.pn.ecoordconv`

            # reg file / det coords file
            echo "&&((DETX,DETY) IN ${shape}($detx,$dety,$radius))" >> ${region_file}.reg-pn.txt
            echo "${shape}($detx,$dety,$radius)" >> $pn_det_reg

            # write info file
            echo >> ${region_file}.ecoords
            echo "X_DET_PN " $detx  >> ${region_file}.ecoords
            echo "Y_DET_PN " $dety  >> ${region_file}.ecoords
            echo "X_PHY_PN " $phyx  >> ${region_file}.ecoords
            echo "Y_PHY_PN " $phyy  >> ${region_file}.ecoords
            echo "X_RAW_PN " $rawx  >> ${region_file}.ecoords
            echo "Y_RAW_PN " $rawy  >> ${region_file}.ecoords
            echo "THETA_PN " $theta >> ${region_file}.ecoords
            echo "PHI_PN "   $phi   >> ${region_file}.ecoords
            echo "CCD_PN "   $ccds  >> ${region_file}.ecoords

        else
            echo -e "\n** error: missing pn image!"
            echo -e "*** error in script: $0\n"
        fi


        # run coordinate conversion: m1
        ecoordconv_image=`ls -1 mos1S???-obj-im.fits`
        tmp=${region_file}.m1.ecoordconv

        if [[ -e $ecoordconv_image ]]
        then
            ecoordconv imageset=$ecoordconv_image x=$ra y=$de coordtype=EQPOS > $tmp
            # parse output
            detx=`grep DETX ${region_file}.m1.ecoordconv | awk '{print $3}'`
            dety=`grep DETX ${region_file}.m1.ecoordconv | awk '{print $4}'`
            theta=`grep Theta ${region_file}.m1.ecoordconv | awk '{print $3}'` # [ arcsec ]
            phi=`grep Theta ${region_file}.m1.ecoordconv | awk '{print $4}'`
            phyx=`grep "X: Y:" ${region_file}.m1.ecoordconv | awk '{print $3}'`
            phyy=`grep "X: Y:" ${region_file}.m1.ecoordconv | awk '{print $4}'`
            rawx=`grep RAWX ${region_file}.m1.ecoordconv | awk '{print $3}'`
            rawy=`grep RAWX ${region_file}.m1.ecoordconv | awk '{print $4}'`
            ccds=`grep CCD\(s\) ${region_file}.m1.ecoordconv`

            echo "&&((DETX,DETY) IN ${shape}($detx,$dety,$radius))" >> ${region_file}.reg-m1.txt
            echo "${shape}($detx,$dety,$radius)" >> $m1_det_reg

            # write info file
            echo >> ${region_file}.ecoords
            echo "X_DET_M1 " $detx  >> ${region_file}.ecoords
            echo "Y_DET_M1 " $dety  >> ${region_file}.ecoords
            echo "X_PHY_M1 " $phyx  >> ${region_file}.ecoords
            echo "Y_PHY_M1 " $phyy  >> ${region_file}.ecoords
            echo "X_RAW_M1 " $rawx  >> ${region_file}.ecoords
            echo "Y_RAW_M1 " $rawy  >> ${region_file}.ecoords
            echo "THETA_M1 " $theta >> ${region_file}.ecoords
            echo "PHI_M1 "   $phi   >> ${region_file}.ecoords
            echo "CCD_M1 "   $ccds  >> ${region_file}.ecoords

        else
            echo -e "\n** error: missing m1 image!"
            echo -e "*** error in script: $0\n"
        fi


        # run coordinate conversion: m2
        ecoordconv_image=`ls -1 mos2S???-obj-im.fits`
        tmp=${region_file}.m2.ecoordconv

        if [[ -e $ecoordconv_image ]]
        then
            ecoordconv imageset=$ecoordconv_image x=$ra y=$de coordtype=EQPOS > $tmp
            # parse output
            detx=`grep DETX ${region_file}.m2.ecoordconv | awk '{print $3}'`
            dety=`grep DETX ${region_file}.m2.ecoordconv | awk '{print $4}'`
            theta=`grep Theta ${region_file}.m2.ecoordconv | awk '{print $3}'`    # [ arcsec ]
            phi=`grep Theta ${region_file}.m2.ecoordconv | awk '{print $4}'`
            phyx=`grep "X: Y:" ${region_file}.m2.ecoordconv | awk '{print $3}'`
            phyy=`grep "X: Y:" ${region_file}.m2.ecoordconv | awk '{print $4}'`
            rawx=`grep RAWX ${region_file}.m2.ecoordconv | awk '{print $3}'`
            rawy=`grep RAWX ${region_file}.m2.ecoordconv | awk '{print $4}'`
            ccds=`grep CCD\(s\) ${region_file}.m2.ecoordconv`
            echo "&&((DETX,DETY) IN ${shape}($detx,$dety,$radius))" >> ${region_file}.reg-m2.txt
            echo "${shape}($detx,$dety,$radius)" >> $m2_det_reg

            # write info file
            echo >> ${region_file}.ecoords
            echo "X_DET_M2 " $detx  >> ${region_file}.ecoords
            echo "Y_DET_M2 " $dety  >> ${region_file}.ecoords
            echo "X_PHY_M2 " $phyx  >> ${region_file}.ecoords
            echo "Y_PHY_M2 " $phyy  >> ${region_file}.ecoords
            echo "X_RAW_M2 " $rawx  >> ${region_file}.ecoords
            echo "Y_RAW_M2 " $rawy  >> ${region_file}.ecoords
            echo "THETA_M2 " $theta >> ${region_file}.ecoords
            echo "PHI_M2 "   $phi   >> ${region_file}.ecoords
            echo "CCD_M2 "   $ccds  >> ${region_file}.ecoords
            echo "###########################################" >> ${region_file}.ecoords

        else
            echo -e "\n** error: missing m2 image!"
            echo -e "*** error in script: $0\n"
        fi

    fi


	read
done
exec 0<&6 6<&-


######################################################################
# exit

cd $here

echo -e "\nDetector coordinate region descriptors:"
echo ${region_file}.reg-pn.txt
echo ${region_file}.reg-m1.txt
echo ${region_file}.reg-m2.txt
echo

echo -e "\nDetector coordinate region file:"
echo $pn_det_reg
echo $m1_det_reg
echo $m2_det_reg
echo

echo "Coordinate summary list:"
echo  ${region_file}.ecoords

# add output to analysis note file
echo >> ${NOTESFILE}
cat ${region_file}.ecoords | tee -a ${NOTESFILE}

echo -e "\n$0 in $obsid done!"
exit 0


