from database import connection
import pandas as pd

def extract_csv():
    """
    Load CSV files
    """
    attendance = pd.read_csv("/Users/sa17/Library/Mobile Documents/com~apple~CloudDocs/Brag Folder/projects/Education-Capstone/data/attendance.csv")
    graduation = pd.read_csv("/Users/sa17/Library/Mobile Documents/com~apple~CloudDocs/Brag Folder/projects/Education-Capstone/data/2023-graduation-rates-public-borough.csv")
    regents = pd.read_csv("/Users/sa17/Library/Mobile Documents/com~apple~CloudDocs/Brag Folder/projects/Education-Capstone/data/2014-15-to-2022-23-nyc-regents-overall-and-by-category---public 2 (1).csv")
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
    "Graduation Year": "grad_year",
})

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
    "Year": "test_year",
    "Total Tested": "total_tested",
    "Mean Score": "mean_score",
    "Number Scoring Below 65": "number_scoring_below_60",
    "Percent Scoring Below 65": "percent_scoring_below_60",
    "Number Scoring 80 or Above": "number_scoring_above_80",
    "Percent Scoring 80 or Above": "percent_scoring_above_80",
    "Number Scoring 65 or Above": "number_scoring_cr",
    "Percent Scoring 65 or Above": "percent_scoring_cr"
    })

    return regents


def load_postgres(df, table_name):
    """
    Insert cleaned data into PostgreSQL table.
    """
    conn = connection()
    cursor = conn.cursor()

    # Prepare and insert data row by row
    if table_name == "attendance_and_absenteeism":
        insert_into = """
        INSERT INTO "attendance_and_absenteeism" 
        ("borough", "grade", "category_name", "academic_year_id", "total_days", "days_absent_count", 
        "days_present_count", "attendance_percent", "contributing_10plus_total_days_and_1plus_pres_day", 
        "chronically_absent_count", "chronically_absent_percent")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for _, row in df.iterrows():
            values = (
                row["borough"], row["grade"], row["category_name"], row["academic_year_id"],
                row["total_days"], row["days_absent_count"], row["days_present_count"],
                row["attendance_percent"], row["contributing_10plus_total_days_and_1plus_pres_day"],
                row["chronically_absent_count"], row["chronically_absent_percent"]
            )
            cursor.execute(insert_into, values)

    elif table_name == "graduation_data":
        insert_into = """
        INSERT INTO "graduation_data" 
        ("borough", "cohort_name", "cohort_year", "category_name", "total_cohort", "grad_count",
        "grad_percent", "total_regents_count", "total_regents_percent", "total_regents_grad_percent",
        "advanced_regents_count", "advanced_regents_percent", "advanced_regents_grads_percent",
        "regents_without_advanced_count", "regents_without_advanced_percent", "regents_without_advanced_grad_percent",
        "local_diploma_count", "local_diploma_perc", "percent_local_of_grads",
        "still_enrolled_count", "still_enrolled_percent", "dropout_count", "dropout_percent",
        "sacc_iep_diploma_count", "sacc_iep_diploma_percent", "tasc_ged_count", "tasc_ged_percent", "grad_year")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for _, row in df.iterrows():
            values = (
                row["borough"], row["cohort_name"], row["cohort_year"], row["category_name"], row["total_cohort"],
                row["grad_count"], row["grad_percent"], row["total_regents_count"], row["total_regents_percent"],
                row["total_regents_grad_percent"], row["advanced_regents_count"], row["advanced_regents_percent"],
                row["advanced_regents_grads_percent"], row["regents_without_advanced_count"],
                row["regents_without_advanced_percent"], row["regents_without_advanced_grad_percent"],
                row["local_diploma_count"], row["local_diploma_perc"], row["percent_local_of_grads"],
                row["still_enrolled_count"], row["still_enrolled_percent"], row["dropout_count"], 
                row["dropout_percent"], row["sacc_iep_diploma_count"], row["sacc_iep_diploma_percent"],
                row["tasc_ged_count"],row["tasc_ged_percent"], row["grad_year"]
            )
            cursor.execute(insert_into, values)

    elif table_name == "regents":
        insert_into = """
        INSERT INTO "regents"
        ("regents_exam", "borough", "category_name", "test_year", "total_tested", "mean_score",
        "number_scoring_below_60", "percent_scoring_below_60", "number_scoring_above_80",
        "percent_scoring_above_80", "number_scoring_cr", "percent_scoring_cr") 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for _, row in df.iterrows():
            values = (
                row["regents_exam"], row["borough"], row["category_name"], row["test_year"],row["total_tested"], 
                row["mean_score"], row["number_scoring_below_60"], row["percent_scoring_below_60"],row["number_scoring_above_80"],
                row["percent_scoring_above_80"],row["number_scoring_cr"],row["percent_scoring_cr"]
            )
            cursor.execute(insert_into, values)
             
    # Commit transaction and close connection
    conn.commit()
    print(f"{table_name.capitalize()} data successfully loaded to PostgreSQL.")
    cursor.close()
    conn.close()

          
def main():
    # Extract
    attendance, graduation, regents = extract_csv()

    # Transform
    clean_attendance = transform_attendance(attendance)
    clean_graduation = transform_graduation(graduation)
    clean_regents = transform_regents(regents)

    # Load
    load_postgres(clean_attendance, "attendance_and_absenteeism")
    load_postgres(clean_graduation, "graduation_data")
    load_postgres(clean_regents, "regents")


if __name__ == "__main__":
    main()