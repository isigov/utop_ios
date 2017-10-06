import os
import sys
import pika

for filename in os.listdir("/srv/data/ios/exes/idb"):
    if(filename.endswith('.idb') == True):
        os.system("/home/isigov/ida-6.8/idal -A -S/srv/data/ios/Crypt.py /srv/data/ios/exes/idb/{0}".format(sys.stdin.readlines()[0]))
