from Rest import app
from flask_jwt_extended import JWTManager
app.config['JWT_SECRET_KEY'] = b'\xe9\xc1\x96\xb6\xe1\xd6\xbe\xd3>{;\xe2S\x05,\xb6E\xdf\xc2\x01!G\x9c\xc4\xc5\x0f\x1c\xf8oS'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr



jwt = JWTManager(app)
blacklist = set()
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
            jsonify(error="ratelimit exceeded {}".format(e.description))
            , 429
    )