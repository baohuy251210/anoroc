import datetime
import csv
import datacollect
import pandas as pd
mlcovid_url = 'https://covid19-api.org/api/'


dict_alpha_name = pd.read_csv('./data_rebase/country_alpha_index.csv',
                              index_col='alpha2', keep_default_na=False, na_values=['__'], encoding='utf-8').to_dict('index')


def remake_country_alpha():
    df = pd.read_csv('./data_rebase/country_all.csv',
                     encoding='utf-8', keep_default_na=False, index_col='alpha-2', na_values=['__'])[['alpha-3']]
    return df


dict_alpha_23 = remake_country_alpha().to_dict('index')


def csv_all_new_status():
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
    url_all_status = './data_rebase/country_all_status.csv'
    with open(url_all_status, 'w', encoding='utf-8') as csv_file:
        field_names = ['country', 'alpha-3', 'name', 'cases',
                       'deaths', 'recovered', 'last_update']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        writer.writeheader()
        for country in data:
            country['name'] = dict_alpha_name[country['country']]['name']
            if country['country'] in dict_alpha_23.keys():
                country['alpha-3'] = dict_alpha_23[country['country']]['alpha-3']
                writer.writerow(country)
            else:
                print('skipped: ', country['country'])


'''
TODO : Functions that fetch from API and update database.
-----
country timeline
'''


def get_country_timeline(alpha):
    """[summary]

    Arguments:
        alpha {[type]} -- [description]

    Returns:
    """
    baseurl = mlcovid_url+'timeline/'+alpha
    data = datacollect.get_json(baseurl, {})
    df_timeline = pd.DataFrame(eval(str(data))).drop(columns='country')
    return df_timeline
    print('##Database: retrieve timeline ' +
          alpha + ": OK")


'''
TODO: Since using client-based connection is too slow,
I decided to use the country-timeline again
'''


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


def get_quick_country_name(alpha):
    return dict_alpha_name[alpha]['name']


def get_quick_country_timeline(alpha):
    """Retrieve country's data from 
    a stored .csv 

    Arguments:
        alpha {str} -- country's alpha

    Returns:
        pandas.DF -- timeline df with country, name, cases, deaths, recovered, last_update
        Dropped last row (current day) 
    """
    return pd.read_csv('./data_rebase/country-timeline/'+alpha+'.csv',
                       keep_default_na=False, na_values=['__'], encoding='utf-8')[:-1]


def get_country_live_status(alpha):
    """Retrieve country status from API
    https://covid19-api.org/api/status/:country
    Arguments:
        alpha str -- country alpha value

    Returns:
        cases, deaths, recovered - tuple of 3
    """
    baseurl = 'https://covid19-api.org/api/status/'+alpha
    data = datacollect.get_json(baseurl, {})
    return data['cases'], data['deaths'], data['recovered']

# print(retrieve_all_country_timeline())


# sql_update_all_status(False)
# print(get_df_all_country_status(False))
