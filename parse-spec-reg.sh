######################################################################
# parse a ds9 region file to create a descriptor file

inreg=$1
remove=$2

if [[ $# != 2 ]]
then
    echo "\nmissing second parameter! 1 = this should be an active region, 0 = remove these regions"
    exit 1
fi

if [[ -e ${inreg}.desc ]]
then
    echo "backuping region file ${inreg}.desc"
    mv ${inreg}.desc ${inreg}.desc.bk
fi


if [[ $remove -eq 0 ]]
then

    egrep "circle"  $inreg | tr -d "\-circle(" | tr -d ")" | awk '{print "&&! circle("$1",X,Y)"}' | tr '\n' ' ' > ${inreg}.desc

    egrep "polygon"  $inreg | tr -d "\-polygon(" | tr -d ")" | awk '{print "&&! polygon("$1",X,Y)"}' | tr '\n' ' ' >> ${inreg}.desc

    egrep "ellipse"  $inreg | tr -d "\-ellipse(" | tr -d ")" | awk '{print "&&! ellipse("$1",X,Y)"}' | tr '\n' ' ' >> ${inreg}.desc


else

    egrep "circle"  $inreg | tr -d "\-circle(" | tr -d ")" | awk '{print "circle("$1",X,Y)"}' | tr '\n' ' ' > ${inreg}.desc

    egrep "annulus"  $inreg | tr -d "\-annulus(" | tr -d ")" | awk '{print "annulus("$1",X,Y)"}' | tr '\n' ' ' >> ${inreg}.desc

    egrep "polygon"  $inreg | tr -d "\-polygon(" | tr -d ")" | awk '{print "polygon("$1",X,Y)"}' | tr '\n' ' ' >> ${inreg}.desc

    egrep "ellipse"  $inreg | tr -d "\-ellipse(" | tr -d ")" | awk '{print "ellipse("$1",X,Y)"}' | tr '\n' ' ' >> ${inreg}.desc

fi

echo "Done parsing file $inreg"

ls ${inreg}.desc