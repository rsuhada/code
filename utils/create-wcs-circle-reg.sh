# simple script to create a circle region for analysis

id=$1
ra=$2
de=$3

echo "

# Region file format: DS9 version 4.1
# Filename: dummy.fits
global color=green font=\"helvetica 10 normal\" select=1 highlite=1 edit=1 move=1 delete=1 include=1 fixed=0 source=1
fk5
circle($ra, $de, 60\") # color=green width=2 font=\"helvetica 24 normal\" text={$id}

"