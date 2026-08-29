import csv
from itertools import count

import pandas as pd
import numpy as np



def import_file(path) :
        path = path

        try:
            # with open( path, newline='') as csvfile:
            df = pd.read_csv(path)
            print(df.head(15))
            return df
        except FileNotFoundError:
            print("File not found")


def data_filteration(dataf) ->pd.DataFrame :

        # Inspect the structure, column names, and basic statistics.
        print(f" shape of data is = {dataf.shape} ")

        print(f" description of data is = {dataf.describe()} ")
        print(f" information about data is =  ");dataf.info()
        print(f" number of duplicates in  data is = {dataf.duplicated(subset=['category','value_1','value_2']).sum()} ")


        print( f"total row count = {dataf.shape[0]} " )
        print(f" columns in data are = {dataf.columns} ")
        print(f" types of columns are = {dataf.dtypes}")
        filtered_data = dataf[dataf['value_1'] >50]
        print( f" the rows having having values greater than 50 in value_1 column are= {filtered_data} ")



        #  filtering
        filtered_data.drop_duplicates(inplace = True, keep = "first")
        return filtered_data

def data_summarization(dataf) ->pd.DataFrame :


        # grouping rows by region
        rows_by_region = dataf.groupby('region')
        for region, group in rows_by_region:
            print( f"{region} = {group} ")

        # count rows per group
        count_rows = rows_by_region['region'].value_counts()
        print(count_rows.iloc[:1])

        sum_rows= rows_by_region['value_1'].sum()
        avg_rows = rows_by_region.agg(avg=('value_1', 'mean'))
        print(sum_rows.iloc[:1])
        print(avg_rows.iloc[:1])


        summarized_data = pd.concat([count_rows, sum_rows, avg_rows], axis=1)
        return summarized_data



def saving_data(dataf1 ,dataf2) ->object:
        dataf1.to_csv('output_filtered.csv' ,index= True)
        dataf2.to_csv("output_summary.csv", index = True)



df = import_file(r"D:\User\warda\Downloads\data_quality_validation_dataset.csv")

df1 = data_filteration(df)
df2 = data_summarization(df1)
saving_data(df1,df2)