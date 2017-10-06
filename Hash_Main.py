import psycopg2
import os
import sys
import pika
import logging

def process(fnames, conn, db, cursor, mq_conn):
        for fname in fnames:
                os.system("/home/isigov/ida-6.8/idal -A -S/srv/data/ios/Hash.py /srv/data/ios/exes/idb/{0}".format(fname))
                try:
			        with open("Output.txt", "r") as f:
                        for line in f:
                        	splitter = line.split(",")
                        	my_hash = splitter[0]
                        	fname = int(splitter[1])
                        	funcname = splitter[2]
			                startea = int(splitter[3])
			                length = int(splitter[4])
                        	cursor.execute("INSERT INTO hashes (HASH, FUNCNAME, STARTEA, APPID, LEN) VALUES ('%s', '%s', '%d', '%d', '%d')" % (my_hash, funcname, startea, fname, length));
                except:
                    pass                
                try:
        			db.commit()
                    os.remove("Output.txt")
                except:
                    pass

                
                
dbh = psycopg2.connect('dbname=iosapps')
conn = dbh.cursor()
try:
	conn.execute('''CREATE TABLE hashes
       (HASH CHAR(32)   NOT NULL,
	FUNCNAME TEXT NOT NULL,
       STARTEA INTEGER     NOT NULL,
       APPID INTEGER     NOT NULL,
	LEN INTEGER NOT NULL,
	FOREIGN KEY (APPID) REFERENCES app(id)) TABLESPACE slow;''')
	dbh.commit()
except:
	print("Tables already exist!\n")

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.CRITICAL)
filenames = []
creds = pika.PlainCredentials('foo', 'bar')
parameters = pika.ConnectionParameters(host='rmq', port=5672, virtual_host='/', credentials=creds, heartbeat_interval=0)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.basic_qos(prefetch_count=1)
for method_frame, properties, body in channel.consume('hash'):
        if body == "STOP":
                break
        filenames = [body]
        process(filenames, connection, dbh, conn, connection)
        channel.basic_ack(method_frame.delivery_tag)
dbh.commit()
connection.close()
dbh.close()
