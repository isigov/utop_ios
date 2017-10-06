import os
import sys
import shutil

config = [ 'com.apple.itunesstored', 'ConfigurationProfiles', 'Cookies', 'Passes', 'Preferences', 'TCC' ]

folderName = sys.argv[1]

for folders in os.listdir("/private/var/mobile/apple_ids"):
    if(folders == folderName):
        for c in config:
            shutil.rmtree('/private/var/mobile/Library/' + c)
            shutil.copytree('/private/var/mobile/apple_ids/' + folderName + '/' + c, '/private/var/mobile/Library/' + c)
        os.system("chmod -R 777 /private/var/mobile/Library/")
        os.system("reboot")
