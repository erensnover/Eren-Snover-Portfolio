'''
This file was used to calculate several statistics all at once. These statistics required unique and complex formulas for achieving the desired results.
This specific file takes in a single excel spreadsheet and returns another spreadsheet with 8 different tables of all the desired information, formatted
in a way which is immediately readable and presentable in Excel or printed out on paper.
'''
import pandas as pd
import locale
import statistics as st
import xlsxwriter
from openpyxl.styles import Alignment


workbook = xlsxwriter.Workbook(r"file path")

locale.setlocale(locale.LC_ALL, '')

originalDF=pd.read_excel(r'file path',0,header=4)

def CERT(x):
    d = {}
    d['Sales in Period'] = "{:.0f}".format(x['ASSESSMENT'].count())
    d['Lowest Sale Price'] = locale.currency(x['Consider'].min(),grouping=True,symbol=True).split('.', 1)[0]
    d['Highest Sale Price'] = locale.currency(x['Consider'].max(),grouping=True,symbol=True).split('.', 1)[0]
    d['Mean Sale Price'] = locale.currency(x['Consider'].mean(),grouping=True,symbol=True).split('.', 1)[0]
    d['Median Sale Price'] = locale.currency(x['Consider'].median(),grouping=True,symbol=True).split('.', 1)[0]
    d['Total Assessed 70% Value (Sold Parcels)'] = locale.currency(sum(x['ASSESSMENT']),grouping=True,symbol=True).split('.', 1)[0]
    d['Total Sale Price'] = locale.currency(sum(x['Consider']),grouping=True,symbol=True).split('.', 1)[0]
    d['Weighted Mean (70% Value/Total Sales)'] = "{:.3f}".format(sum(x['ASSESSMENT'])/sum(x['Consider']))
    d['Median Ratio'] = "{:.3f}".format(st.median(x['cert RATIO'].astype(float)))
    d['Mean'] = "{:.3f}".format(x['cert RATIO'].mean())
    d['COD'] = "{:.3f}".format(st.mean(abs(x['cert RATIO']-st.median(x['cert RATIO'])))/st.median(x['cert RATIO'])*100)
    d['PRD'] = "{:.3f}".format(((x['ASSESSMENT'] / x['Consider']).mean())/(sum(x['ASSESSMENT'])/sum(x['Consider'])))
    return pd.Series(d)

def WKSHT(x):
    d = {}
    d['Sales in Period'] = "{:.0f}".format(x['Consider'].count())
    d['Lowest Sale Price'] = locale.currency(x['Consider'].min(),grouping=True,symbol=True).split('.', 1)[0]
    d['Highest Sale Price'] = locale.currency(x['Consider'].max(),grouping=True,symbol=True).split('.', 1)[0]
    d['Mean Sale Price'] = locale.currency(x['Consider'].mean(),grouping=True,symbol=True).split('.', 1)[0]
    d['Median Sale Price'] = locale.currency(x['Consider'].median(),grouping=True,symbol=True).split('.', 1)[0]
    d['Total Assessed 70% Value (Sold Parcels)'] = locale.currency(sum(x['WKSHT']),grouping=True,symbol=True).split('.', 1)[0]
    d['Total Sale Price'] = locale.currency(sum(x['Consider']),grouping=True,symbol=True).split('.', 1)[0]
    d['Weighted Mean (70% Value/Total Sales)'] = "{:.3f}".format(sum(x['WKSHT'])/sum(x['Consider']))
    d['Median Ratio'] = "{:.3f}".format(st.median(x['wksht RATIO'].astype(float)))
    d['Mean'] = "{:.3f}".format(x['wksht RATIO'].mean())
    d['COD'] = "{:.3f}".format(st.mean(abs(x['wksht RATIO']-st.median(x['wksht RATIO'])))/st.median(x['wksht RATIO'])*100)
    d['PRD'] = "{:.3f}".format(((x['WKSHT'] / x['Consider']).mean())/(sum(x['WKSHT'])/sum(x['Consider'])))
    return pd.Series(d)

def BEST(x):
    d = {}
    d['Sales in Period'] = "{:.0f}".format(x['good assessment'].count())
    d['Lowest Sale Price'] = locale.currency(x['Consider'].min(),grouping=True,symbol=True).split('.', 1)[0]
    d['Highest Sale Price'] = locale.currency(x['Consider'].max(),grouping=True,symbol=True).split('.', 1)[0]
    d['Mean Sale Price'] = locale.currency(x['Consider'].mean(),grouping=True,symbol=True).split('.', 1)[0]
    d['Median Sale Price'] = locale.currency(x['Consider'].median(),grouping=True,symbol=True).split('.', 1)[0]
    d['Total Assessed 70% Value (Sold Parcels)'] = locale.currency(sum(x['good assessment']),grouping=True,symbol=True).split('.', 1)[0]
    d['Total Sale Price'] = locale.currency(sum(x['Consider']),grouping=True,symbol=True).split('.', 1)[0]
    d['Weighted Mean (70% Value/Total Sales)'] = "{:.3f}".format(sum(x['good assessment'])/sum(x['Consider']))
    d['Median Ratio'] = "{:.3f}".format(st.median(x['good ratio'].astype(float)))
    d['Mean'] = "{:.3f}".format(x['good ratio'].mean())
    d['COD'] = "{:.3f}".format(st.mean(abs(x['good ratio']-st.median(x['good ratio'])))/st.median(x['good ratio'])*100)
    d['PRD'] = "{:.3f}".format(((x['good assessment'] / x['Consider']).mean())/(sum(x['good assessment'])/sum(x['Consider'])))
    return pd.Series(d)

cell_format = workbook.add_format()
cell_format.set_align('center')
cell_format.set_align('vcenter')

pivotTables = {}

dfCondos=originalDF[(originalDF['BA CODE'].astype(str)=='nan') &
      (originalDF['Class'] < 128) & (originalDF['Class'] > 120) &
      (originalDF['Consider'] > 0)].dropna(subset=['Parcel ID'])

dfRes = originalDF[(originalDF['BA CODE'].astype(str)=='nan') &
      (originalDF['Class'] < 121) &
      (originalDF['Consider'] > 0)].dropna(subset=['Parcel ID'])

dfs = [dfCondos,dfRes]

for i in range(2021,2024):
    for j in [BEST]:
        for k in dfs:
            tableNameDistrict = str(i) + ' ' + j.__name__ + " District" + (' CONDOS' if k.equals(dfCondos) else ' RES')
            tableNamePrice = str(i) + ' ' + j.__name__ + " Price Range" + (' CONDOS' if k.equals(dfCondos) else ' RES')
            print(tableNameDistrict)
            print(tableNamePrice)
            pivotTables[tableNameDistrict] = pd.concat([k[
                (k['PXfer Date'] >= pd.Timestamp('10-01-'+str(i))) &
                (k['PXfer Date'] < pd.Timestamp('9-30-'+str(i+1))) &
                (k['Analysis']=='Y') & (k['RatioC']=='Y')
            ].groupby('District')[k.columns.values.tolist()].apply(j, include_groups=True).sort_index(),
            k[
                (k['PXfer Date'] >= pd.Timestamp('10-01-'+str(i))) &
                (k['PXfer Date'] < pd.Timestamp('9-30-'+str(i+1))) &
                (k['Analysis']=='Y') & (k['RatioC']=='Y')
                ].groupby('Twp')[k.columns.values.tolist()].apply(j,include_groups=True).rename(index={1:'Total'})])
            if k.equals(dfCondos):
                pivotTables[tableNamePrice] = pd.concat([k[
                    (k['PXfer Date'] >= pd.Timestamp('10-01-'+str(i))) &
                    (k['PXfer Date'] < pd.Timestamp('9-30-'+str(i+1))) &
                    (k['Analysis']=='Y') & (k['RatioC']=='Y')
                ].groupby('condo Price Range')[k.columns.values.tolist()].apply(j, include_groups=True).reindex(['$0 - $500,000','$500,000 - $1,000,000','$1,000,000 - $2,000,000','$2,000,000 - $3,000,000','$3,000,000 + ']),
                k[
                    (k['PXfer Date'] >= pd.Timestamp('10-01-'+str(i))) &
                    (k['PXfer Date'] < pd.Timestamp('9-30-'+str(i+1))) &
                    (k['Analysis']=='Y') & (k['RatioC']=='Y')
                    ].groupby('Twp')[k.columns.values.tolist()].apply(j,include_groups=True).rename(index={1:'Total'})])
            else:
                pivotTables[tableNamePrice] = pd.concat([k[
                    (k['PXfer Date'] >= pd.Timestamp('10-01-'+str(i))) &
                    (k['PXfer Date'] < pd.Timestamp('9-30-'+str(i+1))) &
                    (k['Analysis']=='Y') & (k['RatioC']=='Y')
                ].groupby('Price Range')[k.columns.values.tolist()].apply(j, include_groups=True).reindex(['$0 - $1,500,000','$1,500,000 - $3,000,000','$3,000,000 - $6,000,000','$6,000,000 - $10,000,000','$10,000,000 + ']),
                k[
                    (k['PXfer Date'] >= pd.Timestamp('10-01-'+str(i))) &
                    (k['PXfer Date'] < pd.Timestamp('9-30-'+str(i+1))) &
                    (k['Analysis']=='Y') & (k['RatioC']=='Y')
                    ].groupby('Twp')[k.columns.values.tolist()].apply(j,include_groups=True).rename(index={1:'Total'})])




with pd.ExcelWriter(r"file path") as writer:
    for i in pivotTables:
        sheetName = i
        pivotTables[i].to_excel(writer,sheet_name=sheetName,index=True)
        worksheet = writer.sheets[sheetName]
        if 'District' in i:
            options = dict(columns=[{'header': c} for c in pivotTables[i].columns.insert(0,'District')],style = 'Table Style Light 15')
        else:
            options = dict(columns=[{'header': c} for c in pivotTables[i].columns.insert(0,'Price Range')],style = 'Table Style Light 15')
        worksheet.add_table(0,0,pivotTables[i].shape[0],pivotTables[i].shape[1],options)
        for j in range(1,pivotTables[i].shape[0]+1):
            worksheet.set_row(j, 20)
        for column in range(pivotTables[i].shape[1]):
            for row in range(pivotTables[i].shape[0]):

                cell=worksheet.cell(row, column)
                cell.alignment = Alignment(horizontal='center', vertical='center')
        worksheet.autofit()
