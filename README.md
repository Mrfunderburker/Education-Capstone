# Capstone: Education Anaysis
### How did the Covid-19 Pandemic affect the educational outcomes for children in the New York City Public School system? 


This EDA is broken down into analysis of 3 different datasets. 

1. Citywide End of Year Attendance & Chronic Absenteeism Data for the school years 2016-17 to 2020-23.
2. Citywide Demographic Data
3. Graduation 

I decided to break down the years in all three datasets into 3 parts: 
* Pre-Covid: the years that make up the time before Covid began
* Mid-Covid: the years that make up the time during Covid
* Post-Covid: the years that make up the time when we were considered to be out of the pandemic. In truth, Covid is not over but the `Post-Covid` years represent the time when vaccines were implemented, we were better educated about Covid and students were able to return to in-school learning.

## 1. Absenteeism Dataset Description
This dataset shows citywide attendance and chronic absenteeism for New York City Public Schools. 

"Citywide" means all 5 boroughs of NYC: Bronx, Brooklyn, Manhattan, Queens and Staten Island.

The dataset cites attendance and absenteeism rates for the academic years: 
* 2016-17
* 2017-18
* 2018-19
* 2020-21 
* 2021-22
* 2022-23

Included in this dataset: 
* students in Districts 1-32 and 75(Special Education)
* Pre-K students in K-12 schools that offer Pre-K

Excluded from this dataset: 
* students in District 79 (Alternative Schools & Programs)
* charter schools
* home schooling
* home & hospital instruction
* NYC Early Education Centers
* District Pre-K Centers

Key Notes:
* attendance is attributed to the school the student attended at the time
* if a student attended multiple schools in a school year, the student will contribute data toward multiple schools
* due to the Covid-19 pandemic, data for the 2019-20 school year only shows attendance information for September 2019 thru March 13, 2020. 
* 2020-21 school year: due to the shift to hybrid learning, attendance data for the 2020-21 school year includes in-person and remote instruction. The fields `# Total Days`, `# Days Absent` and `# Days Present` include in-person and remote attendance.

Definitions:
* chronic abseentism: having an attendanc of 90% or less. In other words, being absent 10% or more, of the total days. Students must be enrolled for more than 10 days & must be present for atleast one day. 

## 2. Demographic Dataset Description
* Citywide student demographic & enrollment data, 2015-16 to 2019-20

Notes
1. There seems to be a discrepancy between the definitions of `# Multiple Race Categories Not Represented` and `% Multiple Race Categories Not Represented`, as provided by the NYC Department of Education: 
* `# Multiple Race Categories Not Represented`: this column indicates students who did not report their race, as well as students who identified as Native American or Multi-Racial

* `% Multiple Race Categories Not Represented`: students who reported their race, as well as students who reported as Native American or Multi-Race

2. `# Students with Disabilities` and `% Students with Disabilities`: "Students with Disabilities" are defined as any child receiving an Individualized Education Program (IEP) as of the end of the school year

3. `# Poverty` and `% Poverty`: NYC DOE "Poverty" counts are based on the number of students with families who qualify for free or reduced priced lunch, or are eligible for Human Resources Adminstration (HRA) benefits. In 2017-18 school year, all students became elegible for free lunch. 

4. `Economic Need Index` (ENI): the ENI is the average of a student's Economic Need Values (ENV). The ENI estimates the percentage of students facing economic hardship. The 2014-15 school year was the first time that ENI estimates were provided. The metric is calculated by: 
    a. The ENI is 1 if: the student is eligible for public assistance from NYC Human Resources Admminstration (HRA); 
    b. the student lived in temporary housing in the past 4 years; 
    c. the student is in high school, has a home language other than English, and entered the NYC DOE for the first time within the last four years; 
    d. otherwise the student's ENV is based on the percentage of families with school-age children whose income is pelove the poverty level, as estimated by the American Comunity Survey 5-Year estimate. The student's ENV equals this percentage divided by 100. 

## 3. Graduation Dataset Description

This dataset includes graduation outcomes as calculated by the New York State Education Department.

* The dataset is described by "Cohort" and "Class". "Cohort" refers to the year that the student began 9th grade. "Class of" refers to the year that the student graduated. For example, the Class of 2005 would be the Cohort of 2001: these students entered the 9th grade in 2001 and graduated in 2005. 

Pre-Covid: graduation rates were steadily increasing
Mid-Covid: there was a slight decrease in graduation rates, which is to be expected. There was an interruption in learning and this dataset does not reflect the young lives that were lost to Covid. 
Post-Covid: graduation rates seems to have rebounded and were increasing

## Conclusion
It is important to note that these datasets do not tell the full story of how the pandemic affected students' academics and their success. To truly analyze that, we will have to look at test scores.


