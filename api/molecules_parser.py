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


def get_name_for_mass_pair(precursor=None, fragment=None, mass_name_list=None, pm_tolerance=0.3, fm_tolerance=None, atol=True):
    """
    This function accepts a precursor mass, a fragment mass, and a list of known precursor/fragment mass pairs and their names,
    and returns the the name/s string that match the precursor/fragment mass pair (to a certain 'mass_tolerance')
    passed in as arguments.
    :param precursor: The float value of a precursor mass.
    :param fragment: The float value of a fragment mass.
    :param mass_name_list: A pandas.DataFrame that contains the list of known mass pairs and their names. The DataFrame
    MUST have at least the following column names: 'precursor', 'fragment', and 'name'.
    :param pm_tolerance: The precursor mass tolerance within which a precursor mass will be considered matched from the precursor mass
    in the list.
    :param fm_tolerance: The fragment mass tolerance within which a fragment mass will be considered matched from the fragment mass
    in the list. The default is equal to pm_tolerance.
    :param atol: Whether the tolerance parameter is absolute or relative. THe default is True for absolute; and False for relative
    :return: A DataFrame of matched precursor/fragment mass pair, lipid name... from the name list
    """
    # default fragment mass tolerance to precursor mass tolerance if not specified
    if fm_tolerance is None:
        fm_tolerance = pm_tolerance
    # raise error for missing parameters
    if precursor is None or fragment is None or mass_name_list is None:
        raise ValueError("Both 'precursor' and 'mass_name_list' parameter required")
    if 'precursor' not in list(mass_name_list) or 'fragment' not in  list(mass_name_list) or 'lipid_name' not in list(mass_name_list):
        raise ValueError("'mass_name_list' DataFrame must have 'precursor', 'fragment', and 'name' columns")
    # chose between either relative or absolute tolerance
    if atol:
        precursor_matches = pd.Series(np.isclose(mass_name_list['precursor'], pd.Series(precursor, mass_name_list.index), atol=pm_tolerance))
        fragment_matches = pd.Series(np.isclose(mass_name_list['fragment'], pd.Series(fragment, mass_name_list.index), atol=fm_tolerance))
        pair_matches = np.logical_and(precursor_matches, fragment_matches)
        return mass_name_list[pair_matches]
    else:
        precursor_matches = pd.Series(np.isclose(mass_name_list['precursor'], pd.Series(precursor, mass_name_list.index), atol=pm_tolerance))
        fragment_matches = pd.Series(np.isclose(mass_name_list['fragment'], pd.Series(fragment, mass_name_list.index), atol=fm_tolerance))
        pair_matches = np.logical_and(precursor_matches, fragment_matches)
        return mass_name_list[pair_matches]



def get_mass_from_formula(formula=None, elements_mass_file=None):
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


def parse_lipid_name(name=None):
    """
    This function accept a lipid name string and return a list with elements name as
    keys, and their occurrences as values. If a lipid has 1 head group, it will return the
    head group as well. It utilizes regular expression to accomplish such task.
    :param name: A string that represents the name of a lipids. Read projects_design_guidelines.md
    for more info.
    return: A list of elements name and their occurences.
    """
    if name is None:
        raise ValueError("The 'name' parameter must be specified!")
    parsed = re.findall(r'\w+|\d:\d|\(\d:\d\,\d:\d\,\d:\d\)', name)
    return parsed


def get_mass_from_name(name=None, elements_mass_dict=None, head_group_mass_dict = None):
    """
    This function calculates the mass of a neutral/non-ionized lipid name passed in as a string. What it does is that it
    parses the elements mass defined in the dictionary passed in as 'elements_mass_dict', head group mass passed in as
    'head_group_mass_dict, and return the total mass for that lipid name.
    :param name: A name string. The name is expected to be something like this: FFA|14:1|(14:1)[-H],
                                                                                FAHFA|40:9|(MS2-20:4,20:5)[-H],
                                                                                LPC|22:6|(22:6)[HF2],
                                                                                CE|24:0|(24:0)[NH4],
                                                                                DAG|34:4|(NL-16:1,18:3)[NH4]
                                                                                ...
    :param elements_mass_dict: A dictionary that contains element symbols and their exact masses (non isotopic/standard). The dictionary is expected
    to have the form: {'C': 12.000000, 'H': 1.00782503223, 'O': 15.99491461957, 'P': 30.97376199842,...}.
    :param head_group_mass_dict: A dictionary that contains common head groups and their masses.
    :return: A float mass value for the given name.
    """
    if name is None or elements_mass_dict is None or head_group_mass_dict is None:
        raise ValueError("The 'name', 'elements_mass_dict', and 'head_group_mass_dict' parameters must be specified!")
    # First parse the name into individual entities such as: head group, total carbons, total double bonds
    parsed = parse_lipid_name(name)
    mass = 0
    try:
        # mass = head_group's mass + (ncarbons * carbon_mass) + (ncarbons * 2 + 1) * hydrogen_mass
        mass = (head_group_mass_dict[parsed[0]]  + (elements_mass_dict['C'] * int(parsed[1])) # head group and ncarbons mass
                                                + (int(parsed[1]) * 2 + 1) * int(elements_mass_dict['H']) # total possible hydrogen mass
                                                - (int(parsed[2]) * 2) * int(elements_mass_dict['H'])) # minus hydrogen mass replaced by double bonds
    except:
        print ("Some elements and head group not found")
    return mass



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
