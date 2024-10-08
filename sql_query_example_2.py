'''
I utilized DuckDB in this file, a library which allows you to seemlessly integrate Sql code directly into a Python file.
This allowed me to join two very large data sets based on a complex set of conditions. This file was able to
search through the data sets and combine them within 18 Seconds.
'''
import pandas as pd
import duckdb
import time

start_time = time.time()

df1=pd.read_excel(r"file path",4).drop(['Twp','Corp','District','District.1','Neigh','Wksht Val','Wksht Val.1','Cert Val','Cert Val.1','Type','Grade','Cond'],axis=1)
df2=pd.read_excel(r"file path",6)
df1=df1[df1['Parcel ID'].astype(str) != 'nan'].reset_index().reset_index()
df2=df2.reset_index().rename(columns={'index':'index_0'}).drop(df2.columns[0:6],axis=1)

sql='''
SELECT *
FROM (SELECT * FROM df1 WHERE df1['level_0'] IN (
    SELECT df1['level_0']
    FROM df1
    FULL OUTER JOIN df2
    ON df2['PACEL ID'] = df1['Parcel ID']
    WHERE (
        (df1['Parcel ID'] = df2['PACEL ID']) AND
        (
            (df2['YEAR BP']-df1['SXfer Date']=1 AND MONTH(df1['PXfer Date'])>=7) OR
            (df1['SXfer Date']>=df2['YEAR BP'])
        ) AND (
            (UPPER(df2['MEMO']) like '%DEMO%') AND
            (df2['MEMO'] like '%100%') AND NOT
            (UPPER(df2['MEMO']) like '%GARAGE%') AND NOT
            (UPPER(df2['MEMO']) like '%SHED%') AND NOT
            (UPPER(df2['MEMO']) like '%BATH%') AND NOT
            (UPPER(df2['MEMO']) like '%SPA%') AND NOT
            (UPPER(df2['MEMO']) like '%DECK%') AND NOT
            (UPPER(df2['MEMO']) like '%ROOF%') AND NOT
            (UPPER(df2['MEMO']) like '%PORCH%') AND NOT
            (UPPER(df2['MEMO']) like '%OUTBUILDING%') AND NOT
            (UPPER(df2['MEMO']) like '%INTERIOR%') AND NOT
            (UPPER(df2['MEMO']) like '%KITCHEN%') AND NOT
            (UPPER(df2['MEMO']) like '%INT %')
            )
        )
    AND NOT EXISTS (
        SELECT *
        FROM df2
        WHERE (
            df1['Parcel ID'] = df2['PACEL ID'] AND
            df1['SXfer Date'] > df2['YEAR BP'] AND
            (
                UPPER(df2['MEMO']) NOT like '%DEMO%' AND
                UPPER(df2['MEMO']) NOT like '%PORCH%' AND
                UPPER(df2['MEMO']) NOT like '%ROOF%' AND
                UPPER(df2['MEMO']) NOT like '%DECK%' AND
                UPPER(df2['MEMO']) NOT like '%POOL%' AND
                UPPER(df2['MEMO']) NOT like '%SPA%' AND
                UPPER(df2['MEMO']) NOT like '%ROOM%' AND
                UPPER(df2['MEMO']) NOT like '%REPAIR%' AND
                UPPER(df2['MEMO']) NOT like '%RENOVAT%' AND
                (
                    UPPER(df2['MEMO']) like '%SFR%' OR
                    UPPER(df2['MEMO']) like '%FAMILY%' OR
                    UPPER(df2['MEMO']) like '%DWELL%' OR
                    UPPER(df2['MEMO']) like '%BUILD%' OR
                    UPPER(df2['MEMO']) like '%BLD%' OR
                    UPPER(df2['MEMO']) like '%HOUSE%' OR
                    UPPER(df2['MEMO']) like '%NEW%'
                    )
                )
            )
        )
    )) AS E
LEFT JOIN df2
ON E['Parcel ID'] = df2['PACEL ID']
ORDER BY E['level_0'],df2['YEAR BP'],df2['BP CODE'],df2['MEMO']
'''

sqlTable = duckdb.sql(sql).df()

print("My program took", time.time() - start_time, "to run")
