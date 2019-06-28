###############################################
# This documents contains all the auxiliary ###
# functions and classes being used in the #####
# model. ######################################

class SetInput():
    """
    This is an object that initialise the input sets
    """
    def __init__(self, i, j, g, t, m, c, h):
        self.i = i
        self.j = j
        self.g = g
        self.t = t
        self.m = m
        self.c = c
        self.h = h

class ParaFixedInput():
    """
    This is an object that initialise the fixed parameters
    """
    def __init__(self, p_min, p_max, PR, tao, miu, n, LT, IC_low, IH_low):
        self.p_min = p_min
        self.p_max = p_max
        self.PR = PR
        self.tao = tao
        self.miu = miu
        self.n = n
        self.LT = LT
        self.IC_low = IC_low
        self.IH_low = IH_low

class ParaVarInput():
    """
    This is an object that initialise the varying parameters
    """
    def __init__(self, f, phi, D, SP, SO, PC, OC, OP,
    IC_ini_level, IH_ini_level, S_ini_level):
        self.f = f
        self.phi = phi
        self.D = D
        self.SP = SP
        self.SO = SO
        self.PC = PC
        self.OC = OC
        self.OP = OP
        self.IC_ini_level = IC_ini_level
        self.IH_ini_level = IH_ini_level
        self.S_ini_level = S_ini_level

def result_data_load(optimisation_model, var_list):
    """
    This function takes the model and the list of variables
    and return the solutions as a dictionary
    """
    result_data = {}
    for i in var_list:
        var_obj = getattr(optimisation_model, i)
        result_data[i] = {}
        for k in var_obj.keys():
            result_data[i][k] = var_obj[k].value
    return result_data
