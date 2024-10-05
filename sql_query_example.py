'''
I utilized DuckDB in this file, a library which allows you to seemlessly integrate Sql code directly into a Python file.
I originally wrote this file without using DuckDB and joined my datasets in python. This process however took several hours to complete,
and knowing that this file would likely need to be run more than once, I decided to instead run the join in Sql.
This allows me to conditionally the large data sets in seconds rather than hours.
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


df1=pd.read_excel(r"file path",0)
df2=pd.read_excel(r"file path",1)
df1=df1.reset_index()
df2=df2.reset_index()

df1 = df1[['index','Uid','Taxpayer','AppName','SpouseName','Address']]
df1[['AppName','SpouseName']] = df1[['AppName','SpouseName']].astype(str).apply(lambda x: [[i for i in j.upper().split() if '/' not in i] for j in x]).apply(lambda x: [listFormat(tuple(i)) for i in x])
df2[['Grantor','Grantee']] = df2[['Grantor','Grantee']].astype(str).apply(lambda x: [tuple(i.upper().split()) for i in x])

sql='''
SELECT *
FROM df1
LEFT JOIN df2
ON (((((cast(df2.Grantor AS VARCHAR[]) @> cast(df1.AppName[1] AS VARCHAR[])) OR (cast(df2.Grantor AS VARCHAR[]) <@ cast(df1.AppName[1] AS VARCHAR[]))) AND len(df1.AppName[1])>1) OR
    (((cast(df2.Grantor AS VARCHAR[]) @> cast(df1.AppName[2] AS VARCHAR[])) OR (cast(df2.Grantor AS VARCHAR[]) <@ cast(df1.AppName[2] AS VARCHAR[]))) AND len(df1.AppName[2])>1)) AND list_contains(df2.Grantor,'EST')) OR
   (((((cast(df2.Grantee AS VARCHAR[]) @> cast(df1.AppName[1] AS VARCHAR[])) OR (cast(df2.Grantee AS VARCHAR[]) <@ cast(df1.AppName[1] AS VARCHAR[]))) AND len(df1.AppName[1])>1) OR
     (((cast(df2.Grantee AS VARCHAR[]) @> cast(df1.AppName[2] AS VARCHAR[])) OR (cast(df2.Grantee AS VARCHAR[]) <@ cast(df1.AppName[2] AS VARCHAR[]))) AND len(df1.AppName[2])>1)) AND list_contains(df2.Grantee,'EST'))
'''

sql2='''
SELECT *
FROM tableJoin
LEFT JOIN df2
ON ((((cast(df2.Grantor AS VARCHAR[]) @> cast(tableJoin.SpouseName[1] AS VARCHAR[])) OR (cast(df2.Grantor AS VARCHAR[]) <@ cast(tableJoin.SpouseName[1] AS VARCHAR[]))) AND len(tableJoin.SpouseName[1])>1) AND list_contains(df2.Grantor,'EST')) OR
   ((((cast(df2.Grantee AS VARCHAR[]) @> cast(tableJoin.SpouseName[1] AS VARCHAR[])) OR (cast(df2.Grantee AS VARCHAR[]) <@ cast(tableJoin.SpouseName[1] AS VARCHAR[]))) AND len(tableJoin.SpouseName[1])>1) AND list_contains(df2.Grantee,'EST'))
'''

tableJoin = duckdb.sql(sql).df()
tableJoin = duckdb.sql(sql2).df().drop_duplicates(subset='index')

tableJoin[['AppName','SpouseName']] = tableJoin[['AppName','SpouseName']].apply(lambda y: [tuple(tuple(x) for x in z) for z in y])


print("My program took", time.time() - start_time, "to run")
