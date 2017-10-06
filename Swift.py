import os

swift = 0
no_swift = 0
admob = 0
total = 0
for folderName in os.listdir("certs"):
    path = s.path.join("certs", folderName, "analysis.txt")
    with open(path, "r") as file:
        for line in file:
            if(line.find("App uses swift!") != -1):
                swift = swift + 1
            if(line.find("App doesn't use swift!") != -1):
                no_swift = no_swift + 1
            if(line.find("Found AWS token:") != -1):
                print("%s: %s\n" % (folderName, line))
            if(line.find("admob") != -1):
                admob = admob + 1
    total = total + 1
print("%d apps use swift, %d apps don't use swift, %d apps use admob, %d apps total\n" % (swift, no_swift, admob, total))


