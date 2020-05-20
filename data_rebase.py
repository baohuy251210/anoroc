"""
Version 0.3: I decided to change the base API from covid19api.com to
covid19-api.org
They have prediction for 2 weeks and also much more updated and sorted 
data.
postman documentation: 
https://documenter.getpostman.com/view/10877427/SzYW2f8n?version=latest#e56a91bb-7d30-47bf-bfc5-3666397c4813


"""
import psycopg2
import json
import csv
import numpy as np
import pandas as pd
import datacollect
import datetime
mlcovid_url = 'https://covid19-api.org/api/'


def create_table_1():
    conn = psycopg2.connect(
        'host=localhost dbname=postgres user=postgres password=cyos94')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE alpha2_index(
        alpha2 char(2) PRIMARY KEY,
        name text
    )
    ''')
    conn.commit()


def load_country():
    thost = 'localhost'
    tport = '5432'
    tdbname = 'postgres'
    tuser = 'postgres'
    tpw = 'cyos94'
    db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                               user=tuser, password=tpw)
    db_cursor = db_conn.cursor()
    with open('./data_rebase/country_alpha_index.csv', 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            db_cursor.execute(
                "INSERT INTO alpha2_index VALUES (%s, %s)", (row['alpha2'], row['name']))
            print(row['alpha2'], row['name'])
    db_conn.commit()


dict_alpha_name = pd.read_csv('./data_rebase/country_alpha_index.csv',
                              index_col='alpha2', keep_default_na=False, na_values=['__'], encoding='utf-8').to_dict('index')


# sql_retrieve_all_status()

# load_country()
"""
    https://covid19-api.org/api/country/:country #get countries 
    --Focus on "name" and "alpha2"
    ---"name": official name?
    ---"alpha2": country code also param for country in this api
"""


def retrieve_country_alpha2():
    """This function should only be called once
    to collect from api the countries and store it into csv as countries and alpha2
    https://covid19-api.org/api/countries
    returns a list of dicts, each dict has "name" and "alpha2" to get
    """
    baseurl = mlcovid_url+'countries'
    data = datacollect.get_json(baseurl, {})
    with open('./data_rebase/country_alpha_index.csv', 'w', encoding='utf-8') as csv_file:
        field_names = ['name', 'alpha2']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        writer.writeheader()
        for country in data:
            writer.writerow(country)
    print("##country_alpha_index created")


def retrieve_all_country_status():
    """Retrieve current status ('cases','deaths', 'recovered', 'last_update','country':alpha2)
    to make live table (live updated from jhu csse)
    https://covid19-api.org/api/status
    returns a list of dicts [{}, {},....]
    each has country alpha2 and live status  
    Returns:
        [type] -- [description]
    """
    baseurl = mlcovid_url+'status'
    data = datacollect.get_json(baseurl, {})
    url_all_status = './data_rebase/country_all_new_status.csv'
    url_last_update = './extra/last_update.txt'
    with open(url_all_status, 'w', encoding='utf-8') as csv_file, open(url_last_update, 'w') as txt_file:
        field_names = ['country', 'name', 'cases',
                       'deaths', 'recovered', 'last_update']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        writer.writeheader()
        for country in data:
            country['name'] = dict_alpha_name[country['country']]['name']
            # print(country)
            if country['country'] == 'US':
                txt_file.write(country['last_update'])
                print("##updated last_update")
            writer.writerow(country)

    print("##country_all_new_status retrieved")


def retrieve_country_timeline(country_alpha2):
    """Function to retrieve timeline of a country from around jan 22
    https://covid19-api.org/api/timeline/:country_alpha2
    return list of dicts: from current date -> start date
    --'country' : alpha2
    --'last_update'
    --'cases'
    --'deaths'
    --'recovered'
    Arguments:
        country_alpha2 {String-length=2} -- alpha2 of queried country
    """
    baseurl = mlcovid_url+'timeline/'+country_alpha2
    data = datacollect.get_json(baseurl, {})
    with open('./data_rebase/country-timeline/'+country_alpha2+'.csv', 'w', encoding='utf-8') as csv_file:
        field_names = ['country', 'name', 'cases',
                       'deaths', 'recovered', 'last_update']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        writer.writeheader()
        for day in data[::-1]:
            day['name'] = dict_alpha_name[day['country']]['name']
            writer.writerow(day)
    print('cluster timeline ' +
          dict_alpha_name[country_alpha2]['name'] + ": OK")


def retrieve_all_country_timeline():
    for alpha2 in dict_alpha_name.keys():
        retrieve_country_timeline(alpha2)
        # print(alpha2)


'''
Data Rebaser execution lines (execute only one, offline handling)
'''
# print(retrieve_all_country_timeline())
# print(retrieve_country_timeline('CI'))
# print(retrieve_country_alpha2())  # made country_alpha_index.csv
# print(retrieve_all_country_status())  # updated country status all


def update_check():
    """
    https://covid19-api.org/api/status
    Retrieve current status ('cases','deaths', 'recovered', 'last_update','country':alpha2)
    This Function check for US last_update(time) and check whether 
    the ./extra/last_update.csv matches the live time
    if not it will retrieve all status for country
    *data[0] should be US

    Return: string - live time updated from JHU CSSE 
    """

    baseurl = mlcovid_url+'status'
    data = datacollect.get_json(baseurl, {})
    time_live = data[0]['last_update']
    time_app_current = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open('./extra/last_update.txt', 'r') as txt_file:
        time_last = txt_file.readlines()[0].strip()
        if (time_last != time_live):
            print("##data outdate: Updating...({}->{})".format(time_last, time_live))
            retrieve_all_country_status()
        else:
            print('##data is live and updated{} |app: {} ' +
                  time_last, time_app_current)
    return time_app_current


'''
    Helper function for app.py
'''
