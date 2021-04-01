from flask import request, make_response, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource
from werkzeug.security import check_password_hash

import config
from database.mongodb import mongo_connect


class Login(Resource):

    def __init__(self):
        super().__init__()
        self.globel_db = mongo_connect()
        self.client_db = self.globel_db[str("spiceblue_database")]
        self.collection = config.USER_COLLECTION

    def post(self):
        """
        body:
        {
            "email":" ",
            "password":" "
        }
        This method is used to get Token if user credentials is valid
        :return: dict
        """
        try:
            meta_data_dict = request.get_json()
            try:
                email = meta_data_dict['email']
                password = meta_data_dict['password']
            except Exception as e:
                return make_response(
                    jsonify({'message': "Missing {} Key".format(str(e)), 'status_code': 400}), 400)
            res = self.client_db.get_collection(self.collection).find_one({'email':email})

            if res is not None:
                hashed_password = res['password']
                if check_password_hash(hashed_password, password):
                    data = {
                        'access_token': create_access_token(identity=email),
                        'refresh_token': create_refresh_token(identity=email)
                    }
                    return make_response(jsonify({'result':data,'message': "Successfully Loged In", 'status_code': 200}), 200)
                else:
                    return make_response(jsonify({'message': 'Invalid Password', 'status_code': 401}), 401)
            else:
                return make_response(jsonify({'message': 'Invalid Email', 'status_code': 401}), 401)
        except Exception as e:
            return make_response(jsonify({'message': str(e), 'status_code': 400}), 400)
