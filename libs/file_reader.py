"""

Created: 09/20/2017
Author: Cat Tran
Description: In general, this module contains the functions that help reading raw data files and convert them to pandas.DataFrame

"""
import os

import pandas as pd

def read_experiment_meta(file_path):
    """
    This function reads a file (excel, or csv) and return a pandas.DataFrame() that represents the data inside that file.
    File extension must be either *.csv or *.xlsx!
    :param file_path: The absolute path string to file
    :return: pandas.DataFrame object
    :raise: raises exception when file extension is not one of these above
    """
    dataframe = None
    if file_path.endswith('.csv'):
        dataframe = pd.read_csv()
    elif file_path.endswith('xlsx'):
        dataframe = pd.read_excel()
    else:
        raise IOError('File extension not supported')
    return dataframe


