#!/bin/bash
if [ $# -lt 1 ]
then
	echo "Tests, if observation has a residual quiescent soft proton contamination"
	echo
    echo
	echo "Syntax:"
	echo "fifo.sh my_obs_dir"
	echo
	echo "NOTES:"
	echo
	echo "1. directory should have a standard dcp naming tree"
    echo "2. based on de Luca & Molendi 2004, using ~/data1/sw/misc/Fin_over_Fout"
    echo "   their code was improved to account for new hot PN column"
else

# m1ev      - MOS1 event file (N = ignore)
# m2ev      - MOS2 event file (N = ignore)
# pnev      - pn event file (N = ignore)
# elo       - low-energy threshold [eV] (N = use recommended default values)
# ehi       - high-energy threshold [eV] (N = use recommended default values)
# keepfiles - keep intermediate files (Y/N?)
# outfile   - ouput file name (N = just output to screen)
#
# e.g. ./Fin_over_Fout myM1ev.fits myM2ev.fits N 7000 12000 Y MyFinFout.dat


dir=$1

# ~/data1/sw/misc/Fin_over_Fout $dir/MOS/MOS1_clevents2.fits $dir/MOS/MOS2_clevents2.fits $dir/PN/PN_clevents2.fits \

Fin_over_Fout $dir/analysis/mos1[S,U]*-clean.fits $dir/analysis/mos2[S,U]*-clean.fits $dir/analysis/pn[S,U]*-clean.fits \
N N N fifo_$dir.txt


Fin_over_Fout $dir/analysis/mos1U*-clean.fits $dir/analysis/mos2U*-clean.fits $dir/analysis/pnS*-clean.fits \
N N N fifo_$dir.txt


# for id in U S
# do


#     echo ~/data1/sw/misc/Fin_over_Fout $dir/analysis/mos1${id}*-clean.fits $dir/analysis/mos2${id}*-clean.fits $dir/analysis/pn${id}*-clean.fits \
# N N N fifo_$dir.txt

#     ~/data1/sw/misc/Fin_over_Fout $dir/analysis/mos1${id}*-clean.fits $dir/analysis/mos2${id}*-clean.fits $dir/analysis/pn${id}*-clean.fits \
# N N N fifo_$dir.txt

# done

fi
