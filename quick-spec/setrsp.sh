# path
# /data05s/archtheo/rsuhada/lab/xdcp/gwp/xspec-2/
# /data05s/archtheo/rsuhada/lab/xdcp/gwp/xspec-2/
# /data05s/archtheo/rsuhada/lab/xdcp/gwp/xspec-2/


# bg
# spobs_M1_gnfwcs_bkg.b.c.pha
# spobs_M2_gnfwcs_bkg.b.c.pha
# spobs_PN_gnfwcs_bkg.ob.c.pha

# fparkey 'M1.rsp'  spobs_M1_gnfwcs_bkg.b.c.pha[1] RESPFILE
# fparkey 'M2.rsp'  spobs_M2_gnfwcs_bkg.b.c.pha[1] RESPFILE
# fparkey 'PN.rsp' spobs_PN_gnfwcs_bkg.ob.c.pha[1] RESPFILE
#
# fparkey 'spbkg_M1_gnfwcs_soue.pha'  spobs_M1_gnfwcs_bkg.b.c.pha[1] BACKFILE
# fparkey 'spbkg_M2_gnfwcs_soue.pha'  spobs_M2_gnfwcs_bkg.b.c.pha[1] BACKFILE
# fparkey 'spbkg_PN_gnfwcs_soue.pha' spobs_PN_gnfwcs_bkg.ob.c.pha[1] BACKFILE

# source
# fparkey 'M1.rsp'  spobs_M1_gnfwcs_sou40.b.c.pha[1] RESPFILE
# fparkey 'M2.rsp'  spobs_M2_gnfwcs_sou40.b.c.pha[1] RESPFILE
# fparkey 'PN.rsp'  spobs_PN_gnfwcs_sou40.ob.c.pha[1] RESPFILE
#
# fparkey 'M1.rsp'  spbkg_M1_gnfwcs_sou40.pha[1] RESPFILE
# fparkey 'M2.rsp'  spbkg_M2_gnfwcs_sou40.pha[1] RESPFILE
# fparkey 'PN.rsp'  spbkg_PN_gnfwcs_sou40.pha[1] RESPFILE

fparkey 'm1.rsp'  m1.pha[1] RESPFILE
fparkey 'm2.rsp'  m2.pha[1] RESPFILE
fparkey 'pn.rsp'  pn.pha[1] RESPFILE

fparkey 'm1.rsp'  m1.grp.pha[1] RESPFILE
fparkey 'm2.rsp'  m2.grp.pha[1] RESPFILE
fparkey 'pn.rsp'  pn.grp.pha[1] RESPFILE

fparkey 'm1_locbg.rsp'  m1_locbg.pha[1] RESPFILE
fparkey 'm2_locbg.rsp'  m2_locbg.pha[1] RESPFILE
fparkey 'pn_locbg.rsp'  pn_locbg.pha[1] RESPFILE

fparkey 'm1_locbg.rsp'  m1_locbg.grp.pha[1] RESPFILE
fparkey 'm2_locbg.rsp'  m2_locbg.grp.pha[1] RESPFILE
fparkey 'pn_locbg.rsp'  pn_locbg.grp.pha[1] RESPFILE
