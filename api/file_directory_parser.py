"""

Created: 09/20/2017
Author: Cat Tran
Description: In general, this module contains the functions that help reading/parsing/listing files and directories.

"""
import os

import pandas as pd

def read_data_from_file(file_path):
    """
    This function reads a file (excel or csv) and return a pandas.DataFrame() that represents the data inside that file.
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

def list_files_in_directory(dir_path):
    """
    This function lists all files that live in a given directory
    :param dir_path: The absolute path to a directory
    :return: a list of file names
    """
    file_names = os.walk(dir_path)[2]
    return  file_names

def list_directories_in_directory(dir_path):
    """
    This function lists all sub directories within a given directory
    :param dir_path: the parent directory
    :return: a list of sub directories
    """
    sub_directory_names = os.walk(dir_path)[1]
    return sub_directory_names

