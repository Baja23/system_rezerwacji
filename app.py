from flask import Flask, request, jsonify, session, render_template
import database as db
from werkzeug.security import check_password_hash
from schemas import UserRegistrationModel, ValidationError
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/index')
def index_page():
    return render_template("index.html")

@app.route('/')
def index():
    is_logged_in = 'user_id' in session
    return render_template('index.html', logged_in=is_logged_in)


@app.route('/registration')
def registration_page():
    return render_template("registration.html")

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    user_data_needed = ['first_name', 'last_name', 'email', 'phone_number', 'user_name', 'password', 'user_type_id']
    #validating user input
    try:
        user_data = {key: data[key] for key in user_data_needed}
        user = UserRegistrationModel(**user_data)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400 
    #adding user to the database
    if not db.get_user_by_username(user.user_name):
        user_id = db.add_user(
            data['first_name'],
            data['last_name'],
            data['email'],
            data['phone_number'],
            data['user_name'],
            data['password'],
            data['user_type_id']
        )
        if user_id:
            return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201
        else:
            return jsonify({'error': 'Registration failed'}), 500
    else:
        return jsonify({'error': 'Username already exists'}), 400
    # dodać walidację unikalności email i phone_number
      
@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user_in_db = db.get_user_by_username(data.get('user_name'))
    if user_in_db and check_password_hash(user_in_db['password'], data.get('password')):
        session['user_id'] = user_in_db['id']
        session['user_type_id'] = user_in_db['userTypeID']
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/reservation')
def reservation_page():
    return render_template("reservation.html")

#@app.route('/api/reservation', method=['POST'])
#def new_reservation():
    #data = request.json
    #date = data.get('date')
    #startTime = data.get('start_time')
    #endTime = data.get('end_time)
    #people = data.get('number_of_people')



if __name__ == '__main__':

    app.run(debug=True)

