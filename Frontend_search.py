from bottle import route, run, get, post, request, static_file

@route('/')
def hello():
	Content='<br><br><br><h2 style="font-size: 300%; text-align: center;"><span style="background-color: #ffffff; color: #000000;">Fxxk Google, Ask Me</span></h2>'
	Content+='<form action="http://localhost:8080/secondpage" method="get">'
	Content+='<p style="text-align: center;"><strong><img src="http://buffalobrewersfestival.com/wp-content/uploads/2015/04/Craft-Beer.jpeg" alt="" width="405" height="253" /></strong></p>'
	Content+='<p style="text-align: center;"><strong>&nbsp;Type Your Search Here:</strong></p>'
	Content+='<p style="text-align: center;"><input name="keywords" type="text" style="width: 500px"/></p>'
	Content+='<p style="text-align: center;"><input type="submit" value="Submit" /></p>'
	Content+='</form>'
	Content+='<p>&nbsp;</p>'
        return Content

@route('/secondpage')
def sp():
    #Keywords=request.forms.get('keywords')
    Keywords=request.query_string
    Keywords=Keywords[9:]
    Keywords=Keywords.replace("+"," ")
    Keywords=Keywords.lower()
    words=Keywords.split()
    histogram={}
    for word in words:
        if word not in histogram:
            histogram[word]=1
        else:
            histogram[word]=histogram[word]+1
    Keywords="<h1 style='text-align:center'>Search for \""+Keywords+"\"</h1>"
    Keywords=Keywords+"<br>"
    Keywords=Keywords+"<table id='results' align='center'>"
    Keywords=Keywords+"<th sytle='text-align: center; font-size:200%'>Word Count</th>"
    
    for c in histogram:
        Keywords=Keywords+"<tr><td style='text-align: center'>"+c+" = "+str(histogram[c])+"</td></tr>"
    Keywords=Keywords+"</table><br><p style='text-align: left'><form action='http://localhost:8080' method='get'>"
    Keywords=Keywords+"<input type='submit' value='Back'>"
    Keywords=Keywords+"</form>"
    return Keywords

#@route('/static/<filename>')
#def server_static(filename):
#    return static_file(filename, root='static/')

#@route('/images/<filename:re:.*\.png>')
#def send_image(filename):
#    return static_file(filename, root='static/', mimetype='image/png')

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='/Users/shuxu/Desktop/csc326lab1/bottle-0.12.7/')


run(host='localhost',port=8080,debug=True)
