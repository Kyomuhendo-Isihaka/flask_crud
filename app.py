from flask import Flask,redirect,render_template,request, session, url_for
import mysql.connector

app = Flask(__name__)

app.secret_key = "hello world"
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "flaskdb"
    
)
mycursor = conn.cursor()

@app.route("/", methods =["POST", "GET"])
def login():
    msg = ''
    if request.method =="POST":
        email = request.form['email']
        password = request.form['password']
        
        if email and password:
            mycursor.execute("SELECT * FROM account WHERE email=%s", (email,))
            account = mycursor.fetchone()
                                  
            if account:
                session['loggedin']= True
                session['userId'] = account[0]
                session['username']=account[1]
                
                return redirect(url_for('dashboard'))
            else:
                msg = "Invalid Email or Wrong Password"
                              
    return render_template("login.html", msg=msg)

@app.route("/logout")
def logout():
    session.pop['loggedin', None]
    session.pop['id', None]
    session.pop['username', None]
    return redirect(url_for('login'))

@app.route("/signup", methods = ["POST", "GET"])
def signup():
    if request.method == "POST":
        unname = request.form['uname']
        email = request.form['email']
        password = request.form['password']
        conf_pass = request.form['conf_password']
        
        if password == conf_pass:
            mycursor.execute("INSERT INTO account(fullname, email, password) VALUES(%s, %s,%s)", (unname,email,password))
            conn.commit()
            return redirect("/")
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    if 'loggedin' in session:
        mycursor.execute("SELECT * FROM student")
        students = mycursor.fetchall()
        return render_template("index.html", students=students, username=session['username'])
    return redirect(url_for('login'))

@app.route("/add_student", methods=["POST", "GET"])
def addStudent():
    if request.method == "POST":
        studentName = request.form['name']
        studentEmail = request.form['email']
        studentCourse = request.form['course']
        
        mycursor.execute("INSERT INTO student(student_name, email, course) VALUES(%s, %s, %s)", (studentName, studentEmail, studentCourse))
        conn.commit()
    return redirect("/dashboard")

@app.route("/editStudent/<id>" , methods=["POST","GET"])
def editStudent(id):
    if request.method == "POST":
        studentName = request.form['st_name']
        email = request.form['email']
        course = request.form['course']
        mycursor.execute("""UPDATE student SET student_name=%s, email=%s, course=%s WHERE id=%s""",(studentName, email, course, id))
        conn.commit()
        return redirect("/dashboard")
    
@app.route("/deleteStudent/<id>", methods=["POST", "GET"])
def deleteStudent(id):
    mycursor.execute("DELETE FROM student WHERE id=%s", (id,))
    conn.commit()
    return redirect("/dashboard")
        



if __name__ == "__main__":
    app.run(debug=True)