import os
import sys
import json

def main():
	for (path, fileName) in recursiveFindJson(sys.argv[1]):
		os.system("amqp-publish -r cocoajson -u amqp://foo:bar@rmq -b \"{0}\"".format(path + "/" + fileName))


def recursiveFindJson(path):
	jsonList = []
	for fileName in os.listdir(path):
		if(fileName.endswith(".json") and os.path.isfile(path + "/{0}".format(fileName))):
			try:
				pod = json.loads(open(path + "/{0}".format(fileName)).read())
				url = pod['source']
				jsonName = pod['name']
				jsonVersion = pod['version']
				if('http' in url):
					jsonList.append((path, fileName))
			except:
				pass
		if(os.path.isdir(path + "/{0}".format(fileName))):
			output = recursiveFindJson(path + "/{0}".format(fileName))
			jsonList.extend(output)
	return jsonList

if __name__ == '__main__':
	main()