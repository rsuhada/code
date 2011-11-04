######################################################################
# library of utility functions

function get_cluster_pars {

    ######################################################################
    # looks through an analysis notebook file returning the requested
    # parameters. Input is an array, e.g.  pars=(RA DE RA60
    # DE60 X_IM Y_IM X_PHY Y_PHY NH REDSHIFT), output is a string

    if [[ -e $NOTESFILE ]]
    then

        pars=$1
        declare -a values

        for i in ${!pars[@]}
        do
            val=`grep ${pars[i]} $NOTESFILE | head -1 | awk '{print $2}'`
            values=( "${values[@]}" "$val" )
            # echo ${pars[i]} ${values[i]}
        done

        # this is the output
        echo ${values[@]}

    else
        echo "$NOTESFILE does not exist, not returning parameters!"
    fi
}


function make_src_reg_file {
    ######################################################################
    # write a ds9 region file
    # supports wcs and physical coords
    # supports circle and annnulus shapes (easily extensible to other)

    shape=$1
    regname=$2
    coords=$3
    x=$4
    y=$5
    radius=$6
    radius2=$7

    echo $shape
    echo $regname
    echo $coords
    echo $x
    echo $y
    echo $radius
    echo $radius2

    ######################################################################
    # resolve coordinate system

    if [[ "$coords" == "phy" || "$coords" == "physical" ]]
    then
        coords="physical"
        units=''
    fi

    if [[ "$coords" == "wcs" || "$coords" == "fk5" ]]
    then
        coords="fk5"
        units='"'
    fi

    ######################################################################
    # resolve region shape

    case $shape in
        "annulus")
            regionexpression="${shape}($x,$y,${radius}${units},${radius2}${units})"
            ;;
        "circle")
            regionexpression="${shape}($x,$y,${radius}${units})"
            ;;
        *)
            regionexpression="${shape}($x,$y,${radius}${units})"
            echo "Unknown shape, using circle"
    esac

    ######################################################################
    # write the region file

    (
    echo "# Region file format: DS9 version 4.1"
    echo global color=green dashlist=8 3 width=1 font=\"helvetica 10 normal\" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1
    echo $coords
    echo $regionexpression

    ) > $regname

    echo "Written region file: " $regname

}


function ds9reg_to_sasdesc {
    ######################################################################
    # parse a ds9 region file to create a SAS descriptor file

    inreg=$1                    # ds9 region file
    remove=$2                   # [ 0/1 ] should I remove these regions?

    if [[ $# != 2 ]]
    then
        echo "missing second parameter! 1 = this should be an active region, 0 = remove these regions"
        exit 1
    fi

    # if [[ -e ${inreg}.desc ]]
    # then
    #     echo "backuping region file ${inreg}.desc"
    #     mv ${inreg}.desc ${inreg}.desc.bk
    # fi

    if [[ $remove -eq 0 ]]
    then

        egrep "circle" $inreg | tr -d "\-circle(" | tr -d ")" | awk '{print "&&! circle("$1",X,Y)"}' | tr '\n' ' ' > ${inreg}.desc

    else

        egrep "circle" $inreg | tr -d "\-circle(" | tr -d ")" | awk '{print "circle("$1",X,Y)"}' | tr '\n' ' ' > ${inreg}.desc

        egrep "annulus" $inreg | tr -d "\-annulus(" | tr -d ")" | awk '{print "annulus("$1",X,Y)"}' | tr '\n' ' ' >> ${inreg}.desc

    fi

    echo "Done parsing file $inreg"

    ls ${inreg}.desc
}