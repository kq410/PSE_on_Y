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
                'ProductionOlefins', (5, 'C'), (6, 'H'), (0, 1))

    p_max = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (10, 'C'), (11, 'H'), (0, 1))

    OC = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (15, 'C'), (16, 'H'), (0, 1))

    miu = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (22, 'C'), (70, 'L'), (2, 1))

    IC_upper = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (74, 'C'), (75, 'J'), (0, 1))


    # load the parameters for the production of polyolefins
    PR = faux.read_par_from_excel(file_name,
                'ProductionPolyolefins', (4, 'D'), (14, 'O'), (1, 1))

    tao = faux.read_par_from_excel(file_name,
                'ProductionPolyolefins', (18, 'D'), (28, 'O'), (1, 1))

    n = faux.read_par_from_excel(file_name,
                'ProductionPolyolefins', (32, 'D'), (37, 'N'), (1, 1))

    OP = faux.read_par_from_excel(file_name,
                'ProductionPolyolefins', (47, 'D'), (57, 'O'), (1, 1))


    # Load the parameters for the warehouse shipping
    LT = faux.read_par_from_excel(file_name,
                'WarehousesShipping', (5, 'C'), (6, 'E'), (0, 1))

    IH_low = faux.read_par_from_excel(file_name,
                'WarehousesShipping', (9, 'C'), (19, 'F'), (1, 1))

    # Load the parameters for availability scenarios
    f = faux.read_par_from_excel(file_name,
                'ScenarioAvailability', (15, 'D'), (16, 'I'), (0, 1))

    phi = faux.read_par_from_excel(file_name,
                'ScenarioAvailability', (19, 'D'), (30, 'J'), (1, 1))


    # Load the parameters for sales scenarios
    D = faux.read_par_from_excel(file_name,
                'ScenarioSales', (7, 'D'), (67, 'K'), (2, 1))

    SP = faux.read_par_from_excel(file_name,
                'ScenarioSales', (74, 'D'), (134, 'K'), (2, 1))

    SO = faux.read_par_from_excel(file_name,
                'ScenarioSales', (137, 'D'), (145, 'J'), (1, 1))

    # Loead the parameters for purchases scenarios
    PC = faux.read_par_from_excel(file_name,
                'ScenarioPurchases', (26, 'D'), (34, 'J'), (1, 1))

    IC_ini_level = faux.read_par_from_excel(file_name,
                'ScenarioPurchases', (38, 'D'), (39, 'K'), (0, 1))


    # initialise HC
    HCYES = faux.read_par_from_excel(file_name,
                'set', (25, 'E'), (28, 'K'), (1, 1))

    HC = {keys : 1 if values == 'yes' else 0
          for keys, values in HCYES.items()}

    # Initialise other parameters
    IC_low = {
    material : 0 for material in m
    }
    S_ini_level = {
    material : 0 for material in m
    }

    fixed_var = faux.ParaFixedInput(p_min, p_max, PR, tao, miu,
                                    n, LT, IC_low, IH_low, IC_upper, HC)

    variable_par = faux.ParaVarInput(f, phi, D, SP, SO, PC, OC, OP,
                                     IC_ini_level, S_ini_level)

    return set_input, fixed_var, variable_par


def main():
    """
    This is the main function which calls all other functions to solve the
    optimisation model
    """
    # initialise the concreteModel
    PSE_model = ConcreteModel()

    # get the data input as objects
    Excel_file = 'Borouge_Data_Scott_Demo.xlsx'
    set_input, fixed_par, variable_par = data_construction(Excel_file)
    #print(fixed_par.IH_low)
    #print(variable_par.SP)
    # set initialisation
    fset.set_initialisation(PSE_model, set_input)

    # parameter initialisation
    fpar.parameter_initialisation(PSE_model, fixed_par, variable_par)

    # variable initialisation
    fvar.variable_initialisation(PSE_model)

    # constraint initialisation
    fcon.constraint_definition(PSE_model)

    # set up the model
    opt = SolverFactory('cbc')
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
