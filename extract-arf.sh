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
export set="withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de} withrmfset=true withdetbounds=yes extendedsource=yes detmaptype=flat filterdss=no detxbins=10 detybins=10 modelee=N withbadpixcorr=N modeleffarea=Y modelquantumeff=Y modelfiltertrans=Y"

arfgen spectrumset=${specdir}/${instrument}-${spectrumid}.pha $set rmfset=${specdir}/${instrument}-${spectrumid}.rmf arfset=${specdir}/${instrument}-${spectrumid}.arf
