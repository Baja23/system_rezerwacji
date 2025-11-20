from flask import Flask, request, jsonify, session, render_template
import database as db
import string
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    is_logged_in = 'user_id' in session
    return render_template('index.html', logged_in=is_logged_in)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    user_data_needed = ['first_name', 'last_name', 'email', 'phone_number', 'user_name', 'password', 'user_type_id']

    #validating user input
    if not all(key in data for key in user_data_needed):
        return jsonify({'error': 'Missing user data'}), 400
    elif not data['first_name'].isalpha() or not data['last_name'].isalpha():
        return jsonify({'error': 'First name and last name must contain only letters'}), 400
    elif not data['phone_number'].isnumeric() or len(data['phone_number']) != 9:
        return jsonify({'error': 'Phone number must be numeric and exactly 9 digits long'}), 400
    elif '@' not in data['email'] or '.' not in data['email']:
        return jsonify({'error': 'Invalid email format'}), 400
    elif not data['user_name'].isalnum() or len(data['user_name']) < 5:
        return jsonify({'error': 'Username must be alphanumeric and at least 5 characters long'}), 400
    elif db.get_user_by_phone_number(data['phone_number']) and db.get_user_by_email(data['email']):
        return jsonify({'error': 'Phone number and email already registered'}), 400
    elif db.get_user_by_username(data['user_name']):
        return jsonify({'error': 'Username already exists'}), 400
    elif len(data['password']) < 10:
        return jsonify({'error': 'Password must be at least 10 characters long'}), 400
    elif not any(char.isdigit() for char in data['password']):
        return jsonify({'error': 'Password must contain at least one digit'}), 400
    elif not any(char.isupper() for char in data['password']):
        return jsonify({'error': 'Password must contain at least one uppercase letter'}), 400
    elif not any(char.islower() for char in data['password']):
        return jsonify({'error': 'Password must contain at least one lowercase letter'}), 400
    elif not any(c in string.punctuation for c in data['password']):
        return jsonify({'error': 'Password must contain at least one special character'}), 400
    elif ' ' in data['password']:
        return jsonify({'error': 'Password must not contain spaces'}), 400   
    else: 
    #adding user to the database
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

@app.route('/api/reservation', method=['POST'])
def new_reservation():
    data = request.json
    date = data.get('date')
    time = data.get('time')
    people = data.get('number_of_people')

if __name__ == '__main__':
    app.run(debug=True)
