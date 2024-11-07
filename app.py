from flask import *
app = Flask(__name__)
#This secret key encrypts your user session for security reasons
app.secret_key = 'ASDF__awth$%%!=l'#16
@app.route('/')
def home():
    return render_template('home.html')

import pymysql
#establish db connection
connection = pymysql.connect(host='localhost', user='root', password='', database='airbnb_db')

@app.route('/register', methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        client_fname = request.form['client_fname']
        client_lname = request.form['client_lname']
        client_surname = request.form['client_surname']
        client_email = request.form['client_email']
        client_phone = request.form['client_phone']
        client_password = request.form['client_password']
        client_password2 = request.form['client_password2']
        client_gender = request.form['client_gender']
        client_address = request.form['client_address']


        # validations
        import re
        if client_password != client_password2:
            return render_template('register.html', password='Password does not match')

        elif len(client_password) < 8:
            return render_template('register.html', password='Password must have 8 characters')

        elif not re.search("[a-z]", client_password):
            return render_template('register.html', password='Must have a small letter')

        elif not re.search("[A-Z]", client_password):
            return render_template('register.html', password='Must have a caps letter')

        elif not re.search("[0-9]", client_password):
            return render_template('register.html', password='Must have a number')

        elif not re.search("[_@$]", client_password):
            return render_template('register.html', password='Must have a small letter')

        elif len(client_phone) < 10:
            return render_template('register.html', phone='Must be above 10 numbers')

        else:
            connection = pymysql.connect(host='localhost', user='root', password='', database='airbnb_db')

            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO registration(client_fname, client_lname, client_surname, client_email, client_phone, client_password, client_gender, client_address) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                                , (client_fname, client_lname, client_surname,
                                     client_email,client_phone, client_password,
                                     client_gender, client_address))
                connection.commit()
                return render_template('location.html', success='Saved Successfully')
            except:
                return render_template('register.html', error='Failed')
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #receive the posted email and password as variables
        email = request.form['email']
        password = request.form['password']
        #we move to the db and confirm if above details exist
        #create a cursor and execute above sql
        connection = pymysql.connect(host='localhost', user='root', password='', database='airbnb_db')

        cursor = connection.cursor()
        #execute the sql,provide email and password to fit %s placeholders
        cursor.execute("SELECT * FROM registration where client_email = %s and client_password = %s", (email, password))
        #check if a match was found
        if cursor.rowcount == 0:
            return render_template('login.html', error='Wrong Credentials')
        elif cursor.rowcount == 1:
            session['user'] = email
            return redirect('/locations')
        else:
            return render_template('login.html', error='Error Occurred, Try Later')
    else:
        return render_template('login.html')

@app.route('/locations')
def locations():
    #create ur query
    #run ur query
    #create a cursor used to execute sql
    cursor = connection.cursor()
    #now use the cursor to execute the sql
    cursor.execute("SELECT * FROM houses_tbl")
    #check how many rows are returned
    if cursor.rowcount == 0:
        return render_template("locations.html", msg='Not Available at the moment')
    else:
        rows = cursor.fetchall()
        return render_template('locations.html', rows=rows)


@app.route('/singlelocations/<house_id>')
def singlelocations(house_id):
    #create ur query
    #run ur query
    #create a cursor used to execute sql
    cursor = connection.cursor()
    #now use the cursor to execute the sql
    cursor.execute("SELECT * FROM houses_tbl WHERE house_id = %s", (house_id))
    #check how many rows are returned
    if cursor.rowcount == 0:
        return render_template("singlelocations.html", msg='Not available at the moment')
    else:
        row = cursor.fetchone()
        return render_template('singlelocations.html', row=row)

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/login')

@app.route('/reviews',methods=['POST','GET'])
def reviews():
    if request.method == 'POST':
        user = request.form['user']
        house_id = request.form['house_id']
        message = request.form['message']
        #Do a table for reviews
        sql = "insert into reviews(user,house_id,message)values(%s,%s,%s)"
        cursor = connection.cursor()
        try:
            cursor.execute(sql, (user, house_id, message))
            connection.commit()

            flash("Thank you for your review")
            return redirect(url_for('singlelocations', house_id=house_id ))
        except:
            flash("Review not posted")
            flash("Please try again")
            return redirect(url_for('singlelocations', house_id=house_id))
    else:
        return

@app.route('/contact',methods = ['POST','GET'])
def contact():
    if request.method == 'POST':
        contact_name = request.form['contact_name']
        contact_email = request.form['contact_email']
        contact_message = request.form['contact_message']

        sql = "insert into contact(contact_name,contact_email,contact_message)values(%s,%s,%s)"
        cursor = connection.cursor()
        try:
            cursor.execute(sql, (contact_name, contact_email, contact_message))
            connection.commit()
            flash("Message sent successfully")
            return redirect('/locations')
        except:
            flash("Message not sent")
            flash("Please try again")
            return render_template('contact.html', error='Error Occurred, Try Later')
    else:
        return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)