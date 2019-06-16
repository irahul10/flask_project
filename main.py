import time
from flask import Flask,render_template,redirect,request,url_for,session
import pymysql
from mylib import *


app=Flask(__name__)

app.secret_key = "super secret key"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['T1']
        password=request.form['T2']
        conn=pymysql.connect(host=gethost(),port=getport(),user=getdbuser(),passwd=getdbpass(),db=getdb(),autocommit=True)
        cur=conn.cursor()
        sql="select * from logindata where email='"+email+"' AND password='"+password+"'"
        cur.execute(sql)
        n=cur.rowcount
        if n>0:
            row=cur.fetchone()
            usertype=row[2]
            #Create session
            session['email']=email
            session['usertype']=usertype
            #Redirect to page
            if usertype=='admin':
                return redirect(url_for('admin_home'))
            elif usertype=='student':
                return redirect(url_for('student_home'))
        else:
            return render_template('login_error.html')
    else:
        return render_template('login.html')

#admin's Program

@app.route('/admin_home')
def admin_home():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            return render_template('admin_home.html',e1=email)
        else:
            return render_template("authorization_error.html")

    else:
        return render_template("authorization_error.html")



@app.route('/logout')
def logout():
    if 'usertype'in session:
        session.pop('usertype', None)
        session.pop('email', None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))



@app.route('/admin_registration',methods=['GET','POST'])
def admin_registration():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            if request.method=='POST':
                name=request.form['T1']
                address=request.form['T2']
                contact=request.form['T3']
                email=request.form['T4']
                password=request.form['T5']
                conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='qbank',autocommit=True)
                cur=conn.cursor()
                sql = "insert into admindata values ('" + name + "','" + address + "','" + contact + "','" + email + "')"
                cur.execute(sql)
                n = cur.rowcount
                sql1="insert into logindata values ('"+ email +"','"+ password +"','admin')"
                cur.execute(sql1)
                m=cur.rowcount

                if(n==1):
                    return render_template('admin_registration.html', result='success')
                else:
                    return render_template('admin_registration.html', result='failure')
                if(m==1):
                    return render_template('admin_registration.html', result='login success')
                else:
                    return render_template('admin_registration.html', result='login failure')
            else:
                return render_template('admin_registration.html')
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")


@app.route('/show_admin')
def show_admin():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='qbank')
            cur=conn.cursor()
            cur.execute("SELECT * from admindata")
            result = cur.fetchall()
            return render_template('show_admin.html', result=result)
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")

@app.route('/admin_change_password', methods=['GET','POST'])
def admin_change_password():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            if request.method=='POST':
                oldpass=request.form['T1']
                newpass=request.form['T2']
                conn=pymysql.connect(host=gethost(), port=getport(), user=getdbuser(), passwd=getdbpass(), db=getdb(),autocommit=True)
                cur=conn.cursor()
                cur.execute("update logindata set password='" + newpass + "' where email='" + email + "' AND password='" + oldpass + "'")

                n = cur.rowcount
                msg = "Error: Cannot change password. Try again"
                if n > 0:
                    msg = "Password changed successfully"
                return render_template('admin_change_password.html',result=msg)
            else:
                return render_template('admin_change_password.html')
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")

@app.route('/admin_profile',methods=['GET','POST'])
def admin_profile():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            if request.method=='POST':
                name=request.form['T1']
                address=request.form['T2']
                contact=request.form['T3']

                conn = pymysql.connect(host=gethost(), port=getport(), user=getdbuser(), passwd=getdbpass(), db=getdb(),
                                       autocommit='True')
                cur = conn.cursor()
                sql="update admindata set name='"+name+"',address='"+address+"',contact='"+contact+"' where email='"+email+"'"
                cur.execute(sql)
                return redirect(url_for('admin_home'))
            else:
                conn = pymysql.connect(host=gethost(), port=getport(), user=getdbuser(), passwd=getdbpass(), db=getdb(),
                                       autocommit='True')
                cur = conn.cursor()
                cur.execute("SELECT * FROM admindata where email='" + email + "'")
                n = cur.rowcount
                if n > 0:
                    obj = cur.fetchone()
                    return render_template('admin_profile.html', result=obj)
                else:
                    return render_template('admin_profile.html', result1="No Data Found", email=email)
        else:
            return render_template("authorization_error.html")

    else:
        return render_template("authorization_error.html")


#Student's Program's are here

@app.route('/student_home')
def student_home():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='student':
            return render_template('student_home.html',e1=email)
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")


@app.route('/student_registration',methods=['GET','POST'])
def student_registration():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            if request.method == 'POST':
                name = request.form['T1']
                branch = request.form['T2']
                rollno = request.form['T3']
                contact = request.form['T4']
                email = request.form['T5']
                password= request.form['T6']
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='qbank', autocommit=True)
                cur = conn.cursor()
                sql = "insert into studentdata value ('" + name + "','" + branch + "','" + rollno + "','" + contact + "','" + email + "')"
                #conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='qbank', autocommit=True)
                #cur = conn.cursor()
                cur.execute(sql)
                n = cur.rowcount

                sql1="insert into logindata values ('"+ email +"','"+ password +"','student')"
                cur = conn.cursor()
                cur.execute(sql1)
                m=cur.rowcount
                if (n == 1):
                    return render_template('student_registration.html', result='success')
                else:
                    return render_template('student_registration.html', result='failure')
                if (m == 1):
                    return render_template('student_registration.html', result='login success')
                else:
                    return render_template('student_registration.html', result='login failure')
            else:
                return render_template('student_registration.html')
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")



@app.route('/show_student')
def show_student():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='qbank')
            cur=conn.cursor()
            cur.execute("SELECT * from studentdata")
            result=cur.fetchall()
            return render_template('show_student.html',result=result)
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")



@app.route('/edit_student',methods=['GET','POST'])
def edit_student():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            if request.method=='POST':
                email=request.form['email']
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='qbank')
                cur = conn.cursor()
                cur.execute("SELECT * from studentdata where email='" + email + "'")
                result = cur.fetchall()
                return render_template('edit_student.html', result=result)
            else:
                return redirect(url_for('show_student'))
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")



@app.route('/edit_student1',methods=['GET','POST'])
def edit_student1():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            if request.method=='POST':
                name=request.form['T1']
                branch = request.form['T2']
                rollno = request.form['T3']
                contact = request.form['T4']
                email = request.form ['T5']
                conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='qbank',autocommit=True)
                cur=conn.cursor()
                sql = "update studentdata set name='" + name + "',branch='" + branch + "',rollno='" + rollno + "',contact='" + contact + "' where email='" + email + "'"
                cur.execute(sql)
                n = cur.rowcount
                if(n==1):
                    return render_template('edit_student1.html',result='success')
                else:
                    return render_template('edit_student1.html',result='failure')
            else:
                return redirect(url_for('show_student'))
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")



@app.route('/delete_student',methods=['GET','POST'])
def delete_student():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            if request.method=='POST':
                email=request.form['email']
                conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='qbank')
                cur=conn.cursor()
                cur.execute("select * from studentdata where email='" + email + "'")
                n=cur.rowcount
                if n>0:
                    result=cur.fetchone()
                    return render_template('delete_student.html',result=result)
                else:
                    return render_template('delete_student.html',result1='no data found')
            else:
                return redirect(url_for('show_student'))
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")



@app.route('/delete_student1',methods=['GET','POST'])
def delete_student1():
    if request.method=='POST':
        name=request.form['T1']
        branch=request.form['T2']
        rollno = request.form['T3']
        contact = request.form['T4']
        email = request.form['T5']
        conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='qbank',autocommit=True)
        cur=conn.cursor()
        sql="delete from studentdata where email='" + email + "'"
        cur.execute(sql)
        n=cur.rowcount
        if(n==1):
            return render_template('delete_student1.html',result='success')
        else:
            return render_template('delete_student1.html',result='failure')
    else:
        return redirect(url_for('show_student'))


@app.route('/ask_question',methods=['GET','POST'])
def ask_question():
    if 'usertype' in session:
        usertype=session['usertype']
        e1=session['email']
        if usertype=='student':
            if request.method=='POST':
                subject=request.form['T1']
                question=request.form['T2']
                t=time.time()
                tt=int(t)
                conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='qbank',autocommit=True)
                cur=conn.cursor()
                sql= "insert into qdata values (0,'"+ subject +"','"+ question +"',"+str(tt)+",'"+e1+"')"
                cur.execute(sql)
                n = cur.rowcount
                if(n==1):
                    return render_template('ask_question.html',result='success')
                else:
                    return render_template('ask_question.html', result='failure')
            else:
                return render_template('ask_question.html')
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")


@app.route('/student_change_password', methods=['GET','POST'])
def student_change_password():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='student':
            if request.method == 'POST':
                oldpass=request.form['T1']
                newpass=request.form['T2']
                conn = pymysql.connect(host=gethost(), port=getport(), user=getdbuser(), passwd=getdbpass(), db=getdb(),autocommit=True)

                cur = conn.cursor()
                cur.execute("update logindata set password='"+newpass+"' where email='" + email + "' AND password='"+oldpass+"'")
                n = cur.rowcount
                msg="Error: Cannot change password. Try again"
                if n>0:
                    msg="Password changed successfully"
                return render_template('student_change_password.html', result=msg)
            else:
                return render_template('student_change_password.html')
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")


@app.route('/student_profile',methods=['GET','POST'])
def student_profile():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype=='student':
            if request.method=='POST':
                name=request.form['T1']
                branch = request.form['T2']
                rollno = request.form['T3']
                contact = request.form['T4']

                conn = pymysql.connect(host=gethost(), port=getport(), user=getdbuser(), passwd=getdbpass(), db=getdb(),autocommit='True')
                cur = conn.cursor()
                sql="update studentdata set name ='"+ name +"',branch='"+ branch +"',rollno='"+ rollno +"',contact='"+  contact+"' where email='"+ email +"'"
                cur.execute(sql)
                return redirect(url_for('student_home'))
            else:
                conn = pymysql.connect(host=gethost(), port=getport(), user=getdbuser(), passwd=getdbpass(), db=getdb(),autocommit='True')
                cur = conn.cursor()
                cur.execute("SELECT * FROM studentdata where email='" + email + "'")
                n = cur.rowcount
                if n>0:
                    obj=cur.fetchone()
                    return render_template('student_profile.html',result=obj)
                else:
                    return render_template('student_profile.html',result1="No Data Found",email=email)
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")

@app.route('/show_student_question')
def show_student_question():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='student':
            conn=pymysql.connect(host=gethost(), port=getport(), user=getdbuser(), passwd=getdbpass(), db=getdb())
            cur=conn.cursor()
            cur.execute("select * from qdata")
            result=cur.fetchall()
            return render_template('show_student_question.html',result=result)
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")


@app.route('/solve',methods=['GET','POST'])
def solve():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='student':
            if request.method=='POST':
                qno=request.form['H1']
                conn=pymysql.connect(host=gethost(), port=getport(), user=getdbuser(), passwd=getdbpass(), db=getdb())
                cur=conn.cursor()
                cur.execute("select * from qdata where qno="+qno)
                result=cur.fetchone()
                return render_template('solve.html',row=result)
            else:
                return render_template('show_student_question.html')
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")


@app.route('/solve1',methods=['GET','POST'])
def solve1():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='student':
            if request.method=='POST':

                qno=request.form['H1']
                ans=request.form['T1']
                t=time.time()
                tt=int(t)
                solby=email

                conn=pymysql.connect(host=gethost(), port=getport(), user=getdbuser(), passwd=getdbpass(), db=getdb(),autocommit=True)
                cur=conn.cursor()
                cur.execute("insert into solutions values(0,"+str(qno)+",'"+ans+"',"+str(tt)+",'"+solby+"')")
                n=cur.rowcount
                if n==1:
                    return render_template('solve1.html',data="Answer Saved")
                else:
                    return render_template('solve1.html', data="Cannot Save Answer")
            else:
                return render_template('show_student_question.html')
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")


@app.route('/show_my_questions')
def show_my_questions():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='student':
            conn=pymysql.connect(host=gethost(), port=getport(),user=getdbuser(), passwd=getdbpass(), db=getdb())
            cur=conn.cursor()
            cur.execute("select * from qdata where qby='"+ email +"'")
            result = cur.fetchall()
            return render_template('show_my_questions.html',result=result)
        else:
            return render_template("authorization_error.html")
    else:
        return render_template("authorization_error.html")





if __name__=='__main__':
    app.run(debug=True)