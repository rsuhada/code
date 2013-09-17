if [ $# -lt 1 ]
then
	echo "Creates a DS9 region file from a fits table."
	echo
	echo "Fits table has to have a RA and DEC column (hardcoded)"
	echo "REG specification : DS9/funtools, wcs, fk5"
	echo
	echo "Syntax:"
	echo "fcat2reg file.fits [RADIUS COLUMNAME COLOR]"
    echo
    echo "RADIUS - (optional) circle radius in asec, default 6 asec"
    echo "COLUMNAME - (optional) for REG text e.g. ID"
    echo "COLOR - (optional) color of the source regs, default green"
    echo "RA - (optional) name of the ra column"
    echo "DEC - (optional) name of the dec column"
    echo
else

if [ $# -lt 2 ]
then
    rad=6
else
    rad=$2
fi

if [ $# -lt 4 ]
then
    color=green
else
    color=$4
fi

if [ $# -lt 6 ]
then
    coords="RA DEC $3"
else
    coords="$5 $6 $3"
fi
	export fcat=$1
	echo "...dumping fits to ASCII temporary"

	#--------------------------------------------------------------------
	fdump $fcat $fcat.temporary \
	fldsep=" " prhead=no align=yes wrap=no clobber=yes rows=- showrow=no \
	showcol=no showunit=no \
	column="$coords"
	# column="RA DEC $3"

	echo $3

	#--------------------------------------------------------------------
	echo '# Region file format: DS9 version 4.0' > $fcat.reg
	echo 'global color='$color' font="helvetica 10 normal" select=1 highlite=1 edit=1 move=1 delete=1 include=1 fixed=0 source' >> $fcat.reg
	echo 'fk5' >> $fcat.reg
	awk '{print "circle("$1","$2",'$rad'\") # width=3 font=\"helvetica 10 normal\" text={"$3"}"}' < $fcat.temporary | grep -v '\,\,' | uniq >> $fcat.reg

	#--------------------------------------------------------------------
	rm $fcat.temporary
	echo
	echo "...Done!"
	echo "...REG file writen to :: $fcat.reg"

fi
