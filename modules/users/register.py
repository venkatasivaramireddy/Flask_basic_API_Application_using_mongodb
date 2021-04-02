import re
import uuid

from flask import request, make_response, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash
import config
from database.mongodb import mongo_connect


class SignUp(Resource):
    def __init__(self):
        self.mandatory_keys = ['last_name','first_name','email','password']
        self.invalid_keys = []
        self.missing_keys = []
        self.globel_db = mongo_connect()
        self.client_db = self.globel_db[str("spiceblue_database")]
        self.collection = config.USER_COLLECTION

    def post(self):
        """
        body:
        {
                first_name : 'lead_test@subi.com',
                last_name : '123456'
                email : 'lead_test@subi.com',
                password : '123456',
                mobile:"",
        }

        This method is used to register the user into db
        :return: dict
        """
        try:
            meta_data_dict = request.get_json()
            for keys in meta_data_dict.keys():
                if keys not in self.mandatory_keys:
                    self.invalid_keys.append(keys)

            if len(self.invalid_keys) > 0:
                return make_response(
                    jsonify({'message': "{} Is In_Valid Key".format(self.invalid_keys), 'status_code': 400}), 400)

            for x in self.mandatory_keys:
                if x not in meta_data_dict.keys():
                    self.missing_keys.append(x)

            if len(self.missing_keys) >0:
                return make_response(
                    jsonify({'message': "Missing {} Key".format(self.missing_keys), 'status_code': 400}), 400)


            try:
                first_name = meta_data_dict['first_name']
                last_name = meta_data_dict['last_name']
                email = meta_data_dict['email']
                password = meta_data_dict['password']
                mobile = meta_data_dict.get('mobile', None)

            except Exception as e:
                return make_response(
                    jsonify({'message': "Missing {} Key".format(str(e)), 'status_code': 400}), 400)

            email_status = self.validate_email(address=email)
            if 'ErrorMessage' in email_status:
                return make_response(jsonify({'message': email_status['ErrorMessage'], 'status_code': 400}), 400)

            dict ={"guid":uuid.uuid4().hex,"first_name" :first_name,
                   "last_name" :last_name,"email": email ,
                   "password" :password ,"mobile" :mobile}
            email_id = self.client_db.get_collection(self.collection).find_one({'email':email})
            if email_id is None:
                # first_name = self.validate_user_name(address=first_name)
                # if 'ErrorMessage' in first_name:
                #     return make_response(jsonify({'message': first_name['ErrorMessage'], 'status_code': 400}), 400)
                # if mobile is not None:
                #     mobile_status = self.validate_mobile_number(address=mobile)
                #     if 'ErrorMessage' in mobile_status:
                #         return make_response(jsonify({'message': mobile_status['ErrorMessage'], 'status_code': 400}), 400)
                # password_status = self.validate_password(password=password)
                # if 'ErrorMessage' in password_status:
                #     return make_response(jsonify({'message': password_status['ErrorMessage'], 'status_code': 400}), 400)

                hash_password = generate_password_hash(password)
                dict['password'] = hash_password

                self.client_db.get_collection(self.collection).insert(dict)
                return make_response(jsonify({'message': "Successfully Register, Login Using Email & Password", 'status_code': 201}), 201)
            else:
                return make_response(jsonify({'message': "Email Already Exist", 'status_code': 400}), 400)
        except Exception as e:
            try:
                error = e.args[0]
            except:
                error = "Data Insertion Error"
            return make_response(jsonify({'message': str(error), 'status_code': 400}), 400)

    def validate_email(self,address):
        if re.search('@', address) is None:
            return {"ErrorMessage": "Email Should have @ -> Ex: a@b.c"}
        if re.search('.', address) is None:
            return {"ErrorMessage": "Email Should have . -> Ex: a@b.c"}
        return {}

    def validate_user_name(self,address):
        length = len(address)
        if length >8:
            return {"ErrorMessage": "Username max length should be 8"}
        return {}

    def validate_mobile_number(self,**kwrg):
        number = kwrg.get('address')
        if re.match('^[6-9]\d{9}$',number) is None:
            return {"ErrorMessage": "Phone Number must be a valid Indian Cell phone number -> Ex. 9876543210"}
        return {}

    def validate_password(self, password):
        if re.match('^(?=.*?[A-Za-z])(?=.*?[0-9])(?=.*?[#_-]).{6,}$', password) is None:
            return {"ErrorMessage": "Password must contain at least one character, one number "
                               "and any one of these (underscore, hyphen, hash) and max length should be 6"}
        return {}
