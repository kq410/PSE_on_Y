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


def data_construction(file_name):
    """
    This function constructs the input data object
    """
    # load the sets
    i = faux.read_set_from_excel(file_name, 'set', (3, 'E'), (3, 'J'))
    j = faux.read_set_from_excel(file_name, 'set', (6, 'E'), (6, 'O'))
    t = faux.read_set_from_excel(file_name, 'set', (9, 'E'), (9, 'J'))
    h = faux.read_set_from_excel(file_name, 'set', (12, 'E'), (3, 'G'))
    c = faux.read_set_from_excel(file_name, 'set', (15, 'E'), (15, 'J'))
    g = faux.read_set_from_excel(file_name, 'set', (18, 'E'), (18, 'N'))
    m = faux.read_set_from_excel(file_name, 'set', (21, 'E'), (21, 'L'))

    set_input = faux.SetInput(i, j, g, t, m, c, h)

    # load the parameters for the production of olefins
    p_min = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (13, 'C'), (19, 'K'), (1, 1))

    p_max = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (4, 'C'), (10, 'H'), (1, 1))

    OC = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (22, 'C'), (23, 'H'), (0, 1))

    miu = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (27, 'C'), (75, 'L'), (2, 1))

    IC_upper = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (78, 'C'), (79, 'J'), (0, 1))

    IC_low = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (83, 'C'), (84, 'J'), (0, 1))

    IC_ini_level = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (88, 'C'), (89, 'J'), (0, 1))



    # load the parameters for the production of polyolefins
    PR = faux.read_par_from_excel(file_name,
                'ProductionPolyolefins', (4, 'C'), (14, 'N'), (1, 1))

    tao = faux.read_par_from_excel(file_name,
                'ProductionPolyolefins', (18, 'C'), (28, 'N'), (1, 1))

    n = faux.read_par_from_excel(file_name,
                'ProductionPolyolefins', (32, 'C'), (37, 'M'), (1, 1))

    OP = faux.read_par_from_excel(file_name,
                'ProductionPolyolefins', (47, 'C'), (57, 'N'), (1, 1))


    # Load the parameters for the warehouse shipping
    LT = faux.read_par_from_excel(file_name,
                'WarehousesShipping', (5, 'C'), (6, 'E'), (0, 1))

    IH_low = faux.read_par_from_excel(file_name,
                'WarehousesShipping', (9, 'C'), (19, 'F'), (1, 1))

    # Load the parameters for availability scenarios
    delta = faux.read_par_from_excel(file_name,
                'ScenarioAvailability', (4, 'D'), (5, 'I'), (0, 1))

    phi = faux.read_par_from_excel(file_name,
                'ScenarioAvailability', (8, 'D'), (19, 'J'), (1, 1))


    # Load the parameters for sales scenarios
    D = faux.read_par_from_excel(file_name,
                'ScenarioSales', (7, 'D'), (67, 'K'), (2, 1))

    SP = faux.read_par_from_excel(file_name,
                'ScenarioSales', (74, 'D'), (134, 'K'), (2, 1))

    SO = faux.read_par_from_excel(file_name,
                'ScenarioSales', (137, 'D'), (145, 'J'), (1, 1))

    # Load the parameters for purchases scenarios
    PC = faux.read_par_from_excel(file_name,
                'ScenarioPurchases', (5, 'D'), (13, 'J'), (1, 1))

    PU_max = faux.read_par_from_excel(file_name,
                'ScenarioPurchases', (16, 'D'), (17, 'K'), (0, 1))

    PU_min = faux.read_par_from_excel(file_name,
                'ScenarioPurchases', (20, 'D'), (21, 'K'), (0, 1))


    # Load the additional parameters

    IH_upper = faux.read_par_from_excel(file_name,
                'AdditionalParameters', (3, 'C'), (13, 'F'), (1, 1))

    pie = faux.read_par_from_excel(file_name,
                'AdditionalParameters', (16, 'C'), (17, 'H'), (0, 1))

    S_max = faux.read_par_from_excel(file_name,
                'AdditionalParameters', (21, 'C'), (22, 'J'), (0, 1))

    S_min = faux.read_par_from_excel(file_name,
                'AdditionalParameters', (26, 'C'), (27, 'J'), (0, 1))

    FL_max = faux.read_par_from_excel(file_name,
                'AdditionalParameters', (31, 'C'), (32, 'J'), (0, 1))

    FL_min = faux.read_par_from_excel(file_name,
                'AdditionalParameters', (36, 'C'), (37, 'J'), (0, 1))

    Qtil = faux.read_par_from_excel(file_name,
                'AdditionalParameters', (41, 'C'), (71, 'J'), (2, 1))

    # initialise set mapping
    HC = faux.read_par_from_excel(file_name,
                'set', (25, 'E'), (28, 'K'), (1, 1))

    IM = faux.read_par_from_excel(file_name,
                'set', (31, 'E'), (37, 'M'), (1, 1))

    GJ = faux.read_par_from_excel(file_name,
                'set', (40, 'E'), (50, 'P'), (1, 1))


    # Initialise other parameters

    S_ini_level = {
    material : 0 for material in m
    }

    fixed_var = faux.ParaFixedInput(self, p_min, p_max, PR, tao, miu, n, LT,
    IC_low, IH_low, IC_upper, HC, PU_max, PU_min, S_max, S_min, FL_max,
    FL_min, IM, GJ)

    variable_par = faux.ParaVarInput(delta, phi, D, SP, SO, PC, OC, OP,
    IC_ini_level, pie, Qtil)

    return set_input, fixed_var, variable_par


def main():
    """
    This is the main function which calls all other functions to solve the
    optimisation model
    """
    # initialise the concreteModel
    PSE_model = ConcreteModel()

    # get the data input as objects
    Excel_file = 'Borouge_Data_Final_PYTHON.xlsx'
    set_input, fixed_par, variable_par = data_construction(Excel_file)

    # set initialisation
    fset.set_initialisation(PSE_model, set_input)

    # parameter initialisation
    fpar.parameter_initialisation(PSE_model, fixed_par, variable_par)

    # variable initialisation
    fvar.variable_initialisation(PSE_model)

    # constraint initialisation
    fcon.constraint_definition(PSE_model)

    # set up the model
    opt = SolverFactory('cplex')
    #opt.options['mipgap'] = 0.001
    #opt.options['threads'] = 0

    results = opt.solve(PSE_model, tee = True,
    symbolic_solver_labels = True)

    PSE_model.solutions.store_to(results)
    results.write(filename = 'solution.yml')

    # for m in PSE_model.m:
    #     for t in PSE_model.t:
    print(sum (PSE_model.QC[c, g, h, t].value * PSE_model.SP[c, g, t]
    for g in PSE_model.g for c in PSE_model.c
    for h in PSE_model.h for t in PSE_model.t))
    print(sum(PSE_model.S[m, t].value * PSE_model.SO[m, t]
        for m in PSE_model.m
        for t in PSE_model.t))

    print(sum (PSE_model.QC[c, g, h, t].value
    for g in PSE_model.g for c in PSE_model.c
    for h in PSE_model.h for t in PSE_model.t))

    print(sum(PSE_model.tao[g, j]
                for g in PSE_model.g for j in PSE_model.j))
    #total_Psale = PSE_model.QC#['KSC (UAE)', 'gPE1', 'UAE', '3'].value
    # total_Psale = sum (
    # PSE_model.QC[c, g, h, t].value * PSE_model.SP[c, g, t].value \
    # for g in PSE_model.g for c in PSE_model.c
    # for h in PSE_model.h for t in PSE_model.t)
    #print(total_Psale)
    # result_dict = faux.result_data_load(PSE_model, ['PP'])
    # print(result_dict)
if __name__ == '__main__':
    main()
