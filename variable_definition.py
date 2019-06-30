import pyomo.environ as pyo

def variable_initialisation(optimisation_model):
    """
    This function takes in the optimisation_model as the input and initialise
    the variables, their characteristics and bounds
    """
    # get the set of time period as a list
    hsetlist = list(optimisation_model.h)

    def PObounds(optimisation_model, i, t):
        """
        This function defines the bounds for PO(i)
        """
        #return (20, 30)
        return (optimisation_model.p_min[i], optimisation_model.p_max[i])

    def ICbounds(optimisation_model, m, t):
        """
        This function defines the bounds for IC
        """
        return (optimisation_model.IC_low[m], optimisation_model.IC_upper[m])

    def IHbounds(optimisation_model, g, h, t):
        """
        This function defines the bounds for IH
        """
        return (optimisation_model.IH_low[g, h], None)
        #return (optimisation_model.IH_low[g, h], None)


    def ICini(optimisation_model, m, t):
        """
        This function takes the variable IC and sets its initial condition
        """
        if t == 1:
            optimisation_model.IC[m, t].fixed = True
            return optimisation_model.IC_ini_level[m]
        else:
            return None

    def IHini(optimisation_model, g, h, t):
        """
        This function takes the variable IP and sets its initial condition
        """
        if t <= optimisation_model.LT[h] or t <= 1:
            optimisation_model.IH[g, h, t].fixed = True

            return optimisation_model.IH_low[g, h]
        else:
            return None


    def Sini(optimisation_model, m, t):
        """
        This function takes the variable S and sets its initial condition
        """
        if t == 1:
            optimisation_model.S[m, t].fixed = True
            return 0
        else:
            return None

    def Qfx(optimisation_model, g, h, t):
        """
        This function fix the value of Q at h = 1 to 0 at any time,
        which forbids self shipment from h1 to h1
        """
        if h == hsetlist[0]:
            optimisation_model.Q[g, h, t].fixed = True
            return 0
        else:
            return None

    def QCfx(optimisation_model, c, g, h, t):
        """This function fix the QC value of any customer/region pairs
        that is not feasible to zero
        """
        if optimisation_model.HC[h, c] != 1:
            optimisation_model.QC[c, g, h, t].fixed = True
            return 0

        else:
            return None


    optimisation_model.PM = pyo.Var(
                            optimisation_model.i, optimisation_model.m,
                            optimisation_model.t,
                            within = pyo.NonNegativeReals,
                            doc = 'amount of m consumed in unit i over t'
                            )

    optimisation_model.PO = pyo.Var(
                            optimisation_model.i, optimisation_model.t,
                            within = pyo.NonNegativeReals,
                            bounds = PObounds,
                            doc = 'production amount of plant i in period t'
                            )

    optimisation_model.PP = pyo.Var(
                            optimisation_model.g, optimisation_model.j,
                            optimisation_model.t,
                            within = pyo.NonNegativeReals,
                            doc = 'amount of grade g produced in plant j in t'
                            )

    optimisation_model.IC = pyo.Var(
                            optimisation_model.m, optimisation_model.t,
                            within = pyo.NonNegativeReals, bounds = ICbounds,
                            initialize = ICini, doc = \
                            'plant inventory level of olefin o at t '
                            )

    optimisation_model.PU = pyo.Var(
                            optimisation_model.m, optimisation_model.t,
                            within = pyo.NonNegativeReals,
                            doc = 'amount of olefin o purchased at period t'
                            )

    optimisation_model.S = pyo.Var(
                           optimisation_model.m, optimisation_model.t,
                           within = pyo.NonNegativeReals, initialize = Sini,
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
                            bounds = IHbounds, initialize = IHini, doc = \
                            'inventory level of grade g at IHP h at period t'
                            )

    optimisation_model.QC = pyo.Var(
                           optimisation_model.c, optimisation_model.g,
                           optimisation_model.h, optimisation_model.t,
                           within = pyo.NonNegativeReals,
                           initialize = QCfx,
                           doc = 'supply of g from h to customer c at period t'
                           )
    optimisation_model.Y = pyo.Var(
                           optimisation_model.g, optimisation_model.j,
                           optimisation_model.t, within = pyo.Binary,
                           doc = 'supply of g from h to customer c at period t'
                           )
