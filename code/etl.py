from database import connection
import pandas as pd
import numpy as np


def extract_csv():
    """
    load csv files
    """
    attendance = pd.read_csv("/Users/sa10/Downloads/Education-Capstone/data/2016-17_-_2020-23_Citywide_End-of-Year_Attendance_and_Chronic_Absenteeism_Data_20250604.csv")
    demographics = pd.read_csv("/Users/sa10/Downloads/Education-Capstone/data/2019-20_Demographic_Snapshot_-_Citywide_20250604.csv")
    graduation = pd.read_csv("/Users/sa10/Downloads/Education-Capstone/data/Graduation_results_for_Cohorts_2012_to_2019__Classes_of_2016_to_2023__20250609.csv")
    return attendance, demographics, graduation


def transform_attendance(attendance):
    """
    Change object types into integers or float types
    Remove suppressed data ('s' values).
    """
    # Changing object types into integers or float types for the attendace datasets
    column = [col for col in attendance.columns if "#" in col or "%" in col]
    for col in column:
      attendance[col] = pd.to_numeric(attendance[col], errors="coerce")
      if "#" in col:
        attendance[col] = attendance[col].astype("Int64")

    # The .any(axis=1) checks if 's' is present in at least one column for each row
    rows_with_s_across_columns = attendance.isin(['s']).any(axis=1)
    # Filter the DataFrame to get only those rows
    filtered_attendance = attendance[rows_with_s_across_columns]
    # Count the number of such rows
    count_s_across_columns = len(filtered_attendance)
    # Dropped suppressed data
    rows_to_drop = attendance.isin(['s']).any(axis=1)
    attendance = attendance[~rows_to_drop]

    return attendance

def transform_graduation(graduation):
    """
    Change object types into integers or float types
    Extract cohort duration and calculate graduation year
    """

    # Changing object types into integers or float types for the graduation datasets
    column = [col for col in graduation.columns if "#" in col or "%" in col]
    for col in column:
        graduation[col] = pd.to_numeric(graduation[col], errors="coerce")
        if "#" in col:
            graduation[col] = graduation[col].astype("Int64")

    # Extract the number of years from the Cohort column
    graduation["Cohort Duration"] = graduation["Cohort"].str.extract(r"(\d+)").astype(int)
    # Add to Cohort Year to create Graduation Year
    graduation["Graduation Year"] = graduation["Cohort Year"] + graduation["Cohort Duration"]

    return graduation
