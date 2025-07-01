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
    - Remove suppressed data ("s" values)
    - Convert object types to integers or floats
    """

    # Remove suppressed rows
    suppressed_rows = attendance.isin(["s"]).any(axis=1)
    attendance = attendance[~suppressed_rows]
    
    # Convert objects to numeric columns
    numeric_columns = [col for col in attendance.columns if "#" in col or "%" in col or "Grade" in col]
    for col in numeric_columns:
        attendance[col] = pd.to_numeric(attendance[col], errors="coerce")
        if "#" in col or "Grade" in col:
            attendance[col] = attendance[col].astype("Int64")

    return attendance

def transform_graduation(graduation):
    """
    - Remove suppressed and "Category" data
    - Convert object types to integers or floats
    - Calculate cohort duration and graduation year
    """

    # Remove suppressed rows
    suppressed_rows = graduation.isin(["s"]).any(axis=1)
    graduation = graduation[~suppressed_rows]

    # Dropped "Category" rows
    rows_to_drop = graduation.isin(["Category"]).any(axis=1)
    graduation  = graduation[~rows_to_drop]

    # Convert objects to numeric columns
    numeric_columns = [col for col in graduation.columns if "#" in col or "%" in col or "Cohort Year" in col]
    for col in numeric_columns:
        graduation[col] = pd.to_numeric(graduation[col], errors="coerce")
        if "#" in col  or "Cohort Year" in col :
            graduation[col] = graduation[col].astype("Int64")
    
    # Calculate cohort duration and graduation year
    graduation["Cohort Duration"] = graduation["Cohort"].str.extract(r"(\d+)").astype(int)
    graduation["Graduation Year"] = graduation["Cohort Year"] + graduation["Cohort Duration"]

    return graduation

def transform_regents(regents):

    return regents

def load_postgres(df, table_name):
    """
    Insert cleaned data into PostgreSQL table.
    """
    conn = connection()
    cursor = conn.cursor()

    # Prepare and insert data row by row
    if table_name == "attendance":
        insert_into = """
        INSERT INTO "attendance" ("Borough", "Grade", "Category", "Year", "# Total Days", "# Days Absent", "# Days Present", "% Attendance", "# Contributing 10+ Total Days and 1+ Pres Day", "# Chronically Absent", "% Chronically Absent")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for _, row in df.iterrows():
            values = (
                row["Borough"], row["Grade"], row["Category"], row["Year"],
                row["# Total Days"], row["# Days Absent"], row["# Days Present"],
                row["% Attendance"], row["# Contributing 10+ Total Days and 1+ Pres Day"],
                row["# Chronically Absent"], row["% Chronically Absent"]
            )
            cursor.execute(insert_into, values)

    elif table_name == "graduation":
        insert_into = """
        INSERT INTO "graduation" ("Borough", "Category", "Cohort Year", "Cohort", "# Total Cohort", "# Grads", "% Grads", "# Total Regents", "% Total Regents of Cohort", "% Total Regents of Grads", "# Still Enrolled", "% Still Enrolled", "# Dropout", "% Dropout", "# SACC (IEP Diploma)", "% SACC (IEP Diploma) of Cohort", "# TASC (GED)", "% TASC (GED) of Cohort", "Cohort Duration", "Graduation Year")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for _, row in df.iterrows():
            values = (
                row["Borough"], row["Category"], row["Cohort Year"], row["Cohort"],
                row["# Total Cohort"], row["# Grads"], row["% Grads"],
                row["# Total Regents"], row["% Total Regents of Cohort"], row["% Total Regents of Grads"],
                row["# Still Enrolled"], row["% Still Enrolled"], row["# Dropout"], row["% Dropout"],
                row["# SACC (IEP Diploma)"], row["% SACC (IEP Diploma) of Cohort"],
                row["# TASC (GED)"], row["% TASC (GED) of Cohort"],
                row["Cohort Duration"], row["Graduation Year"]
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
    load_postgres(clean_attendance, "attendance")
    load_postgres(clean_graduation, "graduation")
    load_postgres(clean_regents, "regents")


if __name__ == "__main__":
    main()