"""

Author: Cat Tran
Created on: 09/27/2017

A collections of common filters that are commonly used in lipidomics research.
"""
import pandas as pd


def set_baseline_to_value(dataframe=None, columns=None, rows=None, threshold=100, set_value=None):
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


def neutral_loss_filter(dataframe=None, nl_column='neutral_loss', threshold=0):
    """
    This method accepts a dataframe that contains a neutral loss column as parameter; it will return a new dataframe that
    only contains rows where neutral loss value is greater or equal to the threshold. The original Dataframe is unmodified.
    :param dataframe: A pandas Dataframe contains a neutral loss column.
    :param nl_column: A string name for the neutral loss column.
    :param threshold: A float value for the threshold.
    :return:
    """
    if dataframe is None:
        raise ValueError("The 'dataframe' parameter containing a neutral loss column must be specified!")

    new_df = dataframe.copy()   # make a copy to avoid modifying the original Dataframe
    new_df = new_df[new_df[nl_column] >= threshold] # will potentially throw column not found or key-error error
    return new_df


def low_average_filter(dataframe=None, columns=None, threshold=100):
    """
    This method accepts a dataframe in which row values are numeric intensities and calculate the average of each row. If
    the average of each row is not greater or equal than the threshold, it will filter out those rows, and return a new
    dataframe. The original dataframe will be unmodified.
    :param dataframe: A pandas Dataframe that contains numeric values to be filtered.
    ;:param columns: A list of subset of columns that this method will perform filtering. If the default is None, all columns
    will be considered.
    :param threshold: A float value in which the row averages will be compared against.
    :return: A new pandas Dataframe.
    """
    if dataframe is None:
        raise ValueError("The 'dataframe' parameter containing numeric values must be specified!")

    new_df = dataframe.copy()
    # If the default value of columns is None, all columns are considered
    if columns is None:
        new_df = new_df.loc[new_df.mean(axis=1) >= threshold]
    else:
        new_df = new_df.loc[new_df[columns].mean(axis=1) >= threshold]
    return new_df


def average_and_max_filter(dataframe=None, columns=None, avg_threshold=100, max_threshold=300):
    """
    This method accepts a pandas Dataframe that contains numeric values in its rows. It will perform 2 tests, an average
    test and a max test. The average test is where the average for each row is calculated, if this average is not greater
    or equal to the avg_threshold, that row fails the test. The max test is where the max value of each row is located, if
    the max value of each row is not greater or equal to the max_threshold, that row fails the test. If a row fails BOTH
    tests, it will be filtered out. The returned dataframe only contains the rows that do not fail BOTH test, failing one
    test but passing the other is fine. The original dataframe will be unmodified.
    :param dataframe: A pandas Dataframe that contains numeric values.
    :param columns: A list of columns name in which the tests will be performed.
    :param avg_threshold: A threshold for the average test.
    :param max_threshold: A threshold for the max test.
    :return: A new pandas Dataframe.
    """
    if dataframe is None:
        raise ValueError("The 'dataframe' parameter containing numeric value to be filtered must be specified!")

    new_df = dataframe.copy()
    # if columns is not specified, all columns in the dataframe are considered
    if columns is None:
        new_df = new_df.loc[(new_df.mean(axis=1) >= avg_threshold) | (new_df.max(axis=1) >= max_threshold)]
    else:
        new_df = new_df.loc[(new_df[columns].mean(axis=1) >= avg_threshold) | (new_df[columns].max(axis=1) >= max_threshold)]
    return new_df


def low_average_group_filter(dataframe=None, group=None, threshold=100):
    """
    This is basically a wrapper for low_average_filter().
    :param dataframe: See low_average_filter().
    :param group: A list of group columns that this method will consider.
    :param threshold: See low_average_filter().
    :return: A new dataframe.
    """
    # This wrapper actually requires a group of column names
    if group is None:
        raise ValueError("The 'group' parameter must be specified!")
    return low_average_filter(dataframe=dataframe, columns=group, threshold=threshold)


def average_and_max_group_filter(dataframe=None, group=None, avg_threshold=100, max_threshold=300):
    """
    This is basically a wrapper for average_max_filter()
    :param dataframe: See average_max_filter
    :param group: A list of group columns that this method will consider.
    :param avg_threshold: See average_max_filter
    :param max_threshold: See average_max_filter
    :return: A new dataframe.
    """
    if group is None:
        raise ValueError("The 'group' parameter must be specified!")
    return average_and_max_filter(dataframe=dataframe, columns=group, avg_threshold=avg_threshold, max_threshold=max_threshold)


def child_peaks_filter(dataframe=None, child_peaks=[(1, 10)], neu_loss_col='neutral_loss'):
    """
    This method will filter out any rows that have neutral loss value falls between the 'child_peaks' parameter pair. As
    result, it will only return a new dataframe that contains only rows with neutral loss values that do not fall between
    child_peaks parameter pair/s. The original dataframe is un-modified.
    :param dataframe: An original dataframe that need child peaks filtered.
    :param child_peaks: A list of tuples that contains the range within which neutral loss values are filtered out.
    :param neu_loss_col: A string column name where the neutral loss values can be found.
    :return: A new dataframe
    """
    if dataframe is None:
        raise ValueError("The 'dataframe' parameter must be specified!")
    new_df = dataframe.copy()
    # perform child peak filter for each of the (min,max) child peaks in the 'child_peaks' parameters
    for pair in child_peaks:
        # filter, and concatenate rows that have neutral loss above the max and rows that have neutral loss below the min
        new_df = pd.concat([new_df[new_df[neu_loss_col] > max(pair)], new_df[new_df[neu_loss_col] < min(pair)]])
    return  new_df



def group_quantile_filter(dataframe=None, group=None, quantile=0.3, threshold=100):
    """
    This method will look at a group of columns in the dataframe and perform a quantile test. For each row in that group,
    if there is at least the quantile (fyi, 0.3 = 30%) number of the cells that is above the threshold, it will keep that row in the new dataframe.
    Otherwise, it will filter that row out. The original dataframe will be unmodified.
    :param dataframe: A pandas Dataframe.
    :param group: A list of columns names that we want to perform the test against.
    :param quantile: A quantile (on the scale of [0, 1]).
    :param threshold: A float value for which the quantile is compared against.
    :return: A new dataframe.
    """
    if dataframe is None or group is None:
        raise ValueError("Both 'dataframe' and 'groups' parameters must be specified!")
    if (quantile < 0 or quantile > 1):
        raise ValueError("The 'quantile' parameter must be within the range of [0, 1] (quantile = 0 or 1 is acceptable)!")
    new_df = dataframe.copy()
    new_df = new_df.loc[ (new_df[group] >= threshold).apply(lambda row: (row==True).sum()/len(row) >= quantile, axis=1) ]
    return new_df

