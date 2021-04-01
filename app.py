import datetime
import os
from flask import Flask
# from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

from modules.templates.template_api import Template

app = Flask(__name__)
# CORS(app)
api = Api(app)

#jwt
jwt = JWTManager(app)
blacklist = set()


from modules.users.login import Login
from modules.users.logout import Logout
from modules.users.register import SignUp

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

#version & Env
APP_NAME = 'ENGAGE'
VERSION = "0.0.1.1"

ACTIVE_ENV = ''
ENV_VARIABLE = os.environ.get("ENV") or os.environ.get("FLASK_ENV")
if os.environ.get("FLASK_ENV") is not None or os.environ.get("FLASK_ENV") != '':
    ENV_VARIABLE = os.environ.get("FLASK_ENV")
else:
    ENV_VARIABLE = os.environ.get("ENV")

# jwt
app.config['JWT_SECRET_KEY'] = 'secretkey_unique'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=50)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(hours=5)
app.config['PROPAGATE_EXCEPTIONS'] = True

#session
# app.permanent_session_lifetime = datetime.timedelta(minutes=5)


#endpoints
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Template, '/template','/template/<template_id>')


if __name__ == '__main__':
    app.run(debug=False)
