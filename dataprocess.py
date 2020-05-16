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
    with open('apify.csv', 'w') as csv_file:
        field_names = ['country', 'infected', 'recovered',
                       'deceased', 'tested', 'lastUpdatedApify']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        # write
        writer.writeheader()
        for country in data:
            writer.writerow(country)


def main():
    print("update_csv_apify:..")
    update_csv_apify()
    print("apify.csv updated successful")


if __name__ == '__main__':
    main()
