
import json

datafile = "data1.json"

fp = open(datafile, "r")
data_s = fp.read()
fp.close()

data = json.loads(data_s)
keys = data.keys()

for i in range(len(keys)):
    print("Key: %d %s" % (i, keys[i]))

for key in keys:
    print("Key: %s" % key)
