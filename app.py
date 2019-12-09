import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'python_fyp'

db = MySQL(app)

# User Login
@app.route("/", methods=['GET', 'POST'])
def users():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        fetchdata = db.connection.cursor()  # MySQLdb.cursor.DictCursor
        fetchdata.execute("SELECT * FROM register WHERE email=%s and password=%s", (email, password,))
        logindata = fetchdata.fetchall()
        fetchdata.close()
        if len(logindata) > 0:
            session['email'] = request.form['email']
            # Current this is no working
            if request.form['role'] == "Student":
                return redirect('/student')
            else:
                return redirect('/teacher')

        else:
            return "Error! Password/Name not match"

    return render_template('userlogin.html')
# Teacher Panel
@app.route("/teacher", methods=['GET', 'POST'])
def teacher():
    fetchdata = db.connection.cursor()
    fetchdata.execute("SELECT * FROM register WHERE role='Student'")
    logindata = fetchdata.fetchall()
    fetchdata.close()

    return render_template('teacher.html', register=logindata)


@app.route("/update", methods=["POST", "GET"])
def attendance():
    if request.method == "POST":
        details = request.form
        id = details['id']
        attendance = details['attendance']
        cur = db.connection.cursor()
        cur.execute("""UPDATE register SET attendance=%s  WHERE id=%s""", (attendance,  id))
        db.connection.commit()
        return redirect('/teacher')
# For add Announcement
@app.route("/announcement", methods=["POST", "GET"])
def announcement():

    if request.method == "POST":
        details = request.form
        announcement = details['announcement']

        connect = db.connection.cursor()
        connect.execute("INSERT INTO register(announcement) VALUES (%s)",(announcement))
        run=db.connection.commit()
        connect.close()
        if run:
            return redirect('/teacher')
        else:
            print("Error")

    return render_template('teacher.html')
# -------/Teacher Panel-------

#Student Panel
@app.route("/student", methods=["POST", "GET"])
def studentshow():
    return render_template('student.html')

# Admin Login
@app.route("/admin", methods=['GET', 'POST'])
def admin():
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        fetchdata = db.connection.cursor()  # MySQLdb.cursor.DictCursor
        fetchdata.execute("SELECT * FROM admin WHERE name=%s and password=%s", (name, password,))
        logindata = fetchdata.fetchall()
        fetchdata.close()
        if len(logindata) > 0:
            return redirect('/dashbord')

        # return render_template('index.html')
        else:
            return "Error! Password/Name not match"

    return render_template('adminlogin.html')


@app.route("/dashbord")
def index():
    fetchdata = db.connection.cursor()
    fetchdata.execute("SELECT * FROM register")
    logindata = fetchdata.fetchall()
    fetchdata.close()

    return render_template('index.html', register=logindata)


@app.route("/adduser", methods=["POST", "GET"])
def adduser():
    if request.method == "POST":
        details = request.form
        name = details['name']
        fathername = details['fathername']
        email = details['email']
        password = details['password']
        address = details['address']
        role = details['role']
        connect = db.connection.cursor()
        connect.execute("INSERT INTO register(name, fathername, email,password, address, role) VALUES (%s, %s, %s, %s)",
                        (name,fathername,  email, password,address, role))
        db.connection.commit()
        connect.close()
        return redirect('/dashbord')
    return render_template('addusers.html')


@app.route("/update", methods=["POST", "GET"])
def update():
    if request.method == "POST":
        details = request.form
        id = details['id']
        name = details['name']
        fathername = details['fathername']
        email = details['email']
        password = details['password']
        address = details['address']
        role = details['role']
        cur = db.connection.cursor()
        cur.execute("""UPDATE register SET name=%s,fathername =%s, email=%s,password=%s,address=%s, role=%s WHERE 
        id=%s""",
                    (name,fathername, email, password,address, role, id))
        db.connection.commit()
        return redirect('/dashbord')
		# flash('Data Updated Successfully!')
	# return render_template('update.html')


@app.route("/delete/<string:id>", methods=["GET"])
def delete(id):
    # flash("Record has been Deleted Successully")
    cur = db.connection.cursor()
    cur.execute("DELETE FROM register WHERE id=%s", (id))
    db.connection.commit()
    return redirect('/dashbord')

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=5003, debug="TRUE")