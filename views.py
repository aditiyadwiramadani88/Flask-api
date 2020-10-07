from Rest import app
from flask_restful import(
Resource,Api,fields,
marshal_with,reqparse, abort
)
from flask_jwt_extended import (
jwt_required,
create_access_token,
get_jwt_identity,
get_jwt_claims, create_refresh_token, 
jwt_refresh_token_required, get_raw_jwt
)
from . Jwt import *
from . models import *
from flask import make_response
from werkzeug.security import check_password_hash
api = Api(app)
def validator(value):
    if len(value) <= 3:
        raise ValueError('min 4 char')
    return value
parser1 = reqparse.RequestParser()
parser1.add_argument('username', type=validator, required=1)
parser1.add_argument('password', required=1)
class CreateUser(Resource):
       decorators = [jwt_required]
       def post(self): 
         argv = parser1.parse_args()
         user = UserManajement(**argv)
         db.session.add(user)
         db.session.commit()
         return argv

class CReateToken(Resource):
    decorators = [limiter.limit('3/day')]
    def post(self):
        argv = parser1.parse_args()
        password = argv['password']
        username = argv['username']
        user = UserManajement.query.filter_by(username=username).first()
        if not user:
            return {"msg": 'user not fout'}
        if check_password_hash(user.password, password):
            if user.role_id == 1:
                token = create_access_token(identity=username)
                resfresh_token = create_refresh_token(identity=username)
            return {'token': token, 'resfresh_token': resfresh_token}
        return {'msg': 'wrong password'}
parser = reqparse.RequestParser()
parser.add_argument('title', type=validator)
parser.add_argument('content_text', type=validator)
class List(Resource):
    decorators = [jwt_required]
    def get(self):
        query =Article.query.all()
        return AricleSeriallizer(many=1).dump(query)
    def post(self):
        argv = dict(parser.parse_args())
        add_data  = Article(**argv)
        db.session.add(add_data)
        db.session.commit()
        return argv
    def delete(self):
         jti = get_raw_jwt()['jti']
         blacklist.add(jti)
         return {'message': 'Success Logout'}

class Details(Resource):
    decorators = [jwt_required]
    def get_data(self, id):
        row = Article.query.filter_by(id=id)
        if not row.first():
            return None
        return row
    def get(self, id):
        query= self.get_data(id)
        if not query:
            return {'msg': 'id not fout'},401
        return AricleSeriallizer().dump(query.first())
    def put(self, id):
        argv = parser.parse_args()
        a = self.get_data(id) 
        if not a:
            return {'msg': 'id not fout'},401
        a.update(dict(argv))
        db.session.commit()
        return argv
    def delete(self, id):
        a = self.get_data(id)
        if not a:
            return {'msg': 'id not fout'},401
        a.delete()
        db.session.commit()
        return {'msg': 'succces delete data'}
class Resfresh_token(Resource):
    decorators = [jwt_refresh_token_required]
    def get(self):   
      new_token = get_jwt_identity()
      access_token = create_access_token(identity=new_token, fresh=False)
      return {'new_token': access_token}
    def delete(self):
         jti = get_raw_jwt()['jti']
         blacklist.add(jti)
         return {'message': 'Success Logout'}

class ReaBLog(Resource):
    decorators = [jwt_required]
    def get(self, slug=None):
        if not slug:
            row = Article.query.all()
            return AricleSeriallizer(many=1).dump(row)
        row = Article.query.filter_by(slug=slug).first()
        if not row:
            return {'msg': 'slug not fout'},401
        return AricleSeriallizer().dump(row)

class LoginUser(Resource):
    decorators = [jwt_required]
    def post(self):
        argv = parser1.parse_args()
        username = argv['username']
        password = argv['password']
        row =UserManajement.query.filter_by(username=username).first()
        if not row:
            return {'msg': 'wrong username'},401
        if check_password_hash(row.password, password):
            return UserSerial().dump(row)

api.add_resource(List, '/')
api.add_resource(Details, '/<int:id>')
api.add_resource(CReateToken, '/token')
api.add_resource(CreateUser, '/register')
api.add_resource(Resfresh_token, '/resfresh_token')
api.add_resource(ReaBLog, '/article/<slug>')
api.add_resource(ReaBLog, '/article', endpoint='jjh'),
api.add_resource(LoginUser, '/login')


