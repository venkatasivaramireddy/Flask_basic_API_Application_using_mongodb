from flask import make_response, jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
import config
from database.mongodb import mongo_connect
from bson import ObjectId


class Template(Resource):

    @jwt_required
    def __init__(self):
        super().__init__()
        self.globel_db = mongo_connect()
        self.client_db = self.globel_db[str("spiceblue_database")]
        self.collection = config.TEMPLATE_COLLECTION
        self.mandatory_keys = ['template_name','subject','body']
        self.missing_keys = []
        self.final_dict = []

    def get(self,template_id=''):

        try:
            if template_id == '':
                response_data = self.client_db.get_collection(self.collection).find()
            else:
                response_data = self.client_db.get_collection(self.collection).find_one({"_id":ObjectId(template_id)})
                if response_data is not None:
                    if '_id' in response_data:
                        response_data['_id'] = str(response_data['_id'])
                    return make_response(jsonify({'result': response_data, 'status_code': 200}), 200)
                else:
                    return make_response(jsonify({'result': "No Match Content Found...", 'status_code': 400}), 400)

            if response_data.count() > 0:
                for x in response_data:
                    if '_id' in x:
                        x['_id'] = str(x['_id'])
                    self.final_dict.append(x)
            else:
                self.final_dict = []

            return make_response(jsonify({'result': self.final_dict, 'status_code': 200}), 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e), 'status_code': 400}), 400)


    def post(self):
        """
        {
        'template_name': ' ',
        'subject': ' ',
        'body': ' ',
        }
        :return: dict
        """
        try:
            meta_data_dict = request.get_json()

            for x in self.mandatory_keys:
                if x not in meta_data_dict.keys():
                    self.missing_keys.append(x)

            if len(self.missing_keys) > 0:
                return make_response(
                    jsonify({'message': "Missing {} Key".format(self.missing_keys), 'status_code': 400}), 400)

            self.client_db.get_collection(self.collection).insert(meta_data_dict)
            return make_response(
                jsonify({'message': "Successfully Register, Login Using Email & Password", 'status_code': 201}))
        except Exception as e:
            return make_response(jsonify({'message': str(e), 'status_code': 400}), 400)

    def put(self,template_id):
        meta_data_dict = request.get_json()
        response_data = self.client_db.get_collection(self.collection).find_one({"_id": ObjectId(template_id)})

        if response_data is not None:
            for key, value in meta_data_dict.items():
                if key in response_data:
                    response_data[key] = value
        else:
            return make_response(jsonify({'result': "No Match Content Found..", 'status_code': 400}), 400)

        res = self.client_db.get_collection(self.collection).update_one(
            {'_id': response_data['_id']},
            {'$set': response_data}
        )

        if res.modified_count is 1 or res.matched_count is 1:
            if '_id' in response_data:
                response_data['_id'] = str(response_data['_id'])

            return make_response(jsonify({'result': response_data, 'status_code': 200}), 200)
        else:
            return make_response(jsonify({'result': "Error While Updating Document", 'status_code': 400}), 400)

    def delete(self,template_id):
        response_data = self.client_db.get_collection(self.collection).find_one({"_id": ObjectId(template_id)})
        if response_data is None:
            return make_response(jsonify({'result': "No Match Content Found..", 'status_code': 400}), 400)
        response= self.client_db.get_collection(self.collection).remove({"_id": ObjectId(template_id)})
        return make_response(jsonify({'result': "Document Removed Successfully", 'status_code': 200}), 200)

