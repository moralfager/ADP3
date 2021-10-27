from datetime import datetime, timedelta
from flask.helpers import make_response
from flask import request
from flask.json import jsonify
import jwt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Zhumakhan_Kuatbekov'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/flask_jwt_auth'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), nullable=True)
    token = db.Column(db.String(500))
    def __init__(self, login, password,token):
        self.login = login
        self.password = password
        self.token = token
# db.create_all()
@app.route('/login')
def login():
    auth = request.authorization
    if auth:
        login_auth = Users.query.filter_by(login=auth.username).first()

    if auth and auth.password == login_auth.password:
        token = jwt.encode({'user': auth.username, 'exp': datetime.utcnow() + timedelta(minutes=1)},
                           app.config['SECRET_KEY'])
        token_commit = Users.query.filter_by(login=auth.username).first()
        token_commit.token = token
        db.session.commit()

        return jsonify({'token': token})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm = "Login required'})


@app.route('/protected')
def protected():
    token = request.args.get('token')

    if not token:
        return "<h1>Hello, Token is missing! </h1>"
    arr = db.session.query(Users.token).all()
    for i in range(len(arr)):
        if arr[i][0] == token:
            return '<h1>Hello, token which is provided is correct </h1>'
    else:
        return "<h1>Hello, Could not verify the token </h1>"
    return 'nothin gonna work'

if __name__ == '__main__':
    app.run(debug=True)