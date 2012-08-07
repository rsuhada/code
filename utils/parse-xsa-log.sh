#!/bin/bash

######################################################################
# help
if [[ $# -lt 1 ]]
then
	echo "Parse a *standard single line text list from XMM XSA*"
	echo
    echo "Parameters:"
    echo "1. xsa list (txt, single line)"
    echo ""
    echo "Syntax:"
	echo "parse-xsa-log.sh xsa-obs-list.txt"
    echo
    exit 1
fi

######################################################################
# main

tab=$1
outtab=${tab}.parsed

if [[ ! -e $tab  ]]
then
    echo "** error: input file does not exist:"
    echo "*** $tab"
fi

# pre-filter the list
grep "|" $tab | grep -v "NO PPS PRODUCTS" > ${tab}.tmp

# do the parsing
awk 'BEGIN{
FS="[ ]*[|][ ]*"
}
NR>1{ # remove header: default NR>22 wo pre-filtering with grep
gsub(/h/,":", $3)
gsub(/m/,":", $3)
gsub(/s /,"@@@", $3)
gsub(/d/,":", $3)
gsub("[:'"'"']",":", $3)
gsub(/"/,"", $3)
print $2 "@@@" $1 "@@@" $11 "@@@" $3 "@@@" $9 "@@@" $10 "@@@" $17 "@@@" $12    # @@@ is a format placeholder
}' ${tab}.tmp > ${outtab}

# fix spaces/comment strings
sed -i.bk 's/ /_/g' ${outtab} ; rm ${outtab}.bk    # remove spaces
sed -i.bk 's/@@@/ /g' ${outtab} ; rm ${outtab}.bk  # add spaces where they should be
sed -i.bk 's/-/-/g' ${outtab} ; rm ${outtab}.bk    # fix encoding inconsitency

# prepand the output table with header info
echo "# xsa_obj_name obsid obs_on_time ra60 de60 obs_start obs_end expiry_date pi_name" |cat - ${outtab} >> /tmp/out && mv /tmp/out ${outtab}

rm ${tab}.tmp

echo "...done! Output written to:"
echo ${outtab}