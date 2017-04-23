from pprint import pprint
import csv
import time
import json
import urllib
import codecs
import io
response = urllib.urlopen('https://udacity.com/public-api/v0/courses')
json_response = json.loads(response.read())
e = open('data.csv', 'w')
csvwriter = csv.writer(e)
"""
for course in json_response['courses']:
    #cell = str(cell).replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", "")
    x = str().replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", "")
    y = str().replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", "")
    z = str().replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", "")
    a = str().replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", "")
    b = str().replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", "")
    x =  str(course['title'])
    y =  str(course['homepage'])
    z =  str(course['image'])
    a = str(course['short_summary'])
    b = str(course['summary'])
    lis = [x,y,z,a,b]
    csvwriter.writerow(lis)
e.close()
"""
for course in json_response['courses']:
    x =  course['title'].encode("utf8")
    y =  course['homepage'].encode("utf8")
    z =  course['image'].encode("utf8")
    a = course['short_summary'].encode("utf8")
    b = course['summary'].encode("utf8")
    lis = [x,y,z,a,b]
    #lis = u' '.join((x,y,z,a,b)).encode('utf-8').strip()
    #print lis
    csvwriter.writerow(lis)
e.close()
