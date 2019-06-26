# from pyomo.environ import *
import pyomo.environ as pyo


def set_initialisation(optimisation_model, set_class):
    """
    This function takes in the model object and the set input (set_class)
    and initialise the set for the model
    """
    # set of monomer production plants
    optimisation_model.i = pyo.Set(initialize = set_class.i,
                         doc = 'monomer production plants', ordered = True)

    optimisation_model.j = pyo.Set(initialize = set_class.j,
                         doc = 'polymer plants', ordered = True)

    optimisation_model.g = pyo.Set(initialize = set_class.g,
                         doc = 'polymer with different grades', ordered = True)

    optimisation_model.t = pyo.Set(initialize = set_class.t,
                         doc = 'time periods', ordered = True)

    optimisation_model.o = pyo.Set(initialize = set_class.o,
                         doc = 'olefins/monomers', ordered = True)

    optimisation_model.c = pyo.Set(initialize = set_class.c,
                         doc = 'customers', ordered = True)

    optimisation_model.h = pyo.Set(initialize = set_class.h,
                         doc = 'IHP', ordered = True)
