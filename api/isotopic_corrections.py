"""
Author: Cat Tran
Created: 10/03/2017

This file contains functions that perform isotopic related operation on a dataset
"""
import re
import json

from scipy.stats import binom

def get_isotope_distribution_json(isotope_distribution_file=None):
    """
    This functions read a JSON file that contains an JSON object of isotopes and their abundances in nature. It will return a JSON object.
    The JSON file is expected to contain ONE single JSON object with the form: {
                                                                                  "H1":   {"mass": null, "abundance": 99.9885},
                                                                                  "H2":   {"mass": null, "abundance": 0.0115},
                                                                                  "Li6":  {"mass": null, "abundance":7.59},
                                                                                  "Li7":  {"mass": null, "abundance":92.71},
                                                                                  "C12":  {"mass": null, "abundance":98.93},
                                                                                  "C13":  {"mass": null, "abundance":1.07},
                                                                                  "O16":  {"mass": null, "abundance":99.757},
                                                                                  "O17":  {"mass": null, "abundance":0.038},
                                                                                  "O18":  {"mass": null, "abundance":0.205},
                                                                                  "F19":  {"mass": null, "abundance":100},
                                                                                  "NA23": {"mass": null, "abundance":100},
                                                                                  "P31":  {"mass": null, "abundance":100},
                                                                                    ...
                                                                                }.
    Currently, exact mass of elements is stored in a separate JSON file, but one could add value to the "mass" key for these
    isotopes distribution in their own isotope files if desired. The "mass" key defined here is just for the sake of convenience.
    :param isotope_distribution_file: An absolute path to the JSON file that contains isotopes
    :return: A JSON object.
    """
    # Open the JSON file and read the JSON object
    with open(isotope_distribution_file) as json_data:
        data = json.load(json_data)
    return data

def get_isotope_distribution_from_natoms(natoms=None, isotope=None, abundance=None):
    """
    This function output the potential number of isotopes atoms and their probabilities given the total number of carbons
    (in a molecule). What it does is basically calculate the probability mass function.
    :param natoms: An integer number of atoms of interest in a molecule.
    :param isotope: An isotope string of interest(ex: "C13"). NOTE: current not used, and has no effect on the output whatsoever.
    :param mass_abundances: A JSON object in which the keys are the isotopes interest such as "C13", "O16" ..., and the values
    are the abundances of that isotope in nature. It is expected to be in the form: {
                                                                                        "C12":  {"mass": null, "abundance":98.93},
                                                                                        "C13":  {"mass": null, "abundance":1.07},
                                                                                    }.
    :return: A dictionary of potential number of isotopes and their probabilities.
    """
    # If
    if natoms is None or abundance is None:
        raise ValueError("Both 'natoms' and 'abundance' parameters are required!")
    n_isotopes_probabilities = dict()
    for k_isotopes in range(0,natoms + 1):
        n_isotopes_probabilities[k_isotopes] = binom.pmf(k_isotopes, natoms, abundance)
        print(n_isotopes_probabilities)
    
