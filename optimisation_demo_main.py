## Import built packages ##
import pandas as pd
from pyomo.environ import *
from pyomo.opt import SolverStatus, TerminationCondition

## Import model components ##
import set_definition as fset
import parameter_definition as fpar
import variable_definition as fvar
import constraint_definition as fcon
import auxiliary_function as faux


def data_construction():
    """
    This function constructs the input data object
    """
    i = ['i1']
    #p = ['propane', 'ethane', 'ethylene', 'propylene', 'PE1', 'PE2']
    j = ['j1', 'j2']
    g = ['PE1', 'PE2']
    t = [1, 2, 3]
    o = ['ethylene', 'propylene']
    c = ['c1']
    h = [1, 2]

    set_input = faux.SetInput(i, j, g, t, o, c, h)

    p_min = {
    'i1' : 50
    }

    p_max = {
    'i1' : 200
    }

    PR = {
    ('PE1', 'j1') : 10, ('PE1', 'j2') : 16,
    ('PE2', 'j1') : 8, ('PE2', 'j2') : 20
    }

    tao = {
    ('PE1', 'j1') : 3, ('PE1', 'j2') : 5,
    ('PE2', 'j1') : 3, ('PE2', 'j2') : 5
    }

    f = {
    1 : 7, 2 : 7, 3 : 7
    }

    phi = {
    ('j1', 1) : 1, ('j1', 2) : 1, ('j1', 3) : 1,
    ('j2', 1) : 1, ('j2', 2) : 1, ('j2', 3) : 1
    }

    miu = {
    ('ethylene', 'i1') : 0.5, ('propylene', 'i1') : 0.5
    }

    n = {
    ('ethylene', 'PE1') : 0.5, ('ethylene', 'PE2') : 0.35,
    ('propylene', 'PE1') : 0.5, ('propylene', 'PE2') : 0.65
    }

    D = {
    ('PE1', 'c1', 1) : 5, ('PE1', 'c1', 2) : 5, ('PE1', 'c1', 3) : 5,
    ('PE2', 'c1', 1) : 6, ('PE2', 'c1', 2) : 6, ('PE2', 'c1', 3) : 6
    }

    SP = {
    ('PE1', 'c1') : 500, ('PE2', 'c1') : 700
    }

    SO = {
    'ethylene' : 25, 'propylene' : 0
    }

    PC = {
    'ethylene' : 1000, 'propylene' : 30
    }

    OC = {
    'i1' : 5
    }

    OP = {
    ('PE1', 'j1') : 4, ('PE1', 'j2') : 5,
    ('PE2', 'j1') : 5, ('PE2', 'j2') : 4
    }

    LT = {
    1 : 1, 2 : 2
    }

    IC_low = {
    'ethylene' : 0, 'propylene' : 0
    }

    IH_low = {
    ('PE1', 1) : 5, ('PE1', 2) : 5,
    ('PE2', 1) : 5, ('PE2', 2) : 5
    }

    IC_ini_level = {
    'ethylene' : 20, 'propylene' : 20
    }

    IH_ini_level = {
    ('PE1', 1) : 5, ('PE1', 2) : 5,
    ('PE2', 1) : 5, ('PE2', 2) : 5
    }

    S_ini_level = {
    'ethylene' : 0, 'propylene' : 0
    }

    'lfd'

    fixed_var = faux.ParaFixedInput(p_min, p_max, PR, tao, miu,
                                    n, LT, IC_low, IH_low)

    variable_par = faux.ParaVarInput(f, phi, D, SP, SO, PC, OC, OP,
                                     IC_ini_level, IH_ini_level, S_ini_level)

    return set_input, fixed_var, variable_par


def main():
    """
    This is the main function which calls all other functions to solve the
    optimisation model
    """
    # initialise the concreteModel
    PSE_model = ConcreteModel()

    # get the data input as objects
    set_input, fixed_par, variable_par = data_construction()

    # set initialisation
    fset.set_initialisation(PSE_model, set_input)

    # parameter initialisation
    fpar.parameter_initialisation(PSE_model, fixed_par, variable_par)

    # variable initialisation
    fvar.variable_initialisation(PSE_model)

    # constraint initialisation
    fcon.constraint_definition(PSE_model)




if __name__ == '__main__':
    main()
