#!/bin/bash

######################################################################
# updates the analysis*log and *conf file
# run after the filter module! REQUIRES manual tweaking: paths and awk
# column ids
######################################################################

######################################################################
# set paths
cat=/home/moon/rsuhada/w/xspt/wl/cat/wl-xmm-processing.tab
nhscript=/home/moon/rsuhada/data1/sw/scripts/
analysis_path=~/w/xspt/data/notes
config_path=~/w/xspt/data/configs/

# for cluster in SPT-CL-J2136-5726

for cluster in `iterlines $cat 1 1`
do

    # need to get tha basic info from a file - adjust column ids
    data=`grep $cluster $cat`
    redshift=`echo $data | awk '{print $4}'`
    ra=`echo $data | awk '{print $5}'`
    de=`echo $data | awk '{print $6}'`
    obsid=`echo $data | awk '{print $13}'`
    progid=${obsid:0:5}

    # get the nH log and values
    nhcommand="${nhscript}/getnH.sh $ra $de"
    nhval=`${nhscript}/getnH.sh $ra $de | tail -3 | head -1 | awk '{print $4}' | sed 's/E+20/E-2/g'`
    nh_line1=`${nhscript}/getnH.sh $ra $de | tail -4 | head -1`
    nh_line2=`${nhscript}/getnH.sh $ra $de | tail -3 | head -1`

    echo $cluster $redshift $ra $de $obsid $progid $nhval

    ######################################################################
    # update the analysis file
    infile=${analysis_path}/analysis-${cluster}.txt

    sed -i.bk "s/CLNAME/CLNAME ${cluster}/g" ${infile} ; rm ${infile}.bk
    sed -i.bk "s/OBSID/OBSID ${obsid}/g" ${infile} ; rm ${infile}.bk
    sed -i.bk "s/PROPOSAL_ID/PROPOSAL_ID ${progid}/g" ${infile} ; rm ${infile}.bk
    sed -i.bk "s/\bRA\b/RA ${ra}/g" ${infile} ; rm ${infile}.bk
    sed -i.bk "s/\bDE\b/DE ${de}/g" ${infile} ; rm ${infile}.bk
    sed -i.bk "s/\bRADE_SINGLE_LINE\b/RADE_SINGLE_LINE ${ra} ${de}/g" ${infile} ; rm ${infile}.bk
    sed -i.bk "s/REDSHIFT/REDSHIFT ${redshift}/g" ${infile} ; rm ${infile}.bk
    sed -i.bk "s/NH/NH ${nhval}/g" ${infile} ; rm ${infile}.bk
    sed -i.bk "s/getnH\.sh/getnH.sh $ra $de\n${nh_line1}\n${nh_line2}/g" ${infile} ; rm ${infile}.bk

    ######################################################################
    # need to change also the prefixes
    PN_EV_PREFIX_LIST=`grep "export PN_EV_PREFIX_LIST" ${infile} | tr -d \' | awk -F= '{print $2}'`
    M1_EV_PREFIX_LIST=`grep "export M1_EV_PREFIX_LIST" ${infile} | tr -d \' | awk -F= '{print $2}'`
    M2_EV_PREFIX_LIST=`grep "export M2_EV_PREFIX_LIST" ${infile} | tr -d \' | awk -F= '{print $2}'`
    MOS_EV_PREFIX_LIST="$M1_EV_PREFIX_LIST $M2_EV_PREFIX_LIST"

    # prefixes
    line="prefixes\n\n"

    pn_line="export PN_EV_PREFIX_LIST='$PN_EV_PREFIX_LIST'"
    m1_line="export M1_EV_PREFIX_LIST='$M1_EV_PREFIX_LIST'"
    m2_line="export M2_EV_PREFIX_LIST='$M2_EV_PREFIX_LIST'"
    m3_line="export MOS_EV_PREFIX_LIST='$MOS_EV_PREFIX_LIST'"
    echo $pn_line
    echo $m1_line
    echo $m2_line
    echo $m3_line

    sed -i.bk "s/prefixes/${line}\n${pn_line}\n${m1_line}\n${m2_line}\n${m3_line}/g" ${infile} ; rm ${infile}.bk

    ######################################################################
    # adjust also the .conf file
    infile=${config_path}/${cluster}.conf

    sed -i.bk "s/export RA=0.0000/export RA=${ra}/g" ${infile} ; rm ${infile}.bk
    sed -i.bk "s/export DE=-24.0000/export DE=${de}/g" ${infile} ; rm ${infile}.bk

    # # this part is no longer necessary
    # sed -i.bk "s/S003/${PN_EV_PREFIX_LIST}/g" ${infile} ; rm ${infile}.bk
    # sed -i.bk "s/1S001/${M1_EV_PREFIX_LIST}/g" ${infile} ; rm ${infile}.bk
    # sed -i.bk "s/2S002/${M2_EV_PREFIX_LIST}/g" ${infile} ; rm ${infile}.bk
    # sed -i.bk "s/1S001 2S002/${MOS_EV_PREFIX_LIST}/g" ${infile} ; rm ${infile}.bk

done