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

# rmfgen spectrumset=${specdir}/${instrument}-${spectrumid}.pha rmfset=${specdir}/${instrument}-${spectrumid}.rmf detmaptype=flat  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}

# no source position is SAS and esas default
rmfgen spectrumset=${specdir}/${instrument}-${spectrumid}.pha rmfset=${specdir}/${instrument}-${spectrumid}.rmf detmaptype=$detmaptype detmaparray=$detmaparray withsourcepos=no sourcecoords="eqpos" sourcex=${ra} sourcey=${de}
