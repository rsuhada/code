#!/bin/bash

echo "id nh_dl    nh_lab"

while read line
do
    test=`echo $line | sed 's/\ //g'`
	if [[ ${test:0:1} != "#" ]]                # skip commented lines
	then

        id=`echo $line | awk '{print $1}'`
        ra=`echo $line | awk '{print $2}'`
        de=`echo $line | awk '{print $3}'`

        nh equinox=2000 ra=$ra dec=$de usemap=1 >  nh.tmp
        nh equinox=2000 ra=$ra dec=$de usemap=0 >> nh.tmp

        dl=`cat nh.tmp | grep "DL >> Weighted average nH" | awk '{print $7}'`
        lab=`cat nh.tmp | grep "LAB >> Weighted average nH" | awk '{print $7}'`
        rel_diff=`/Users/rs/bin/calc 100*\($dl - $lab\)/$dl`

        # echo $ra $de $dl $lab $rel_diff
        echo $id $dl $lab

        rm nh.tmp

    fi

done < $1


