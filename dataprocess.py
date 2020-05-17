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


# Code to execute only once:
# retrieve_country_slug()
