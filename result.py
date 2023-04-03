# Name - result.py
# Purpose - webpage that outputs the result of a search string 

import pymongo, cgi, os, gridfs, re, html
from pprint import pprint

#connecting to the database, getting the landings collection
client = pymongo.MongoClient("mongodb://root:student@localhost:27017")
db = client["meteorcsv"]
coll = db["landings"]
 
print( 'Content-Type: text/html;charset=utf-8\r\n\r\n' )

#created variables for limit and skip for different pages
collLimit = 20
collSkip = 20

print(html.header) #from html.py
print("<h2>Results: </h2>")
form = cgi.FieldStorage() #get data from url/form data

#get the value of page number in get request/url
pgNum = form.getvalue('pg')
pgNum = int(pgNum)

### REGEX
meteor_name = form.getvalue('meteor_name') #gets value of name from submitted form (GET)
regx = re.compile("^"+meteor_name, re.IGNORECASE) #uses regex module to create regex with variable, searches for substrings, ignores case
mydoc = coll.find(
  {'name':{'$regex':regx}}, #get name of regexed statement, returns name
  {'_id':0, 'id':1, 'name':1} #include ID not in print but to query on
).limit(collLimit).skip(collSkip * (pgNum - 1)) #limit query to 20

#instantiates variables from list of dictionary items
for x in mydoc:
  meteorID = x['id']
  meteorName = x['name']
  print(f"<a href='/cgi-bin/info.py?meteorID={meteorID}'>{meteorName}</a></br>")

#count number of documents based off of previous query 
#number determines if next button should appear or not
mydocCount = coll.count_documents(
  {'name':{'$regex':regx}}, 
  skip=(collSkip * (pgNum - 1)), 
  limit=collLimit
)

print('</br>')
#check if back or next need to appear
if pgNum > 1:
  print(f'<a href="/cgi-bin/result.py?meteor_name={meteor_name}&pg={pgNum - 1}">Back</a>')
if mydocCount == collLimit:
  print(f'<a href="/cgi-bin/result.py?meteor_name={meteor_name}&pg={pgNum + 1}">Next</a>')

print(html.footer)