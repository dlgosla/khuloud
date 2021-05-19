import jwt
import bcrypt
from flask import request
from flask_restx import Resource, Api, Namespace, fields
import requests


users = {}

Auth = Namespace(
    name="Auth",
    description="사용자 인증을 위한 API",
)

user_fields = Auth.model('User', {  # Model 객체 생성
    'name': fields.String(description='a User Name', required=True, example="id")
})

user_fields_auth = Auth.inherit('User Auth', user_fields, {
    'password': fields.String(description='Password', required=True, example="password")
})


jwt_fields = Auth.model('JWT', {
    'Authorization': fields.String(description='Authorization which you must inclued in header', required=True, example="eyJ0e~~~~~~~~~")
})

@Auth.route('/register')
class AuthRegister(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={500: 'Register Failed'})
    def post(self):
        
        id = request.form.get("id")
        password = request.form.get("password")
        re_password = request.form.get("re_password")
        check = request.form.get("check")

        if id in users:
            data = {'msg': "존재하는 id 입니다."}
            return data, 500
        
        elif id is "" or password is "" or re_password is "":
            data = {"msg": "입력되지 않은 항목이 있습니다."}
            return data, 500

        elif password != re_password:
            data = {"msg": "비밀번호가 일치하지 않습니다."}
            return data, 500

        elif check == None:
            data = {"msg":"약관에 동의해주세요."}
            return data, 500
        
        else:
            users[id] = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())  # 비밀번호 저장
            data ={
                'msg' : 'success',
                #'Authorization': jwt.encode({'name': id}, "secret", algorithm="HS256") #.decode("UTF-8")  # str으로 반환하여 return
            }
            return data, 200

@Auth.route('/login')
class AuthLogin(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={404: 'User Not Found'})
    @Auth.doc(responses={500: 'wrong password'})
    def post(self):
        name = request.form.get('id')
        password = request.form.get('password')

        if name not in users:
            return {
                "status" : "fail",
                "message": "존재하지 않는 id입니다."
            }, 500

        elif not bcrypt.checkpw(password.encode('utf-8'), users[name]):  # 비밀번호 일치 확인
            return {
                "status" : "fail",
                "message": "아이디와 비밀번호가 일치하지 않습니다."
            }, 500

        else:
            return {
                "status": "success"
                #'Authorization': jwt.encode({'name': name}, "secret", algorithm="HS256").decode("UTF-8") # str으로 반환하여 return
            }, 200

"""
@Auth.route('/get')
class AuthGet(Resource):
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={404: 'Login Failed'})
    def get(self):
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {"message": "Please Login"}, 404
        data = jwt.decode(header, "secret", algorithm="HS256")
        return data, 200
"""