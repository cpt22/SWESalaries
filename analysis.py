import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from common import *


#%%
# GENERATE SALARY BY LANGUAGE PLOT
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

dfLanguage = pd.read_sql_query(AVG_LANG_SAL_QUERY, conn)
dfLanguage = dfLanguage.rename(columns={'language': 'Language', 'avg': 'Average Salary', 'n': 'N'})
print(dfLanguage)
dfLanguage_sorted_desc = dfLanguage.sort_values("Average Salary", ascending=False)

plt.figure(figsize=(15, 8))
plt.bar(dfLanguage_sorted_desc['Language'], dfLanguage_sorted_desc['Average Salary'])
plt.xlabel("Languages", size=15)
plt.ylabel("Average Salary in US Dollars", size=15)
plt.title("Average Salary vs. Languages", size=18)
plt.savefig("plots/language_vs_salary.png")


#%%
# GENERATE SALARY BY FRAMEWORK PLOT
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

dfFramework = pd.read_sql_query(AVG_FRAMEWORK_SAL_QUERY, conn)
dfFramework = dfFramework.rename(columns={'framework': 'Framework', 'avg': 'Average Salary', 'n': 'N'})
print(dfFramework)
dfFramework_sorted_desc = dfFramework.sort_values("Average Salary", ascending=False)

plt.figure(figsize=(15, 8))
plt.bar(dfFramework_sorted_desc['Framework'], dfFramework_sorted_desc['Average Salary'])
plt.xlabel("Frameworks", size=15)
plt.ylabel("Average Salary in US Dollars", size=15)
plt.title("Average Salary vs. Frameworks", size=18)
plt.savefig("plots/framework_vs_salary.png")
plt.show()


#%%
# GENERATE AVG SALARY BY LOCATION
SAL_BY_LOCATION = '''
SELECT p.location, ROUND(AVG(p.salary)) as avg, COUNT(p.salary) as n
FROM positions p
         INNER JOIN positions_techs pt ON p.id=pt.position_id
         INNER JOIN techs t ON pt.tech_id=t.id
WHERE p.salary IS NOT NULL
GROUP BY p.location
HAVING COUNT(p.salary) > 5
ORDER BY AVG(p.salary) DESC
'''

dfLocSal = pd.read_sql_query(SAL_BY_LOCATION, conn)
dfLocSal = dfLocSal.rename(columns={'location': 'Location', 'avg': 'Average Salary', 'n': 'N'})
print(dfLocSal)

plt.figure(figsize=(50, 30))
plt.bar(dfLocSal['Location'], dfLocSal['Average Salary'])
plt.xticks(rotation=45, size=23, ha='right')
plt.yticks(size=25)
plt.xlabel("Location", size=30)
plt.ylabel("Average Salary in US Dollars", size=30)
plt.title("Average Salary vs. Location (N > 5)", size=48)
plt.savefig("plots/location_vs_salary.png")
plt.show()


#%%
# GENERATE NUM JOBS BY LANGUAGE PLOT
NUM_LANG_QUERY = '''
SELECT pt.tech_id as language, COUNT(p.id) as n
FROM positions p
         INNER JOIN positions_techs pt ON p.id=pt.position_id
         INNER JOIN techs t ON pt.tech_id=t.id
WHERE t.type='language'
GROUP BY pt.tech_id
ORDER BY COUNT(p.id) DESC
'''

dfNumLang = pd.read_sql_query(NUM_LANG_QUERY, conn)
dfNumLang = dfNumLang.rename(columns={'language': 'Language', 'n': 'N'})
dfNumLang['Percentage'] = dfNumLang.N / dfNumLang.N.sum()
print(dfNumLang)

plt.figure(figsize=(15, 15))
plt.pie(np.array(dfNumLang['Percentage']), labels=dfNumLang['Language'])
plt.title("Percent Jobs by Language", size=18)
plt.savefig("plots/num_jobs_by_lang.png")
plt.show()



#%%
# GENERATE NUM JOBS BY FRAMEWORK PLOT
NUM_FRAMEWORK_QUERY = '''
SELECT pt.tech_id as framework, COUNT(p.id) as n
FROM positions p
         INNER JOIN positions_techs pt ON p.id=pt.position_id
         INNER JOIN techs t ON pt.tech_id=t.id
WHERE t.type='framework'
GROUP BY pt.tech_id
ORDER BY COUNT(p.id) DESC
'''

dfNumFramework = pd.read_sql_query(NUM_FRAMEWORK_QUERY, conn)
dfNumFramework = dfNumFramework.rename(columns={'framework': 'Framework', 'n': 'N'})
dfNumFramework['Percentage'] = dfNumFramework.N / dfNumFramework.N.sum()
print(dfNumFramework)

plt.figure(figsize=(15, 15))
plt.pie(np.array(dfNumFramework['Percentage']), labels=dfNumFramework['Framework'])
plt.title("Percent Jobs by Framework", size=18)
plt.savefig("plots/num_jobs_by_framework.png")
plt.show()



#%%
# GENERATE NUM JOBS BY LOCATION PLOT
NUM_BY_LOCATION = '''
SELECT p.location, COUNT(p.id) as n
FROM positions p
         INNER JOIN positions_techs pt ON p.id=pt.position_id
         INNER JOIN techs t ON pt.tech_id=t.id
GROUP BY p.location
HAVING COUNT(p.id) > 15
ORDER BY COUNT(p.id) DESC
'''

dfNumLoc = pd.read_sql_query(NUM_BY_LOCATION, conn)
dfNumLoc = dfNumLoc.rename(columns={'location': 'Location', 'n': 'N'})
dfNumLoc['Percentage'] = dfNumLoc.N / dfNumLoc.N.sum()
print(dfNumLoc)

plt.figure(figsize=(15, 15))
plt.pie(np.array(dfNumLoc['Percentage']), labels=dfNumLoc['Location'])
plt.title("Percent Jobs by Location (N per loc > 15)", size=18)
plt.savefig("plots/num_jobs_by_location.png")
plt.show()




#%%
