# RedCapQueries
All of the main queries that the Yassa lab uses outside of the default exporting options in RedCap.

These queries use the RedCap API and format the data in ways that RedCap does not officially support.

## Currently Supported Queries
To view individual query instructions, go to the individual folder of each query.

### Merge 
Query and merge data across projects. 

Example:

| master_id | date       | project_id | form1_field | form1_field | form2_field | form2_field |
|-----------|------------|------------|-------------|-------------|-------------|-------------|
| 1         | 05/10/2015 | adrc       | 1           | 2           | 1           | 0           |
| 1         | 06/10/2015 | adrc       | 5           | 2           | 1           | 0           |
| 2         | 01/01/2014 | nia_ro1    | 2           | 3           | 0           | 0           |
| 3         | 02/02/2015 | nia_ro1    | 10          | 2           | 1           | 1           |
