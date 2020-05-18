"""
dataprocess makes use of datacollect.py
and turn json collected to csv file.
"""
import json
import csv
import numpy as np
import pandas as pd
import datacollect
from datetime import datetime
apify_url = 'https://api.apify.com/v2/key-value-stores/tVaYRsPHLjNdNBu7S/records/LATEST?disableRedirect=true'


def update_csv_apify():
    params = {'disableRedirect': True}
    data = datacollect.get_json(apify_url, params)
    # print(json.dumps(data, indent=2))
    with open('./data/apify.csv', 'w') as csv_file:
        field_names = ['country', 'infected', 'recovered',
                       'deceased', 'tested', 'lastUpdatedApify']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        # write
        writer.writeheader()
        for country in data:
            writer.writerow(country)


jhu_url = 'https://api.covid19api.com/summary'


def update_csv_jhu():
    params = {}
    data = datacollect.get_json(jhu_url, params)
    if (type(data) == str):
        print("failed connecting to API source, returning cached data...")
        return "a few hours ago"

    # Get new data successfully
    with open('./data/jhu.csv', 'w') as csv_file:
        field_names = ['Country', 'TotalConfirmed', 'NewConfirmed',
                       'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'NewRecovered']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        # write
        writer.writeheader()
        for country in data['Countries']:
            writer.writerow(country)
    with open('./data/jhu_sorted.csv', 'w') as csv_file:
        field_names = ['Country', 'TotalConfirmed', 'NewConfirmed',
                       'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'NewRecovered']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        # write
        writer.writeheader()
        sorted_infected = sorted(
            data['Countries'], reverse=True, key=lambda x: int(x['TotalConfirmed']))
        for country in sorted_infected:
            writer.writerow(country)
    with open('./data/global_jhu.csv', 'w') as csv_file:
        field_names = ['TotalConfirmed', 'NewConfirmed',
                       'NewDeaths', 'TotalDeaths', 'NewRecovered', 'TotalRecovered']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        # write
        writer.writeheader()

        writer.writerow(data['Global'])
    print("jhu.csv updated successful")
    return datetime.now().strftime('%b %d %Y %H:%M:%S')


def retrieve_country_slug():
    """This function should only be called once
    to collect from api the countries and store it into csv as countries and slug
    """
    data = datacollect.get_json(jhu_url, {})
    with open('./data/country_index.csv', 'w') as csv_file:
        field_names = ['Country', 'Slug']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        writer.writeheader()
        for country in data['Countries']:
            writer.writerow(country)
    print("index created")


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
"""
# print(cluster_all_country_dayone())
# print(cluster_from_day_one('australia'))
# Code to execute only once:
# retrieve_country_slug()
# print(process_samedate_to_one('china'))
