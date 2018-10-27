from flask import Flask,render_template,redirect,request,session,flash
import re
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


app=Flask(__name__)

@app.route('/')
def index():
    
    query ="select* from drinks"
    mysql =connectToMySQL('cudycoffee')
    alldrinks=mysql.query_db(query)
    print(alldrinks)

    return render_template('index.html',alldrinks=alldrinks)

@app.route('/adddrinks',methods=['POST'])
def add_drinks():
    print(request.form)
    data ={
        "name" :  request.form['coffee'],
        "price": request.form['price']
    }
    query ="insert into drinks(name, price,created_at,updated_at) values(%(name)s,%(price)s,now(),now());"
    mysql =connectToMySQL('cudycoffee')
    mysql.query_db(query,data)
  
    return redirect('/')
  
@app.route('/edit/<int:drink_id>')
def edit_coffee(drink_id):
    data ={
        "drink_id": drink_id
    }
    query = "select * from drinks where id =%(drink_id)s"
    mysql =connectToMySQL('cudycoffee')
    drink=mysql.query_db(query,data)
    drink=drink[0]
    return render_template('edit.html',drink=drink)

@app.route('/editcoffee/<int:drink_id>',methods=['POST'])
def update(drink_id):
    data={
        "drink_id":drink_id,
        "price":request.form['price'],
        "name":request.form['coffee']
    }
    query="update drinks set name =%(name)s,price =%(price)s where id = %(drink_id)s"
    mysql =connectToMySQL('cudycoffee')
    drink=mysql.query_db(query,data)
    return redirect('/')

@app.route('/delete/<int:drink_id>')
def delete(drink_id):
    data={
        "drink_id":drink_id,
    }
    query="delete from drinks where id = %(drink_id)s"
    mysql =connectToMySQL('cudycoffee')
    drink=mysql.query_db(query,data)
    return redirect('/')
if __name__=='__main__':
    app.run(debug=True)

