######################################################################
# extract arf for spectroscopy

######################################################################
# inputs

instrument=$1
spectrumid=$2
specdir=$3
ra=$4
de=$5


######################################################################
# select the eventlist and the selection pattern
case $instrument in
    "pn")
        prefix=$PN_EV_PREFIX_LIST
        evlist=pn${prefix}-clean.fits
        ootevlist=pn${prefix}-clean-oot.fits
        ;;
    "m1")
        prefix=$M1_EV_PREFIX_LIST
        evlist=mos${prefix}-clean.fits
        ;;
    "m2")
        prefix=$M2_EV_PREFIX_LIST
        evlist=mos${prefix}-clean.fits
        ;;
    *)
        echo "unknown instrument!"
        exit 1
esac


######################################################################
# extraction

# the quickspec version
export set="badpixelresolution=2 crossregionarf=no detmaptype=dataset extendedsource=yes filterdss=yes filteredset=filteredpixellist.ds ignoreoutoffov=yes keeparfset=yes modelee=no modeleffarea=yes modelfiltertrans=yes modelootcorr=no modelquantumeff=yes psfenergy=2 setbackscale=no sourcecoords="eqpos" sourcex=${ra} sourcey=${de} useodfatt=no withbadpixcorr=yes withdetbounds=no withfilteredset=no withrmfset=yes withsourcepos=yes"

export set="badpixelresolution=2 crossregionarf=no detmaptype=dataset extendedsource=yes filterdss=yes filteredset=filteredpixellist.ds ignoreoutoffov=yes keeparfset=yes modelee=no modeleffarea=yes modelfiltertrans=yes modelootcorr=no modelquantumeff=yes psfenergy=2 setbackscale=no sourcecoords="eqpos" sourcex=0 sourcey=0 useodfatt=no withbadpixcorr=yes withdetbounds=no withfilteredset=no withrmfset=yes withsourcepos=no"

arfgen spectrumset=${specdir}/${instrument}-${spectrumid}.pha $set rmfset=${specdir}/${instrument}-${spectrumid}.rmf badpixlocation=${evlist} detmaparray=${specdir}/${instrument}-${spectrumid}-detmap.ds arfset=${specdir}/${instrument}-${spectrumid}.arf
