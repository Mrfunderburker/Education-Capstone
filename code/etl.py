from database import connection
import pandas as pd

def extract_csv():
    """
    Load CSV files
    """
    attendance = pd.read_csv("/Users/sa17/Library/Mobile Documents/com~apple~CloudDocs/Brag Folder/projects/Education-Capstone/data/attendance.csv")
    graduation = pd.read_csv("/Users/sa17/Library/Mobile Documents/com~apple~CloudDocs/Brag Folder/projects/Education-Capstone/data/2023-graduation-rates-public-borough.csv")
    regents = pd.read_csv("/Users/sa17/Library/Mobile Documents/com~apple~CloudDocs/Brag Folder/projects/Education-Capstone/data/2014-15-to-2022-23-nyc-regents-overall-and-by-category---public 2 (1).csv", low_memory=False)
    return attendance, graduation, regents 


def transform_attendance(attendance):
    """
    - Remove suppressed data ("s" values) and "All Students" data
    - Convert object types to integers or floats
    - Rename columns to match SQL
    """

    # Remove suppressed rows
    suppressed_rows = attendance.isin(["s"]).any(axis=1)
    attendance = attendance[~suppressed_rows]
    
    # Drop "All Students" rows 
    attendance = attendance.drop(attendance[attendance["Category"] == "All Students"].index)

    # Convert objects to numeric columns
    numeric_columns = [col for col in attendance.columns if "#" in col or "%" in col or "Grade" in col]
    for col in numeric_columns:
         attendance[col] = pd.to_numeric(attendance[col], errors="coerce")
         if "#" in col or "Grade" in col:
             attendance[col] = attendance[col].astype("Int64")

    # Rename cloumns to match SQL schema
    attendance = attendance.rename(columns={
    "Borough": "borough",
    "Grade": "grade",
    "Category": "category_name",
    "Year": "academic_year_id",
    "# Total Days": "total_days",
    "# Days Absent": "days_absent_count",
    "# Days Present": "days_present_count",
    "% Attendance": "attendance_percent",
    "# Contributing 10+ Total Days and 1+ Pres Day": "contributing_10plus_total_days_and_1plus_pres_day",
    "# Chronically Absent": "chronically_absent_count",
    "% Chronically Absent": "chronically_absent_percent"
    })
  
    # Create start year column 
    attendance["year"] = attendance["academic_year_id"].str[:4]

    # Drop unnecesary columns
    attendance = attendance.drop(["total_days", "days_absent_count", "contributing_10plus_total_days_and_1plus_pres_day", "chronically_absent_percent", "days_present_count"], axis=1)
    
    return attendance


def transform_graduation(graduation):
    """
    - Remove suppressed, "Category" and "All Students" data 
    - Convert object types to integers or floats
    - Calculate cohort duration and graduation year
    - Rename columns to match SQL
    """

    # Remove suppressed rows
    suppressed_rows = graduation.isin(["s"]).any(axis=1)
    graduation = graduation[~suppressed_rows]

    # Drop "Category" rows
    rows_to_drop = graduation.isin(["Category"]).any(axis=1)
    graduation  = graduation[~rows_to_drop]

    # Drop "All Students" rows 
    graduation = graduation.drop(graduation[graduation["Category"] == "All Students"].index)

    # Convert objects to numeric columns
    numeric_columns = [col for col in graduation.columns if "#" in col or "%" in col or "Cohort Year" in col]
    for col in numeric_columns:
         graduation[col] = pd.to_numeric(graduation[col], errors="coerce")
         if "#" in col  or "Cohort Year" in col :
             graduation[col] = graduation[col].astype("Int64")
    
    # Calculate cohort duration and graduation year
    graduation["Cohort Duration"] = graduation["Cohort"].str.extract(r"(\d+)").astype(int)
    graduation["Graduation Year"] = graduation["Cohort Year"] + graduation["Cohort Duration"]

    # Drop cohort duration (No longer needed after creating "Graduation Year")
    graduation = graduation.drop("Cohort Duration", axis=1)   

    # Rename columns to match SQL schema
    graduation = graduation.rename(columns={
    "Borough": "borough",
    "Cohort": "cohort_name", 
    "Cohort Year": "cohort_year",
    "Category": "category_name",
    "# Total Cohort": "total_cohort",
    "# Grads": "grad_count",
    "% Grads": "grad_percent",
    "# Total Regents": "total_regents_count",
    "% Total Regents of Cohort": "total_regents_percent",
    "% Total Regents of Grads": "total_regents_grad_percent",  
    "# Advanced Regents": "advanced_regents_count",
    "% Advanced Regents of Cohort": "advanced_regents_percent",
    "% Advanced Regents of Grads": "advanced_regents_grads_percent",  
    "# Regents without Advanced": "regents_without_advanced_count",
    "% Regents without Advanced of Cohort": "regents_without_advanced_percent",
    "% Regents without Advanced of Grads": "regents_without_advanced_grad_percent",
    "# Local": "local_diploma_count",
    "% Local of Cohort": "local_diploma_perc",
    "% Local of Grads": "percent_local_of_grads",
    "# Still Enrolled": "still_enrolled_count",
    "% Still Enrolled": "still_enrolled_percent",
    "# Dropout": "dropout_count",
    "% Dropout": "dropout_percent",
    "# SACC (IEP Diploma)": "sacc_iep_diploma_count",
    "% SACC (IEP Diploma) of Cohort": "sacc_iep_diploma_percent",
    "# TASC (GED)": "tasc_ged_count",
    "% TASC (GED) of Cohort": "tasc_ged_percent",
    "Graduation Year": "year",
    })
    
    # Select columns i only want to keep 
    graduation = graduation[["borough", "category_name", "advanced_regents_grads_percent", "dropout_count", "dropout_percent", "grad_year", "year"]]
    
    return graduation


def transform_regents(regents):
    """
    - Remove suppressed, "Category" and "All Students" data 
    - Drop unnecessary columns 
    - Convert object types to integers or floats
    - Rename columns to match SQL
    """

    # Remove suppressed rows
    suppressed_rows = regents.isin(['s']).any(axis=1)
    regents = regents[~suppressed_rows]

    # Drop "Category" rows
    rows_to_drop = regents.isin(["Category"]).any(axis=1)
    regents = regents[~rows_to_drop]

    # Drop "All Students" rows 
    regents = regents.drop(regents[regents["Category"] == "All Students"].index)
  
    # Drop unnecesary columns
    regents = regents.drop(["School DBN", "School Name", "School Type", "School Level", "Number meeting CUNY proficiency requirmenets", "Percent meeting CUNY proficiency requirmenets"], axis=1)
    
    # Change objects to numeric columns
    numeric_columns = [
    "Year",
    "Total Tested", 
    "Mean Score",
    "Number Scoring Below 65", 
    "Percent Scoring Below 65",
    "Number Scoring 65 or Above",
    "Percent Scoring 65 or Above",
    "Number Scoring 80 or Above", 
    "Percent Scoring 80 or Above",
]

    for col in numeric_columns:
         regents[col] = pd.to_numeric(regents[col], errors="coerce")
         if regents[col].dropna().apply(lambda x: float(x).is_integer()).all():
             regents[col] = regents[col].astype("Int64")

    # Rename columns to match SQL schema
    regents = regents.rename(columns={
    "Regents Exam": "regents_exam",
    "Borough": "borough",
    "Category": "category_name",
    "Year": "year",
    "Total Tested": "total_tested",
    "Mean Score": "mean_score",
    "Number Scoring Below 65": "number_scoring_below_60",
    "Percent Scoring Below 65": "percent_scoring_below_60",
    "Number Scoring 80 or Above": "number_scoring_above_80",
    "Percent Scoring 80 or Above": "percent_scoring_above_80",
    "Number Scoring 65 or Above": "number_scoring_cr",
    "Percent Scoring 65 or Above": "percent_scoring_cr"
    })
    
    # Select columns I only want to keep
    regents = regents[["regents_exam", "borough", "category_name", "year", "total_tested", "mean_score", "number_scoring_below_60", "percent_scoring_below_60", "number_scoring_above_80", "percent_scoring_above_80"]]

    return regents

def merge_export(attendance, graduation, regents):
    """
    Merge the cleaned datasets on 'borough' and export to CSV.
    """
    # Merge on borough, year, and category_name
    merged_df = pd.merge(attendance, graduation, on=["borough", "year", "category_name"], how="inner")
    merged_df = pd.merge(merged_df, regents, on=["borough", "year", "category_name"], how="inner")

    # Export CSV
    merged_df.to_csv("/Users/sa17/Library/Mobile Documents/com~apple~CloudDocs/Brag Folder/projects/Education-Capstone/data/merged_education_data.csv", index=False)

    return merged_df

          
def main():
    # Extract
    attendance, graduation, regents = extract_csv()

    # Transform
    clean_attendance = transform_attendance(attendance)
    clean_graduation = transform_graduation(graduation)
    clean_regents = transform_regents(regents)

    # Merge
    merged_df = merge_export(clean_attendance, clean_graduation, clean_regents)

if __name__ == "__main__":
    main()