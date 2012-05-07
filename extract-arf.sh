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
# extraction


# WITH VIG CORR!!!!!!!!!!!! -> special purpose  - if you use: 1. local bg & 2. zcolumn of spectra is "NO"
# export set="withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de} withrmfset=true withdetbounds=yes extendedsource=yes detmaptype=flat filterdss=no detxbins=10 detybins=10 modelee=N withbadpixcorr=N modeleffarea=Y modelquantumeff=Y modelfiltertrans=Y"
# arfgen spectrumset=${specdir}/${instrument}-${spectrumid}.pha $set rmfset=${specdir}/${instrument}-${spectrumid}.rmf arfset=${specdir}/${instrument}-${spectrumid}.arf


case ${instrument} in
    "pn")
        EV_PREFIX=pn"$PN_EV_PREFIX_LIST"
    ;;
    "m1")
        EV_PREFIX=mos"$M1_EV_PREFIX_LIST"
    ;;
    "m2")
        EV_PREFIX=mos"$M2_EV_PREFIX_LIST"
    ;;
    *)
        echo "** error in $0"
        echo "*** unknown instrument: ${instrument}"
        exit 1
    ;;
esac

export set="badpixelresolution=2 crossregionarf=no detmaptype=dataset extendedsource=yes filterdss=no filteredset=filteredpixellist.ds ignoreoutoffov=yes keeparfset=yes modelee=no modeleffarea=yes modelfiltertrans=yes modelootcorr=no modelquantumeff=yes psfenergy=2 setbackscale=no sourcecoords=eqpos sourcex=${ra} sourcey=${de} useodfatt=no withbadpixcorr=yes withdetbounds=no withfilteredset=no withrmfset=yes withsourcepos=no"

echo arfgen spectrumset=${specdir}/${instrument}-${spectrumid}.pha $set rmfset=${specdir}/${instrument}-${spectrumid}.rmf arfset=${specdir}/${instrument}-${spectrumid}.arf badpixlocation=${EV_PREFIX}-clean.fits detmaparray=${specdir}/${instrument}-${spectrumid}-detmap.ds

arfgen spectrumset=${specdir}/${instrument}-${spectrumid}.pha $set rmfset=${specdir}/${instrument}-${spectrumid}.rmf arfset=${specdir}/${instrument}-${spectrumid}.arf badpixlocation=${EV_PREFIX}-clean.fits detmaparray=${specdir}/${instrument}-${spectrumid}-detmap.ds
