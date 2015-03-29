import urllib2
import json
import jula

url = "https://dl.dropboxusercontent.com/u/1277351/api/jula.json"
data = urllib2.urlopen(url).read()
d = json.loads(data)

unit = d["unit"]
cmd = d["cmd"]

print data
print unit
print cmd

jula.send(unit, cmd)


