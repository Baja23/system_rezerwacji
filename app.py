from flask import Flask, request, jsonify, session, render_template, current_app
import database as db
from werkzeug.security import check_password_hash
from schemas import UserRegistrationModel, ValidationError, ReservationModel
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


@app.route('/register')
def registration_page():
    return render_template("register.html")


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    user_data_needed = ['first_name', 'last_name', 'email', 'phone_number', 'user_name', 'password', 'user_type_id']

    # validating user input
    try:
        user_data = {key: data[key] for key in user_data_needed}
        user = UserRegistrationModel(**user_data)
        user.validate_password(user.password)
        user.validate_user_name(user.user_name)
    except ValidationError as e:
        messages = "; ".join([err['msg'] for err in e.errors()])
        return jsonify({'error': messages}), 400
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
        # checking for existing user
    user_info_in_db = {'username': db.get_user_by_username(user.user_name),
                       'email': db.get_user_by_email(user.email),
                       'phone_number': db.get_user_by_phone_number(user.phone_number)
                       }
    for key, value in user_info_in_db.items():
        if value:
            return jsonify({'error': f'{key.replace("_", " ").capitalize()} already exists'}), 400
    # adding user to the database
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


# route to get guest user info
@app.route('/user_info', methods=['POST'])
def get_guest_user_info():
    user_data = request.json
    user_id = db.add_user(
        user_data['first_name'],
        user_data['last_name'],
        user_data['email'],
        user_data['phone_number'],
        None,
        None,
        1  # guest user type ID
    )
    return user_data


@app.route('/reservation')
def reservation_page():
    return render_template("reservation.html")


@app.route('/api/reservation', methods=['POST'])
def make_reservation():
    # co jak user załaduje stronę z formularzem rezerwacji bez podania danych i bez zalogowania?
    if 'user_id' not in session:
        user_info = get_guest_user_info()
        user_id = user_info['id']
    else:
        user_id = session['user_id']
    data = request.json
    data_needed = ['date', 'start_time', 'end_time', 'number_of_people']
    try:
        reservation_data = {key: data[key] for key in data_needed}
        reservation = ReservationModel(**reservation_data)
    except ValidationError as e:
        messages = "; ".join([err['msg'] for err in e.errors()])
        return jsonify({'error': messages}), 400
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    reservation_id = db.create_reservation(
        reservation['date'],
        reservation['start_time'],
        reservation['end_time'],
        reservation['number_of_people'],
        user_id
    )
    if reservation_id:
        return jsonify({'message': 'Reservation created successfully', 'reservation_id': reservation_id}), 201
    else:
        return jsonify({'error': 'Reservation creation failed'}), 500


@app.route('/personal_data')
def personal_page():
    return render_template("personal_data.html")

@app.route('/reservation_sent')
def reservation_sent_page():
    return render_template("reservation_accepted.html")

@app.route('/reservation_fail')
def reservation_fail_page():
    return render_template("reservation_fail.html")

@app.route('/user_account')
def user_account_page():
    return render_template("user_account.html")

@app.route('/reservation_accepted')
def reservation_accepted_page():
    return render_template("reservation_accepted.html")

@app.route('/active_reservations')
def active_reservations_page():
    return render_template("active_reservations.html")

@app.route('/manager_account')
def manager_account_page():
    return render_template("manager_account.html")

@app.route('/waiter_account')
def waiter_account_page():
    return render_template("waiter_account.html")

@app.route('/rules')
def rules_page():
    return render_template("rules.html")

@app.route('/password_recovery')
def password_recovery_page():
    return render_template("password_recovery.html")

#-------------------------------------MOJE-------------------------------



@app.route('/api/reservations', methods=['GET'])
def list_reservations():
    date = request.args.get('date')
    firstName = request.args.get('firstName')
    lastName= request.args.get('lastName')
    startTime = request.args.get('startTime')
    endTime = request.args.get('endTime')
    status = request.args.get('status')


    try:
        rows = db.get_all_reservations(date=date, firstName=firstName, lastName=lastName, startTime=startTime, endTime=endTime, status=status)
        return jsonify(rows), 200
    except Exception:
        current_app.logger.exception("Błąd przy pobieraniu rezerwacji")
        return jsonify({'error': 'Could not fetch reservations'}), 500

if __name__ == '__main__':
    app.run(debug=True)
