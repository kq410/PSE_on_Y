import pyomo.environ as pyo

def constraint_definition(model):
    """
    This function takes in the model object and initialise
    user-defined constraints
    """
    hsetlist = list(model.h)

    def objective_rule(model):
        """
        This constraint defines the objective function
        """
        return \
          sum (model.QC[g, c, t] * model.SP[c, g, t] for g in model.g \
          for c in model.c for t in model.t) \
        + sum(model.S[m, t] * model.SO[m, t] for m in model.m for t in model.t)\
        - sum(model.PU[m, t] * model.PC[m,t] for m in model.m for t in model.t)\
        - sum(model.PM[i, m, t] * model.OC[i] for i in model.i
        for m in model.m for t in model.t) \
        - sum(model.PP[g, j, t] * model.OP[g, j] for g in model.g
          for j in model.j for t in model.t) \
        - sum(model.pie[c] * model.dell[c, g, t] for c in model.c
        for g in model.g for t in model.t)


    def constraint_rule_1(model, g, j, t):
        """
        This constraint defines the minimal amount
        produced by each polymer plant
        """
        if model.GJ[g, j] != 1:
            return pyo.Constraint.Skip
        return model.PP[g, j, t] >= \
            model.PR[g, j] * model.Y[g, j, t] * model.tao[g, j]



    def constraint_rule_2(model, g, j, t):
        """
        This function defines the maximal amount
        produced by each polymer plant
        """
        if model.GJ[g, j] != 1:
            return pyo.Constraint.Skip
        return model.PP[g, j, t] <= \
            model.PR[g, j] * model.Y[g, j, t] * model.delta[t] * model.phi[j, t]

    def constraint_rule_3(model, j, t):
        """
        This constraint defines the maximum total amount of all polymer
        produced in plant j over time period t
        """
        return \
        sum(model.PP[g, j, t]/model.PR[g, j]
        for g in model.g if model.PR[g, j] != 0) <= \
        model.delta[t] * model.phi[j, t]

    def constraint_rule_4(model, m, t):
        """
        This constraint is the resource balance for the monomer inventory
        at the plant site
        """
        if t == 1:
            return \
            model.IC[m, t] == model.IC_ini_level[m] \
                + sum(model.miu[i, mp, m] * model.PM[i, mp, t] \
                for i in model.i for mp in model.m if model.IM[i, mp] == 1) \
                - sum(model.PM[i, m, t] for i in model.i) \
                + model.PU[m, t] - model.S[m, t] - model.FL[m, t] \
                - sum(model.n[m, g] * model.PP[g, j, t]\
                for g in model.g for j in model.j if model.GJ[g, j] == 1)
        return \
        model.IC[m, t] == model.IC[m, t-1] \
                + sum(model.miu[i, mp, m] * model.PM[i, mp, t] \
                for i in model.i for mp in model.m if model.IM[i, mp] == 1) \
                - sum(model.PM[i, m, t] for i in model.i) \
                + model.PU[m, t] - model.S[m, t] - model.FL[m, t] \
                - sum(model.n[m, g] * model.PP[g, j, t] \
                for g in model.g for j in model.j if model.GJ[g, j] == 1)

    def constraint_rule_5(model, g, h, t):
        """
        This constraint defines the inventory level of UAE Gateway (h=1)
        and all the global IHPs (h>1)
        """
        if h == hsetlist[0] and t == 1:
            return \
            model.IH[g, h, t] == model.IH_ini_level[g, h] \
            - sum(model.Q[g, hp, t] for hp in model.h if hp != h) \
            - sum(model.QC[g, c, t] for c in model.c if model.HC[h, c] == 1)

        elif h != hsetlist[0] and t == 1:
            return \
            model.IH[g, h, t] == model.IH_ini_level[g, h] - \
            sum(model.QC[g, c, t] for c in model.c if model.HC[h, c] == 1)

        elif h == hsetlist[0] and 1 < t and t <= model.LT[h]:
            return\
            model.IH[g, h, t] == model.IH[g, h, t-1] \
            - sum(model.Q[g, hp, t] for hp in model.h if hp != h) \
            - sum(model.QC[g, c, t] for c in model.c if model.HC[h, c] == 1)

        elif h != hsetlist[0] and 1 < t and t <= model.LT[h]:
            return \
            model.IH[g, h, t] == model.IH[g, h, t-1] \
            - sum(model.QC[g, c, t] for c in model.c if model.HC[h, c] == 1)

        elif h == hsetlist[0] and t > model.LT[h]:
            return \
            model.IH[g, h, t] == model.IH[g, h, t-1] \
            + sum(model.PP[g, j, t-model.LT[h]] for j in model.j) \
            - sum(model.Q[g, hp, t] for hp in model.h if hp != h) \
            - sum(model.QC[g, c, t] for c in model.c if model.HC[h, c] == 1) \

        elif h != hsetlist[0] and t > model.LT[h]:
            return \
            model.IH[g, h, t] == model.IH[g, h, t-1] \
            + model.Q[g, h, t-model.LT[h]] \
            - sum(model.QC[g, c, t] for c in model.c if model.HC[h, c] == 1)


    def constraint_rule_6(model, g, c, t):
        """
        This constraint specifies the maximum demand that cannot be exceeded
        """
        return model.QC[g, c, t] == model.D_max[c, g, t] - model.dell[c, g, t]

    def auxiliary_rule_1(model, i, m, t):
        """
        This auxiliary rule defines the amount of monomers produced
        """
        return model.PM_produced[i, m, t] == \
        sum(model.miu[i, mp, m] * model.PM[i, mp, t]
        for mp in model.m if model.IM[i, mp] == 1)

    def auxiliary_rule_2(model, g, j, t):
        """This auxiliary rule defines the maximum amount of g can be
        produced in plant j over t
        """
        return model.PP_max[g, j, t] == \
        model.PR[g, j] * model.Y[g, j, t] * model.delta[t] * model.phi[j, t]

    def auxiliary_rule_3(model, g, j, t):
        """This auxiliary rule defines the minimum amount of g can be
        produced in plant j over t
        """
        return model.PP_min[g, j, t] == \
        model.PR[g, j] * model.Y[g, j, t] * model.tao[g, j]

    def financial_output_1(model, t):
        """This returns the sale revenue of polymers"""
        return model.psale[t] == sum (model.QC[g, c, t] * model.SP[c, g, t]
        for g in model.g for c in model.c)

    def financial_output_2(model, t):
        """This returns the sale revenue of materials"""
        return model.msale[t] == sum(model.S[m, t] * model.SO[m, t]
        for m in model.m)

    def financial_output_3(model, t):
        """This returns the purchase cost of materials"""
        return model.pucost[t] == sum(model.PU[m, t] * model.PC[m,t]
        for m in model.m)

    def financial_output_4(model, t):
        """This returns the operation cost of producing materials"""
        return model.mpcost[t] == sum(model.PM[i, m, t] * model.OC[i]
        for i in model.i for m in model.m)

    def financial_output_5(model, t):
        """This returns the operation cost of producing polymers"""
        return model.ppcost[t] == sum(model.PP[g, j, t] * model.OP[g, j]
        for g in model.g for j in model.j)

    def financial_output_6(model, t):
        """This returns the penalty cost for not fulfilling the demand"""
        return model.penalty_cost[t] == sum(model.pie[c] * model.dell[c, g, t]
        for c in model.c for g in model.g)

    print('Initialising model constraints and the objective function......')

    model.objective_function = pyo.Objective(
                               rule = objective_rule,
                               sense = pyo.maximize, doc = 'maximise revenue'
                               )


    model.constraint1 = pyo.Constraint(
                        model.g, model.j, model.t, rule = constraint_rule_1,
                        doc = 'refer to constraint_rule_1'
                        )

    model.constraint2 = pyo.Constraint(
                        model.g, model.j, model.t, rule = constraint_rule_2,
                        doc = 'refer to constraint_rule_2'
                        )

    model.constraint3 = pyo.Constraint(
                        model.j, model.t, rule = constraint_rule_3,
                        doc = 'refer to constraint_rule_3'
                        )

    model.constraint4 = pyo.Constraint(
                        model.m, model.t, rule = constraint_rule_4,
                        doc = 'refer to constraint_rule_4'
                        )

    model.constraint5 = pyo.Constraint(
                        model.g, model.h, model.t, rule = constraint_rule_5,
                        doc = 'refer to constraint_rule_5'
                        )

    model.constraint6 = pyo.Constraint(
                        model.g, model.c, model.t, rule = constraint_rule_6,
                        doc = 'refer to constraint_rule_6'
                        )

    model.auxiliary1 = pyo.Constraint(
                       model.i, model.m, model.t, rule = auxiliary_rule_1,
                       doc = 'refer to auxiliary_rule_1'
                       )

    model.auxiliary2 = pyo.Constraint(
                       model.g, model.j, model.t, rule = auxiliary_rule_2,
                       doc = 'refer to auxiliary_rule_2'
                       )

    model.auxiliary3 = pyo.Constraint(
                       model.g, model.j, model.t, rule = auxiliary_rule_3,
                       doc = 'refer to auxiliary_rule_3'
                       )

    model.financial1 = pyo.Constraint(
                        model.t,
                        rule = financial_output_1,
                        doc = 'refer to financial_output_1'
    )

    model.financial2 = pyo.Constraint(
                        model.t,
                        rule = financial_output_2,
                        doc = 'refer to financial_output_2'
    )

    model.financial3 = pyo.Constraint(
                        model.t,
                        rule = financial_output_3,
                        doc = 'refer to financial_output_3'
    )

    model.financial4 = pyo.Constraint(
                        model.t,
                        rule = financial_output_4,
                        doc = 'refer to financial_output_4'
    )

    model.financial5 = pyo.Constraint(
                        model.t,
                        rule = financial_output_5,
                        doc = 'refer to financial_output_5'
    )

    model.financial6 = pyo.Constraint(
                        model.t,
                        rule = financial_output_6,
                        doc = 'refer to financial_output_6'
    )
