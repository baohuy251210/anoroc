import csv
import psycopg2
import data_rebase
import datacollect
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


def get_country_status(alpha):
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