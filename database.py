import os
import datetime
import csv
import psycopg2
import datacollect
import pandas as pd
from sqlalchemy import create_engine
mlcovid_url = 'https://covid19-api.org/api/'

# these were all outdated profiles :3
thost = 'localhost'
tport = '5432'
tdbname = 'postgres'
tuser = 'postgres'
tpw = 'cyos94'
database_url = 'postgres://vzcptenkjokmte:2c303f140cd5b887e5f0a3274e5e5db2c6a9d2a4e3825242550974193bf7c910@ec2-34-206-31-217.compute-1.amazonaws.com:5432/daa9tdg04a4o0v'

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


def sql_test_conn(local):
    try:
        if local:
            db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                                       user=tuser, password=tpw)
        else:
            db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT current_database();")
        record = db_cursor.fetchone()
        print("You are connected to - ", record[0])
        db_conn.commit()
        return record
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if(db_conn):
            db_cursor.close()
            db_conn.close()
            print("PostgreSQL connection is closed")


def load_country(local):
    """[summary]
    """
    try:
        if local:
            db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                                       user=tuser, password=tpw)
        else:
            db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        with open('./data_rebase/country_alpha_index.csv', 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                db_cursor.execute(
                    "INSERT INTO alpha2_index VALUES (%s, %s)", (row['alpha2'], row['name']))
                print(row['alpha2'], row['name'])
        db_conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if(db_conn):
            db_cursor.close()
            db_conn.close()
            print("PostgreSQL connection is closed")


def get_country_from_name(country_name, local):
    """Get country index from SQL given country alpha-2
    Returns:
        tuple -- (alpha, name)
    """
    sql_query = 'SELECT alpha2, name FROM alpha2_index WHERE name = %s'
    try:
        if local:
            db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                                       user=tuser, password=tpw)
        else:
            db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        db_cursor.execute(sql_query, (country_name,))
        record = db_cursor.fetchone()
        db_conn.commit()
        return record
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if(db_conn):
            db_cursor.close()
            db_conn.close()
            print("PostgreSQL connection is closed")


def get_country_from_alpha(country_alpha, local):
    """Get country index from SQL given country alpha-2
    Returns:
        tuple -- (alpha, name)
    """
    sql_query = 'SELECT alpha2, name FROM alpha2_index WHERE alpha2 = %s'
    try:
        if local:
            db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                                       user=tuser, password=tpw)
        else:
            db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        db_cursor.execute(sql_query, (country_alpha,))
        record = db_cursor.fetchone()
        db_conn.commit()
        return record
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if(db_conn):
            db_cursor.close()
            db_conn.close()
            print("PostgreSQL connection is closed")


def get_df_country_index(local):
    sql_query = 'SELECT * FROM alpha2_index'
    try:
        if local:
            db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                                       user=tuser, password=tpw)
        else:
            db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        db_cursor.execute(sql_query)
        df_country_index = pd.read_sql(sql_query, db_conn)
        db_conn.commit()
        return df_country_index
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if(db_conn):
            db_cursor.close()
            db_conn.close()
            print("PostgreSQL connection is closed")


def get_country_status(alpha, local):
    """ generate live status of a country to df

    Arguments:
        alpha {str} -- [country's alpha]

    Returns:
        pandas.dataFrame -- alpha's sql report
    """
    sql_query = 'SELECT * FROM live_status WHERE alpha2 = %s'
    try:
        if local:
            db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                                       user=tuser, password=tpw)
        else:
            db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        df_selected = pd.read_sql(sql_query, db_conn, params=(alpha,))
        db_conn.commit()
        return df_selected
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if(db_conn):
            db_cursor.close()
            db_conn.close()
            print("PostgreSQL connection is closed")


def get_df_all_country_status(local):
    """ generate live status of a country to df

    Arguments:
        alpha {str} -- [country's alpha]

    Returns:
        pandas.dataFrame -- alpha's sql report
    """
    sql_query = 'SELECT * FROM live_status'
    try:
        if local:
            db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                                       user=tuser, password=tpw)
        else:
            db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        df_selected = pd.read_sql(sql_query, db_conn)
        db_conn.commit()
        return df_selected
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if(db_conn):
            db_cursor.close()
            db_conn.close()
            print("PostgreSQL connection is closed")


def get_data_last_update_api():
    """Function to fetch the last update time of 
    a country given its alpha code from covid19-api.org
    this function is country specific [US]
    Timezone: UTC / GMT+0
    Arguments:
        alpha {str} -- [country's alpha code]

    Returns:
        [str] -- [time UTC of alpha's last update time]
    """
    baseurl = mlcovid_url+'status'
    data = datacollect.get_json(baseurl, {})
    time_api = data[0]['last_update']
    return time_api


def get_data_last_update_sql(local):
    """Function to fetch the last update time of 
    a country given its alpha code from Postgres
    this function is country specific [US]
    Timezone: UTC / GMT+0
    Arguments:
        alpha {str} -- [country's alpha code]
    Returns:
        [str] -- [time UTC of alpha's last update time]
    """
    sql_query = "SELECT last_update FROM live_status WHERE alpha2 = 'US'"
    try:
        if local:
            db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                                       user=tuser, password=tpw)
        else:
            db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        db_cursor.execute(sql_query)
        db_conn.commit()
        return db_cursor.fetchone()[0]
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if(db_conn):
            db_cursor.close()
            db_conn.close()
            print("PostgreSQL connection is closed")


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


def sql_retrieve_all_status(local):
    """
    `row` format:{'country': 'PR', 'last_update': '2020-03-17T16:13:14', 'cases': 0, 'deaths': 0, 'recovered': 0, 'name': 'Puerto Rico'}
    """
    baseurl = mlcovid_url+'status'
    data = datacollect.get_json(baseurl, {})
    try:
        if local:
            db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                                       user=tuser, password=tpw)
        else:
            db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        sql_query = 'INSERT INTO live_status VALUES(%s, %s, %s, %s, %s, %s)'
        for row in data:
            row['name'] = get_country_from_alpha(row['country'], local)[1]
            db_cursor.execute(sql_query, (row['country'], row['name'], row['cases'],
                                          row['deaths'], row['recovered'], row['last_update']))
            db_conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if(db_conn):
            db_cursor.close()
            db_conn.close()
            print("PostgreSQL connection is closed")


def sql_update_all_status(local):
    baseurl = mlcovid_url+'status'
    data = datacollect.get_json(baseurl, {})
    try:
        if local:
            db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                                       user=tuser, password=tpw)
        else:
            db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        sql_query = '''UPDATE live_status
                        SET cases = %s,
                        name = %s,
                        deaths = %s,
                        recovered = %s,
                        last_update = %s
                        WHERE alpha2 = %s AND last_update != %s
        '''
        for row in data:
            country_name = get_country_from_alpha(row['country'], False)[1]
            print(country_name)
            db_cursor.execute(sql_query, (row['cases'], country_name, row['deaths'], row['recovered'],
                                          row['last_update'], row['country'], row['last_update']))
            db_conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if(db_conn):
            db_cursor.close()
            db_conn.close()
            print("PostgreSQL connection is closed")


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
