import os
import psycopg2
import psycopg2.extras
import sys

dbh = psycopg2.connect('dbname=iosapps')
cursor = dbh.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
cursor.execute('SELECT * FROM apps WHERE downloaded=\'f\'')
#conn = dbh.cursor()

for row in cursor:
    print("App %s isn't downloaded\n" % row['id'])
    #os.system("amqp-publish -r app_download -u amqp://foo:bar@rmq -b \"{0}\"".format(row['id']))

dbh.close()
