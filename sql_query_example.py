'''
This is a file I used for a project where I had to combine informationa about people from two different data sets. These data sets were organized by peoples names,
however their names were often spelt differently between each set (Ex: "John Smith" vs "John Patrick Smith Jr."). I found the program correctly organized data most
efficiently when it would allow for names which were similar but not exact, like the previous example. This process would be impossible using Pandas to merge the 
two data sets. However, using SQL's JOIN functionality, I was able to easy combine these data sets using such conditions.
'''
import pandas as pd
import duckdb
import time

start_time = time.time()

def listFormat(x):
    if '&' in str(x):
        return (x[:x.index('&')],tuple([x[0]]+list(x[x.index('&')+1:])))
    else:
        return tuple([x])


dataframe1=pd.read_excel(r"C:\Users\erens\Desktop\Eren-Snover-Portfolio\dataset1",0)
dataframe2=pd.read_excel(r"C:\Users\erens\Desktop\Eren-Snover-Portfolio\dataset2",1)
dataframe1=dataframe1.reset_index()
dataframe2=dataframe2.reset_index()

dataframe1 = dataframe1[['index','id','Taxpayer','AppName','SpouseName','Address']]
dataframe1[['AppName','SpouseName']] = dataframe1[['AppName','SpouseName']].astype(str).apply(lambda x: [[i for i in j.upper().split() if '/' not in i] for j in x]).apply(lambda x: [listFormat(tuple(i)) for i in x])
dataframe2[['Grantor','Grantee']] = dataframe2[['Grantor','Grantee']].astype(str).apply(lambda x: [tuple(i.upper().split()) for i in x])

sql='''
SELECT *
FROM dataframe1
LEFT JOIN dataframe2
ON (((((cast(dataframe2.Grantor AS VARCHAR[]) @> cast(dataframe1.AppName[1] AS VARCHAR[])) OR (cast(dataframe2.Grantor AS VARCHAR[]) <@ cast(dataframe1.AppName[1] AS VARCHAR[]))) AND len(dataframe1.AppName[1])>1) OR
    (((cast(dataframe2.Grantor AS VARCHAR[]) @> cast(dataframe1.AppName[2] AS VARCHAR[])) OR (cast(dataframe2.Grantor AS VARCHAR[]) <@ cast(dataframe1.AppName[2] AS VARCHAR[]))) AND len(dataframe1.AppName[2])>1)) AND list_contains(dataframe2.Grantor,'EST')) OR
   (((((cast(dataframe2.Grantee AS VARCHAR[]) @> cast(dataframe1.AppName[1] AS VARCHAR[])) OR (cast(dataframe2.Grantee AS VARCHAR[]) <@ cast(dataframe1.AppName[1] AS VARCHAR[]))) AND len(dataframe1.AppName[1])>1) OR
     (((cast(dataframe2.Grantee AS VARCHAR[]) @> cast(dataframe1.AppName[2] AS VARCHAR[])) OR (cast(dataframe2.Grantee AS VARCHAR[]) <@ cast(dataframe1.AppName[2] AS VARCHAR[]))) AND len(dataframe1.AppName[2])>1)) AND list_contains(dataframe2.Grantee,'EST'))
'''

sql2='''
SELECT *
FROM tableJoin
LEFT JOIN dataframe2
ON ((((cast(dataframe2.Grantor AS VARCHAR[]) @> cast(tableJoin.SpouseName[1] AS VARCHAR[])) OR (cast(dataframe2.Grantor AS VARCHAR[]) <@ cast(tableJoin.SpouseName[1] AS VARCHAR[]))) AND len(tableJoin.SpouseName[1])>1) AND list_contains(dataframe2.Grantor,'EST')) OR
   ((((cast(dataframe2.Grantee AS VARCHAR[]) @> cast(tableJoin.SpouseName[1] AS VARCHAR[])) OR (cast(dataframe2.Grantee AS VARCHAR[]) <@ cast(tableJoin.SpouseName[1] AS VARCHAR[]))) AND len(tableJoin.SpouseName[1])>1) AND list_contains(dataframe2.Grantee,'EST'))
'''

tableJoin = duckdb.sql(sql).df()
tableJoin = duckdb.sql(sql2).df().drop_duplicates(subset='index')

tableJoin[['AppName','SpouseName']] = tableJoin[['AppName','SpouseName']].apply(lambda y: [tuple(tuple(x) for x in z) for z in y])


print("My program took", time.time() - start_time, "to run")
