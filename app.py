from flask import Flask, request, jsonify, session, render_template, current_app, redirect
import database as db
from werkzeug.security import check_password_hash
from schemas import UserRegistrationModel, ValidationError, ReservationModel, UserInfo
from classes import User, Reservation

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
        session['user_id'] = logged_user.id
        session['user_name'] = logged_user.user_name
        session['user_type_id'] = logged_user.user_type_id
        target_url = '/user_account'
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

#dopisać przechodzenie na odpowiednią stronę w zależności od property

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
        user.validate_name(user.first_name)
        user.validate_name(user.last_name)
        user.validate_phone_number(user.phone_number)
    except ValidationError as e:
        messages = "; ".join([err['msg'] for err in e.errors()])
        return jsonify({'error': messages}), 400
    new_user = user.model_dump()
    user_data = User(**new_user)
    try:
        user_id = user_data.save_guest_info()
    except ValueError:
        return jsonify({'error': 'User already exists'}), 409
    if not user_id:
        return jsonify({'error': 'Registration failed'}), 500
    else:
        session['user_id'] = user_id
    return jsonify({'id': user_id}), 201


@app.route('/reservation')
def reservation_page():
    return render_template("reservation.html")


@app.route('/api/reservation', methods=['POST'])
def make_reservation():
    if 'user_id' not in session:
        return jsonify({'error': 'Brak użytkownika w sesji'}), 400
    else:
        user_id = session['user_id']
    data = request.json
    data_needed = ['date', 'start_time', 'end_time', 'number_of_people']
    try:
        reservation_data = {key: data[key] for key in data_needed}
        reservation = ReservationModel(**reservation_data)
        reservation.validate_date(reservation.date)
        reservation.validate_time(reservation.start_time)
        reservation.validate_time(reservation.end_time)
        reservation.validate_end_time(reservation.end_time)
    except ValidationError as e:
        messages = "; ".join([err['msg'] for err in e.errors()])
        return jsonify({'error': messages}), 400
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    reservation = reservation.model_dump()
    reservation['user_id'] = user_id
    new_reservation = Reservation(**reservation)
    reservation_id = new_reservation.add_reservation()
    if reservation_id:
        # wyslij_email(...)
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
        reservation.validate_date(reservation.date)
        reservation.validate_time(reservation.start_time)
        reservation.validate_time(reservation.end_time)
        reservation.validate_end_time(reservation.end_time)
    except ValidationError as e:
        messages = "; ".join([err['msg'] for err in e.errors()])
        return jsonify({'error': messages}), 400
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    new_reservation = reservation.model_dump()
    old_reservation = Reservation(db.get_reservation_by_id(reservation_id))
    modification_confirmation = old_reservation.modify_reservation({key: new_reservation[key] for key in data_needed}, reservation_id)
    if modification_confirmation:
        return jsonify({'Reservation modified successfully.'}), 200
    else:
        return jsonify({'Reservation not found'}), 404

@app.route('/api/delete_reservation')

@app.route('/reservation_sent') 
def reservation_sent_page():
    return render_template("reservation_accepted.html")

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
    return render_template('new_reservation.html')


@app.route('/api/reservations/<int:reservation_id>/status', methods=['PUT'])
def modify_reservation_status(reservation_id: int, new_status: str):
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
