import psycopg2
import sys

my_hash = sys.argv[1]
fname = int(sys.argv[2])
funcname = sys.argv[3]

dbh = psycopg2.connect('dbname=iosapps')
conn = dbh.cursor()

#conn.execute("INSERT INTO apps (APPID, HASH) VALUES ('%s', '%s')" % (fname, my_hash));
conn.execute("INSERT INTO hashes (HASH, FUNCNAME, APPID) VALUES ('%s', '%s', '%d')" % (my_hash, funcname, fname));
dbh.commit()

dbh.close()
