from flask import Flask, request, jsonify, make_response, has_request_context
from flask_sqlalchemy import SQLAlchemy
import uuid
from itertools import permutations, product, chain, zip_longest
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from itertools import permutations, product, chain, zip_longest
from   fractions  import Fraction as F
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, ForeignKey
from flask_request_id_header.middleware import RequestID
from flask_login import current_user,login_manager,LoginManager,UserMixin
##########################################################


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'thisissecret'                           #
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/Game'

db = SQLAlchemy(app)


#
login_manager =LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)


class numbers(db.Model):

    numbers_id = db.Column(db.Integer, primary_key=True,autoincrement =True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    first = db.Column(db.Integer,nullable=False)
    second = db.Column(db.Integer,nullable=False)
    third = db.Column(db.Integer,nullable= False)
    fourth = db.Column(db.Integer,nullable= False)
    users = db.relationship('User')
    def __init__(self,user_id,first, second, third, fourth):
        self.user_id = user_id
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth

class Solve(db.Model):

    solve_id = db.Column(db.Integer,primary_key= True,autoincrement =True)
    solve = db.Column(db.Text,nullable=True)
    num_id = db.Column(db.Integer, db.ForeignKey('numbers.numbers_id'),nullable=False)
    nums = db.relationship('numbers')


db.create_all()
db.session.commit()

@app.route('/user', methods=['GET'])
def get_all_users():
    output = []
    users = User.query.all()
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})


@app.route('/user', methods=['POST'])

def create_user():


    data = request.get_json()
    print(data)
    hashed_password = generate_password_hash(data['password'], method='sha256')
    print(hashed_password)
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})


@app.route('/user/<public_id>', methods=['DELETE'])

def delete_user(public_id):



    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})

@app.route('/login')
def login():
    auth = request.authorization
    print(request.authorization.username)
    if not auth or not auth.username or not auth.password:
        return make_response('111111 couldnt verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()
    print(user)
    print(user.id)
    if not user:
        return make_response('22222 couldnt verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        print(token)
        return jsonify({'token' : token})

    return make_response('33333333 couldnt verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


###############################################################################
####SOLUTION######
##########################
@app.route('/test',methods = ['GET'])
def test():
    return {'test':'test1'}

######################################

@app.route("/numbers",methods = ['POST'])
# @token_required
def enternums():
    # no = numbers.query.filter_by(numbers_id=numbers.numbers_id).first()
    # print(no)
    # if not no:
    #     return jsonify({'message' : 'No solution found!'})
#########################################################3
    auth = request.authorization
    print(auth)
    numdata = request.get_json()
    user = User.query.filter_by(name=auth.username).first()
    print(user)
    num = numbers(user_id=user.id,first=numdata['first'], second = numdata['second'],
                  third = numdata['third'], fourth= numdata['fourth'])

    db.session.add(num)
    db.session.commit()

    return jsonify(numdata)

@app.route("/numbers",methods = ['GET'])
def getnumbers():
    allnumbers = numbers.query.order_by(numbers.numbers_id.desc()).limit(1).all()
    output = []
    for number in allnumbers:
        currnum = {}
        #currnum['id'] = numbers.id
        currnum['first'] = str(number.first)
        currnum['second'] = str(number.second)
        currnum['third'] = str(number.third)
        currnum['fourth'] = str(number.fourth)
        output.append(currnum)


    solutions = []
    digit_length = len(output[0])
    expr_length = 2 * digit_length - 1
    digit_perm = sorted(set(permutations(output[0].values()))) #listin biri alındı
    op_comb = list(product('+-*/', repeat=digit_length-1))
    brackets = ([()] + [(x,y)
    for x in range(0, expr_length, 2)
    for y in range(x+4, expr_length+2, 2)
    if (x,y) != (0,expr_length+1)]
                 + [(0, 3+1, 4+2, 7+3)])
    total = []
    for d in digit_perm:
        for ops in op_comb:
            if '/' in ops:
                d2 = [('F(%s)' % i) for i in d]
            else:
                d2 = d
            ex = list(chain.from_iterable(zip_longest(d2, ops, fillvalue='')))

            for b in brackets:
                exp = ex[::]
                for insert_point, bracket in zip(b, '()'*(len(b)//2)):
                    exp.insert(insert_point, bracket) # str oldu
                txt = ''.join(exp)

                try:
                    num = eval(txt)
                except ZeroDivisionError:
                    continue
                if num == 24:
                    if '/' in ops:
                        exp = [(term if not term.startswith('F(') else term[2])
                               for term in exp]
                    ans = ' '.join(exp).rstrip()
                    print("Solution found:", ans,'= 24')
                    solutions.extend(ans)
                    total.append(ans)

    if len(total)>0:
        user = numbers.query.order_by(numbers.numbers_id.desc()).limit(1).all()

        for i in user:
            num_id = i.numbers_id
        solvedata = total
        num = Solve(solve = solvedata,num_id=num_id)
        db.session.add(num)
        db.session.commit()
        return f'number of solutions: {len(total)} \n number of attempt: {len(solutions)} \n Solutions: {total}'
    else:
        user = numbers.query.order_by(numbers.numbers_id.desc()).limit(1).all()

        for i in user:
            num_id = i.numbers_id
        num = Solve(solve='No solution found',num_id=num_id)
        db.session.add(num)
        db.session.commit()
        return "No solution found"

if __name__ == '__main__':
    app.run(host="0.0.0.0")
