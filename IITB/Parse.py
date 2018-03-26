import json
import urllib2

fl = '/home/rupesh20/ProjectFinal/IITB/conv.txt'
ID = 'optimistic'
url = 'https://glosbe.com/gapi/translate?from=eng&dest=hin&format=json&phrase={}&pretty=true'.format(ID)
txt = open(fl,'w')
response = urllib2.urlopen(url)
data = json.loads(response.read())
print data 
x=data['tuc'][0]['phrase']['text']
print x
x=x.encode("utf-8")
print x
x_translate = json.dumps(x,ensure_ascii=False)

print x_translate
txt.write(x)
