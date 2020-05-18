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


def cluster_from_day_one(country_slug, case_status='confirmed'):
    """Function to retrieve data of a country from day one(first confirmed case)
    to current date
    example url: https://api.covid19api.com/total/dayone/country/united-states/status/confirmed
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
    with open('./data/countries/'+country_slug+".csv", 'w') as csv_file:
        field_names = ['Country', 'Cases', 'Date']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        writer.writeheader()
        for day in data:
            writer.writerow(day)
    try:
        return("Retrieve {} from {} to {}".format(country_slug, data[0]['Date'], data[-1]['Date']))
    except:
        print(country_slug+" : "+baseurl)
        return(country_slug)


def cluster_all_country_dayone():
    """[summary]
    """
    # country_slug = dict_slug_index['United States of America']['Slug']
    [cluster_from_day_one(dict_slug_index[country_name]['Slug'])
     for country_name in dict_slug_index.keys()]


print(cluster_all_country_dayone())

# Code to execute only once:
# retrieve_country_slug()
