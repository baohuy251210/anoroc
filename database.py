import os
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
database_url = 'postgres://wokxqtzumnljhn:58d6e6165cec6a0de10683ac93d242099c1b3add8751fc18f80a838379c6d4c2@ec2-34-200-72-77.compute-1.amazonaws.com:5432/dcr96h9mtra8a4'


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
        print("You are connected to - ", record[0], "\n")
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
        db_cursor.execute("SELECT current_database();")
        record = db_cursor.fetchone()
        print("You are connected to - ", record[0], "\n")
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
        db_cursor.execute("SELECT current_database();")
        record = db_cursor.fetchone()
        print("You are connected to - ", record[0], "\n")
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
        db_cursor.execute("SELECT current_database();")
        record = db_cursor.fetchone()
        print("You are connected to - ", record[0], "\n")
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
        db_cursor.execute("SELECT current_database();")
        record = db_cursor.fetchone()
        print("You are connected to - ", record[0], "\n")
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
        db_cursor.execute("SELECT current_database();")
        record = db_cursor.fetchone()
        print("You are connected to - ", record[0], "\n")
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
        db_cursor.execute("SELECT current_database();")
        record = db_cursor.fetchone()
        print("You are connected to - ", record[0], "\n")
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
        db_cursor.execute("SELECT current_database();")
        record = db_cursor.fetchone()
        print("You are connected to - ", record[0], "\n")

        sql_query = 'INSERT INTO live_status VALUES(%s, %s, %s, %s, %s, %s)'
        for row in data:
            row['name'] = get_country_from_alpha(row['country'], local)[0]
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
        db_cursor.execute("SELECT current_database();")
        record = db_cursor.fetchone()
        print("You are connected to - ", record[0], "\n")

        sql_query = '''UPDATE live_status
                        SET cases = %s,
                        deaths = %s,
                        recovered = %s,
                        last_update = %s
                        WHERE alpha2 = %s AND last_update != %s
        '''
        for row in data:
            db_cursor.execute(sql_query, (row['cases'], row['deaths'], row['recovered'],
                                          row['last_update'], row['country'], row['last_update']))
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if(db_conn):
            db_cursor.close()
            db_conn.close()
            print("PostgreSQL connection is closed")
