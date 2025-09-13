
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Police(db.Model):
    __tablename__ = 'police'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50))
    profession = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    fulladdress = db.Column(db.String(255))

class Citizen(db.Model):
    __tablename__ = 'citizen'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    aadhar = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(255))

class Case(db.Model):
    __tablename__ = 'case'
    id = db.Column(db.Integer, primary_key=True)
    casename = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

class Accident(db.Model):
    __tablename__ = 'accident'
    id = db.Column(db.Integer, primary_key=True)
    criminalid = db.Column(db.Integer, db.ForeignKey('citizen.id'), nullable=False)
    caseid = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    personname = db.Column(db.String(100), nullable=False)
    vehicleno = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255))
    description = db.Column(db.String(255))
    datee = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    photo = db.Column(db.String(255))

    citizen = db.relationship('Citizen', backref='accidents')
    case = db.relationship('Case', backref='accidents')

def init_db():
    db.create_all()
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(username='admin', password_hash=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()

def seed_demo_data():
    # If there are already records, skip seeding
    if Police.query.first() or Citizen.query.first() or Case.query.first() or Accident.query.first():
        return
    # Add sample police
    p1 = Police(firstname='Virat', lastname='Kohli', department='Traffic', profession='Officer', username='virat', password_hash=generate_password_hash('virat123'), fulladdress='City Center')
    p2 = Police(firstname='Rohit', lastname='Sharma', department='Highway', profession='Inspector', username='rohit', password_hash=generate_password_hash('rohit123'), fulladdress='North Station')
    db.session.add_all([p1,p2])
    # Add citizens
    c1 = Citizen(firstname='Vishal', lastname='S', mobile='8652365896', aadhar='123412341234', address='Palladam')
    c2 = Citizen(firstname='Saravanan', lastname='K', mobile='8754652230', aadhar='950095009500', address='Coimbatore')
    db.session.add_all([c1,c2])
    # Add cases
    case1 = Case(casename='Over Speed', description='Driving above speed limit')
    case2 = Case(casename='Drunk Driving', description='Driving under influence')
    db.session.add_all([case1, case2])
    db.session.commit()
    # Add accidents
    a1 = Accident(criminalid=c1.id, caseid=case1.id, personname='Vishal', vehicleno='TN 35 4568', mobile='8652365896', address='Palladam', description='Minor collision', datee=datetime.utcnow() - timedelta(days=3))
    a2 = Accident(criminalid=c2.id, caseid=case2.id, personname='Saravanan', vehicleno='TN 35 4585', mobile='8754652230', address='Coimbatore', description='Major accident', datee=datetime.utcnow() - timedelta(days=10))
    db.session.add_all([a1,a2])
    db.session.commit()
