import os


for filename in os.listdir("/srv/data/ios/exes/idb"):
    if(filename.endswith('.idb') == True):
        os.system("amqp-publish -r hash -u amqp://foo:bar@rmq -b \"{0}\"".format(filename))
