"""
dataprocess makes use of datacollect.py 
and turn json collected to csv file.
"""
import json
import csv
import numpy as np
import pandas as pd
import datacollect

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


def main():
    # print("update_csv_apify:..")
    # update_csv_apify()
    # print("apify.csv updated successful")

    print("update_csv_jhu:..")
    update_csv_jhu()
    print("jhu.csv updated successful")


if __name__ == '__main__':
    main()
