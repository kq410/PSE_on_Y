import pyomo.environ as pyo

def parameter_initialisation(optimisation_model,
                            fixed_par_input, var_par_input):
    """
    This function takes the model input (optimisation_model) and the
    parameter input objects to initialise the model's parameters
    """
    optimisation_model.p_min = pyo.Param(
                               optimisation_model.i,
                               initialize = fixed_par_input.p_min,
                               doc = 'minimum operation for plant i'
                               )

    optimisation_model.p_max = pyo.Param(
                               optimisation_model.i,
                               initialize = fixed_par_input.p_max,
                               doc = 'maximum operation for plant i'
                               )

    optimisation_model.PR = pyo.Param(
                            optimisation_model.g, optimisation_model.j,
                            initialize = fixed_par_input.PR,
                            doc = 'production rate of g in polymer plant j'
                            )

    optimisation_model.tao = pyo.Param(
                             optimisation_model.g, optimisation_model.j,
                             initialize = fixed_par_input.tao,
                             doc = 'minimum runtime for g to be produced in j'
                             )

    optimisation_model.f = pyo.Param(
                           optimisation_model.t,
                           initialize = var_par_input.f,
                           doc = 'length of time period t'
                           )

    optimisation_model.phi = pyo.Param(
                             optimisation_model.j, optimisation_model.t,
                             initialize = var_par_input.phi,
                             doc = 'available fraction of time for j in t'
                             )

    optimisation_model.miu = pyo.Param(
                             optimisation_model.i, optimisation_model.m,
                             optimisation_model.m,
                             initialize = fixed_par_input.miu,
                             doc = 'production coefficient of olefin o in i'
                             )

    optimisation_model.n = pyo.Param(
                           optimisation_model.m, optimisation_model.g,
                           initialize = fixed_par_input.n, default = 0,
                           doc = 'consumption coefficient of o producing g'
                           )

    optimisation_model.D = pyo.Param(
                           optimisation_model.c, optimisation_model.g,
                           optimisation_model.t,
                           initialize = var_par_input.D,
                           doc = 'demand of grade g of customer c in period t'
                           )

    optimisation_model.SP = pyo.Param(
                            optimisation_model.c, optimisation_model.g,
                            optimisation_model.t,
                            initialize = var_par_input.SP,
                            doc = 'sale price of grade g to customer c'
                            )

    optimisation_model.SO = pyo.Param(
                            optimisation_model.m, optimisation_model.t,
                            initialize = var_par_input.SO, default = 0,
                            doc = 'export price of olefin o'
                            )

    optimisation_model.PC = pyo.Param(
                            optimisation_model.m, optimisation_model.t,
                            initialize = var_par_input.PC,
                            doc = 'purchase price of olefin o'
                            )


    optimisation_model.OC = pyo.Param(
                            optimisation_model.i,
                            initialize = var_par_input.OC,
                            doc = 'operation cost coef of monomer plant i')

    optimisation_model.OP = pyo.Param(
                            optimisation_model.g, optimisation_model.j,
                            initialize = var_par_input.OP,
                            doc = 'operation cost of plant j for producing g'
                            )

    optimisation_model.LT = pyo.Param(
                            optimisation_model.h,
                            initialize = fixed_par_input.LT,
                            doc = 'lead time from UAE gateway to IHP h'
                            )

    optimisation_model.IC_low = pyo.Param(
                                optimisation_model.m,
                                initialize = fixed_par_input.IC_low,
                                doc = 'lower bound for plant inventory of o'
                                )

    optimisation_model.IC_upper = pyo.Param(
                                optimisation_model.m,
                                initialize = fixed_par_input.IC_upper,
                                doc = 'upper bound for plant inventory of o'
                                )

    optimisation_model.IH_low = pyo.Param(
                                optimisation_model.g, optimisation_model.h,
                                initialize = fixed_par_input.IH_low,
                                doc = 'lower bound for IHP inventory of g in h'
                                )

    optimisation_model.IC_ini_level = pyo.Param(
                                optimisation_model.m,
                                initialize = var_par_input.IC_ini_level,
                                default = 0,
                                doc = 'initial level of plant inventory of o'
                                )


    optimisation_model.S_ini_level = pyo.Param(
                                optimisation_model.m,
                                initialize = var_par_input.S_ini_level,
                                doc = 'initial level of sale of product o'
                                )

    optimisation_model.HC = pyo.Param(
                                optimisation_model.h, optimisation_model.c,
                                initialize = fixed_par_input.HC,
                                doc = 'HC pair parameter'
                                )
