#!/bin/python

import csv
import MySQLdb
import codecs
import settings

def is_numeric(s):
    try:
      i = float(s)
    except ValueError:
        # not numeric
        return False
    else:
        # numeric
        return True

def main():
    conn = MySQLdb.connect (host=settings.MYSQL_HOST, user=settings.MYSQL_USER, passwd=settings.MYSQL_PASSWORD, db=settings.MYSQL_DATABASE)
    cursor = conn.cursor()
    
    TABLES = ['agency', 'calendar_dates', 'routes', 'stops', 'stop_times', 'trips']
    
    for table in TABLES:
        print 'processing %s' % table
        f = open('gtfs/%s.txt' % table, 'r')
        reader = csv.reader(f)
        
        columns = reader.next()
        newcolumns = []
        for c in columns:
            print c
            c=c.decode('utf-8-sig').encode('utf-8')
            print c
            newcolumns.append(c.replace("\xef\xbb\xbf",""))
        for row in reader:
            insert_row = []
            for value in row:
                value = value.decode('utf-8-sig').encode('utf-8')
                print value
                if not is_numeric(value):
                    insert_row.append('"' + MySQLdb.escape_string(value) + '"')
                else:
                    insert_row.append(value)

            insert_sql = "INSERT INTO %s (%s) VALUES (%s);" % (table, ','.join(newcolumns), ','.join(insert_row))  
            cursor.execute(insert_sql)
            conn.commit()

    cursor.close ()
    conn.close ()

    
if __name__ == '__main__':
    main()