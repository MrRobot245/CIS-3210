from flask import Flask, request, jsonify, make_response
import urllib2
import urllib
import json
import MySQLdb

app = Flask(__name__, static_url_path='')
tasks = {}



# Routes
@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/nyt/', methods=['GET'])
def get_task():
    apiKey="6462dcd33e1d47bc2be98167e19c86ab:10:72958436"
    keywords = request.args.get("data");
    db = MySQLdb.connect(host="dursley.socs.uoguelph.ca", # our host, do not modify
                         user="nreymer", # your username (same as in lab)
                         passwd="0797359", # your password (your student id number)
                         db="nreymer") # name of the data base, your username, do not modify

    cur = db.cursor()
    cur.execute("SELECT * FROM test5")
    query = ""
    jResult = ""
    for row in cur.fetchall() :
        if(keywords == row[1]):
            query = row[1]
            jResult = row[2]

    if query!=keywords:
        #print "NYT"
        response = urllib2.urlopen('http://api.nytimes.com/svc/search/v2/articlesearch.json?q='+keywords+'&limit=10&api-key='+apiKey)
        #print 'http://api.nytimes.com/svc/search/v2/articlesearch.json?q='+keywords+'&api-key='+apiKey
        data = json.load(response)
        response.close()
        query=json.dumps(data)
        insertThis=("INSERT INTO test5 "
                        "VALUES (NULL,%s,%s)")
        data=(keywords,query)
        cur.execute(insertThis,data)
        db.commit();
        return query,201
    else:
        #print "DB"
        n=json.dumps(jResult,ensure_ascii=False)
        t=json.loads(n)
        return t,201

    cur.close()
    db.close()

if __name__ == '__main__':
    app.run(debug=True)
