"""
Version 0.3: I decided to change the base API from covid19api.com to
covid19-api.org
They have prediction for 2 weeks and also much more updated and sorted 
data.
postman documentation: 
https://documenter.getpostman.com/view/10877427/SzYW2f8n?version=latest#e56a91bb-7d30-47bf-bfc5-3666397c4813


"""
import json
import csv
import numpy as np
import pandas as pd
import datacollect
from datetime import datetime


"""
    https://covid19-api.org/api/country/:country #get countries 
    --Focus on "name" and "alpha2"
    ---"name": official name?
    ---"alpha2": country code also param for country in this api
"""

mlcovid_url = 'https://covid19-api.org/api/'


def retrieve_country_alpha2():
    """This function should only be called once
    to collect from api the countries and store it into csv as countries and alpha2
    https://covid19-api.org/api/countries
    returns a list of dicts, each dict has "name" and "alpha2" to get
    """
    baseurl = mlcovid_url+'countries'
    data = datacollect.get_json(baseurl, {})
    with open('./data_rebase/country_alpha_index.csv', 'w') as csv_file:
        field_names = ['name', 'alpha2']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        writer.writeheader()
        for country in data:
            writer.writerow(country)
    print("##country_alpha_index created")


dict_alpha_name = pd.read_csv('./data_rebase/country_alpha_index.csv',
                              index_col='alpha2', keep_default_na=False, na_values=['__'], encoding='cp1252').to_dict('index')


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
    with open(url_all_status, 'w') as csv_file, open(url_last_update, 'w') as txt_file:
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
    with open('./data_rebase/country-timeline/'+country_alpha2+'.csv', 'w') as csv_file:
        field_names = ['country', 'name', 'cases',
                       'deaths', 'recovered', 'last_update']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        writer.writeheader()
        for day in data[::-1]:
            day['name'] = dict_alpha_name[day['country']]['name']
            writer.writerow(day)
    print('cluster timeline ' + country_alpha2 + ": OK")


def retrieve_all_country_timeline():
    for alpha2 in dict_alpha_name.keys():
        retrieve_country_timeline(alpha2)
        # print(alpha2)


'''
Data Rebaser execution lines (execute only one, offline handling)
'''
# print(retrieve_all_country_timeline())
# print(retrieve_country_timeline('US'))
# print(retrieve_country_alpha2()) #made country_alpha_index.csv
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
    with open('./extra/last_update.txt', 'r') as txt_file:
        time_last = txt_file.readlines()[0].strip()
        if (time_last != time_live):
            print("##data outdate: Updating...({}->{})".format(time_last, time_live))
            retrieve_all_country_status()
        else:
            print('##data is live and updated '+time_last)
    return time_live


'''
    Helper function for app.py
'''
