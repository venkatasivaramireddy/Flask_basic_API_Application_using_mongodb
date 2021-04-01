from flask import make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt
from flask_restful import Resource

from app import blacklist


class Logout(Resource):

    @jwt_required
    def __init__(self):
        super().__init__()
        self.email = get_jwt_identity()

    def delete(self):
        """
        This method is used to revoke Token/clear token if user access token is valid
        :return: dict
        """
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return make_response(jsonify({'message': "Successfully logged out", 'status_code': 200}), 200)
