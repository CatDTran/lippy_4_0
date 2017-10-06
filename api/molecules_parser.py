"""

Author: Cat Tran
Created on: 09/27/2017

This module contains functions that can return work on lipids molecular properties. For example, it can parse name
strings based on number of elements and double bonds, calculate mass, find name that fit precursor/fragment mass pair...
"""


import json
import re

import numpy as np
import pandas as pd


def search_name_from_mass_pair(precursor=None, fragment=None, mass_name_list=None, cols_tuple=('mass_pre', 'mass_frag', 'name'), pm_tolerance=0.3, fm_tolerance=None, atol=True):
    """
    This function accepts a precursor mass, a fragment mass, and a list of known precursor/fragment mass pairs and their names,
    and returns the the name/s string that match the precursor/fragment mass pair (to a certain 'mass_tolerance')
    passed in as arguments.
    :param precursor: The float value of a precursor mass.
    :param fragment: The float value of a fragment mass.
    :param mass_name_list: A pandas.DataFrame that contains the list of known mass pairs and their names. The DataFrame must have
    the columns names shown in 'cols_tuple' parameter.
    :param cols_tuple: A tuple of columns names that appears in the 'mass_name_list' DataFrame. This tuple MUST have the following
    order: 0: Precursor mass | 1: Fragment mass | 2: name/formula!
    :param pm_tolerance: The precursor mass tolerance within which a precursor mass will be considered matched from the precursor mass
    in the list.
    :param fm_tolerance: The fragment mass tolerance within which a fragment mass will be considered matched from the fragment mass
    in the list. The default is equal to pm_tolerance.
    :param atol: Whether the tolerance parameter is absolute or relative. THe default is True for absolute; and False for relative
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
        if atol:    # absolute tolerance is the default
            # first search for precursor match
            if np.isclose(precursor, row[cols_tuple[0]], atol=pm_tolerance):
                # then search for fragment match
                if np.isclose(fragment, row[cols_tuple[1]], atol=fm_tolerance):
                    names.append(row[cols_tuple[2]])
        else:   # when atol is false, then relative tolerance is used instead
            # first search for precursor match
            if np.isclose(precursor, row[cols_tuple[0]], rtol=pm_tolerance):
                # then search for fragment match
                if np.isclose(fragment, row[cols_tuple[1]], rtol=fm_tolerance):
                    names.append(row[cols_tuple[2]])
    return names


def calculate_mass_from_formula(formula=None, elements_mass_file=None):
    """
    This function calculate the mass of a formula passed in as a string. What it does is that it parses the elements appear
    in the formula string and look for their masses defined in a JSON file specified in 'elements_mass_file', and return the
    mass by multiplication and addition.
    :param formula: A string formula. It is expected to be something like this C57H104O6
    :param elements_mass_file: The absolute path to a file that contain JSON for a list of elements. The JSON file should
    contains 1 single object and have the format similar to this:   {
                                                                      "C": 12.000000,
                                                                      "H": 1.00782503223,
                                                                      "O": 15.99491461957,
                                                                      "P": 30.97376199842
                                                                      ...
                                                                    }
    :return: A float mass value of the formula.
    """
    # Raise error if neither formula nor elements_mass_file are specified
    if formula is None or elements_mass_file is None:
        raise ValueError("Both 'formula' and 'elements_mass_file' must be specified!")
    mass_sum = 0
    # first open the json file that contains elements and their masses
    with open(elements_mass_file) as json_data:
        data = json.load(json_data)
        for tup in re.findall(r'([A-Z][a-z]*)(\d*)', formula):
            if tup[1]:
                mass_sum = mass_sum + int(tup[1]) * data[tup[0]]
            else:
                mass_sum = mass_sum + data[tup[0]]
    return mass_sum


def calculate_mass_from_common_name(name=None, elements_mass_file=None):
    """
    This function calculate the mass of a formula passed in as a string. What it does is that it parses the elements appear
    in the formula string and look for their masses defined in a JSON file specified in 'elements_mass_file', and return the
    mass by multiplication and addition.
    :param formula: A string formula. It is expected to be something like this C57H104O6
    :param elements_mass_file: The absolute path to a file that contain JSON for a list of elements. The JSON file should
    contains 1 single object and have the format similar to this:   {
                                                                      "C": 12.000000,
                                                                      "H": 1.00782503223,
                                                                      "O": 15.99491461957,
                                                                      "P": 30.97376199842
                                                                      ...
                                                                    }
    :return: A float mass value of the formula.
    """
    pass


def get_name_from_carbons_double_bonds(group=None, ncarbons=None, ndouble_bonds=None):
    """
    This function accept a lipid group, number of carbons, and number of double bonds as arguments and return a name string
    that represents a lipid. NOTE: This function perform no test on whether the resulting lipid name is valid!
    :param group: A lipid group string. Ex: TAG, DAG, PI ...
    :param ncarbons: Number of total carbons in that lipid.
    :param ndouble_bonds: Number of total double bonds in that lipid. Default is None, which represent saturated lipid (no double bonds).
    :return: A lipid name string
    """
    if group is None or ncarbons is None:
        raise ValueError("'group' and 'ncarbons' parameters must be specified!")
    if ndouble_bonds is None:
        return ("%s|%s:%s|" % (group, ncarbons, 0))
    else:
        return ("%s|%s:%s|" % (group, ncarbons, ndouble_bonds))


def get_name_from_double_chains(group=None, chain_1=(0, 0), chain_2=(0, 0)):
    """
    This function return a lipid name from 2 chain tuples passed in as arguments. NOTE: This function perform no test on
    whether the resulting lipid name is valid!
    :param group: A lipid group string. Ex: TAG, PI, DAG ...
    :param chain_1: A tuple contains number of carbon and double bonds in chain 1. Ex: (16, 0)
    :param chain_2: A tuple contains number of carbon and double bonds in chain 2. Ex: (16, 2)
    :return: A lipid name string
    """
    if group is None:
        raise ValueError("'group' and parameter must be specified!")
    name = (get_name_from_carbons_double_bonds(group=group, ncarbons=(chain_1[0] + chain_2[0]) , ndouble_bonds=(chain_1[1] + chain_2[1]))
                                + "(%d:%d~%d:%d)" % (chain_1[0], chain_1[1], chain_2[0], chain_2[1]))
    return name


def build_lipids_from_group_chains(group=None, chains=None):
    pass