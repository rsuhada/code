######################################################################
# extract rmf for spectroscopy

######################################################################
# inputs

instrument=$1
spectrumid=$2
specdir=$3
ra=$4
de=$5

######################################################################
# extraction

rmfgen spectrumset=${specdir}/${instrument}-${spectrumid}.pha rmfset=${specdir}/${instrument}-${spectrumid}.rmf detmaptype=flat  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}

