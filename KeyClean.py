import os

for folderName in os.listdir("/srv/data/ios/cccrypt"):
    with open(os.path.join("cccrypt", folderName, "analysis.txt"), "r") as f:
        for line in f:
            txt = line.replace("Found string in fcn using CCCrypt: ", "")
            print("Potential key/IV: %s in %s" % (txt, folderName))
