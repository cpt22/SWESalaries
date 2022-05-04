import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from common import *

AVG_LANG_SAL_QUERY = '''
SELECT pt.tech_id as language, ROUND(AVG(p.salary)) as avg, COUNT(p.salary) as n
FROM positions p
         INNER JOIN positions_techs pt ON p.id=pt.position_id
         INNER JOIN techs t ON pt.tech_id=t.id
WHERE p.salary IS NOT NULL
  AND t.type='language'
GROUP BY pt.tech_id
ORDER BY AVG(p.salary) DESC
'''

NUM_LANG_QUERY = '''
SELECT pt.tech_id as language, COUNT(p.id) as n
FROM positions p
         INNER JOIN positions_techs pt ON p.id=pt.position_id
         INNER JOIN techs t ON pt.tech_id=t.id
WHERE t.type='language'
GROUP BY pt.tech_id
ORDER BY COUNT(p.id) DESC
'''

AVG_FRAMEWORK_SAL_QUERY = '''
SELECT pt.tech_id as framework, ROUND(AVG(p.salary)) as avg, COUNT(p.salary) as n
FROM positions p
         INNER JOIN positions_techs pt ON p.id=pt.position_id
         INNER JOIN techs t ON pt.tech_id=t.id
WHERE p.salary IS NOT NULL
  AND t.type='framework'
GROUP BY pt.tech_id
ORDER BY AVG(p.salary) DESC
'''

NUM_FRAMEWORK_QUERY = '''
SELECT pt.tech_id as framework, COUNT(p.id) as n
FROM positions p
         INNER JOIN positions_techs pt ON p.id=pt.position_id
         INNER JOIN techs t ON pt.tech_id=t.id
WHERE t.type='framework'
GROUP BY pt.tech_id
ORDER BY COUNT(p.id) DESC
'''

SAL_BY_LOCATION = '''
SELECT p.location, ROUND(AVG(p.salary)) as avg, COUNT(p.salary) as n
FROM positions p
         INNER JOIN positions_techs pt ON p.id=pt.position_id
         INNER JOIN techs t ON pt.tech_id=t.id
WHERE p.salary IS NOT NULL
GROUP BY p.location
HAVING COUNT(p.salary) > 1
ORDER BY AVG(p.salary) DESC
'''

NUM_BY_LOCATION = '''
SELECT p.location, COUNT(p.id) as n
FROM positions p
         INNER JOIN positions_techs pt ON p.id=pt.position_id
         INNER JOIN techs t ON pt.tech_id=t.id
GROUP BY p.location
ORDER BY COUNT(p.id) DESC
'''

# GENERATE SALARY BY LANGUAGE PLOT
dfLanguage = pd.read_sql_query(AVG_LANG_SAL_QUERY, conn)
dfLanguage = dfLanguage.rename(columns={'language': 'Language', 'avg': 'Average Salary', 'n': 'N'})
print(dfLanguage)
dfLanguage_sorted_desc = dfLanguage.sort_values("Average Salary", ascending=False)

plt.figure(figsize=(15, 8))
plt.bar(dfLanguage_sorted_desc['Language'], dfLanguage_sorted_desc['Average Salary'])
plt.xlabel("Languages", size=15)
plt.ylabel("Average Salary in US Dollars", size=15)
plt.title("Average Salary vs. Languages", size=18)
plt.savefig("language_vs_salary.png")


# GENERATE SALARY BY FRAMEWORK PLOT
dfFramework = pd.read_sql_query(AVG_FRAMEWORK_SAL_QUERY, conn)
dfFramework = dfFramework.rename(columns={'framework': 'Framework', 'avg': 'Average Salary', 'n': 'N'})
print(dfFramework)
dfFramework_sorted_desc = dfFramework.sort_values("Average Salary", ascending=False)

plt.figure(figsize=(15, 8))
plt.bar(dfFramework_sorted_desc['Framework'], dfFramework_sorted_desc['Average Salary'])
plt.xlabel("Frameworks", size=15)
plt.ylabel("Average Salary in US Dollars", size=15)
plt.title("Average Salary vs. Frameworks", size=18)
plt.savefig("framework_vs_salary.png")


# GENERATE AVG SALARY BY LOCATION
dfLocSal = pd.read_sql_query(SAL_BY_LOCATION, conn)
dfLocSal = dfLocSal.rename(columns={'location': 'Location', 'avg': 'Average Salary', 'n': 'N'})
print(dfLocSal)


# GENERATE NUM JOBS BY LANGUAGE PLOT
dfNumLang = pd.read_sql_query(NUM_LANG_QUERY, conn)
dfNumLang = dfNumLang.rename(columns={'language': 'Language', 'n': 'N'})
print(dfNumLang)


# GENERATE NUM JOBS BY FRAMEWORK PLOT
dfNumFramework = pd.read_sql_query(NUM_FRAMEWORK_QUERY, conn)
dfNumFramework = dfNumFramework.rename(columns={'framework': 'Framework', 'n': 'N'})
print(dfNumFramework)


# GENERATE NUM JOBS BY LOCATION PLOT
dfNumLoc = pd.read_sql_query(NUM_BY_LOCATION, conn)
dfNumLoc = dfNumLoc.rename(columns={'location': 'Location', 'n': 'N'})
print(dfNumLoc)


#%%
