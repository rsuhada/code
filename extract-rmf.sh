######################################################################
# extract rmf for spectroscopy

######################################################################
# inputs

instrument=$1
spectrumid=$2
specdir=$3
ra=$4
de=$5
detmaptype=$6
detmaparray=$7

######################################################################
# extraction

if [[ "$detmaptype" == "flat" ]]
then
    rmfgen spectrumset=${specdir}/${instrument}-${spectrumid}.pha rmfset=${specdir}/${instrument}-${spectrumid}.rmf detmaptype=flat  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}
fi

if [[ "$detmaptype" == "psf" ]]
then
    rmfgen spectrumset=${specdir}/${instrument}-${spectrumid}.pha rmfset=${specdir}/${instrument}-${spectrumid}.rmf detmaptype=psf  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}
fi

if [[ "$detmaptype" == "dataset" ]]
then
    rmfgen spectrumset=${specdir}/${instrument}-${spectrumid}.pha rmfset=${specdir}/${instrument}-${spectrumid}.rmf detmaptype=dataset withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de} detmaparray=$detmaparray
fi