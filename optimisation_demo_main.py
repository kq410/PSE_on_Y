## Import built packages ##
import os
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
    print('Loading sets data......')
    # load the sets
    i = faux.read_set_from_excel(file_name, 'set', (3, 'E'), (3, 'J'))
    j = faux.read_set_from_excel(file_name, 'set', (6, 'E'), (6, 'O'))
    t = faux.read_set_from_excel(file_name, 'set', (9, 'E'), (9, 'P'))
    h = faux.read_set_from_excel(file_name, 'set', (12, 'E'), (3, 'G'))
    m = faux.read_set_from_excel(file_name, 'set', (15, 'E'), (15, 'L'))
    g = faux.read_set_from_excel(file_name, 'set', (18, 'E'), (18, 'N'))
    c = faux.read_set_from_excel(file_name, 'set', (21, 'E'), (21, 'J'))

    set_input = faux.SetInput(i, j, g, t, m, c, h)

    print('Loading olefin production data......')
    # load the parameters for the production of olefins
    p_min = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (13, 'C'), (19, 'K'), (1, 1))

    p_max = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (4, 'C'), (10, 'K'), (1, 1))

    OC = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (22, 'C'), (23, 'H'), (0, 1))

    miu = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (27, 'C'), (75, 'L'), (2, 1))

    IC_upper = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (78, 'C'), (79, 'J'), (0, 1))

    IC_low = faux.read_par_from_excel(file_name,
                'ProductionOlefins', (83, 'C'), (84, 'J'), (0, 1))


    print('Loading polymer production data......')
    # load the parameters for the production of polyolefins
    PR = faux.read_par_from_excel(file_name,
                'ProductionPolyolefins', (4, 'C'), (14, 'N'), (1, 1))

    tao = faux.read_par_from_excel(file_name,
                'ProductionPolyolefins', (18, 'C'), (28, 'N'), (1, 1))

    n = faux.read_par_from_excel(file_name,
                'ProductionPolyolefins', (32, 'C'), (40, 'M'), (1, 1))

    OP = faux.read_par_from_excel(file_name,
                'ProductionPolyolefins', (44, 'C'), (54, 'N'), (1, 1))


    print('Loading IHP data......')
    # Load the parameters for the warehouse shipping
    LT = faux.read_par_from_excel(file_name,
                'IHPs', (6, 'C'), (7, 'E'), (0, 1))

    IH_low = faux.read_par_from_excel(file_name,
                'IHPs', (10, 'C'), (20, 'F'), (1, 1))

    IH_upper = faux.read_par_from_excel(file_name,
                'IHPs', (23, 'C'), (33, 'F'), (1, 1))

    pie = faux.read_par_from_excel(file_name,
                'IHPs', (36, 'C'), (37, 'H'), (0, 1))


    print('Loading Scenario data......')
    # Load the parameters for availability scenarios
    delta = faux.read_par_from_excel(file_name,
                'ScenarioAvailability', (4, 'D'), (5, 'O'), (0, 1))

    phi = faux.read_par_from_excel(file_name,
                'ScenarioAvailability', (8, 'D'), (19, 'P'), (1, 1))


    # Load the parameters for sales scenarios
    D = faux.read_par_from_excel(file_name,
                'ScenarioSales', (7, 'D'), (67, 'Q'), (2, 1))

    SP = faux.read_par_from_excel(file_name,
                'ScenarioSales', (72, 'D'), (132, 'Q'), (2, 1))

    SO = faux.read_par_from_excel(file_name,
                'ScenarioSales', (135, 'D'), (143, 'P'), (1, 1))

    S_max = faux.read_par_from_excel(file_name,
                'ScenarioSales', (146, 'D'), (147, 'K'), (0, 1))

    S_min = faux.read_par_from_excel(file_name,
                'ScenarioSales', (151, 'D'), (152, 'K'), (0, 1))


    # Load the parameters for purchases scenarios
    PC = faux.read_par_from_excel(file_name,
                'ScenarioPurchases', (5, 'D'), (13, 'P'), (1, 1))

    PU_max = faux.read_par_from_excel(file_name,
                'ScenarioPurchases', (16, 'D'), (17, 'K'), (0, 1))

    PU_min = faux.read_par_from_excel(file_name,
                'ScenarioPurchases', (20, 'D'), (21, 'K'), (0, 1))

    IC_ini_level = faux.read_par_from_excel(file_name,
                'ScenarioPurchases', (24, 'C'), (25, 'J'), (0, 1))

    # Load the additional parameters
    print('Loading additional data......')

    FL_max = faux.read_par_from_excel(file_name,
                'AdditionalParameters', (3, 'C'), (4, 'J'), (0, 1))

    FL_min = faux.read_par_from_excel(file_name,
                'AdditionalParameters', (8, 'C'), (9, 'J'), (0, 1))

    Qtil = faux.read_par_from_excel(file_name,
                'AdditionalParameters', (13, 'C'), (43, 'P'), (2, 1))

    # initialise set mapping
    HC = faux.read_par_from_excel(file_name,
                'set', (25, 'E'), (28, 'K'), (1, 1))

    IM = faux.read_par_from_excel(file_name,
                'set', (31, 'E'), (37, 'M'), (1, 1))

    GJ = faux.read_par_from_excel(file_name,
                'set', (40, 'E'), (50, 'P'), (1, 1))


    fixed_var = faux.ParaFixedInput(p_min, p_max, PR, tao, miu, n, LT,
    IC_low, IH_low, IC_upper, IH_upper, HC, PU_max, PU_min, S_max, S_min,
    FL_max, FL_min, IM, GJ)

    variable_par = faux.ParaVarInput(delta, phi, D, SP, SO, PC, OC, OP,
    IC_ini_level, pie, Qtil)

    return set_input, fixed_var, variable_par


def main():
    """
    This is the main function which calls all other functions to solve the
    optimisation model
    """
    print('Start building the model......')
    # initialise the concreteModel
    PSE_model = ConcreteModel()

    # get the data input as objects
    workingDirectory = os.environ.get('PSE_BOROUGE_WORKING_DIR')
    Excel_file = os.path.join(workingDirectory, 'Borouge_Data_Final_Demo.xlsm')
    set_input, fixed_par, variable_par = data_construction(Excel_file)

    print(fixed_par.p_max)
    print(fixed_par.p_min)

    #print(fixed_par.)
    # set initialisation
    fset.set_initialisation(PSE_model, set_input)

    # parameter initialisation
    fpar.parameter_initialisation(PSE_model, fixed_par, variable_par)

    # variable initialisation
    fvar.variable_initialisation(PSE_model)

    # constraint initialisation
    fcon.constraint_definition(PSE_model)


    print('Solving......')
    # set up the model
    opt = SolverFactory('CBC.exe')
    #opt.options['mipgap'] = 0.001
    #opt.options['threads'] = 0

    results = opt.solve(PSE_model, tee = True,
    symbolic_solver_labels = True)

    PSE_model.solutions.store_to(results)
    results_file = os.path.join(workingDirectory, 'solution_fi.yml')
    #print(results_file)

    results.write(filename = results_file)

if __name__ == '__main__':
    main()
