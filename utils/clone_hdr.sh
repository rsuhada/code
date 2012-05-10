######################################################################
# clone header of one fits to another, include everything
# FIXME: add automatic iteration through all headers

cphead ${1}+0 ${2}+0 comment=yes history=yes scale=yes
cphead ${1}+1 ${2}+1 comment=yes history=yes scale=yes