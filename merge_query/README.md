# Merge
This query merges RedCap data across projects. Each row in the output will be unique combination of **master_id**, **date**, and **project_id**. 

# Requirements
In order to use this query you need the following:

#### 1. Working knowledge of command-line tools
#### 2. API Tokens
You can only query across the projects you have access to, and you will only be able to get data that you have access to. In order to use this query you need an **API Token** for each project that you want to query. Ask a research specialist how you can get your API tokens. **_DO NOT SHARE THESE WITH ANYONE_**. These tokens are unique to and should only be used by **YOU**.
#### 3. API URL
You also need the API URL for UCI's database. Ask a research specialist how you can obtain the API URL. **_DO NOT SHARE THIS WITH ANYONE_**.
#### 4. Python 3.x
You will need a working version of Python3 to use this.

# Setup / Use
Put your API Tokens and API URL in _config.py_.  
You can also edit which projects you want to query in _config.py_.
Run the query by using the following command:
```
python3 merge.py
```
This will, by default, output the results to _out.csv_.
You can specify which file you want to save by adding an additional argument:
```
python3 merge.py my_results.csv 
```
If run correctly, you should see output in your terminal like this:
!["Merge Query"](https://raw.githubusercontent.com/Yassalab/RedCapQueries/master/images/merge_example.png)

Example csv file:

| master_id | date       | project_id | form1_field | form1_field | form2_field | form2_field |
|-----------|------------|------------|-------------|-------------|-------------|-------------|
| 1         | 05/10/2015 | adrc       | 1           | 2           | 1           | 0           |
| 1         | 06/10/2015 | adrc       | 5           | 2           | 1           | 0           |
| 2         | 01/01/2014 | nia_ro1    | 2           | 3           | 0           | 0           |
| 3         | 02/02/2015 | nia_ro1    | 10          | 2           | 1           | 1           |
