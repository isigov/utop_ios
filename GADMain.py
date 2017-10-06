import os
import sys
import pika
import psycopg2
import psycopg2.extras
import pika

def main():
	dbh = psycopg2.connect('dbname=iosapps')
	#conn = dbh.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)

	while(True):
		try:
			creds = pika.PlainCredentials('foo', 'bar')
			parameters = pika.ConnectionParameters(host='rmq', port=5672, virtual_host='/', credentials=creds, heartbeat_interval=0)
			connection = pika.BlockingConnection(parameters)
			channel = connection.channel()
			channel.basic_qos(prefetch_count=1)
			for method_frame, properties, body in channel.consume('cocoapods'):
					if body == "STOP":
						break
					filenames = [body]
					channel.basic_ack(method_frame.delivery_tag)
					callback(filenames, dbh)
			conn.close()
			dbh.close()
		except:
			pass

def callback(filenames, dbh):

	for fname in filenames:
		if(os.path.isfile(fname + "/Output.txt")):
			os.remove(fname + "/Output.txt")

		if(not os.path.isdir(fname)):
			continue

		for fileName in os.listdir(fname):
			if(fileName.endswith(".txt")):
				continue
			if(os.path.isfile("{0}/{1}".format(fname, fileName))):
				os.system("/home/isigov/ida-6.8/idal -A -S/srv/data/ios/GADHash.py {0}/{1}".format(fname, fileName))
				
		if(os.path.isfile(fname + "/Output.txt")):
			ID = 0
			ID_Framework = 0
			path_split = fname.split("/")
			path_len = len(path_split)
			libString = path_split[path_len - 1]
			versionString = path_split[path_len - 2]
			nameString = path_split[path_len - 3]
			try:
				temp = dbh.cursor(nameString, cursor_factory=psycopg2.extras.DictCursor)
				temp.execute("SELECT ID FROM LibMain WHERE NAME = '%s'" % nameString[:32])
				for row in temp:
					ID = int(row[0])
					break
				temp.close()

				temp = dbh.cursor(nameString, cursor_factory=psycopg2.extras.DictCursor)
				temp.execute("SELECT ID FROM LibVer WHERE NAME = '%s' AND LIBID = '%d'" % (versionString[:32], ID))
				for row in temp:
					ID = int(row[0])
					break
				temp.close()

				temp = dbh.cursor(nameString, cursor_factory=psycopg2.extras.DictCursor)
				temp.execute("SELECT ID FROM LibFrame WHERE NAME = '%s' AND LIBID = '%d'" % (libString[:32], ID))
				for row in temp:
					ID_Framework = int(row[0])
					break
				temp.close()
			except:
				pass

			total_list = []
			print("[DEBUG] Testing %s\n" % (fname))
			with open(fname + "/Output.txt", "r") as f:
				for line in f:
					new_list = []
					splitter = line.split(",")
					my_hash = splitter[0]
					filname = splitter[1]
					funcname = splitter[2]
					funclen = int(splitter[3])
					print("[DEBUG] Testing hash %s with funcName of %s and funcLen of %d\n" % (my_hash, filname, funclen))
					conn = dbh.cursor(fname, cursor_factory=psycopg2.extras.DictCursor)
					conn.execute("SELECT APPID FROM hashes WHERE hash = '%s'" % my_hash)
					for row in conn:
						new_list.append(row[0])
					conn.close()
					print("[DEBUG] Found %d matches for hash %s\n" % (len(new_list), my_hash))
					if(len(new_list) == 0):
						print("[DEBUG] Mismatch, moving to next file\n")
						total_list = []
						break
					if(len(total_list) == 0):
						total_list = new_list
					total_list = list(set(new_list).intersection(total_list))
					print("[DEBUG] New total list is of length %s\n" % len(total_list))
					if(len(total_list) == 0):
						print("[DEBUG] Mismatch, moving to next file\n")
						break

			temp = dbh.cursor()
			for app_id in total_list:
				temp.execute("INSERT INTO app2Lib (APPID, LIBID, FRAMEID) VALUES ('%d', '%d')" % (app_id, ID, ID_Framework));
				dbh.commit()
			temp.close()

			os.remove(fname + "/Output.txt")

if __name__ == '__main__':
	main()
