"""
This is the minimizers.py of lmfit adjusted for my needs.

Based on lmfit v0.7. for use - replace minimizer.py with this script
(don't forget to remove minimizer.pyc)

Changes should be pushed to the original.

The original minimizer.py is part of the lmfit package developed by:
   Copyright (c) 2011 Matthew Newville, The University of Chicago
   <newville@cars.uchicago.edu>

Changelog:

2013-06-13: added interface to fmin (nelde-mead) and fixed a small bug
for keyword passing.
"""



from numpy import array, dot, eye, ndarray, ones_like, sqrt, take, transpose, triu
from numpy.dual import inv
from numpy.linalg import LinAlgError

from scipy.optimize import leastsq as scipy_leastsq
from scipy.optimize import fmin as scipy_fmin
from scipy.optimize import lbfgsb as scipy_lbfgsb
from scipy.optimize import anneal as scipy_anneal


class Minimizer(object):
    """general minimizer"""
    err_nonparam = \
     "params must be a minimizer.Parameters() instance or list of Parameters()"
    err_maxfev   = """Too many function calls (max set to  %i)!  Use:
    minimize(func, params, ...., maxfev=NNN)
or set  leastsq_kws['maxfev']  to increase this maximum."""

    def __init__(self, userfcn, params, fcn_args=None, fcn_kws=None,
                 iter_cb=None, scale_covar=True, **kws):
        self.userfcn = userfcn
        self.userargs = fcn_args
        if self.userargs is None:
            self.userargs = []

        self.userkws = fcn_kws
        if self.userkws is None:
            self.userkws = {}
        self.kws = kws
        self.iter_cb = iter_cb
        self.scale_covar = scale_covar
        self.nfev = 0
        self.nfree = 0
        self.message = None
        self.var_map = []
        self.jacfcn = None
        self.asteval = Interpreter()
        self.namefinder = NameFinder()
        self.__prepared = False
        self.__set_params(params)
        self.prepare_fit()

    def __update_paramval(self, name):
        """
        update parameter value, including setting bounds.
        For a constrained parameter (one with an expr defined),
        this first updates (recursively) all parameters on which
        the parameter depends (using the 'deps' field).
       """
        # Has this param already been updated?
        # if this is called as an expression dependency,
        # it may have been!
        if self.updated[name]:
            return
        par = self.params[name]
        if par.expr is not None:
            for dep in par.deps:
                self.__update_paramval(dep)
            par.value = self.asteval.run(par.ast)
            out = check_ast_errors(self.asteval.error)
            if out is not None:
                self.asteval.raise_exception(msg=msg)
        self.asteval.symtable[name] = par.value
        self.updated[name] = True

    def update_constraints(self):
        """update all constrained parameters, checking that
        dependencies are evaluated as needed."""
        self.updated = dict([(name, False) for name in self.params])
        for name in self.params:
            self.__update_paramval(name)

    def __residual(self, fvars):
        """
        residual function used for least-squares fit.
        With the new, candidate values of fvars (the fitting variables),
        this evaluates all parameters, including setting bounds and
        evaluating constraints, and then passes those to the
        user-supplied function to calculate the residual.
        """
        # set parameter values
        for varname, val in zip(self.var_map, fvars):
            # self.params[varname].value = val
            par = self.params[varname]
            par.value = par.from_internal(val)
        self.nfev = self.nfev + 1

        self.update_constraints()
        out = self.userfcn(self.params, *self.userargs, **self.userkws)
        if hasattr(self.iter_cb, '__call__'):
            self.iter_cb(self.params, self.nfev, out,
                         *self.userargs, **self.userkws)
        return out

    def __jacobian(self, fvars):
        """
        analytical jacobian to be used with the Levenberg-Marquardt

        modified 02-01-2012 by Glenn Jones, Aberystwyth University
        """
        for varname, val in zip(self.var_map, fvars):
            # self.params[varname].value = val
            self.params[varname].from_internal(val)

        self.nfev = self.nfev + 1
        self.update_constraints()
        # computing the jacobian
        return self.jacfcn(self.params, *self.userargs, **self.userkws)

    def __set_params(self, params):
        """ set internal self.params from a Parameters object or
        a list/tuple of Parameters"""
        if params is None or isinstance(params, Parameters):
            self.params = params
        elif isinstance(params, (list, tuple)):
            _params = Parameters()
            for _par in params:
                if not isinstance(_par, Parameter):
                    raise MinimizerException(self.err_nonparam)
                else:
                    _params[_par.name] = _par
            self.params = _params
        else:
            raise MinimizerException(self.err_nonparam)


    def prepare_fit(self, params=None):
        """prepare parameters for fit"""
        # determine which parameters are actually variables
        # and which are defined expressions.
        if params is None and self.params is not None and self.__prepared:
            return
        if params is not None and self.params is None:
            self.__set_params(params)
        self.nfev = 0
        self.var_map = []
        self.vars = []
        self.vmin, self.vmax = [], []
        for name, par in self.params.items():
            if par.expr is not None:
                par.ast = self.asteval.parse(par.expr)
                check_ast_errors(self.asteval.error)
                par.vary = False
                par.deps = []
                self.namefinder.names = []
                self.namefinder.generic_visit(par.ast)
                for symname in self.namefinder.names:
                    if (symname in self.params and
                        symname not in par.deps):
                        par.deps.append(symname)
            elif par.vary:
                self.var_map.append(name)
                self.vars.append(par.setup_bounds())
                # self.vars.append(par.set_internal_value())
                #self.vmin.append(par.min)
                #self.vmax.append(par.max)

            self.asteval.symtable[name] = par.value
            par.init_value = par.value
            if par.name is None:
                par.name = name

        self.nvarys = len(self.vars)

        # now evaluate make sure initial values
        # are used to set values of the defined expressions.
        # this also acts as a check of expression syntax.
        self.update_constraints()
        self.__prepared = True

    def leastsq(self, scale_covar=True, **kws):
        """
        use Levenberg-Marquardt minimization to perform fit.
        This assumes that ModelParameters have been stored,
        and a function to minimize has been properly set up.

        This wraps scipy.optimize.leastsq, and keyward arguments are passed
        directly as options to scipy.optimize.leastsq

        When possible, this calculates the estimated uncertainties and
        variable correlations from the covariance matrix.

        writes outputs to many internal attributes, and
        returns True if fit was successful, False if not.
        """
        self.prepare_fit()
        lskws = dict(full_output=1, xtol=1.e-7, ftol=1.e-7,
                     gtol=1.e-7, maxfev=2000*(self.nvarys+1), Dfun=None)

        lskws.update(self.kws)
        lskws.update(kws)

        if lskws['Dfun'] is not None:
            self.jacfcn = lskws['Dfun']
            lskws['Dfun'] = self.__jacobian

        lsout = scipy_leastsq(self.__residual, self.vars, **lskws)
        _best, _cov, infodict, errmsg, ier = lsout

        self.residual = resid = infodict['fvec']

        self.ier = ier
        self.lmdif_message = errmsg
        self.message = 'Fit succeeded.'
        self.success = ier in [1, 2, 3, 4]

        if ier == 0:
            self.message = 'Invalid Input Parameters.'
        elif ier == 5:
            self.message = self.err_maxfev % lskws['maxfev']
        else:
            self.message = 'Tolerance seems to be too small.'

        self.nfev =  infodict['nfev']
        self.ndata = len(resid)

        sum_sqr = (resid**2).sum()
        self.chisqr = sum_sqr
        self.nfree = (self.ndata - self.nvarys)
        self.redchi = sum_sqr / self.nfree

        # need to map _best values to params, then calculate the
        # grad for the variable parameters
        grad = ones_like(_best)
        vbest = ones_like(_best)
        for ivar, varname in enumerate(self.var_map):
            par = self.params[varname]
            grad[ivar] = par.scale_gradient(_best[ivar])
            vbest[ivar] = par.value
        # modified from JJ Helmus' leastsqbound.py
        infodict['fjac'] = transpose(transpose(infodict['fjac']) /
                                     take(grad, infodict['ipvt'] - 1))
        rvec = dot(triu(transpose(infodict['fjac'])[:self.nvarys,:]),
                   take(eye(self.nvarys),infodict['ipvt'] - 1, 0))
        try:
            cov = inv(dot(transpose(rvec),rvec))
        except LinAlgError:
            cov = None

        for par in self.params.values():
            par.stderr, par.correl = 0, None

        self.covar = cov
        if cov is None:
            self.errorbars = False
            self.message = '%s. Could not estimate error-bars'
        else:
            self.errorbars = True
            if self.scale_covar:
                 self.covar = cov = cov * sum_sqr / self.nfree
            for ivar, varname in enumerate(self.var_map):
                par = self.params[varname]
                par.stderr = sqrt(cov[ivar, ivar])
                par.correl = {}
                for jvar, varn2 in enumerate(self.var_map):
                    if jvar != ivar:
                        par.correl[varn2] = (cov[ivar, jvar]/
                                        (par.stderr * sqrt(cov[jvar, jvar])))


        # set uncertainties on constrained parameters.
        # Note that first we set all named params to
        # have values that include uncertainties, then
        # evaluate all constrained parameters, then set
        # the values back to the nominal values.
        if HAS_UNCERT and self.covar is not None:
            uvars = uncertainties.correlated_values(vbest, self.covar)
            for v, nam in zip(uvars, self.var_map):
                self.asteval.symtable[nam] = v

            for pname, par in self.params.items():
                if hasattr(par, 'ast'):
                    try:
                        out = self.asteval.run(par.ast)
                        par.stderr = out.std_dev()
                    except:
                        pass

            for v, nam in zip(uvars, self.var_map):
                self.asteval.symtable[nam] = v.nominal_value

        for par in self.params.values():
            if hasattr(par, 'ast'):
                delattr(par, 'ast')
        return self.success
