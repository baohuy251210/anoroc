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
    with open('./data_rebase/country_all_new_status.csv', 'w') as csv_file:
        field_names = ['country', 'name', 'cases',
                       'deaths', 'recovered', 'last_update']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        writer.writeheader()
        for country in data:
            country['name'] = dict_alpha_name[country['country']]['name']
            print(country)
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

'''
    Helper function for app.py
'''


'''
##(old) data process
'''

dict_slug_index = pd.read_csv(
    './data/country_index.csv', index_col='Country', encoding='cp1252').to_dict('index')


def index_name_slug(country_name):
    """Takes country name and 
    return country's slug (short name)
    Arguments:
        country_name {string} -- [Country Name]

    Returns:
        [string] -- [slug name]
    """
    return dict_slug_index[country_name]['Slug']


def cluster_from_day_one(country_slug, case_status='confirmed'):
    """Function to retrieve data of a country from day one(first confirmed case)
    to current date
    example url: https://api.covid19api.com/total/dayone/country/united-states/status/confirmed
    dayone (mixed) very confused: https://api.covid19api.com/dayone/country/{}/status/{}
    will return a list of confirmed case (in total) from dayone
    ### Useful keys: "Country", "Cases", "Date", "Status"(confirmed),
    Arguments:
    country_slug str - must be a country's slug from country_index.csv
    """
    baseurl = "https://api.covid19api.com/total/dayone/country/{}/status/{}".format(
        country_slug, case_status)
    data = datacollect.get_json(baseurl, {})
    if (type(data) == str):
        print("failed connecting to API source, returning cached data...")
        return "Day by day cluster failed"
    with open('./data/countries-total-dayone/'+country_slug+".csv", 'w') as csv_file:
        field_names = ['Country', 'Cases', 'Date']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        writer.writeheader()
        for day in data:
            writer.writerow(day)
    try:
        return("Retrieve {} from {} to {}".format(country_slug, type(data[0]['Date']), type(data[-1]['Date'])))
    except:
        print(country_slug+" : "+baseurl)
        return(country_slug)


def cluster_all_country_dayone():
    """Function calls to execute cluster_from_day_one for all countries
    """
    # country_slug = dict_slug_index['United States of America']['Slug']
    [cluster_from_day_one(dict_slug_index[country_name]['Slug'])
     for country_name in dict_slug_index.keys()]


def process_samedate_to_one(country_slug, case_status='confirmed'):
    """Function to process data from data/countries 
    to data/countries-total-dayone
    for now its australia and china
    Returns:
        [type] -- [description]
    """
    readUrl = './data/countries/'+country_slug+'.csv'
    writeUrl = './data/countries-total-dayone/'+country_slug+'.csv'
    with open(readUrl, 'r') as csv_read, open(writeUrl, 'w') as csv_write:
        reader = [x for x in list(csv.reader(csv_read)) if len(x) > 0]
        reader_2 = reader.copy()
        total = 0
        processed_lst = []
        for row in reader:
            if row[1] != 'Cases':
                cur_date = row[2]
                day_total = 0
                for finder in reader_2:
                    if finder[1] != 'Cases' and finder[2] == cur_date:
                        day_total += int(finder[1])
                # put day-total into dict
                ndict = {'Country': row[0],
                         'Cases': day_total, 'Date': cur_date}
                if ndict not in processed_lst:
                    processed_lst.append(ndict)

        field_names = ['Country', 'Cases', 'Date']
        writer = csv.DictWriter(
            csv_write, fieldnames=field_names, extrasaction='ignore')
        writer.writeheader()
        for data in processed_lst:
            writer.writerow(data)
            print(data)


# ERRORing countries:
"""
australia (done)
china(done)
For country like australia and china 
seems like total confirmed to {date} is sum of {cases} within that date
----------------
Version 0.3 worklog:
 -country from day one cluster new day only
"""


def cluster_dayone_newday(country_slug, case_status='confirmed'):
    baseurl = "https://api.covid19api.com/total/dayone/country/{}/status/{}".format(
        country_slug, case_status)

# print(cluster_all_country_dayone())
# print(cluster_from_day_one('australia'))
# Code to execute only once:
# retrieve_country_slug()
# print(process_samedate_to_one('china'))
