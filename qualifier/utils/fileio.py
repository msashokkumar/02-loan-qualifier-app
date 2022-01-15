# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv
import os

def load_csv(csvpath):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        CSV header.
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # We will have to preserve header for the output csv file

        csv_header = []

        # Read the CSV data
        for row in csvreader:
            if csv_header:
                data.append(row)
            else:
                csv_header = row
    return csv_header, data


def write_csv(csvpath, headers, data):
    """
    Write a new csv file in the provided location with the provided header and data.

    Args:
        csvpath(Path): The csv file path where the csv file has to be written.
        headers: The header row for the csv file.
        data: Data to be stored in the csv file.
    """

    dir_name = os.path.dirname(csvpath)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    with open(csvpath, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(headers)
        csv_writer.writerows(data)

    return csvpath
