import os
from flask import Flask
from dashgourd.web_api import init_web_api, BasicAuth
from dashgourd.api.actions import ActionsApi

"""
Not sure if this is the best way to initialize the api. 
Will Flask keep the mongodb connection open continously? 
Or will mongodb automatically handle creating and closing 
connections?
"""
actions_api = ActionsApi(os.environ.get('MONGO_URI'), os.environ.get('MONGO_DB'))

auth = BasicAuth('user', 'secret')
web_api = init_web_api(actions_api, auth)

app = Flask(__name__)
app.port = int(os.environ.get('PORT', 5000))
app.debug = True if os.environ.get('APP_DEBUG', None) else False
app.register_blueprint(web_api)

if __name__ == '__main__':
    app.run(host='0.0.0.0')