from flask import Flask,session,flash,render_template,redirect,session,url_for,request,send_from_directory,send_file
from uuid import uuid1
import sqlite3 as sql
import os
import shutil
from certificategenerator import certificategenerate
from functools import wraps
from sendmail import SendMail

app = Flask(__name__)
app.secret_key = 'Alexas'
DOWNLOAD_FOLDER = r'G:\certificate-Generator projevct\downlodds'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
global msg 
global con 


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        else:
            flash(u'You need to login first','danger')
            return render_template("index.html")
    return wrap
    

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        #try:
        username = request.form['uname']
        password = request.form['psw']
        con = sql.connect("database.db") 
        cur = con.cursor()
        cur.execute("SELECT * FROM SIGNUPLIST WHERE USERNAME = ? and PASSWORD = ?",(username,password,))
        account = cur.fetchone()
        #account = cur.execute("""SELECT * FROM SIGNUPLIST WHERE USERNAME =' %s '"""%(username)) 
        print(account)
        cur.close() 
        if account:
            if account[3] != 'Issuer':
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['is_admin'] = False
                return render_template("cg1.html")
            else:
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['is_admin'] = True
                return render_template("admin.html") 
        else:
            flash("Invalid Credentials")   
        #except:
            #flash("check later and try again")
    
    return render_template("index.html")
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('is_admin',None)
   session.pop('username', None)
   flash("Successfully Logout")
   # Redirect to login page
   return redirect(url_for('main'))


@app.route('/addcred',methods = ['POST', 'GET'])
def addcred():
    if request.method == 'POST':
      try:
         fullname = request.form['fullname']
         username = request.form['username']
         email = request.form['email']
         contacts = request.form['contacts']
         password = request.form['password']
         confirmpassword = request.form['confirmpassword']
         accounttype = request.form['type']
         if password == confirmpassword:
            con = sql.connect("database.db") 
            cur = con.cursor()
            cur.execute("INSERT INTO SIGNUPLIST(FULLNAME,USERNAME,EMAILID,ACCOUNTTYPE,CONTACTNO,PASSWORD) VALUES (?,?,?,?,?,?)",(fullname,username,email,accounttype,contacts,password) )
            con.commit()
            con.close()
            flash("Registered Successfully Please Login ")
         else:
            flash("password and confirm password are not similar")
      except:
         con.rollback()
         con.close()
         flash("check later and try again")
      
      finally:
         return render_template("index.html")

@app.route('/certgen',methods = ['POST', 'GET'])
def certgen():
    if request.method == 'POST':
      try:
         fullname = request.form['Fullname']
         registeredno = request.form['Admissionno']
         CourseName = request.form['GraduationDegree']
         courseyear = request.form['YStudying']
         specialization = request.form['specialization']
         joiningyear = request.form['jdate']
         courseduration = request.form['cduration']
         emailid = request.form['emailid']
         print(fullname,registeredno,CourseName,courseyear,specialization,joiningyear,courseduration,emailid)
         con = sql.connect("database.db") 
         cur = con.cursor()
         cur.execute("INSERT INTO certificateissuelist(fullname,registeredno,coursename,courseyear,specialization,joiningyear,courseduration,emailid) VALUES (?,?,?,?,?,?,?,?)",(fullname,registeredno,CourseName,courseyear,specialization,joiningyear,courseduration,emailid))
         con.commit()
         con.close()
         flash("Wait for 5 Hours and check your mail or Visit Registrar Office")
         return render_template("cg1.html")
      except:
          return "<h1>Error , Oops Server Error</h1>"
    else:
        return "<h1>Error 404 ,  File Not Found</h1>"

@app.route('/adminpanel')
@login_required
def adminpanel():
    try:
        if session['is_admin'] == True:
            return render_template("admin.html")
        else:
            return render_template('index.html')
    except:
        return "<h1>Error 404 Not Found</h1>"

@app.route("/pendinglist")
@login_required
def pendinglist():
    try:
        if session['is_admin'] == True:
            con = sql.connect("database.db")
            con.row_factory = sql.Row 
            cur = con.cursor()
            cur.execute("SELECT * FROM certificateissuelist")
            rows = cur.fetchall()
            return render_template('pendinglist.html',rows = rows)
        else:
            return render_template('index.html')
    except:
        return "<h1>Error , Oops Server Error</h1>"

@app.route('/studentlist')
@login_required
def studentlist():
    try:
        if session['is_admin'] == True:
            con = sql.connect("database.db") 
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM SIGNUPLIST")
            rows = cur.fetchall()
            return render_template('studentlist.html',rows=rows)
        else:
            return render_template('index.html')
    except:
        return "<h1>Error , Oops Server Error</h1>"

@app.route('/generate',methods = ['POST', 'GET'])
@login_required
def generate():
    try:
        if session['is_admin'] == True:
            fullname = request.form.get('fullname')
            registeredno = request.form.get('rollno')
            CourseName = request.form.get('cname')
            courseyear = request.form.get('cyear')
            specialization = request.form.get('spztion')
            joiningyear = request.form.get('jyear')
            courseduration = request.form.get('cduration')
            emailid = request.form.get('emailid')
            print("+generate function",fullname,registeredno,CourseName,courseyear,specialization,joiningyear,courseduration,emailid)
            certificategenerate(fullname,registeredno,CourseName,courseyear,specialization,joiningyear,courseduration,emailid)
            con = sql.connect("database.db")
            con.row_factory = sql.Row 
            cur = con.cursor()
            cur.execute("SELECT * FROM certificateissuelist")
            rows = cur.fetchall()
            return render_template('issuelist.html',rows=rows)
        else:
            return render_template('index.html')
    except:
        return "<h1>Error , Oops Server Error</h1>"

@app.route('/sendmail',methods = ['POST', 'GET'])
@login_required
def sendmail():
    fullname = request.form.get('fullname')
    registeredno = request.form.get('rollno')
    emailid = request.form.get('emailid')
    filename = registeredno+".jpg"
    attachment = os.path.join( app.config['DOWNLOAD_FOLDER'],filename)
    SendMail(attachment,emailid,fullname)
    print("+sendmail",fullname,registeredno,emailid)
    con = sql.connect("database.db")
    con.row_factory = sql.Row 
    cur = con.cursor()
    cur.execute("SELECT * FROM certificateissuelist")
    rows = cur.fetchall()
    return render_template('issuelist.html',rows=rows)

if __name__ == "__main__":
    app.run(debug=True)