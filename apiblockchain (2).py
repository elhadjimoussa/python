import flask
from flask import redirect, url_for, request, jsonify, render_template
import sqlite3
import json
from hashlib import sha256
from datetime import datetime

from blockchain import  calculHash
 
# Creation  d'un Web App
 
app = flask.Flask(__name__, template_folder='./')
app.config["DEBUG"] = True

def calculHash(block):
    bloc = str(block.index) + str(block.previousHash) + str(block.timestamp) + str(block.data) + str(block.nonce)
    return(sha256(bloc.encode('utf-8')).hexdigest())


    def createBlock(self, difficulty):
        while self.hash[0:difficulty] != "0000":
            self.nonce = self.nonce + 1
            self.hash = calculHash(self)

#Creation d'un bloc
class Block(object):
    def __init__(self, index, previousHash, timestamp, data):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.data = data
        self.nonce = 0
        self.hash = calculHash(self)

    def createBlock(self, difficulty):
        while self.hash[0:difficulty] != "0000":
            self.nonce = self.nonce + 1
            self.hash = calculHash(self)
 
# Creation d'un Blockchain
 
class Blockchain(object):
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.blocks = []

bchain=Blockchain(4)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
 
 
 
@app.route('/', methods = ['POST','GET'])
 
def index():
    
    if request.method == 'POST':
        index = request.form.get('index')
        previousHash= request.form.get('previousHash')
        timestamp = request.form.get('timestamp')
        data = request.form.get('data')
        hash = request.form.get('hash')
        nonce = request.form.get('nonce')

        block = Block(index, previousHash, timestamp, data)
        block.createBlock(4)
        conn = sqlite3.connect('blockchainDB.db')

        sql = '''INSERT INTO bloc(`index`, previousHash, timestamp, data, hash,nonce)
                    VALUES(?,?,?,?,?,?) '''
        
        conn.execute(sql, (block.index,block.previousHash, block.timestamp,block.data,block.hash, block.nonce))
                    


        conn.commit()
        return redirect(url_for('index'))
    return render_template("index.html")
    
 

@app.route('/bloc/all', methods = ['GET'])
 
def all_bloc():

    results= calculHash

    return render_template("index.html", all_bloc=results)
 
@app.route('/bloc', methods=['POST'])

def add_bloc():
    conn = sqlite3.connect('blockchainDB.db')

    sql = '''INSERT INTO books(index, previousHash, timestamp, data, hash,nonce)
                VALUES(?,?,?,?,?) '''
    
    conn.execute(req, ("4", "12zjp1234sko", "124577", "dr","849ezqo", "346"))
                
    cur = conn.cursor()

    body = request.get_json()

    data = json.loads(json.dumps(body))
    blockchainDB = (data['index'], data['previousHash'], data['timestamp'], data['data'], data['hash'],data['nonce'])

    cur.execute(sql, blockchainDB)

    conn.commit()

    return render_template("index.html",object = all_bloc)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>Page non trouvée</p>", 404

@app.route('/bloc', methods=['GET'])
def api_filter():
    query_parameters = request.args

    index = query_parameters.get('index')
    previousHash= query_parameters.get('previousHash')
    timestamp = query_parameters.get('timestamp')
    data = query_parameters.get('data')
    hash = query_parameters.get('hash')
    nonce = query_parameters.get('nonce')


    query = "SELECT * FROM bloc WHERE"
    to_filter = []

    if index:
        query += ' index=? AND'
        to_filter.append(index)
    if previousHash:
        query += ' previousHash=? AND'
        to_filter.append(previousHash)
    if timestamp:
        query += ' timestamp=? AND'
        to_filter.append(timestamp)
    if data:
        query += ' data=? AND'
        to_filter.append(data)
    if hash:
        query += ' hash=? AND'
        to_filter.append(hash)
    if nonce:
        query += 'nonce =? AND'
        to_filter.append(nonce)
    if not (index or previousHash or  timestamp or data or hash or nonce):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('blockchainDB.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()
 
 
