from flask import Flask
from actions import bp as actionsbp
app = Flask(__name__) 

app.secret_key = 'SECERT_KEY' 

app.register_blueprint(actionsbp)