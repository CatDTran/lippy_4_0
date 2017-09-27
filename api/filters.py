"""
A collections of common filters that might come handy sometimes
"""
import pandas as pd


def set_baseline_to_threshold(dataframe=None, columns=None, rows=None, threshold=100, set_value=None):
    """
    This function will take a DataFrame and check to see which value is under a threshold. If a value is under a threshold,
    it will set that value equal to set_value parameter. The columns, and rows in which values are checked can be specified.
    :param dataframe: The pandas DataFrame that hold values that we want to set a baseline.
    :param columns: Columns that contains values to be checked.
    :param rows: Rows that contains values to be checked
    :param threshold: The threshold under which values will be set to set_value
    :param set_value: The value to set to for values that is under or equal to threshold.
    :return: A new DataFrame that contains modified values.
    """
    # Raise error when there's no dataframe
    if dataframe is None:
        raise ValueError("A dataframe parameter is required")
    # use all dataframe columns if no columns parameter specified
    if columns is None:
        columns = list(dataframe)
    # use all rows if no rows parameter specified, currently all rows are considered
    if rows is None:
        pass
    # if no set_value is passed, default to the threshold value
    if set_value is None:
        set_value = threshold

    new_df = dataframe.copy()
    new_df = new_df.where(new_df >= threshold, set_value, raise_on_error=False)
    return new_df

