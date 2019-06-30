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
          sum (model.QC[c, g, h, t] * model.SP[c, g, t] for g in model.g \
          for c in model.c for h in model.h for t in model.t) \
        + sum(model.S[m, t] * model.SO[m, t] for m in model.m for t in model.t)\
        - sum(model.PU[m, t] * model.PC[m,t] for m in model.m for t in model.t)\
        - sum(model.PO[i, t] * model.OC[i] for i in model.i for t in model.t) \
        - sum(model.PP[g, j, t] * model.OP[g, j] for g in model.g \
          for j in model.j for t in model.t)


    def constraint_rule_1(model, g, j, t):
        """
        This constraint defines the minimal amount
        produced by each polymer plant
        """
        return \
        model.PP[g, j, t] >= model.PR[g, j] * model.Y[g, j, t] * model.tao[g, j]

    def constraint_rule_2(model, g, j, t):
        """
        This function defines the maximal amount
        produced by each polymer plant
        """
        return \
        model.PP[g, j, t] <= model.PR[g, j] * model.Y[g, j, t] \
                           * model.f[t] * model.phi[j, t]

    def constraint_rule_3(model, j, t):
        """
        This constraint defines the maximum total amount of all polymer
        produced in plant j over time period t
        """
        return \
        sum(model.PP[g, j, t]/model.PR[g, j]
        for g in model.g if model.PR[g, j] != 0) <= \
        model.f[t] * model.phi[j, t]

    def constraint_rule_4(model, m, t):
        """
        This constraint is the resource balance for the monomer inventory
        at the plant site
        """
        if t == 1:
            return pyo.Constraint.Skip
        return \
        model.IC[m, t] == model.IC[m, t-1] \
                + sum(model.miu[i, mp, m] * model.PM[i, mp, t] \
                for i in model.i for mp in model.m) \
                - sum(model.PM[i, m, t] for i in model.i) \
                + model.PU[m, t] - model.S[m, t]  \
                - sum(model.n[m, g] * model.PP[g, j, t] \
                for g in model.g for j in model.j)

    def constraint_rule_5(model, g, h, t):
        """
        This constraint defines the inventory level of UAE Gateway (h=1)
        and all the global IHPs (h>1)
        """
        if h == hsetlist[0] and t == 1:
            return \
            model.IH[g, h, t] >= sum(model.Q[g, hp, t]
            for hp in model.h if hp != h) + sum(model.QC[c, g, h, t]
            for c in model.c)

        elif h != hsetlist[0] and t == 1:
            return \
            model.IH[g, h, t] >= sum(model.QC[c, g, h, t]
            for c in model.c)

        elif h == hsetlist[0] and 1 < t and t <= model.LT[h]:
            return\
            model.IH[g, h, t] == model.IH[g, h, t-1] \
            - sum(model.Q[g, hp, t] for hp in model.h if hp != h) \
            - sum(model.QC[c, g, h, t] for c in model.c)
            
        elif h != hsetlist[0] and 1 < t and t <= model.LT[h]:
            return \
            model.IH[g, h, t] == model.IH[g, h, t-1] \
            - sum(model.QC[c, g, h, t] for c in model.c)

        elif h == hsetlist[0] and t > model.LT[h]:
            return \
            model.IH[g, h, t] == model.IH[g, h, t-1] \
            + sum(model.PP[g, j, t-model.LT[h]] for j in model.j) \
            - sum(model.Q[g, hp, t] for hp in model.h if hp != h) \
            - sum(model.QC[c, g, h, t] for c in model.c) \

        elif h != hsetlist[0] and t > model.LT[h]:
            return \
            model.IH[g, h, t] == model.IH[g, h, t-1] \
            + model.Q[g, h, t-model.LT[h]] \
            - sum(model.QC[c, g, h, t] for c in model.c)


    def constraint_rule_6(model, g, c, t):
        """
        This constraint specifies the maximum demand that cannot be exceeded
        """
        return \
        sum(model.QC[c, g, h, t] for h in model.h) <= model.D[c, g, t]


    def constraint_rule_7(model, i, t):
        """
        This constraint connects PM(i,m,t) with the capacity of the monomer
        plants PO(i,t)
        """
        return \
        sum(model.PM[i, m, t] for m in model.m) == model.PO[i, t]



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

    model.constraint7 = pyo.Constraint(
                        model.i, model.t, rule = constraint_rule_7,
                        doc = 'refer to constraint_rule_7'
                        )
