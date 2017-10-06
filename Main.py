import os
from subprocess import check_output

for filename in os.listdir(os.getcwd()):
    if(filename.find(".bin") != -1):
        check_output("/home/isigov/ida-6.3/idaw -A -B -OIDAPython:/home/pizzaman/ios/exes/Test.py /srv/data/ios/exes/{0}".format(filename), shell=True)
#        check_output("cmd /C \"C:\Program Files (x86)\IDA 6.8\idaw.exe\" -A -B -SC:\Users\Administrator\Desktop\Test.py C:\Users\Administrator\Desktop\{0}".format(filename), shell=True)
