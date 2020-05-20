import datetime
import csv
import psycopg2
import data_rebase
import datacollect
import pandas as pd
from sqlalchemy import create_engine
mlcovid_url = data_rebase.mlcovid_url


thost = 'localhost'
tport = '5432'
tdbname = 'postgres'
tuser = 'postgres'
tpw = 'cyos94'


def get_country_from_name(country_name):
    """Get country index from SQL given country alpha-2
    Returns:
        tuple -- (alpha, name)
    """
    sql_query = 'SELECT alpha2, name FROM alpha2_index WHERE name = %s'
    try:
        db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                                   user=tuser, password=tpw)
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT version();")
        record = db_cursor.fetchone()
        print("You are connected to - ", record, "\n")
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


def get_country_from_alpha(country_alpha):
    """Get country index from SQL given country alpha-2
    Returns:
        tuple -- (alpha, name)
    """
    sql_query = 'SELECT alpha2, name FROM alpha2_index WHERE alpha2 = %s'
    try:
        db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                                   user=tuser, password=tpw)
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT version();")
        record = db_cursor.fetchone()
        print("You are connected to - ", record, "\n")
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


def get_df_country_index():
    sql_query = 'SELECT * FROM alpha2_index'
    try:
        db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                                   user=tuser, password=tpw)
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT version();")
        record = db_cursor.fetchone()
        print("You are connected to - ", record, "\n")
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


def get_country_status(alpha):
    """ generate live status of a country to df

    Arguments:
        alpha {str} -- [country's alpha]
    Returns:
        pandas.dataFrame --
    """
    sql_query = 'SELECT * FROM live_status WHERE alpha2 = %s'
    try:
        db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                                   user=tuser, password=tpw)
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT version();")
        record = db_cursor.fetchone()
        print("You are connected to - ", record, "\n")
        db_cursor.execute(sql_query, (alpha,))
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


def get_country_timeline(alpha):
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
    baseurl = mlcovid_url+'timeline/'+alpha
    country_name = get_country_from_alpha(alpha)
    data = datacollect.get_json(baseurl, {})
    with open('./data_rebase/country-timeline/'+alpha+'.csv', 'w', encoding='utf-8') as csv_file:
        field_names = ['country', 'name', 'cases',
                       'deaths', 'recovered', 'last_update']
        writer = csv.DictWriter(
            csv_file, fieldnames=field_names, extrasaction='ignore')
        writer.writeheader()
        for day in data[::-1]:
            day['name'] = country_name
            writer.writerow(day)
    print('cluster timeline ' +
          country_name + ": OK")


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


def get_data_last_update_sql():
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
        db_conn = psycopg2.connect(host=thost, port=tport, dbname=tdbname,
                                   user=tuser, password=tpw)
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT version();")
        record = db_cursor.fetchone()
        print("You are connected to - ", record, "\n")
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
