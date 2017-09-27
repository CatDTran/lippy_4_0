"""
This module contains functions that can return work on lipids molecular properties. For example, it can parse formula
string based on number of elements and double bonds, calculate mass, find formula that fit precursor/fragment mass pair...
"""


def get_formula_from_mass_pair(precursor=None, fragment=None, mass_formula_list=None, mass_tolerance=0.3):
    """
    This function accept a precursor mass, a fragment mass, and a list of known precursor/fragment mass pairs and their formulas,
    and return the the formula/s string that match the precursor/fragment mass pair (to a certain 'mass_tolerance')
    passed in as arguments.
    :param precursor: The float value of a precursor mass.
    :param fragment: The float value of a fragment mass.
    :param mass_formula_list: A pandas.DataFrame that contains the list of known mass pairs and their formulas. The DataFrame
    must have
    :param mass_tolerance: The mass tolerance within which precursor/fragment mass will be considered matched from the mass
    in the list.
    :return: A formula string.
    """
    # raise error when
    if precursor is None or fragment is None or mass_formula_list is None:
        raise ValueError('Both \'precursor\' and \'mass_formula_list\' parameter required')
