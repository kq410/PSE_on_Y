import pyomo.environ as pyo

def variable_initialisation(optimisation_model):
    """
    This function takes in the optimisation_model as the input and initialise
    the variables, their characteristics and bounds
    """
    # get the set of time period as a list
    hsetlist = list(optimisation_model.h)

    def PMbounds(optimisation_model, i, m, t):
        """
        This function defines the bounds for PM(i, t)
        """
        return (optimisation_model.p_min[i, m]*optimisation_model.delta[t],
        optimisation_model.p_max[i, m] * optimisation_model.delta[t])


    def Sbounds(optimisation_model, m, t):
        """
        This function defines the bounds for the sale of m
        """
        return (optimisation_model.S_min[m] * optimisation_model.delta[t],
        optimisation_model.S_max[m] * optimisation_model.delta[t])

    def FLbounds(optimisation_model, m, t):
        """
        This function defines the bounds for the flare of m
        """
        return (optimisation_model.FL_min[m] * optimisation_model.delta[t],
        optimisation_model.FL_max[m] * optimisation_model.delta[t])


    def ICbounds(optimisation_model, m, t):
        """
        This function defines the bounds for IC
        """
        return (optimisation_model.IC_low[m], optimisation_model.IC_upper[m])

    def IHbounds(optimisation_model, g, h, t):
        """
        This function defines the bounds for IH
        """
        return (optimisation_model.IH_low[g, h],
                optimisation_model.IH_upper[g, h])

    def QCbounds(optimisation_model, g, c, t):
        """
        This function defines the lower bound for QC
        """
        return(optimisation_model.D_min[c, g, t], None)

    def Qfx(optimisation_model, g, h, t):
        """
        This fix the Q value for ord(h) = 1 to zero
        """
        if h == hsetlist[0]:
            optimisation_model.Q[g, h, t].fixed = True
            return 0

    def PPfx(optimisation_model, g, j, t):
        """
        This fix the Q value for ord(h) = 1 to zero
        """
        if optimisation_model.GJ[g, j] != 1:
            optimisation_model.PP[g, j, t].fixed = True
            return 0

    print('Initialising model variables......')

    optimisation_model.PM = pyo.Var(
                            optimisation_model.i, optimisation_model.m,
                            optimisation_model.t,
                            within = pyo.NonNegativeReals,
                            bounds = PMbounds,
                            doc = 'amount of m consumed in unit i over t'
                            )

    optimisation_model.PP = pyo.Var(
                            optimisation_model.g, optimisation_model.j,
                            optimisation_model.t,
                            within = pyo.NonNegativeReals,
                            initialize = PPfx,
                            doc = 'amount of grade g produced in plant j in t'
                            )

    optimisation_model.IC = pyo.Var(
                            optimisation_model.m, optimisation_model.t,
                            within = pyo.NonNegativeReals, bounds = ICbounds,
                            doc = 'plant inventory level of olefin o at t '
                            )

    optimisation_model.PU = pyo.Var(
                            optimisation_model.m, optimisation_model.t,
                            within = pyo.NonNegativeReals,
                            doc = 'amount of olefin o purchased at period t'
                            )

    optimisation_model.S = pyo.Var(
                           optimisation_model.m, optimisation_model.t,
                           within = pyo.NonNegativeReals,
                           bounds = Sbounds,
                           doc = 'amount of olefin sold by export at period t'
                           )

    optimisation_model.Q = pyo.Var(
                           optimisation_model.g, optimisation_model.h,
                           optimisation_model.t, within = pyo.NonNegativeReals,
                           initialize = Qfx,
                           doc = 'shipment of g from UAE to h at period t'
                           )

    optimisation_model.IH = pyo.Var(
                            optimisation_model.g, optimisation_model.h,
                            optimisation_model.t,
                            within = pyo.NonNegativeReals,
                            bounds = IHbounds, doc = \
                            'inventory level of grade g at IHP h at period t'
                            )

    optimisation_model.QC = pyo.Var(
                           optimisation_model.g, optimisation_model.c,
                           optimisation_model.t,
                           within = pyo.NonNegativeReals,
                           bounds = QCbounds,
                           doc = 'supply of g from h to customer c at period t'
                           )

    optimisation_model.FL = pyo.Var(
                            optimisation_model.m, optimisation_model.t,
                            within = pyo.NonNegativeReals,
                            bounds = FLbounds,
                            doc = 'amount of material m flared at period t'
                            )

    optimisation_model.dell = pyo.Var(
                            optimisation_model.c, optimisation_model.g,
                            optimisation_model.t,
                            within = pyo.NonNegativeReals,
                            doc = 'amount of g short for customer c over t'
                            )

    optimisation_model.Y = pyo.Var(
                           optimisation_model.g, optimisation_model.j,
                           optimisation_model.t, within = pyo.Binary,
                           doc = 'supply of g from h to customer c at period t'
                           )

    optimisation_model.PM_produced = pyo.Var(
                            optimisation_model.i, optimisation_model.m,
                            optimisation_model.t,
                            within = pyo.NonNegativeReals,
                            doc = 'amount of monomers produced'
                            )

    optimisation_model.PP_max = pyo.Var(
                            optimisation_model.g, optimisation_model.j,
                            optimisation_model.t,
                            within = pyo.NonNegativeReals,
                            doc = 'maximum amount of g produced in plant j in t'
                            )

    optimisation_model.PP_min = pyo.Var(
                            optimisation_model.g, optimisation_model.j,
                            optimisation_model.t,
                            within = pyo.NonNegativeReals,
                            doc = 'minimum amount of g produced in plant j in t'
                            )

    optimisation_model.psale = pyo.Var(
                            within = pyo.NonNegativeReals,
                            doc = 'sale revenue of polymers'
                            )

    optimisation_model.msale = pyo.Var(
                            within = pyo.NonNegativeReals,
                            doc = 'sale revenue of materials'
                            )

    optimisation_model.pucost = pyo.Var(
                            within = pyo.NonNegativeReals,
                            doc = 'purchase cost'
                            )

    optimisation_model.mpcost = pyo.Var(
                            within = pyo.NonNegativeReals,
                            doc = 'material production operational cost'
                            )

    optimisation_model.ppcost = pyo.Var(
                            within = pyo.NonNegativeReals,
                            doc = 'polymer production operational cost'
                            )

    optimisation_model.penalty_cost = pyo.Var(
                            within = pyo.NonNegativeReals,
                            doc = 'penalty cost'
                            )
