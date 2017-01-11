import bottle

import httplib2

import urllib

import difflib

import sqlite3 as lite

from bottle import route, run, get, post, request, static_file

from collections import Counter

from oauth2client.client import OAuth2WebServerFlow

from oauth2client.client import flow_from_clientsecrets

from googleapiclient.errors import HttpError

from googleapiclient.discovery import build

#import beaker

from beaker.middleware import SessionMiddleware

#from beaker.middleware import SessionMiddleware





#export PYTHONPATH=/Library/Python/2.7/site-packages



CLIENT_ID = '978601881809-fcb3sk09s4avlmms5e2esrpogrqkesgu.apps.googleusercontent.com'

CLIENT_SECRET = 'PIuGfxVTgnRys0fuk26oiNMs'

SCOPE = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'

REDIRECT_URI = "http://ec2-52-6-43-123.compute-1.amazonaws.com/redirect"

#global history

history = {}

urllist = []

urllistid = []

suggestword = []

returnsuggestword = []

urllistidrank = []

finalurllist = []

grouplist = []

firstword = ""

#global checklogin

checklogin = False

trylogin = False

logoutsecond = False

secondlogoutkeywords = ""

user_email = ""

return_url = ""

Keywords = ""





session_opts = {

    'session.type': 'file',

    'session.cookie_expires': 300,

    'session.data_dir': './data',

    'session.auto': True

}

app = SessionMiddleware(bottle.app(), session_opts)







@route('/')

def hello():

    global return_url

    return_url = "http://ec2-52-6-43-123.compute-1.amazonaws.com/"

    #if session_opts.cookie_expires == False:

    #   checklogin = False

    if not checklogin:

        Content = "<form  style = 'text-align: right'action =http://ec2-52-6-43-123.compute-1.amazonaws.com/login> <input type = 'submit' value= 'Login'></form>"

        Content += "<form style = 'text-align: right' action =http://ec2-52-6-43-123.compute-1.amazonaws.com/logout> <input type = 'submit' value= 'Logout'></form>"

    else:

        Content = "<p style = 'text-align: right'>" + user_email + "</p>"

        Content += "<form style = 'text-align: right' action =http://ec2-52-6-43-123.compute-1.amazonaws.com/logout> <input type = 'submit' value= 'Logout'></form>"



    Content+="<br><br><br><p style='text-align: center;'><strong><img src='/static/name.png' alt='team_logo' width='405' height='100' /></strong></p>"

        #use get method request data from user

    Content+='<form action="http://ec2-52-6-43-123.compute-1.amazonaws.com/secondpage" method="get">'

    Content+="<p style='text-align: center;'><strong><img src='/static/logo.png' alt='team_logo' width='405' height='180' /></strong></p>"

    Content+='<p style="text-align: center;"><strong>&nbsp;Type Your Search Here:</strong></p>'

    Content+='<p style="text-align: center;"><input name="keywords" type="text" placeholder="Search.." style="width:70%; height:30px"/></p>'

    Content+='<p style="text-align: center;"><input type="submit" value="Submit" style="padding:10px 24px; border:2ox solid #e7e7e7; background-color: white;" /></p>'

    Content+='</form>'

    Content+='<p>&nbsp;</p>'

    return Content



@route('/secondpage')

def sp():

    global checklogin

    global user_email

    global return_url

    global Keywords

    global secondlogoutkeywords

    global logoutsecond

    global urllist,urllistid,urllistidrank,finalurllist,grouplist



    urllist[:] = []

    urllistid[:] = []

    urllistidrank[:] = []

    finalurllist[:] = []

    returnsuggestword[:] = []

    print "enter secondpage"



    return_url = "http://ec2-52-6-43-123.compute-1.amazonaws.com/secondpage"

    #Keywords get from user input

    sortlist = []



    if not logoutsecond:

        Keywords=request.query_string

        #print "Keyword1: ",Keywords

        if "updatelist" not in Keywords:

            secondlogoutkeywords = Keywords

    else:

        Keywords = secondlogoutkeywords

        #print "Keyword2: ",Keywords

        secondlogoutkeywords = False

    print "keyword3:",Keywords

    if "updatelist" in Keywords:

    	update = True

    	Keywords = Keywords[11:]

    	urlindex = int(Keywords)-1

        Keywords = secondlogoutkeywords[9:]

    else:

    	update = False

    	grouplist[:] = []

    	Keywords=Keywords[9:]



    #remove space

    Keywords=Keywords.lstrip('+')

    Keywords=Keywords.rstrip('+')

    

    words=Keywords.split("+")

    print "words: ",words, "keyword: ",Keywords

    firstword = words[0]

    #print firstword

    while '' in words:words.remove('')

    histogram={}

    printcheck={}

    Keywords=''

    Keywords=Keywords+"<h1 style='text-align:center'>Search for: \""

    for word in words:

        word=urllib.unquote(word).decode('utf-8')

        Keywords=Keywords+word+" "

        word=word.lower()

        #if current word does not in histogram dictionary, add into histogram dictionary and set value to be 1

        if (word not in histogram):

            histogram[word]=1

        #if current word exist in histogram dictionary, increment the the histogram[word] value by 1

        else:

            histogram[word]=histogram[word]+1



    if Keywords != "<h1 style='text-align:center'>Search for: \"":

        Keywords=Keywords[:-1]

    Keywords=Keywords+"\"</h1>"

    if checklogin:

        Keywords += "<p style = 'text-align: right'>" + user_email + "</p>"

    Keywords += "<form style = 'text-align: right;' action =http://ec2-52-6-43-123.compute-1.amazonaws.com/logout> <input type = 'submit' value= 'Logout'></form>"

    Keywords=Keywords+"<br>"

    Keywords=Keywords+"<table id='results' align='center'>"

    Keywords=Keywords+"<th sytle='text-align: center; font-size:200%'>Word</th><th sytle='text-align: center; font-size:200%'>Count</th>"

    

    #following loop make sure key words print in the order of user input

    for word in words:

        word=word.lower()

        if word not in printcheck:

            printcheck[word.lower()]=1

            tempword=urllib.unquote(word).decode('utf-8')

            tempword=tempword.lower()

            # add the result of histogram dictionary to html tag

            Keywords=Keywords+"<tr><td style='text-align: center'>"+tempword+"</td><td style='text-align: center'>"+str(histogram[tempword])+"</td></tr>"

    if checklogin:

        Keywords=Keywords+"</table>"

        Keywords=Keywords+"<p style='text-align:center; font-size:200%'><b>History Top 20 words: </b></p>"

        Keywords=Keywords+"<br>"

        Keywords=Keywords+"<table id='results' align='center'>"

        Keywords=Keywords+"<th sytle='text-align: center; font-size:200%'>Word</th><th sytle='text-align: center; font-size:200%'>Count</th>"



        #build a new dictionary store all history keyword

        for i,j in histogram.iteritems():

            if(i not in history):

                history[i] = j

            else:

                history[i] += histogram[i]

      #sort the history dictionary by its value from the highest to the lowest. Sort the sort history key to sortlist.

        for k, v in sorted(history.iteritems(), key=lambda x:x[::-1], reverse=True):

            sortlist.append(k) 

            print k, v



     #if total history keyword less than 20. Set the keylen to be the total number of history words

        if len(sortlist) <= 20:

            keylen = len(sortlist)

        else:

            keylen = 20



        for i in range(keylen):

            #put all history keyword into htaml tag

            Keywords=Keywords+"<tr><td style='text-align: center'>"+sortlist[i]+"</td><td style='text-align: center'>"+str(history[sortlist[i]])+"</td></tr>"



    Keywords=Keywords+"</table><br><p style='text-align: left'><form action='http://ec2-52-6-43-123.compute-1.amazonaws.com' method='get'>"

    Keywords=Keywords+"<input type='submit' value='Back'>"

    Keywords=Keywords+"</form>"

    

    #for lab3 add result query page in the result page

    Keywords+='<form action="http://ec2-52-6-43-123.compute-1.amazonaws.com/secondpage" method="get">'

    Keywords+='<p style="text-align: center;"><strong>&nbsp;Type Your Query Here:</strong></p>'

    Keywords+='<p style="text-align: center;"><input name="keywords" type="text" placeholder="Search.." style="width:70%; height:30px"/></p>'

    Keywords+='<p style="text-align: center;"><input type="submit" value="Submit" style="padding:10px 24px; border:2ox solid #e7e7e7; background-color: white;" /></p>'

    Keywords+='</form>'

    

    if not update:

    	con = lite.connect("dbFile.db")

    	cur = con.cursor()



        querystring = "select word from resolvedInvertedIndex "

        cur.execute(querystring)

        for row in cur:

            #print "row: ",row

            if row[0] not in suggestword:

                suggestword.append(str(row[0]))

        #print "suggestword: ",suggestword,"suggestword length:",len(suggestword)



        for word in words:

            print "returnsuggestwork: ",difflib.get_close_matches(word, suggestword,n=1,cutoff=0.8)

            returnsuggestword.append(difflib.get_close_matches(word, suggestword,n=1,cutoff=0.8))



        for firstword in words:

            querystring = "select doc from resolvedInvertedIndex where word=" + "\'"+firstword+"\'"

            #print "querystring:",querystring

            cur.execute(querystring)

            for row in cur:

                #print "row: ",row,"row type:",type(row),"row[0]:",row[0]

                urllist.append(row[0])

            #print "urllist:",urllist



        print "urllist: ",urllist

        for url in urllist:

            querystring = "select rank from pageRankResult where docid=" + "\'"+str(url)+"\'"

            cur.execute(querystring)

            for row in cur:

                urllistidrank.append(row[0])

        print "urllistidrank",urllistidrank

   #      for url in urllist:

   #          urlliststring = "select id from documentIndex where url=" + "\'"+url+"\'"

   #          cur.execute(urlliststring)

   #          for row in cur:

   #              print "row in urllist:",row,"urllistid:",urllistid

   #              if row[0] not in urllistid:

   #                  urllistid.append(row[0])

   #      print "length of urllistid: ",len(urllistid)

   #      print "urllistid: ",urllistid



   #  	#get page rank for each url

   #  	for pagerank in urllistid:

			# #print "pagerank",pagerank

			# pagerankstring = "select rank from pageRankResult where docid=" + "\'"+str(pagerank)+"\'"

			# cur.execute(pagerankstring)

			# for row2 in cur:

			# 	urllistidrank.append(row2[0])



    	finalurllist = zip(urllistidrank,urllist)



    	con.close()

    	finalurllist.sort(reverse=True)



    	#if not finalurllist:

        	#bottle.redirect("http://ec2-52-6-43-123.compute-1.amazonaws.com/ErrorPage")



    temp = []

    count_element = 0

    i = 0

    while i<len(finalurllist):

        if count_element < 5:

            temp.append(finalurllist[i][1])

            count_element += 1

        else:

            #print "temp: ",temp

            grouplist.append(temp[:])

            temp[:] = []

            temp.append(finalurllist[i][1])

            count_element = 1

        i +=1

    if temp:

    	grouplist.append(temp[:])

    Num_bot = len(grouplist)

    print "grouplist: ",grouplist,"grouplist length: ",Num_bot



    if not update:

    	urlindex = 0

    i = 0

    

    Keywords += "<p style='text-align:center; font-size:200%'><b>Do you mean to search: "

    for word in returnsuggestword:

        print "type of word",type(word),"word",word

        Keywords += word[0]+" "

    Keywords+="</b></p><br>"

    Keywords += "<p style='text-align:center; font-size:200%'><b>Top Url List: </b></p>"

    Keywords +="<br>"

    Keywords +="<table id='results' align='center'>"

    while i < len(grouplist[urlindex]):

    	print "grouplist[url]: ",grouplist[urlindex][i]

    	Keywords += "<tr><td style='text-align: center'>"+"<a href="+"\'"+grouplist[urlindex][i]+"\'>"+grouplist[urlindex][i]+"</td>"+"</tr>"

    	i += 1

    Keywords +="</table>"





    i = 0

    Keywords += "<form action='http://ec2-52-6-43-123.compute-1.amazonaws.com/secondpage' method='get'><p style='text-align:center'>"

    while i < Num_bot:

        Keywords += "<input type='submit' name='updatelist' value=" + str(i+1) +">"

        i += 1

    Keywords += "</form>"

    return Keywords

    '''

@route('/querypage')

def querypage():

	Querykeywords=request.query_string

	Querykeywords=Querykeywords[14:]

	Querykeywords = Querykeywords.split('+')

	QueryWords = Querykeywords[0]

	print Querykeywords,QueryWords

	'''

@route('/ErrorPage')

def ErrorPage():

	#global logoutsecond

	#logoutsecond = True

	#Keywords = ''

	ErrorContent = "<h1 style='text-align:center'>Access Page does not existed</h1>"

	ErrorContent += "<form action='http://ec2-52-6-43-123.compute-1.amazonaws.com/'><input type='submit' value='Go to home page'></form>"

	#ErrorContent += '''<form><input type = "button" value = "Back" onClick = "bottle.redirect('http://ec2-52-6-43-123.compute-1.amazonaws.com/secondpage')"></from>'''

	#ErrorContent += "</table><br><p style='text-align: left'><form action='http://ec2-52-6-43-123.compute-1.amazonaws.com/secondpage' method='get'>"

	#ErrorContent += "<input type='submit' value='Back'>"

	#ErrorContent += "</form>"

	return ErrorContent



@route('/login','GET')

def home():

    global trylogin 

    trylogin = True

    flow = flow_from_clientsecrets("./client_secrets.json",scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',redirect_uri="http://ec2-52-6-43-123.compute-1.amazonaws.com/redirect")

    uri = flow.step1_get_authorize_url()

    bottle.redirect(str(uri))



@route('/redirect')

def redirect_page():

    global checklogin

    global trylogin

    global user_email

    if not checklogin and trylogin:

        code = request.query.get('code', '')

        flow = OAuth2WebServerFlow( client_id=CLIENT_ID,client_secret=CLIENT_SECRET,scope=SCOPE,redirect_uri=REDIRECT_URI)

        credentials = flow.step2_exchange(code)

        token = credentials.id_token['sub']

        http = httplib2.Http()

        http = credentials.authorize(http)

        # Get user email

        users_service = build('oauth2', 'v2', http=http)

        user_document = users_service.userinfo().get().execute()

        user_email = user_document['email']



        print "code: ",code

        trylogin = False

        checklogin = True

    bottle.redirect(return_url) 



@route('/logout')

def redirect_page():

    global checklogin

    global logoutsecond

    checklogin = False

    if return_url == "http://ec2-52-6-43-123.compute-1.amazonaws.com/secondpage":

        logoutsecond = True

    bottle.redirect(return_url) 



@route('/static/<filename:path>')

def send_static(filename):

    return static_file(filename, root='static/') 





#run(host='localhost',port=8080,debug=True)

run(host='0.0.0.0',port=80,debug=True)

#run(app=app)



# <script>

# $( "select" )

#   .change(function () {

#     var str = "";

#     $( "select option:selected" ).each(function() {

#       str += $( this ).text() + " ";

#     });

#     $( "div" ).text( str );

#   })

#   .change();

# </script>
