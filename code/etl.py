from database import connection
import pandas as pd
import numpy as np

def extract_csv():
    """
    Load CSV files
    """
    attendance = pd.read_csv("/Users/sa10/Downloads/Education-Capstone/data/2016-17_-_2020-23_Citywide_End-of-Year_Attendance_and_Chronic_Absenteeism_Data_20250604.csv")
    graduation = pd.read_csv("/Users/sa10/Downloads/Education-Capstone/data/Graduation_results_for_Cohorts_2012_to_2019__Classes_of_2016_to_2023__20250609.csv")
    return attendance, graduation

def transform_attendance(attendance):
    """
    - Convert object types to integers or floats
    - Remove suppressed data ('s' values)
    """
    # Convert numeric columns
    numeric_columns = [col for col in attendance.columns if "#" in col or "%" in col]
    for col in numeric_columns:
        attendance[col] = pd.to_numeric(attendance[col], errors="coerce")
        if "#" in col:
            attendance[col] = attendance[col].astype("Int64")

    # Remove suppressed rows
    suppressed_rows = attendance.isin(['s']).any(axis=1)
    attendance = attendance[~suppressed_rows]

    return attendance

def transform_graduation(graduation):
    """
    - Convert object types to integers or floats
    - Calculate cohort duration and graduation year
    """
    numeric_columns = [col for col in graduation.columns if "#" in col or "%" in col]
    for col in numeric_columns:
        graduation[col] = pd.to_numeric(graduation[col], errors="coerce")
        if "#" in col:
            graduation[col] = graduation[col].astype("Int64")

    graduation["Cohort Duration"] = graduation["Cohort"].str.extract(r"(\d+)").astype(int)
    graduation["Graduation Year"] = graduation["Cohort Year"] + graduation["Cohort Duration"]

    return graduation

