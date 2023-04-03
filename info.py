# Name - info.py
# Purpose - webpage that shows user info of selected meteor 

import pymongo, cgi, os, gridfs, re, html
from pprint import pprint

client = pymongo.MongoClient("mongodb://root:student@localhost:27017")
db = client["meteorcsv"]
coll = db["landings"]

print( 'Content-Type: text/html;charset=utf-8\r\n\r\n' )
 
print(html.header)
print("<h2>Info: </h2>")
form = cgi.FieldStorage()

#Gets ID of meteor from GET request
formMeteorID = form.getvalue('meteorID')
meteorID = int(formMeteorID) #parsing form value
author = form.getvalue('author')
comment = form.getvalue('comment')

mydoc = coll.find_one( #mydoc returns a dictionary variable
  {"id":meteorID},
  {"_id":0, "name":1, "mass (g)":1, "year":1} #can be changed to view desired info
)

#instantiates variables from returned dictionary
meteorName = mydoc['name']
meteorMass = mydoc['mass (g)']
meteorYear = mydoc['year']
print(f"<p'>Name: {meteorName}<p/>")
print(f"<p'>Mass: {meteorMass}(g)<p/>")
print(f"<p'>Year: {meteorYear}<p/>")

#ERROR CHECKING FOR COMMENTS
if(author != None and comment != None): #checks if Nothing is submitted
  if (author.isspace() == False and comment.isspace() == False):
    print(f"<h2>Submitted!</h2>")
  else:
    print("ERROR: Nothing Submitted")

#changed form to use meteorID to send data
print(f'''<form action="/cgi-bin/info.py" method="get">
        <input type="hidden" name="meteorID" value="{meteorID}">
        Write a comment: </br>
        Author: <input type="text" name="author" required/><br/>
        Comment: <input type="text" name="comment" required/><br/>
        <input type="submit" value="Submit"/>
      </form>''')


print(html.footer)