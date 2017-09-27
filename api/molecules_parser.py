"""
This module contains functions that can return work on lipids molecular properties. For example, it can parse name
strings based on number of elements and double bonds, calculate mass, find name that fit precursor/fragment mass pair...
"""
import numpy as np
import pandas as pd

def get_name_from_mass_pair(precursor=None, fragment=None, mass_name_list=None, cols_tuple=('mass_pre', 'mass_frag', 'name'), pm_tolerance=0.3, fm_tolerance=None):
    """
    This function accepts a precursor mass, a fragment mass, and a list of known precursor/fragment mass pairs and their names,
    and return the the name/s string that match the precursor/fragment mass pair (to a certain 'mass_tolerance')
    passed in as arguments.
    :param precursor: The float value of a precursor mass.
    :param fragment: The float value of a fragment mass.
    :param mass_name_list: A pandas.DataFrame that contains the list of known mass pairs and their names.
    :param cols_tuple: A list of columns name in the mass_name_list DataFrame that this function will search in for matching.
    :param pm_tolerance: The precursor mass tolerance within which a precursor mass will be considered matched from the precursor mass
    in the list.
    :param fm_tolerance: The fragment mass tolerance within which a fragment mass will be considered matched from the fragment mass
    in the list. The default is equal to pm_tolerance.
    :return: A list of matched name strings.
    """
    # default fragment mass tolerance to precursor mass tolerance if not specified
    if fm_tolerance is None:
        fm_tolerance = pm_tolerance
    # raise error when
    if precursor is None or fragment is None or mass_name_list is None:
        raise ValueError('Both \'precursor\' and \'mass_name_list\' parameter required')
    names = list()
    for index, row in mass_name_list.iterrows():
        # first search for precursor match
        if np.isclose(precursor, row[cols_tuple[0]], atol=pm_tolerance):
            # then search for fragment match
            if np.isclose(fragment, row[cols_tuple[1]], atol=fm_tolerance):
                names.append(row[cols_tuple[2]])
    return names