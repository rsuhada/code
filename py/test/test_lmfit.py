import lmfit
import numpy as np

x=np.linspace(0.3,10,100)
y=1/(0.1*x)+2+0.1*np.random.randn(x.size)

p=lmfit.Parameters()
p.add_many(('a',0.1),('b',1))

def residual(p):
    a=p['a'].value
    b=p['b'].value
    return 1/(a*x)+b-y

# We have to fit it, before we can generate the confidence intervals.

mi=lmfit.minimize(residual, p)
mi.leastsq()

# lmfit.printfuncs.report_errors(mi.params)
  # a:     0.099993 +/- 0.000210 (0.21%) initial =  0.100000
  # b:     2.007299 +/- 0.013129 (0.65%) initial =  1.000000
# Correlations:
    # C(a, b)                      =  0.601
# Now it just a simple function call to start the calculation:



# ci=lmfit.conf_interval(mi)
# lmfit.printfuncs.report_ci(ci)
