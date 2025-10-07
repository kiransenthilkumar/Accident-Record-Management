
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from datetime import datetime
from models import db, Police, Citizen, Case, Accident, Admin, init_db, seed_demo_data
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os, csv, io, uuid
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accident.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-key')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
with app.app_context():
    init_db()
    seed_demo_data()

def login_required(role=None):
    from functools import wraps
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in first.', 'warning')
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                flash('Access denied for your role.', 'danger')
                return redirect(url_for('dashboard'))
            return view(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = Admin.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = f"admin:{user.id}"
            session['role'] = 'admin'
            session['name'] = 'Administrator'
            flash('Logged in as Admin', 'success')
            return redirect(url_for('dashboard'))
        police = Police.query.filter_by(username=username).first()
        if police and check_password_hash(police.password_hash, password):
            session['user_id'] = f"police:{police.id}"
            session['role'] = 'police'
            session['name'] = police.firstname
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required()
def dashboard():
    stats = {
        'police_count': Police.query.count(),
        'citizen_count': Citizen.query.count(),
        'case_count': Case.query.count(),
        'accident_count': Accident.query.count(),
    }
    latest_accidents = Accident.query.order_by(Accident.datee.desc()).limit(6).all()
    return render_template('dashboard.html', stats=stats, latest_accidents=latest_accidents)

# Police
@app.route('/police/add', methods=['GET', 'POST'])
@login_required(role='admin')
def police_add():
    if request.method == 'POST':
        data = {k: request.form.get(k, '').strip() for k in ['firstname','lastname','department','profession','username','password','address']}
        if not all([data['firstname'], data['lastname'], data['username'], data['password']]):
            flash('Firstname, Lastname, Username and Password are required.', 'warning')
            return render_template('police_add.html', data=data)
        if Police.query.filter_by(username=data['username']).first():
            flash('Username already exists.', 'danger')
            return render_template('police_add.html', data=data)
        police = Police(
            firstname=data['firstname'],
            lastname=data['lastname'],
            department=data['department'],
            profession=data['profession'],
            username=data['username'],
            password_hash=generate_password_hash(data['password']),
            fulladdress=data['address']
        )
        db.session.add(police)
        db.session.commit()
        flash('Police added successfully', 'success')
        return redirect(url_for('police_list'))
    return render_template('police_add.html', data={})

@app.route('/police/list')
@login_required()
def police_list():
    all_police = Police.query.order_by(Police.id.desc()).all()
    return render_template('police_list.html', all_police=all_police)

# Citizen
@app.route('/citizen/add', methods=['GET', 'POST'])
@login_required()
def citizen_add():
    if request.method == 'POST':
        data = {k: request.form.get(k, '').strip() for k in ['firstname','lastname','mobile','aadhar','address']}
        if not all([data['firstname'], data['lastname'], data['mobile'], data['aadhar']]):
            flash('All fields except address are required.', 'warning')
            return render_template('citizen_add.html', data=data)
        if Citizen.query.filter_by(aadhar=data['aadhar']).first():
            flash('Aadhar already registered.', 'danger')
            return render_template('citizen_add.html', data=data)
        citizen = Citizen(**data)
        db.session.add(citizen)
        db.session.commit()
        flash('Citizen registered successfully', 'success')
        return redirect(url_for('citizen_list'))
    return render_template('citizen_add.html', data={})

@app.route('/citizen/list')
@login_required()
def citizen_list():
    citizens = Citizen.query.order_by(Citizen.id.desc()).all()
    return render_template('citizen_list.html', citizens=citizens)

# Case
@app.route('/case/add', methods=['GET', 'POST'])
@login_required(role='admin')
def case_add():
    if request.method == 'POST':
        casename = request.form.get('casename', '').strip()
        description = request.form.get('description', '').strip()
        if not casename:
            flash('Case name is required.', 'warning')
            return render_template('case_add.html', data={'casename': casename, 'description': description})
        c = Case(casename=casename, description=description)
        db.session.add(c)
        db.session.commit()
        flash('Case added', 'success')
        return redirect(url_for('case_list'))
    return render_template('case_add.html', data={})

@app.route('/case/list')
@login_required()
def case_list():
    cases = Case.query.order_by(Case.id.desc()).all()
    return render_template('case_list.html', cases=cases)

# Allocate / Accident (with photo)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.route('/allocate', methods=['GET', 'POST'])
@login_required()
def allocate():
    cases = Case.query.order_by(Case.casename.asc()).all()
    if request.method == 'POST':
        aadhar = request.form.get('aadhar', '').strip()
        personname = request.form.get('personname', '').strip()
        vehicleno = request.form.get('vehicleno', '').strip()
        mobile = request.form.get('mobile', '').strip()
        address = request.form.get('address', '').strip()
        case_id = request.form.get('case_id')
        description = request.form.get('description', '').strip()
        datee = datetime.utcnow()

        citizen = Citizen.query.filter_by(aadhar=aadhar).first()
        if not citizen:
            flash('Citizen with given Aadhar not found. Please register the citizen first.', 'danger')
            return render_template('allocate_case.html', cases=cases)

        try:
            case_id = int(case_id)
            case = Case.query.get(case_id)
        except Exception:
            case = None
        if not case:
            flash('Please select a valid case.', 'warning')
            return render_template('allocate_case.html', cases=cases)

        photo_file = request.files.get('photo')
        filename = None
        if photo_file and photo_file.filename and allowed_file(photo_file.filename):
            fname = secure_filename(photo_file.filename)
            unique = f"{uuid.uuid4().hex}_{fname}"
            path = os.path.join(app.config['UPLOAD_FOLDER'], unique)
            photo_file.save(path)
            filename = unique

        accident = Accident(
            criminalid=citizen.id,
            caseid=case.id,
            personname=personname,
            vehicleno=vehicleno,
            mobile=mobile,
            address=address,
            description=description,
            datee=datee,
            photo=filename
        )
        db.session.add(accident)
        db.session.commit()

        try:
            with open('notifications.log', 'a') as nf:
                nf.write(f"{datetime.utcnow().isoformat()} - Accident recorded for Aadhar {aadhar} by user {session.get('name')}\n")
        except Exception:
            pass

        flash('Accident recorded/allocated successfully (notification logged).', 'success')
        return redirect(url_for('history_search', aadhar=aadhar))
    return render_template('allocate_case.html', cases=cases)

# History
@app.route('/history', methods=['GET', 'POST'])
@login_required()
def history():
    if request.method == 'POST':
        aadhar = request.form.get('aadhar', '').strip()
        return redirect(url_for('history_search', aadhar=aadhar))
    return render_template('history.html', records=None, aadhar=None)

@app.route('/history/<aadhar>')
@login_required()
def history_search(aadhar):
    citizen = Citizen.query.filter_by(aadhar=aadhar).first()
    if not citizen:
        flash('Citizen not found for given Aadhar.', 'danger')
        return render_template('history.html', records=None, aadhar=aadhar)
    records = (db.session.query(Accident, Case)
               .join(Case, Accident.caseid == Case.id)
               .filter(Accident.criminalid == citizen.id)
               .order_by(Accident.datee.desc())
               .all())
    return render_template('history.html', records=records, aadhar=aadhar, citizen=citizen)


# Exports
@app.route('/export/accidents.csv')
@login_required(role='admin')
def export_accidents_csv():
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Date','Aadhar','Person','Mobile','Vehicle','Case','Description','Photo'])
    for acc in Accident.query.join(Citizen, Accident.criminalid==Citizen.id).join(Case, Accident.caseid==Case.id).all():
        cw.writerow([acc.datee.isoformat(), acc.citizen.aadhar, acc.personname, acc.mobile, acc.vehicleno, acc.case.casename, acc.description or '', acc.photo or ''])
    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    return send_file(output, mimetype='text/csv', download_name='accidents.csv', as_attachment=True)

@app.route('/export/accidents.pdf')
@login_required(role='admin')
def export_accidents_pdf():
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40
    p.setFont('Helvetica-Bold', 14)
    p.drawString(40, y, 'Accident Records')
    p.setFont('Helvetica', 10)
    y -= 30
    for acc in Accident.query.join(Citizen, Accident.criminalid==Citizen.id).join(Case, Accident.caseid==Case.id).order_by(Accident.datee.desc()).all():
        line = f"{acc.datee.strftime('%Y-%m-%d %H:%M')} | {acc.citizen.aadhar} | {acc.personname} | {acc.vehicleno} | {acc.case.casename}"
        p.drawString(40, y, line)
        y -= 14
        if y < 60:
            p.showPage()
            y = height - 40
    p.save()
    buffer.seek(0)
    return send_file(buffer, mimetype='application/pdf', download_name='accidents.pdf', as_attachment=True)

# API for chart data
@app.route('/api/stats/accidents-by-case')
@login_required()
def accidents_by_case():
    rows = db.session.query(Case.casename, db.func.count(Accident.id)).join(Accident, Accident.caseid==Case.id).group_by(Case.casename).all()
    data = {'labels': [r[0] for r in rows], 'counts': [r[1] for r in rows]}
    return jsonify(data)


@app.route('/citizens')
@login_required('admin')
def citizens():
    citizens = Citizen.query.all()
    return render_template('citizen.html', citizens=citizens)

@app.route('/citizen/add', methods=['POST'])
@login_required('admin')
def add_citizen():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    mobile = request.form['mobile']
    aadhar = request.form['aadhar']
    address = request.form['address']

    # Check for duplicate aadhar
    if Citizen.query.filter_by(aadhar=aadhar).first():
        flash('A citizen with this Aadhar already exists.', 'danger')
        return redirect(url_for('citizens'))

    citizen = Citizen(
        firstname=firstname,
        lastname=lastname,
        mobile=mobile,
        aadhar=aadhar,
        address=address
    )
    db.session.add(citizen)
    db.session.commit()
    flash('Citizen added successfully!', 'success')
    return redirect(url_for('citizens'))

if __name__ == '__main__':
    app.run(debug=True, port=8080)
