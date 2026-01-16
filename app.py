from flask import Flask, request, jsonify, session, render_template, current_app, redirect, url_for
import database as db
from werkzeug.security import check_password_hash
from schemas import UserRegistrationModel, ValidationError, ReservationModel, UserInfo
from classes import User, Reservation
from datetime import timedelta
import threading
from email_notifications import send_reservation_email

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

@app.before_request
def make_session_permanent():
    session.modified = True

@app.route('/index')
def index_page():
    return render_template("index.html")


@app.route('/')
def index():
    is_logged_in = 'user_id' in session or 'email' in session
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
    except ValidationError as e:
        messages = "; ".join([err['msg'] for err in e.errors()])
        return jsonify({'error': messages}), 400
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    
    #initializing a User object with verified data
    new_user = User(**user.model_dump())
    try:
        user_id = new_user.save_user_info()
    except ValueError:
        return jsonify({'error': 'User already exists'}), 409
    if user_id:
        target_url = '/user_account'
        return jsonify({'message': 'User registered successfully', 
                        'user_id': user_id,
                        'redirect_url': target_url}), 201
    else:
        return jsonify({'error': 'Registration failed'}), 500


@app.route('/login')
def login_page():
    return render_template("login.html")


@app.route('/api/login', methods=['POST']) 
def login():
    data = request.json
    logged_user = User.login(data.get('user_name'), data.get('password'))
    if logged_user:
        session.clear()
        session['user_id'] = logged_user.id
        session['user_name'] = logged_user.user_name
        session['user_type_id'] = logged_user.user_type_id
        target_url = '/user_account'
        session.permanent = True
        if session['user_type_id'] == 3:
            target_url = '/waiter_account'
        elif session['user_type_id'] == 4 or session['user_type_id'] == 5:
            target_url = '/manager_account'
    # 5. Wysyłamy instrukcję do Frontendu
        return jsonify({
        'message': 'Zalogowano pomyślnie',
        'redirect_url': target_url
        }), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/logout_button')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/personal_data')
def personal_page():
    return render_template("personal_data.html")

# route to get guest user info
#PRZETESTOWAĆ
@app.route('/api/personal_data', methods=['POST'])
def get_guest_user_info():
    data = request.json
    try:
        user = UserInfo(**data)
    except ValidationError as e:
        messages = "; ".join([err['msg'] for err in e.errors()])
        return jsonify({'error': messages}), 400
    new_user = user.model_dump()
    user_data = User(**new_user)
    user_in_db = user_data.get_user_by_email()
    if user_in_db == True:
        return jsonify({'error': 'User already exists'}), 409
    else:
        session['first_name'] = user_data.first_name
        session['last_name'] = user_data.last_name
        session['email'] = user_data.email
        session['phone_number'] = user_data.phone_number
        session['user_type_id'] = user_data.user_type_id
    return jsonify('User saved to session correctly'), 201


@app.route('/reservation')
def reservation_page():
    return render_template("reservation.html")


@app.route('/api/reservation', methods=['POST'])
def make_reservation():
    if not 'user_id' in session and not 'email' in session:
        return jsonify({'error': 'Brak użytkownika w sesji'}), 403
    
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
    reservation = reservation.model_dump()
    new_reservation = Reservation(**reservation)
    available_tables = new_reservation.check_available_tables()
    if available_tables == []:
        return jsonify('No available tables in selected date.'), 409
    else: 
        session['date'] = new_reservation.date
        session['start_time'] = new_reservation.start_time
        session['end_time'] = new_reservation.end_time
        session['number_of_people'] = new_reservation.number_of_people
        return jsonify({'available_tables': available_tables}), 200

@app.route('/api/get_table', methods=['POST'])
def get_table_save_reservation():
    data = request.json
    table_id = data['id']
    if not table_id:
        available_tables = session['available_tables']
        table_id = list(available_tables)[0] 
    session['table_id'] = table_id
    if 'user_id' in session:
        user_id = session['user_id']
    elif 'email' in session:
        guest_user = User(session['first_name'], session['last_name'], session['email'], session['phone_number'], session['user_type_id'])
        user_id = guest_user.save_guest_info()
    
    new_reservation = Reservation(session['date'], session['start_time'], session['end_time'], session['number_of_people'], user_id)
    reservation_id = new_reservation.add_reservation(table_id)
    if reservation_id:
        email_context = {
        'email': session.get('email'),
        'first_name': session.get('first_name'),
        'last_name': session.get('last_name'),
        'date': session.get('date'),
        'start_time': session.get('start_time')
    }
        email_thread = threading.Thread(target=send_reservation_email, args=(email_context,))
        email_thread.start()
        return jsonify({
            'message': 'Reservation created successfully', 
            'reservation_id': reservation_id,
            'redirect_url': '/reservation_sent'
        }), 201
    else:
        jsonify({
            'error': 'Reservation creation failed',
            'redirect_url': '/reservation_fail'
            }), 500
    
@app.route('/api/reservations/<int:reservation_id>', methods=['GET'])
def get_reservation_details(reservation_id):
    reservation_data = db.get_reservation_by_id(reservation_id)
    if reservation_data:
        return jsonify(reservation_data), 200
    else:
        return jsonify({'error': 'Reservation not found'}), 404

    
@app.route('/api/reservations/<int:reservation_id>', methods=['PUT'])
def modify_reservation(reservation_id):
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
    new_reservation = reservation.model_dump()
    old_resv_dict = dict(db.get_reservation_by_id(reservation_id))
    old_resv_dict['reservation_id'] = old_resv_dict.pop('id')
    old_resv_dict['start_time'] = old_resv_dict.pop('startTime')
    old_resv_dict['end_time'] = old_resv_dict.pop('endTime')
    old_resv_dict['number_of_people'] = old_resv_dict.pop('numberOfPeople')
    old_resv_dict['user_id'] = old_resv_dict.pop('userId')
    old_resv_dict.pop('status')
    old_resv_dict.pop('restaurantTableId')
    old_reservation = Reservation(**old_resv_dict)
    modification_confirmation = old_reservation.modify_reservation({key: new_reservation[key] for key in data_needed})
    if modification_confirmation:
        return jsonify({'message': 'Reservation modified successfully.'}), 200
    else:
        return jsonify({'message': 'Reservation not found'}), 404

@app.route('/api/delete_reservation')

@app.route('/reservation_sent') 
def reservation_sent_page():
    return render_template("reservation_accepted.html")

@app.route('/api/reservation_sent', methods=['POST'])
def reservation_sent():
    reservation_info = {
        'first_name': session.get('first_name'),
        'last_name': session.get('last_name'),
        'date': session.get('date'),
        'start_time': session.get('start_time'),
        'end_time': session.get('end_time'),
        'table_id': session.get('table_id')
    }
    return jsonify(reservation_info), 200

@app.route('/reservation_fail')
def reservation_fail_page():
    return render_template("reservation_fail.html")

@app.route('/api/reservation_fail', methods=['POST'])
def reservation_fail():
    return render_template("reservation.html")

@app.route('/user_account')
def user_account_page():
    if 'user_id' not in session:
        # Jeśli nie, wyrzucamy go do logowania
        return redirect('/login') 
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

@app.route('/new_reservations')
def new_reservations():
    return render_template('new_reservations.html')


@app.route('/api/reservations/<int:reservation_id>/status', methods=['PUT'])
def modify_reservation_status(reservation_id: int):
    data = request.json
    new_status = data.get('status')
    if new_status not in ['Accepted', 'Cancelled']:
        return jsonify({'error': 'Invalid status value'}), 400
    success = db.modify_reservation_status(reservation_id, new_status)
    if success:
        return jsonify({'message': 'Reservation status updated successfully'}), 200
    else:
        return jsonify({'error': 'Reservation not found'}), 404

#-------------------------------------MOJE-------------------------------



@app.route('/api/reservations', methods=['GET'])
def list_reservations():
    try:
        rows = db.get_reservations()
        return jsonify(rows), 200
    except Exception:
        current_app.logger.exception("Błąd przy pobieraniu rezerwacji")
        return jsonify({'error': 'Could not fetch reservations'}), 500

if __name__ == '__main__':
    app.run(debug=True)
