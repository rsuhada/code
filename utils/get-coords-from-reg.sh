######################################################################
# extracts coords from existin reg files,
# INPUT: region ID (bar wcs id and suffix, standard naming)

# reg=cluster-man-01
reg=$1

######################################################################
# wcs
file=${reg}.wcs.reg

if [[ -e ${file} ]]
then

    RA=`grep circle ${reg}.wcs.reg | sed 's/circle(//g' | sed 's/)//g' | awk -F, '{print $1}'`
    DE=`grep circle ${reg}.wcs.reg | sed 's/circle(//g' | sed 's/)//g' | awk -F, '{print $2}'`

    echo
    echo "RA ${RA}"
    echo "DE ${DE}"

fi

######################################################################
# wcs60
file=${reg}.wcs60.reg

if [[ -e ${file} ]]
then

    RA60=`grep circle ${reg}.wcs60.reg | sed 's/circle(//g' | sed 's/)//g' | awk -F, '{print $1}'`
    DE60=`grep circle ${reg}.wcs60.reg | sed 's/circle(//g' | sed 's/)//g' | awk -F, '{print $2}'`

    echo
    echo "RA60 ${RA60}"
    echo "DE60 ${DE60}"

fi

######################################################################
# phy
file=${reg}.phy.reg

if [[ -e ${file} ]]
then

    X_PHY=`grep circle ${reg}.phy.reg | sed 's/circle(//g' | sed 's/)//g' | awk -F, '{print $1}'`
    Y_PHY=`grep circle ${reg}.phy.reg | sed 's/circle(//g' | sed 's/)//g' | awk -F, '{print $2}'`

    echo
    echo "X_PHY ${X_PHY}"
    echo "Y_PHY ${Y_PHY}"

fi

######################################################################
# im
file=${reg}.im.reg

if [[ -e ${file} ]]
then

    X_IM=`grep circle ${reg}.im.reg | sed 's/circle(//g' | sed 's/)//g' | awk -F, '{print $1}'`
    Y_IM=`grep circle ${reg}.im.reg | sed 's/circle(//g' | sed 's/)//g' | awk -F, '{print $2}'`

    echo
    echo "X_IM ${X_IM}"
    echo "Y_IM ${Y_IM}"

fi

echo