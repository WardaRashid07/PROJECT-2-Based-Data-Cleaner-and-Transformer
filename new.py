

path = r'D:\User\warda\Downloads\data_quality_dataset_1000_plus_rows.csv'

import pandas as pd
import numpy as np


import logging
from datetime import datetime
import csv


logging.basicConfig(level= "INFO", format = '%(asctime)s | %(levelname)s | %(message)s')
logger =logging.getLogger()


categorical_columns = ['type','subtype','label']
numerical_columns = ['metric_1','metric_2']
string_columns = ['type','subtype','label','record_id']

Column_type_map = {
    "metric_1" : "flaot",
    "metric_2" : "float"
}

NULL_MAP ={
    "record_id"  :  "drop" ,
    "event_date" : "-/-/-" ,
    "metric_1"   : "mean",
    "metric_2"   : "mean",
    "label"      : "unknown",
    "type"       : "unkown",
    "subtype"    : "unknown"
  }


logging.basicConfig(level='Info', format =" '%(asctime)s'  | '%(level_name)s' | '%(message)s' " , datefmt='%H::%M::%S')
logger = logging.getLogger("Project2 dta quality pipeline")

def is_null(value):
    if isinstance(value,int | float):
        return True
    elif isinstance(value,int | float):
        return False

    return value is None or value.strip() == ""




def loding_csv(path):
    try :
        with open(path,'r',newline='',encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = reader.fieldnames
    except FileNotFoundError as e:
        logger.error("input file not found %s " ,path)
        raise print(e)
    logger.info("CSV successfully loaded ")
    return rows , fieldnames


def genrate_pre_clean_report(rows,fieldnames,categorical_columns):
    """
    build a dictionary of pre-cleaning  quality metrics
    -row count
    -null count per column
    -duplicate row count
    -unique value count per categorical column
    :param rows:
    :param fieldnames:
    :param categorical_columns:
    :return:
    """

    logger.info("generating pre-cleaning quality metrics report")
    report ={}
    report["row_count"]  = len(rows)

    null_counts = {}
    for col in fieldnames :

        count =0
        for row in rows :
            value = row.get(col ,"")
            if value is None or value == value.strip():
                count+=1
        null_counts[col] = count
    report['nullcounts'] = null_counts

    dup=0
    seen=set()
    for row in rows :
        r = tuple(row.get(cols,"") for cols in fieldnames)
        if r in seen :
            dup+=1
        else  :
            seen.add(r)
    report['duplicates']    = dup

    unique_val = {}
    for col in categorical_columns:
        value = set()
        for row in rows:
            val = row.get(col, "")
            if val is not None and val.strip() != "":
                value.add(val.strip())
        unique_val[col] = value
    report['unique_val'] = unique_val

    logger.info(" pre-cleaning report done ! ")
    return report

def remove_duplicates(rows,fieldnames) :

    seen =set()
    removed=0
    cleaned_rows=[]
    for row in rows :
        val = tuple(row.get(col,"") for col in fieldnames )
        if val in seen :
            removed +=1
            continue
        seen.add(val)
        cleaned_rows.append(row)
    logging.info("removed %d duplicates ",removed)
    return cleaned_rows


def compute_column_mean(cleaned_rows , column ):

        mean={}

        total =0.0
        count =0
        for row in cleaned_rows:
            value = row.get(column,"")
            if is_null(value):

                continue
            try:
                total += float(value)
                count+=1
            except (ValueError ,TypeError) :
                continue

        return total/count if count >0 else 0.00


def handle_nulls(null_map ,cleaned_rows):

    """
    handle null values according to teh null_map by checking for each column it's desired strategy
    :param null_map:
    :param rows:
    :return:
    """

    logger.info("Handling null values using configured strategies")
    drop_counts=0
    fill_count={}
    is_drop=False


    mean={}
    for column, strategies in null_map.items():
        if strategies == "mean":
            mean[column] = compute_column_mean(cleaned_rows,column)
            logging.info("computed mean for column %s = %f",column,mean[column])

    t_cleaned_rows=[]
    for row in cleaned_rows :
        is_drop = False
        for column, strategies in null_map.items():
            if not is_null(row.get(column,"")) :
                continue

            elif strategies == "Drop" :
                drop_row =True


            elif strategies == "mean"  :
                row[column] = mean[column]

            else:
                row[column]= strategies

            fill_count[column]= fill_count.get(column,0)+1


        if is_drop:
            drop_counts +=1
        t_cleaned_rows.append(row)

    logger.info("Dropped %d rows due to null values", drop_counts)
    logger.info("Filled null values per column: %s", fill_count)
    return t_cleaned_rows

def standaedize_columns(t_cleaned_rows , string_columns):

    logger.info("Standardizing string columns: %s", string_columns)

    for row in t_cleaned_rows :

        for column in string_columns:
            if column in t_cleaned_rows and t_cleaned_rows[column] is not None:
                row[column]= row.get(column,"").astype(str).str.title()
    return t_cleaned_rows


def defining_types(rows, column_type_map):

    conversion_failures={}
    for row in rows :
        for column, types in column_type_map.items():

            if column not in row:
                continue

            value = row[column]
            if is_null(value):
                continue
            try :
                if types =='int':
                    row[column] = int(float(value))
                if types =='float':
                    row[column]=float(value)
                if types == 'str' or types == 'string':
                    row[column] = str(value)
            except (ValueError,TypeError) as e:
                conversion_failures[column] =conversion_failures.get(column ,0) +1
                logger.warning(
                    "Failed to convert value '%s' in column '%s' to %s: %s",
                    value, column, types, e,
                )

    logger.info("Type conversion failures per column: %s", conversion_failures)
    return rows



rows , fieldnames = loding_csv(path)

report = genrate_pre_clean_report(rows,fieldnames,categorical_columns)

cleaned_rows = remove_duplicates(rows,fieldnames)
for i in numerical_columns:
    means = compute_column_mean(cleaned_rows , i )
    # print(means)

t_cleaned_rows = handle_nulls(NULL_MAP ,cleaned_rows)

s_cleaned_rows = standaedize_columns(t_cleaned_rows , string_columns)

r = defining_types(rows, Column_type_map)

df  = pd.DataFrame(s_cleaned_rows )

df.to_csv("output.csv", index =False)

df1 =pd.DataFrame(report )

df1.to_csv("report.csv" , index= False)





