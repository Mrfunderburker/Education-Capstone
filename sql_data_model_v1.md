# Team Education: 
# *Sprint 1* - DRAFT Explanation of SQL Entity Relationship Model 
___

## Entities and Relationships

- ACADEMIC_YEAR
- BOROUGH
- GRADE_LEVEL
- DEMOGRAPHIC_CATEGORY  
- DEMOGRAPHIC_VALUE
- STUDENT_DEMOGRAPHICS
- ELEMENTARY_MIDDLE_PERFORMANCE
- HIGH_SCHOOL_PERFORMANCE

**ACADEMIC_YEAR (many-to-many relationship with other entities):** Very important primary key that all entities and relationships have in common. The main issue with this choice is that primary keys cannot contain duplicate values and our dataset is quite large and diverse.

A possible fix for this could be combining the ACADEMIC_YEAR, BOROUGH, and GRADE_LEVEL entities into a *Composite Key* - but that will require more research.

**BOROUGH (many-to-many relationship with other entities):** All data is partitioned by NYC’s 5 boroughs. Could be part of Composite Key since all/majority of info can be linked to a borough

**GRADE LEVEL(many-to-many relationship with other entities):** will separate the data into appropriate age groups with available official testing outcomes 

  - *Middle School* (either 3rd/4th/5th to 8th grade) - directly connected to the ELEMENTARY_MIDDLE_PERFORMANCE entity

  - *High School* (9th - 12th grade) - directly connected to the HIGH_SCHOOL_PERFORMANCE entity and tracks Graduation, Regents Exam & SAT Exam results
 
**DEMOGRAPHIC_CATEGORY and DEMOGRAPHIC_VALUE (many-to-many relationships with other entities):**  Demographics will be labeled by “category_name VARCHAR(50)s” like =   "Race/Ethnicity", "Disability Status", “Economic Status”(poverty), etc. 
These two are more broad, track demographics across the board (are related to boroughs, used to track population change & enrollment maybe) and can apply to all other entities

**ELEMENTARY_MIDDLE_PERFORMANCE and HIGH_SCHOOL_PERFORMANCE (many-to-many relationships with other entities):** These entities are student performance metrics. Maybe a little redundant, but they are specifically related to GRADE_LEVEL.

  - *HS Performance* = SAT & Regents Scores followed by performance_id, academic_year_id FK,  borough_id,  grade_level_id (only references 9-12 grade), demographic_value_id,  graduation_count,  regents_test_takers INT, sat_test_takers INT, etc

  - *Elementary and Middle School Performance* = similar attributes to High School, tracks ELA and Math Standardized test results for 3rd - 8th grades

___
## Events

As of Sprint 1, events for the future database will be for one time tasks such as table creation.

Tables housing data from the above entities will be created once key attributes are solidified. Events for edits are TBD.

