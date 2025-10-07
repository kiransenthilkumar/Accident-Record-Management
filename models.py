
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
    if Police.query.first() or Citizen.query.first() or Case.query.first() or Accident.query.first():
        return

    p1 = Police(firstname='Suresh', lastname='K', department='Traffic', profession='Inspector', username='sureshk', password_hash=generate_password_hash('suresh123'), fulladdress='Traffic Police HQ, Chennai')
    p2 = Police(firstname='Priya', lastname='V', department='Highway Patrol', profession='SP', username='priyav', password_hash=generate_password_hash('priya123'), fulladdress='SP Office, Madurai Rural') 
    p3 = Police(firstname='Ajay', lastname='S', department='Investigation', profession='ACP', username='ajays', password_hash=generate_password_hash('ajays123'), fulladdress='CB-CID, Coimbatore') 
    p4 = Police(firstname='Ramesh', lastname='M', department='Patrol', profession='Constable', username='ramesh', password_hash=generate_password_hash('ramesh123'), fulladdress='Kotturpuram Beat, Chennai') 
    p5 = Police(firstname='Nithya', lastname='D', department='Traffic', profession='Sergeant', username='nithyad', password_hash=generate_password_hash('nithya123'), fulladdress='Anna Salai Circle, Chennai') 
    p6 = Police(firstname='Jeeva', lastname='K', department='Highway Patrol', profession='Sub-Inspector', username='jeevak', password_hash=generate_password_hash('jeeva123'), fulladdress='National Highway 38 Checkpost, Trichy') 
    p7 = Police(firstname='Ganesh', lastname='R', department='Investigation', profession='Forensic Analyst', username='ganeshr', password_hash=generate_password_hash('ganesh123'), fulladdress='Forensic Science Lab, Erode') 
    p8 = Police(firstname='Arjun', lastname='S', department='Patrol', profession='Head Constable', username='arjun', password_hash=generate_password_hash('arjun123'), fulladdress='Velachery Patrol Unit, Chennai') 
    p9 = Police(firstname='Vasanth', lastname='I', department='Traffic', profession='Inspector', username='vasanth', password_hash=generate_password_hash('vasant123'), fulladdress='Tambaram Traffic Police') 
    p10 = Police(firstname='Karthik', lastname='N', department='Investigation', profession='Superintendent', username='karthikn', password_hash=generate_password_hash('karthi123'), fulladdress='Tirunelveli Police HQ') 
    p11 = Police(firstname='Divya', lastname='R', department='Highway Patrol', profession='Officer', username='divyar', password_hash=generate_password_hash('divya123'), fulladdress='Krishnagiri Highway Patrol') 
    p12 = Police(firstname='Balaji', lastname='G', department='Patrol', profession='Officer', username='balaji', password_hash=generate_password_hash('balaji123'), fulladdress='Ambattur Police Station, Chennai') 
    db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12])

    c1 = Citizen(firstname='Vishal', lastname='S', mobile='9876543210', aadhar='111122223333', address='East End Apartments, Anna Nagar, Chennai')
    c2 = Citizen(firstname='Deepa', lastname='R', mobile='9988776655', aadhar='444455556666', address='Gandhipuram, Coimbatore') 
    c3 = Citizen(firstname='Vimal', lastname='C', mobile='9000100020', aadhar='777788889999', address='Tallakulam, Madurai') 
    c4 = Citizen(firstname='Shanthi', lastname='D', mobile='8111222333', aadhar='101020203030', address='Shevapet, Salem') 
    c5 = Citizen(firstname='Mohan', lastname='R', mobile='7000700070', aadhar='404050506060', address='Pudur, Tiruppur') 
    c6 = Citizen(firstname='Latha', lastname='S', mobile='6000600060', aadhar='707080809090', address='Srirangam, Trichy') 
    c7 = Citizen(firstname='Rajesh', lastname='P', mobile='9111922293', aadhar='123456789012', address='Tambaram, Chennai') 
    c8 = Citizen(firstname='Sindhu', lastname='N', mobile='8222833384', aadhar='234567890123', address='Perundurai Road, Erode') 
    c9 = Citizen(firstname='Prakash', lastname='V', mobile='7333744475', aadhar='345678901234', address='Near Railway Station, Thanjavur') 
    c10 = Citizen(firstname='Anand', lastname='G', mobile='9444955596', aadhar='456789012345', address='Kosavapatti, Dindigul') 
    c11 = Citizen(firstname='Kavitha', lastname='S', mobile='6555666777', aadhar='567890123456', address='Nanganallur, Chennai') 
    c12 = Citizen(firstname='Ravi', lastname='M', mobile='8877665544', aadhar='678901234567', address='Siruseri IT Park, Kanchipuram') 
    c13 = Citizen(firstname='Sarala', lastname='R', mobile='7766554433', aadhar='789012345678', address='Anna Salai, Villupuram') 
    c14 = Citizen(firstname='Rohit', lastname='M', mobile='9654321098', aadhar='890123456789', address='Near Lake, Kodaikanal') 
    c15 = Citizen(firstname='Sangeetha', lastname='R', mobile='8543210987', aadhar='901234567890', address='NH 44, Krishnagiri') 
    c16 = Citizen(firstname='Babu', lastname='S', mobile='7432109876', aadhar='012345678901', address='Vandiyur, Madurai') 
    c17 = Citizen(firstname='Nanda', lastname='M', mobile='9321098765', aadhar='123400005678', address='Palladam, Tiruppur') 
    c18 = Citizen(firstname='Meena', lastname='K', mobile='8210987654', aadhar='987600005432', address='Posh Colony, Vellore') 
    c19 = Citizen(firstname='Sam', lastname='D', mobile='7109876543', aadhar='135792468013', address='Tuticorin Port Area') 
    c20 = Citizen(firstname='Tarun', lastname='V', mobile='9098765432', aadhar='246801357924', address='Tirunelveli Outer Ring Road') 
    c21 = Citizen(firstname='Usha', lastname='M', mobile='9999888877', aadhar='369258147036', address='Near University, Coimbatore') 
    c22 = Citizen(firstname='Vinod', lastname='G', mobile='8888777766', aadhar='121234345656', address='Ambattur Industrial Estate, Chennai') 
    db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21, c22])

    case1 = Case(casename='Over Speed', description='Driving above speed limit')
    case2 = Case(casename='Drunk Driving', description='Driving under influence of alcohol')
    case3 = Case(casename='Hit and Run', description='Leaving the scene of an accident without reporting')
    case4 = Case(casename='No License', description='Driving without a valid license')
    case5 = Case(casename='Illegal Parking', description='Parking in a no-parking zone or hindering traffic')
    case6 = Case(casename='Signal Jumping', description='Disobeying a traffic light/signal')
    case7 = Case(casename='Using Mobile While Driving', description='Using a handheld mobile device while operating a vehicle')
    case8 = Case(casename='Dangerous Driving', description='Operating a vehicle in a reckless manner')
    case9 = Case(casename='Expired Insurance', description='Driving a vehicle with expired or no insurance')
    case10 = Case(casename='Vehicle Modification', description='Illegal modification of vehicle/exhaust system')
    case11 = Case(casename='Failing to Yield', description='Failing to give way to pedestrians or other vehicles')
    case12 = Case(casename='Tampering with Vehicle Plates', description='Falsifying or obscuring license plates')
    db.session.add_all([case1, case2, case3, case4, case5, case6, case7, case8, case9, case10, case11, case12])
    db.session.commit() 

    a1 = Accident(criminalid=c1.id, caseid=case1.id, personname='Vishal S', vehicleno='TN 01 AA 1234', mobile='9876543210', address=c1.address, description='Speeding violation caught near IIT Madras.', datee=datetime.utcnow() - timedelta(days=1), photo='acc_01.jpg')
    a2 = Accident(criminalid=c2.id, caseid=case2.id, personname='Deepa R', vehicleno='TN 66 BB 5678', mobile='9988776655', address=c2.address, description='Driver failed breathalyzer test after minor crash.', datee=datetime.utcnow() - timedelta(days=5), photo='acc_02.jpg')    
    a3 = Accident(criminalid=c3.id, caseid=case3.id, personname='Vimal C', vehicleno='TN 58 CC 9012', mobile='9000100020', address=c3.address, description='Witnesses reported car hitting a pedestrian and leaving.', datee=datetime.utcnow() - timedelta(days=15), photo='acc_03.jpg')
    a4 = Accident(criminalid=c4.id, caseid=case4.id, personname='Shanthi D', vehicleno='TN 52 DD 3456', mobile='8111222333', address=c4.address, description='Failed to produce any valid driving document.', datee=datetime.utcnow() - timedelta(days=20), photo='acc_04.jpg')
    a5 = Accident(criminalid=c5.id, caseid=case5.id, personname='Mohan R', vehicleno='TN 39 EE 7890', mobile='7000700070', address=c5.address, description='Vehicle blocking the emergency entrance of a factory.', datee=datetime.utcnow() - timedelta(days=2), photo='acc_05.jpg')
    a6 = Accident(criminalid=c6.id, caseid=case6.id, personname='Latha S', vehicleno='TN 45 FF 2345', mobile='6000600060', address=c6.address, description='Drove through a red signal causing a collision.', datee=datetime.utcnow() - timedelta(days=7), photo='acc_06.jpg')
    a7 = Accident(criminalid=c7.id, caseid=case7.id, personname='Rajesh P', vehicleno='TN 02 GG 6789', mobile='9111922293', address=c7.address, description='Texting while driving observed by patrol officer.', datee=datetime.utcnow() - timedelta(days=3), photo='acc_07.jpg')
    a8 = Accident(criminalid=c8.id, caseid=case8.id, personname='Sindhu N', vehicleno='TN 33 HH 0123', mobile='8222833384', address=c8.address, description='Zig-zag driving reported on the main road.', datee=datetime.utcnow() - timedelta(days=10), photo='acc_08.jpg')
    a9 = Accident(criminalid=c9.id, caseid=case9.id, personname='Prakash V', vehicleno='TN 49 II 4567', mobile='7333744475', address=c9.address, description='Stopped for inspection; insurance expired 6 months ago.', datee=datetime.utcnow() - timedelta(days=14), photo='acc_09.jpg')
    a10 = Accident(criminalid=c10.id, caseid=case10.id, personname='Anand G', vehicleno='TN 57 JJ 8901', mobile='9444955596', address=c10.address, description='Loud, non-standard horn installed.', datee=datetime.utcnow() - timedelta(days=1), photo='acc_10.jpg')
    a11 = Accident(criminalid=c11.id, caseid=case11.id, personname='Kavitha S', vehicleno='TN 07 KK 2345', mobile='6555666777', address=c11.address, description='Did not give way to a turning vehicle.', datee=datetime.utcnow() - timedelta(days=18), photo='acc_11.jpg')
    a12 = Accident(criminalid=c12.id, caseid=case12.id, personname='Ravi M', vehicleno='TN 21 LL 6789', mobile='8877665544', address=c12.address, description='License plate bracket partially obscured the number.', datee=datetime.utcnow() - timedelta(days=25), photo='acc_12.jpg')
    a13 = Accident(criminalid=c13.id, caseid=case2.id, personname='Sarala R', vehicleno='TN 32 MM 0123', mobile='7766554433', address=c13.address, description='Found consuming liquor inside parked car, later attempted to drive.', datee=datetime.utcnow() - timedelta(days=2), photo='acc_13.jpg')
    a14 = Accident(criminalid=c14.id, caseid=case1.id, personname='Rohit M', vehicleno='TN 57 NN 4567', mobile='9654321098', address=c14.address, description='Excessive speed recorded on Kodaikanal ghat road.', datee=datetime.utcnow() - timedelta(days=16), photo='acc_14.jpg')
    a15 = Accident(criminalid=c15.id, caseid=case3.id, personname='Sangeetha R', vehicleno='TN 29 OO 8901', mobile='8543210987', address=c15.address, description='Truck struck a barricade on NH 44 and sped away.', datee=datetime.utcnow() - timedelta(days=9), photo='acc_15.jpg')
    a16 = Accident(criminalid=c16.id, caseid=case4.id, personname='Babu S', vehicleno='TN 58 PP 2345', mobile='7432109876', address=c16.address, description='Driving a car without ever obtaining a license.', datee=datetime.utcnow() - timedelta(days=21), photo='acc_16.jpg')
    a17 = Accident(criminalid=c17.id, caseid=case5.id, personname='Nanda M', vehicleno='TN 39 QQ 6789', mobile='9321098765', address=c17.address, description='Parked illegally on a narrow residential street, blocking passage.', datee=datetime.utcnow() - timedelta(days=13), photo='acc_17.jpg')
    a18 = Accident(criminalid=c18.id, caseid=case6.id, personname='Meena K', vehicleno='TN 23 RR 0123', mobile='8210987654', address=c18.address, description='Ignored flashing signal leading to a T-junction mishap.', datee=datetime.utcnow() - timedelta(days=6), photo='acc_18.jpg')
    a19 = Accident(criminalid=c19.id, caseid=case7.id, personname='Sam D', vehicleno='TN 69 SS 4567', mobile='7109876543', address=c19.address, description='Driver seen scrolling on mobile phone at high speed.', datee=datetime.utcnow() - timedelta(days=4), photo='acc_19.jpg')
    a20 = Accident(criminalid=c20.id, caseid=case8.id, personname='Tarun V', vehicleno='TN 72 TT 8901', mobile='9098765432', address=c20.address, description='Performing stunts and sudden lane changes on ring road.', datee=datetime.utcnow() - timedelta(days=19), photo='acc_20.jpg')
    a21 = Accident(criminalid=c21.id, caseid=case9.id, personname='Usha M', vehicleno='TN 66 UU 2345', mobile='9999888877', address=c21.address, description='Insurance lapsed over a year ago; vehicle seized.', datee=datetime.utcnow() - timedelta(days=28), photo='acc_21.jpg')
    a22 = Accident(criminalid=c22.id, caseid=case10.id, personname='Vinod G', vehicleno='TN 04 VV 6789', mobile='8888777766', address=c22.address, description='Car modified to produce excessive smoke/noise.', datee=datetime.utcnow() - timedelta(days=23), photo='acc_22.jpg')
    a23 = Accident(criminalid=c1.id, caseid=case11.id, personname='Vishal S', vehicleno='TN 01 AA 1234', mobile='9876543210', address=c1.address, description='Failed to slow down and allow merging traffic.', datee=datetime.utcnow() - timedelta(days=8), photo='acc_23.jpg')
    a24 = Accident(criminalid=c2.id, caseid=case12.id, personname='Deepa R', vehicleno='TN 66 BB 5678', mobile='9988776655', address=c2.address, description='Had a sticker obscuring part of the district code.', datee=datetime.utcnow() - timedelta(days=30), photo='acc_24.jpg')
    a25 = Accident(criminalid=c4.id, caseid=case4.id, personname='Shanthi D', vehicleno='TN 52 DD 3456', mobile='8111222333', address=c4.address, description='Found driving a motorcycle without license a second time.', datee=datetime.utcnow() - timedelta(days=22), photo='acc_25.jpg')
    db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24, a25])
    db.session.commit()