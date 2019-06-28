###############################################
# This documents contains all the auxiliary ###
# functions and classes being used in the #####
# model. ######################################

# Import nccessary packages
import xlrd


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
    def __init__(self, p_min, p_max, PR, tao, miu, n, LT, IC_low, IH_low,
    IC_upper, HC):
        self.p_min = p_min
        self.p_max = p_max
        self.PR = PR
        self.tao = tao
        self.miu = miu
        self.n = n
        self.LT = LT
        self.IC_low = IC_low
        self.IH_low = IH_low
        self.IC_upper = IC_upper
        self.HC = HC

class ParaVarInput():
    """
    This is an object that initialise the varying parameters
    """
    def __init__(self, f, phi, D, SP, SO, PC, OC, OP,
    IC_ini_level, S_ini_level):
        self.f = f
        self.phi = phi
        self.D = D
        self.SP = SP
        self.SO = SO
        self.PC = PC
        self.OC = OC
        self.OP = OP
        self.IC_ini_level = IC_ini_level
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

def read_par_from_excel(file_name, sheet_name, start_loc, end_loc, par_dim):
    """
    This function takes in the excel and the sheet_name + the location
    of the parameter to be retrieved and the paramter dimention
    and return the dictionary that can be used for the optimisation model
    """
    start_loc = cell_loc_conversion(start_loc)
    end_loc = cell_loc_conversion(end_loc)
    if par_dim == (0, 1):

        for sheet in xlrd.open_workbook(file_name).sheets():
            if sheet.name == sheet_name:
                dic_keys = [
                sheet.cell(start_loc[0], col).value
                for col in range(start_loc[1], end_loc[1] + 1)
                ]

                dic_values = [
                sheet.cell(row, col).value
                if sheet.cell_type(row, col) != xlrd.XL_CELL_EMPTY else 0
                for row in range(start_loc[0] + 1, end_loc[0] + 1)
                for col in range(start_loc[1], end_loc[1] + 1)
                ]

    elif par_dim == (1, 1):
        for sheet in xlrd.open_workbook(file_name).sheets():
            if sheet.name == sheet_name:
                dic_keys = [
                (sheet.cell(row, start_loc[1]).value,
                sheet.cell(start_loc[0], col).value)
                for col in range(start_loc[1], end_loc[1] + 1)
                for row in range(start_loc[0], end_loc[0] + 1)
                if sheet.cell_type(row, start_loc[1]) != xlrd.XL_CELL_EMPTY
                and sheet.cell_type(start_loc[0], col) != xlrd.XL_CELL_EMPTY
                ]

                dic_values = [
                sheet.cell(row, col).value
                if sheet.cell_type(row, col) != xlrd.XL_CELL_EMPTY else 0
                for col in range(start_loc[1] + 1, end_loc[1] + 1)
                for row in range(start_loc[0] + 1, end_loc[0] + 1)
                ]

    elif par_dim == (2, 1):
        for sheet in xlrd.open_workbook(file_name).sheets():
            if sheet.name == sheet_name:
                dic_keys = [
                (sheet.cell(row, start_loc[1]).value,
                sheet.cell(row, start_loc[1] + 1).value,
                sheet.cell(start_loc[0], col).value)
                for col in range(start_loc[1], end_loc[1] + 1)
                for row in range(start_loc[0], end_loc[0] + 1)
                if sheet.cell_type(row, start_loc[1]) != xlrd.XL_CELL_EMPTY
                and sheet.cell_type(row, start_loc[1] + 1) != xlrd.XL_CELL_EMPTY
                and sheet.cell_type(start_loc[0], col) != xlrd.XL_CELL_EMPTY
                ]

                dic_values = [
                sheet.cell(row, col).value
                if sheet.cell_type(row, col) != xlrd.XL_CELL_EMPTY else 0
                for col in range(start_loc[1] + 2, end_loc[1] + 1)
                for row in range(start_loc[0] + 1, end_loc[0] + 1)
                ]

    par_dict = dict(zip(dic_keys, dic_values))
    return par_dict

def read_set_from_excel(file_name, sheet_name, start_loc, end_loc):
    """
    This function takes in the file_name, the sheet_name, and the start and
    end location of the set in the sheet and returns the designated set
    """
    start_loc = cell_loc_conversion(start_loc)
    end_loc = cell_loc_conversion(end_loc)
    for sheet in xlrd.open_workbook(file_name).sheets():
        if sheet.name == sheet_name:
            set_list = [
            sheet.cell(start_loc[0], col).value
            for col in range(start_loc[1], end_loc[1] + 1)
            ]

    return set_list


def cell_loc_conversion(user_input_loc):
    """
    This function takes in the excel cell number (x, A) where x is the
    row number and A is the column letter and convert it into a loc
    tuple which python can read
    """
    return user_input_loc[0] - 1, ord(user_input_loc[1].lower()) - 97
