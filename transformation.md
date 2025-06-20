# Data Transformation Process Notes - Sprint 1
___

## *Stage 1:* **Identifying & Dropping Superfluous Features and Observations**
(Assuming the NYC Open Data information has not been filtered through querying before downloading locally)

- The 3 datasets for NYC Public Schools (K-12) High School Graduation Rates, Demographics, and Chronic Absenteeism/Attendance from 2015-2023 (approximately) will be loaded into the leila_eda.ipynb notebook using "pd.read_csv("file_path")

- The commands below will be run for each dataset to check the resulting dataframes for any total null/NaN values, column data types (dtypes), and any duplicate values in rows.

    - df.isnull().sum()
    - df.info()
    - duplicate_counts = abs_df.value_counts()
      duplicate_count = duplicate_counts[duplicate_counts > 1].sum()

- Currently unnecessary columns/features across all datasets such as "School Name" or "District" will be dropped.

- In the [Absenteeism/Attendance Dataset](https://data.cityofnewyork.us/Education/2016-17-2020-23-Citywide-End-of-Year-Attendance-an/sgsi-66kk/about_data) certain information is hidden to comply with the Family Educational Rights and Privacy Act (FERPA) regulations on public reporting of education outcomes. The hidden data in certain rows is represented by the letter "s" for "SUPPRESSED" and indicates:

    - rows with five or fewer students 
    - rows with 900 or fewer total days (when using total days of attendance as a proxy)  
    - rows that could reveal, through addition or subtraction, the underlying numbers that have been redacted
    - chronic absenteeism values in rows, that are hidden regardless of total days, if the number of students who contribute  at least 20 days is five or fewer

- Thusly, the "s" character will be removed from all rows in that dataset.
    - The "s" may either be replaced with a 0 or "NaN" using astype() to convert it from an object to a category if the amount of that character is significantly impactful
___

## *Stage 2:* **Creating & Tailoring Data to Capstone Specifications**

- Create new dataframe/csv to store location of "s" row values for future reference

- Convert object dtypes for values that represent years or percentages into integers (int64) across all applicable dataframes

- Create 4 datafraemes and 4 corresponding csv files to separate grades by age to better focus on educational outcomes and demographics: 
    - early childhood education data (3K to Kindergarten)
    - younger primary school education results data (1st - 4th grade)
    - middle school (5th - 8th grade)
    - high school (9th - 12th grade)

- Transform **Cohort Year** (year students started high school) and **Class Year** (year students graduate from high school) from the [Graduation Rate dataset](https://data.cityofnewyork.us/Education/Graduation-results-for-Cohorts-2012-to-2019-Classe/mjm3-8dw8/about_data). Options for transformation are:

    - Combine the Cohort and Graduation Year features into new one called "Cohort Duration" or "Total HS Enrollment (Years)", taking the "Cohort" (whether the students graduated in 4, 5, or 6 years) trait into account

    - Transform the **Cohort Year** and **Cohort** features (and save info in separate csv for reference) then create new column called "Total HS Enrollment (Years)"

    - Drop or combine the assorted Cohort features, use that info to create columns showing the percentages of students that graduated in 4, 5, or 6 years
