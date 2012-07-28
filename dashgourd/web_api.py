import os
from functools import wraps
from flask import Blueprint, request, abort, Response, jsonify

def init_web_api(actions_api, auth=None):
    """Wrapper for DashGourd web api blueprint
    
    The wrapper allows the authentication mechanism
    to be changed by passing in an auth object with the
    decorator method "requires_auth".
    
    Args:
        actions_api: Instance of DashGourd actions api
        auth: Class that implements "requires_auth" decorator
    
    Returns
        blueprint: Web api blueprint to use in Flask
        
    TODO(richard-to): Add chart api endpoints
    """
    
    if auth is None:
        auth = NoAuth()
        
    web_api = Blueprint('dashgourd_web_api', __name__)    

    @web_api.route('/users', methods=['POST'])
    @auth.requires_auth
    def api_create_users():
        json = request.json
        if(json is not None  and 'data' in json):
            actions_api.create_user(json['data'])
        return ''
    @web_api.route('/users/<int:user_id>/actions', methods=['POST'])
    @auth.requires_auth
    def api_create_users_actions(user_id):
        json = request.json
        if(json is not None  and 'data' in json):
            actions_api.insert_action(user_id, json['data'])
        return ''     
    
    @web_api.route('/users/<int:user_id>/abtests', methods=['POST'])
    @auth.requires_auth
    def api_create_users_abtests(user_id):
        json = request.json
        if(json is not None  and 'data' in json):
            actions_api.tag_abtest(user_id, json['data'])
        return ''
    
    return web_api


class NoAuth(object):
    """Default auth decorator for DashGourd web api blueprint.
    
    Workaround for changing decorator functionality dynamically.
    There are probably better ways to do this.
    """
    
    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated
    
class BasicAuth(object):
    """Basic auth decorator for DashGourd web api blueprint.
    
    Modified version of the basic auth snippet found here: 
    http://flask.pocoo.org/snippets/8/
    
    Need to wrap in a class to provide flexibility in setting 
    auth decorator for web api.
    
    Attributes:
        username: username for basic auth
        password: password for basic auth
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def check_auth(self, username, password):
        return username == self.username and password == self.password
    
    def authenticate(self):
        return Response(
        'Could not verify your access level for that URL.\n'
        'You have to log in with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not self.check_auth(auth.username, auth.password):
                return self.authenticate()
            return f(*args, **kwargs)
        return decorated 