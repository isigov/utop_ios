import os
import json
import requests
import posixpath
import urlparse
import tarfile
import zipfile
import fat_lipo
import shutil
import sys 
import unix_ar
import pika

Output_Path = ""
Keep = False
def main():
	global Output_Path
	global Keep

	Keep = False
	Output_Path = ""

	# for folderName in os.listdir("/srv/data/ios/Cocoapods/Google-Mobile-Ads-SDK"):
	# 	out = "/srv/data/ios/Cocoapods/Google-Mobile-Ads-SDK/{0}".format(folderName)
	# 	print("Doing %s\n" % out)
	# 	os.system("amqp-publish -r cocoapods -u amqp://foo:bar@rmq -b \"{0}\"".format(out))
	# if(len(sys.argv) != 4):
	# 	print("Invalid arguments\n\nUsage: extract_lib.py <repository directory> <output path> -(k)<keep fat file>(d)<delete fat files>\n")
	# 	return

	# Output_Path = sys.argv[2]
	# Keep = True if (sys.argv[3] == "-k") else False

	# print("Starting with parameters:\nRespository Directory: {0}\nOutput Path: {1}\nKeep Fat Files: {2}\n".format(sys.argv[1], Output_Path, str(Keep)))

	# while True:
	# 	try:
	# 		creds = pika.PlainCredentials('foo', 'bar')
	# 		parameters = pika.ConnectionParameters(host='rmq', port=5672, virtual_host='/', credentials=creds, heartbeat_interval=0)
	# 		connection = pika.BlockingConnection(parameters)
	# 		channel = connection.channel()
	# 		channel.basic_qos(prefetch_count=1)
	# 		for method_frame, properties, body in channel.consume('cocoajson'):
	# 			if body == "STOP":
	# 				break
	# 			filenames = [body]
	# 			channel.basic_ack(method_frame.delivery_tag)
	# 			callback(filenames, connection)
	# 		connection.close()
	# 	except:
	# 		pass

def callback(names, connection):
	for total_path in names:
		path = os.path.dirname(total_path)
		fileName = os.path.basename(total_path)
		print("Parsing %s/%s...\n" % (path, fileName))
		jsonName, jsonVersion, downloadName = doDownload(path, fileName)
		#print("%s\n" % framework)
		if(jsonName != None and jsonVersion != None and downloadName != None):
			print("Downloaded %s %s...\n" % (jsonName, jsonVersion))
			if(not archiveExtract("{0}/{1}/{2}/{3}".format(Output_Path, jsonName, jsonVersion, downloadName), downloadName, jsonName, jsonVersion)):
				shutil.rmtree("{0}/{1}/".format(Output_Path, jsonName))
				continue

			print("Extracted to %s\n" % ("{0}/{1}/{2}/Extract".format(Output_Path, jsonName, jsonVersion)))
			print("Searching for fat files...\n")
			Found = False
			for (path2, fileName2) in recursiveFind("{0}/{1}/{2}/Extract".format(Output_Path, jsonName, jsonVersion)):
				#if(fileName2.endswith(".a")):
				#	continue
				print("Checking {0}\n".format(path2 + "/{0}".format(fileName2)))
				out_folder = doExtract(path2 + "/{0}".format(fileName2), "{0}/{1}/{2}".format(Output_Path, jsonName, jsonVersion))
				if(out_folder != None):
					print("Finished {0} {1} {2}\n\n".format(jsonName, jsonVersion, out_folder))
					Found = True
					out = "{0}/{1}/{2}/{3}".format(Output_Path, jsonName, jsonVersion, out_folder)
					os.system("amqp-publish -r cocoapods -u amqp://foo:bar@rmq -b \"{0}\"".format(out))
			if(Found == False):
				shutil.rmtree("{0}/{1}/".format(Output_Path, jsonName))
			else:
				continue

def parseFolder(folderName):
	for fileName in os.listdir(folderName):
		if(os.path.isfile("{0}/{1}".format(folderName, fileName))):
			jsonName = fileName.split('-')[0]
			jsonVersion = fileName.split('-')[1].replace(".zip", "")

			if not os.path.isdir("{0}/{1}".format(Output_Path, jsonName)):
				os.mkdir("{0}/{1}".format(Output_Path, jsonName))

			if(os.path.isdir("{0}/{1}/{2}".format(Output_Path, jsonName, jsonVersion))):
				return False

			os.mkdir("{0}/{1}/{2}".format(Output_Path, jsonName, jsonVersion))

			if(not archiveExtract("{0}/{1}".format(folderName, fileName), fileName, jsonName, jsonVersion)):
				shutil.rmtree("{0}/{1}/".format(Output_Path, jsonName))
				continue

			print("Extracted to %s\n" % ("{0}/{1}/{2}/Extract".format(Output_Path, jsonName, jsonVersion)))
			print("Searching for fat files...\n")
			Found = False
			for (path2, fileName2) in recursiveFind("{0}/{1}/{2}/Extract".format(Output_Path, jsonName, jsonVersion)):
				#if(fileName2.endswith(".a")):
				#	continue
				print("Checking {0}\n".format(path2 + "/{0}".format(fileName2)))
				out_folder = doExtract(path2 + "/{0}".format(fileName2), "{0}/{1}/{2}".format(Output_Path, jsonName, jsonVersion))
				if(out_folder != None):
					print("Finished {0} {1} {2}\n\n".format(jsonName, jsonVersion, out_folder))
					Found = True
					out = "{0}/{1}/{2}/{3}".format(Output_Path, jsonName, jsonVersion, out_folder)
					os.system("amqp-publish -r cocoapods -u amqp://foo:bar@rmq -b \"{0}\"".format(out))
			if(Found == False):
				shutil.rmtree("{0}/{1}/".format(Output_Path, jsonName))
			else:
				continue

def archiveExtract(path, fileName, jsonName, jsonVersion):
	archive = None
	try:
		archive = tarfile.open(path)
	except:
		try:
			archive = zipfile.ZipFile(path)
		except:
			pass
	if(archive is not None):
		try:
			os.mkdir("{0}/{1}/{2}/Extract".format(Output_Path, jsonName, jsonVersion))
			archive.extractall("{0}/{1}/{2}/Extract".format(Output_Path, jsonName, jsonVersion))
			archive.close()
		except:
			return False
		return True
	else:
		return False

def doExtract(path, output):
	baseName = os.path.basename(path)
	baseName = os.path.splitext(baseName)[0]
	try:
		if(not fat_lipo.checkARMv7(path)):
			return None

		if(not os.path.isdir(output + "/" + baseName)):
			os.mkdir(output + "/" + baseName)
		else:
			return None

		if(not fat_lipo.extractARMv7(path, output + "/" + baseName + "/" + baseName + ".a")):
			return None

		ar = unix_ar.Archive(output + "/" + baseName + "/" + baseName + ".a")
		ar.read_all_headers()
		for f in ar.archived_files.keys():
			out_path = output + "/" + baseName + "/" + f
			with open(out_path.rstrip('\0'), 'wb') as wf: 
				wf.write(ar.archived_files[f].read())

		if(not Keep):
			shutil.rmtree("{0}/Extract/".format(output))
		for fileName in os.listdir(output + "/" + baseName):
			if(fileName.endswith('.o') == False and fileName.find("flat-armv7") < 0 and fileName.endswith("Extract") == False):
				os.remove("{0}/{1}/{2}".format(output, baseName, fileName))
	except:
		return None

	return baseName

def doDownload(path, fileName):
	try:
		pod = json.loads(open(path + "/{0}".format(fileName)).read())
		url = pod['source']
		jsonName = pod['name']
		jsonVersion = pod['version']
		url = url['http']
		urlpath = urlparse.urlsplit(url).path
		name = posixpath.basename(urlpath)

		if not os.path.isdir("{0}/{1}".format(Output_Path, jsonName)):
			os.mkdir("{0}/{1}".format(Output_Path, jsonName))

		if(os.path.isdir("{0}/{1}/{2}".format(Output_Path, jsonName, jsonVersion))):
			return (None, None, None)

		os.mkdir("{0}/{1}/{2}".format(Output_Path, jsonName, jsonVersion))

		request = requests.get(url, timeout=10, stream=True, verify=False)
		fileSize = int(request.headers.get('Content-Length', 0))
		fileSizeDynamic = fileSize
		downloadedBytes = 0
		with open("{0}/{1}/{2}/{3}".format(Output_Path, jsonName, jsonVersion, name), 'wb') as fh:
			for chunk in request.iter_content(1024*1024):
				fh.write(chunk)
				if(fileSizeDynamic - (1024*1024) > 0):
					fileSizeDynamic = fileSizeDynamic - (1024*1024)
					downloadedBytes = downloadedBytes + (1024*1024)
				else:
					downloadedBytes = downloadedBytes + fileSizeDynamic
			
				sys.stdout.write('\r')
				sys.stdout.write("Downloaded {0}/{1} bytes...".format(downloadedBytes, fileSize))
				sys.stdout.flush()
		print("\n")

		return (jsonName, jsonVersion, name)
	except:
		return (None, None, None)

	return (None, None, None)

def recursiveFind(path):
	execList = []
	for fileName in os.listdir(path):
		if(os.path.isfile(path + "/{0}".format(fileName))):
			execList.append((path, fileName))
		if(os.path.isdir(path + "/{0}".format(fileName))):
			output = recursiveFind(path + "/{0}".format(fileName))
			execList.extend(output)
	return execList


if __name__ == '__main__':
    main()
