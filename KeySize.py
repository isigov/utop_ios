import os

for folderName in os.listdir("/srv/data/ios/cccrypt"):
    with open(os.path.join("cccrypt", folderName, "analysis.txt"), "r") as f:
        for line in f:
            line.replace("Found string in fcn using CCCrypt: ", "")
            bits = len(line) * 8
            if(bits == 128 or bits == 192 or bits == 256):
                print("Potential key/IV: %s in %s" % (line, folderName))
