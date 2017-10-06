import os
import sys
import extract_lib
import fat_lipo
import psycopg2
import hashlib

def main():
	Cocoapods = sys.argv[1]

	dbh = psycopg2.connect('dbname=iosapps')
	conn = dbh.cursor()

	LibMain_ID = 0
	LibVer_ID = 0
	LibFrame_ID = 0
	for folderName in os.listdir(Cocoapods):
		if(os.path.isdir("{0}/{1}".format(Cocoapods, folderName))):
			print("[DEBUG] Working on %s\n" % folderName)
			conn.execute("INSERT INTO LibMain (NAME, ID) VALUES ('%s', '%d')" % (folderName[:32], LibMain_ID));
			dbh.commit()
			for versionName in os.listdir("{0}/{1}".format(Cocoapods, folderName)):
				conn.execute("INSERT INTO LibVer (ID, NAME, LIBID) VALUES ('%d', '%s', '%d')" % (LibVer_ID, versionName[:32], LibMain_ID));
				dbh.commit()
				LibVer_ID = LibVer_ID + 1
				for frameworkName in os.listdir("{0}/{1}/{2}".format(Cocoapods, folderName, versionName)):
					if(os.path.isdir("{0}/{1}/{2}/{3}".format(Cocoapods, folderName, versionName, frameworkName))):
						conn.execute("INSERT INTO LibFrame (ID, NAME, LIBID) VALUES ('%d', '%s', '%d')" % (LibFrame_ID, frameworkName[:32], LibVer_ID));
						dbh.commit()
						LibFrame_ID = LibFrame_ID + 1
						# for (path, fileName) in extract_lib.recursiveFind("{0}/{1}/{2}/{3}".format(Cocoapods, folderName, versionName, frameworkName)):
						# 	try:
						# 		#if(fat_lipo.checkARMv7(path + "/{0}".format(fileName))):
						# 			#checksum = md5Checksum(path + "/{0}".format(fileName))
						# 		print("[DEBUG] Found library file at %s with a hash of %s\n" % (path + "/{0}".format(fileName), checksum))
								
						# 		break
						# 	except:
						# 		pass
			LibMain_ID = LibMain_ID + 1

def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

if __name__ == '__main__':
    main()