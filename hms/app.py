from flask import Flask, render_template, request, redirect, url_for,flash,session
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import Form
from wtforms.fields import DateField
from flaskext.mysql import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError,Regexp

import requests
import os
app = Flask(__name__)
app.debug = True
Bootstrap(app)
datepicker(app)
app.secret_key = 'h432hi5ohi3h5i5hi3o2hi'

log='n'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Cloud@123'
app.config['MYSQL_DATABASE_DB'] = 'hms'

mysql = MySQL(app)


photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
configure_uploads(app, photos)


class LoginForm(FlaskForm):
    login   = StringField("Login", validators=[DataRequired(),Length(min=8)])
    password = PasswordField("Password", validators=[DataRequired(), Length(10)])
    submit = SubmitField("Login")

@app.route('/')
def home():
    global log
    log='n'
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    global log
    log='n'
    emptyp='none'
    flag=1
    if request.method == 'POST':
        userDetails = request.form

        name = userDetails['Username']
        password = userDetails['password']
        conn = mysql.connect()
        cursor = conn.cursor()
        

        resultValue = cursor.execute("SELECT * FROM executive")
        if resultValue > 0:
            ExeDetails=cursor.fetchall()
            for Executive in ExeDetails:
                if ((name==Executive[0]) & (password==Executive[1])):
                    flag='e'
                    emptyp = 'Executive'
                    break
                else:
                    flag=1
        resultValue = cursor.execute("SELECT * FROM pharmacist")
        if (resultValue > 0) & (flag==1):
            PharmDetails = cursor.fetchall()
            for Pharmacist in PharmDetails:
                if ((name == Pharmacist[0]) & (password == Pharmacist[1])):
                    flag = 'p'
                    emptyp = 'Pharmacist'
                    break
                else:
                    flag = 1
        resultValue = cursor.execute("SELECT * FROM diagnostic")
        if (resultValue > 0) & (flag==1):
            DiagDetails = cursor.fetchall()
            for Diagnostic in DiagDetails:
                if ((name == Diagnostic[0]) & (password == Diagnostic[1])):
                    flag = 'd'
                    emptyp = 'Diagnostic'
                    break

        if flag=='e':
            log='e'
            conn = mysql.connect()
            cursor = conn.cursor()
            
            if request.form['action'] == 'login':
            	conn = mysql.connect()
            	cursor = conn.cursor()
            	time = datetime.now()
            	cursor.execute("INSERT INTO userstore(login,password,created_at) VALUES(%s,%s,%s)", 
            	[name,password,time.strftime("%Y-%m-%d %H:%M:%S")])
            	conn.commit()
            #ts=time.time()
            #timestampn=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            flash(f"You are successfully logged in as a {emptyp}","success")
            return redirect('/patients')
        if flag=='p':
            log='p'
            flash(f"You are successfully logged in as a {emptyp}","info")
            if request.form['action'] == 'login':
            	conn = mysql.connect()
            	cursor = conn.cursor()
            	time = datetime.now()
            	cursor.execute("INSERT INTO userstore(login,password,created_at) VALUES(%s,%s,%s)", 
            	[name,password,time.strftime("%Y-%m-%d %H:%M:%S")])
            	conn.commit()
       
            return redirect('/issue_medicines')
        elif flag=='d':
            flash(f"You are successfully logged in as a {emptyp}","success")
            log='d'
            if request.form['action'] == 'login':
            	conn = mysql.connect()
            	cursor = conn.cursor()
            	time = datetime.now()
            	cursor.execute("INSERT INTO userstore(login,password,created_at) VALUES(%s,%s,%s)", 
            	[name,password,time.strftime("%Y-%m-%d %H:%M:%S")])
            	conn.commit()
            return redirect('/add_diagnostics')
        else:
            flash("Sorry,something went wrong","error")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/patients')
def patients():
    global log
    if(log=='e'):
    	return render_template('patients.html')
    else:
    	flash("Please Login first")
    	return redirect('/login')

@app.route('/icon')
def icon():
    
    return render_template('icon.html')


@app.route('/issue_medicines', methods=['GET', 'POST'])    
def issue_medicines():
	global log
	if(log=='p'):
		pid=str("")
		pname=str("")
		page=str("")
		paddr=str("")
		pdoj=str("")
		pbed=str("")

		mi=[]

		m_name=""
		status=""
		qty_i="0"

		add=[]
		
		
   
		if request.method == 'POST':
			if request.form['action'] == 'search':
        			p = request.form['pid']
        			session['pid'] = p
        			print("session['pid']=",session['pid'])
        
        			conn = mysql.connect()
        			cursor = conn.cursor()
        			cursor.execute("select * from patients where pid=%s",(p))
        			data = cursor.fetchall() #data from database
        
        			pid=p
        			pname=data[0][2]
        			page=data[0][3]
        			paddr=data[0][6]
        			pdoj=data[0][4]
        			pbed=data[0][9]
        			session['val']=[pid,pname,page,paddr,pdoj,pbed]

        			cursor.execute("select mm.medicine_nm,tm.qty_issued,mm.rate,(tm.qty_issued*mm.rate)from track_medicines 				tm,medicine_master mm where tm.medicine_id=mm.medicine_id and tm.pid=%s",(p))
        			data = cursor.fetchall() #data from database
        
        			for i in data:
        				mi.append(i)
        			session['val_mi'] = mi
        			print("session['val_mi']=",session['val_mi'])
			
			elif request.form['action'] == 'check':
				pid=session['val'][0]
				pname=session['val'][1]
				page = session['val'][2]
				paddr = session['val'][3]
				pdoj = session['val'][4]
				pbed = session['val'][5]
				status="checking"
				m_name = request.form['m_name']
				mi = session.get('val_mi')
				print("mi=",mi)
				
				conn = mysql.connect()
				cursor = conn.cursor()	
				cursor.execute("select qty_available from medicine_master where medicine_nm=%s",(m_name))
				data = cursor.fetchall() #data from database
				
				if data:
					status=" Available : Quantity available is "+ str(data[0][0]) 
					session['mstatus']="Available"
				else:
					
					status=" Not Available"
					session['mstatus']="Not Available"

				a=session.get("add")
				add=a

			elif request.form['action'] == 'Add':
				pid=session['val'][0]
				pname=session['val'][1]
				page = session['val'][2]
				paddr = session['val'][3]
				pdoj = session['val'][4]
				pbed = session['val'][5]				
				mstatus = session['mstatus']
				

				if mstatus == "Available":
					m_name = request.form['m_name']
					qty_i = request.form['qty_i']	

					conn = mysql.connect()
					cursor = conn.cursor()	
					cursor.execute("select rate from medicine_master where medicine_nm=%s",(m_name))
					rate = cursor.fetchall()
					print(rate)
					amount=int(qty_i)* rate[0][0]

					
					mi = session.get('val_mi')
					print("mi=",mi)

					if 'add' in session:
						add=session['add']							
					add.append([m_name,qty_i,rate[0][0],str(amount)])
					session['add'] = add
					a=session.get("add")
					add=a
					
				else:
					flash("medicine not available,cannot specify qty")

			elif request.form['action'] == "Issue Medicines":
				p = request.form['pid']
				m_name = request.form['m_name']	
				qty_i = request.form['qty_i']

				
        
		return render_template('issue_medicines.html',value=[pid,pname,page,paddr,pdoj,pbed],
		val_mi=mi,val_mname=m_name,val_status=status,val_qtyi=qty_i,val_add=add)
	else:
		flash("Please Login First")
		return redirect('/login')
	
@app.route('/add_diagnostics', methods=['GET', 'POST'])    
def add_diagnostics():
    global log
    if(log=='d'):
        pid=str("")
        pname=str("")
        page=str("")
        paddr=str("")
        pdoj=str("")
        pbed=str("")

        dia_names=[]
        charges="0"
        add=[]
        mi=[]
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select test_nm from diagnostics_master")
        data = cursor.fetchall() #data from database

        for i in data:
               dia_names.append(i)

   
        status=str("select test name")
        test="Select test"
   
        if request.method == 'POST':
               if request.form['action'] == 'search':
                        p = request.form['pid']
        	    
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute("select * from patients where pid=%s",(p))
                        data = cursor.fetchall() #data from database
        
                        pid=p
                        pname=data[0][2]
                        page=data[0][3]
                        paddr=data[0][6]
                        pdoj=data[0][4]
                        pbed=data[0][8]
                         
                        cursor.execute("select mm.medicine_nm,tm.qty_issued,mm.rate,(tm.qty_issued*mm.rate)from track_medicines tm,medicine_master mm 				where tm.medicine_id=mm.medicine_id and tm.pid=%s",(p))
                        data = cursor.fetchall() #data from database
                                                                                                                                                      
                        for i in data:
                                mi.append(i)

               if request.form['action'] == 'check':
                        test_nm = request.form['dia_tests']
                        if test_nm == "Select test":
                                status="select test name"
                        else:
                                conn = mysql.connect()
                                cursor = conn.cursor()
                                cursor.execute("select charges from diagnostics_master where test_nm=%s",(test_nm))
                                data = cursor.fetchall() #data from database        	    
                                charges=data[0][0]
                                status=str("Charges are Rs.")+ str(charges)                   

               if request.form['action'] == 'Add':
               		
                	test_nm = request.form['dia_tests']
                	add.append([test_nm,charges])
			
               if request.form['action'] == "Add Diagnostics":
                        print("add diagnostics")
                        '''conn = mysql.connect()
                        cursor = conn.cursor()
																																																																																								 in add:
                        cur.execute("insert into track_diagnostics values(%s,(select test_id from diagnostics_master where test_nm=%s))",(pid,i[0]))
                        conn.commit()
                        '''
    return render_template('add_diagnostics.html',val_diaNames=dia_names,value=[pid,pname,page,paddr,pdoj,pbed],
    val_status=status,val_add=add,val_test=test)

@app.route('/patients/final_billing', methods=['GET', 'POST'])    
def final_billing():
	pid=str("")
	pname=str("")
	page=str("")
	paddr=str("")
	pdoj=str("")
	pdod=str("")
	pbed=str("")

	pc=[]
	total_bp=0
    
	dc=[]
	total_bd=0

	grand=0    
   
	if request.method == 'POST':
		if request.form['action'] == 'search':
			p = request.form['pid']

			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("select * from patients where pid=%s",(p))
			data = cursor.fetchall() #data from database
        
			pid=p
			pname=data[0][2]
			page=data[0][3]
			paddr=data[0][6]
			pdoj=data[0][4]
			pdod=""
			pbed=data[0][9]

			cursor.execute("select mm.medicine_nm,tm.qty_issued,mm.rate,(tm.qty_issued*mm.rate)from track_medicines tm,medicine_master mm 				where tm.medicine_id=mm.medicine_id and tm.pid=%s",(p))
			data = cursor.fetchall() #data from database
        
			for i in data:
				pc.append(i)
				total_bp=total_bp+int(i[1])
			total_bp=str(total_bp)

			cursor.execute("select dm.test_nm, dm.charges from diagnostics_master dm, track_diagnostics td where dm.test_id=td.test_id 				and td.pid=%s",(pid)) 
			data = cursor.fetchall() #data from database

			for i in data:
				dc.append(i)
				total_bd=total_bd+int(i[1])
			total_bd=str(total_bd)

			
			grand=56000+int(total_bp)+int(total_bd)
			grand=str(grand)
			print(grand)

	return render_template('patients/final_billing.html', value=[pid,pname,page,paddr,pdoj,pdod,pbed],val_pc=pc,val_dc=dc,
    	val_total_bp=total_bp,val_total_bd=total_bd,val_grand=grand)




@app.route("/patients/registration", methods=['GET', 'POST'])
def patient_registration():
    """
    Registration for Patient
    :return:
    """
    
    if request.method == 'POST':
        patient_ssnid = request.form['patient_ssnid']
        first_name = request.form['first_name']
        
        age = request.form['age']
        date=request.form['admdate']
        bedtype=request.form['bedtype']
        address=request.form['address']
        state=request.form['state']
        city=request.form['city']
        status=request.form['status']

        conn = mysql.connect()
        cur = conn.cursor()
        
        cur.execute("INSERT INTO patients(pssnid,name,age,doa,bed,address,city,state,status) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s)",
        (patient_ssnid,first_name,age,date,bedtype,address,city,states,status))
        conn.commit()    
        
 
    return render_template('patients/registration.html')


@app.route("/patients/update", methods=['POST', 'GET'])
def patient_updation():
	p=str("")
	name=str("")
	bed=str("")
	address=str("")
	doa=str("")
	age=str("")
	
	if request.method == 'POST':
		if request.form['action'] == 'GET DETAILS':
			p = request.form['patient_ssnid']
                 
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("select * from patients where pssnid=%s",(p))
			data = cursor.fetchall() #data from database
			if data:
				name=data[0][2]
				age=data[0][3]
				doa=data[0][4]
				address=data[0][6]
				bed=data[0][5]  
			else:
				flash("please enter correct pssnid")  
			
		elif request.form['action'] == 'UPDATE':
			p = request.form['patient_ssnid']
			name=request.form['first_name']
			age=request.form['age']
			doa=request.form['admdate']
			address=request.form['address']

			conn = mysql.connect()
			cursor = conn.cursor()
			
			cursor.execute('update patients SET name=%s, age=%s, doa=%s, address=%s where pssnid=%s',(name,age,doa,address,p))
			conn.commit() 
			flash("Updated successfully")
			
	return render_template('patients/update.html',a=name,b=age,c=doa,d=address,e=bed,p=p)
        
	
     
@app.route("/patients/delete", methods=['GET', 'POST'])
def patient_deletion():
	
	p=str("")
	name=str("")
	bed=str("")
	address=str("")
	doa=str("")
	age=str("")
   
	if request.method == 'POST':
		if request.form['action'] == 'GET DETAILS':
			p = request.form['patient_ssnid']
        
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("select * from patients where pssnid=%s",(p))
			data = cursor.fetchall() #data from database
			if data:
				name=data[0][2]
				age=data[0][3]
				doa=data[0][4]
				address=data[0][6]
				bed=data[0][5]  
			else:
				flash("please enter correct pssnid") 

		if request.form['action'] == 'DELETE':
			
			p = request.form['patient_ssnid']
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("delete from patients where pssnid=%s",(p))
			conn.commit()
			

	return render_template("patients/delete.html",a=name,b=age,c=doa,d=address,e=bed,p=p)

@app.route("/patients/view", methods=['GET', 'POST'])
def patient_view():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("select * from patients where status='active' ")
	data = cursor.fetchall() #data from database
	return render_template("patients/view.html", value=data)

@app.route("/patients/search", methods=['GET', 'POST'])

def patient_search():
	p=str("")
	name=str("")
	bed=str("")
	address=str("")
	doa=str("")
	age=str("")
	
	if request.method == 'POST':
		if request.form['action'] == 'GET DETAILS':
			p = request.form['patient_ssnid']
                 
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("select * from patients where pssnid=%s",(p))
			data = cursor.fetchall() #data from database
			if data:
				name=data[0][2]
				age=data[0][3]
				doa=data[0][4]
				address=data[0][6]
				bed=data[0][5]  
			else:
				flash("please enter correct pssnid") 
	return render_template("patients/search.html",a=name,b=age,c=doa,d=address,e=bed,p=p )







