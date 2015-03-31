import urllib2
import json
import jula

url = "http://192.168.0.12/command"
data = urllib2.urlopen(url).read()
d = json.loads(data)

unit = d["unit"]
cmd = d["cmd"]

print data
print unit
print cmd

jula.send(unit, cmd)


