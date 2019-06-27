import pyomo.environ as pyo

def constraint_definition(model):
    """
    This function takes in the model object and initialise
    user-defined constraints
    """
    tsetlist = list(model.t)

    def objective_rule(model):
        """
        This constraint defines the objective function
        """
        return \
          sum (model.QC[g, h, c, t] * model.SP[g, c] for g in model.g \
          for h in model.h for c in model.c for t in model.t) \
        + sum(model.S[o, t] * model.SO[o] for o in model.o for t in model.t) \
        - sum(model.PU[o, t] * model.PC[o] for o in model.o for t in model.t) \
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
        sum(model.PP[g, j, t]/model.PR[g, j] for g in model.g) <= \
        model.f[t] * model.phi[j, t]

    def constraint_rule_4(model, o, t):
        """
        This constraint is the resource balance for the monomer inventory
        at the plant site
        """
        if t == 1:
            return pyo.Constraint.Skip
        return \
        model.IC[o, t] == model.IC[o, t-1] \
                + sum(model.miu[o, i] * model.PO[i,t] for i in model.i)\
                + model.PU[o, t] - model.S[o, t]  \
                - sum(model.n[o, g] * model.PP[g, j, t] \
                for g in model.g for j in model.j)

    def constraint_rule_5(model, g, h, t):
        """
        This constraint defines the inventory level of UAE Gateway (h=1)
        and all the global IHPs (h>1)
        """
        if t <= model.LT[h] or t <= 1:
            return pyo.Constraint.Skip
        if h == 1:
            return \
            model.IH[g, h, t] == model.IH[g, h, t-1] \
            + sum(model.PP[g, j, t-model.LT[h]] for j in model.j) \
            - sum(model.Q[g, hp, t] for hp in model.h if hp > h) \
            - sum(model.QC[g, h, c, t] for c in model.c) \

        elif h > 1:
            return \
            model.IH[g, h, t] == model.IH[g, h, t-1] \
            + model.Q[g, h, t-model.LT[h]] \
            - sum(model.QC[g, h, c, t] for c in model.c)


    def constraint_rule_6(model, g, c, t):
        """
        This constraint specifies the maximum demand that cannot be exceeded
        """
        return \
        sum(model.QC[g, h, c, t] for h in model.h) <= model.D[g, c, t]



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
                        model.o, model.t, rule = constraint_rule_4,
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