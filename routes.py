"""
@author: Sachin Nandakumar

This script routes to different pages with necessary parameters

"""


from flask import Flask, render_template, flash, redirect, url_for, request
from flask_table import Table, Col, LinkCol, ButtonCol
from config import Config
from app.forms import LoginForm, UpdateForm
import re

# --------------------------------------------------------------------------------------------

app = Flask(__name__)
app.config.from_object(Config)

# User database
USER_DB = {} 
email_validation_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

# --------------------------------------------------------------------------------------------

# Declaring Table required for displaying users
class ItemTable(Table):
    first_name = Col('First Name')   
    last_name = Col('Last Name') 
    email = Col('Email')
    edit_details = LinkCol('Edit user', endpoint='update_user', url_kwargs=dict(first_name='first_name', last_name='last_name', email='email'))
    delete_details = LinkCol('Delete user', endpoint='update', url_kwargs=dict(email='email'))

class Item(object):
    def __init__(self, email, first_name, last_name):
        self.first_name = first_name    
        self.last_name = last_name
        self.email = email
    
# --------------------------------------------------------------------------------------------

@app.route('/create', methods=['GET', 'POST'])
def create():
    '''
        This function helps to add a new user
            The user's first name, last name and email details should be provided
            onSubmit -> The forms are validated and stored to the dictionary
            
        Validation:
            The email column is checked using regex
            All input elements are mandatory
            Could add: Validation for text input
    '''
    form = LoginForm()
    if form.validate_on_submit():
        if(re.search(email_validation_regex,form.email.data)): 
            if form.email.data not in USER_DB.keys():
                USER_DB[form.email.data] = {'first_name':form.first_name.data, 'last_name':form.last_name.data}
                return redirect(url_for('home', message='added', name=request.form["first_name"]))
            else:
                flash(f'User already exists!')
        else:
            flash(f'Email address is invalid!')
    return render_template('create.html', title='Add User', form=form)

@app.route('/')    
@app.route('/home')
def home():
    '''
        Home page of the website
        Also used as a redirect after adding/updating a user
    '''
    added_user = request.args.get('name')
    message = request.args.get('message')
    return render_template('home.html', title='Home', message=message, name=added_user )

@app.route('/display_records')
def display_records():
    '''
        Update the records of all the users created so far and saved in the RAM.
        Provides option to update and delete a created user
    '''
    global USER_DB 
    email = request.args.get('email')
    delete_info = ''
    if email:
        del USER_DB[email]
        delete_info = email
        
    data = USER_DB
    items = []
    
    table_length = len(list(data))
    return render_template('display_records.html', title='User Records', data=[data, table_length, delete_info])

@app.route('/update_user', methods=['GET', 'POST', 'DELETE'])
def update_user():
   '''  
        This function updates the user details
            * If the user updates with a new email address, it is validated with the user DB to 
                see it is already taken by some previous users
            * Else:
                * If the email address remains the same -> No change
                * If first name, last name or email changes -> value gets updated
   '''
   global USER_DB
   form = UpdateForm()
   form.first_name.data = request.args.get('first_name')
   form.last_name.data = request.args.get('last_name')
   form.email.data = request.args.get('email')
   old_email_data = request.args.get('email')
   
   if form.validate_on_submit():
        if request.form["email"] == old_email_data:
            USER_DB[request.form["email"]] = {'first_name':request.form["first_name"], 'last_name':request.form["last_name"]}
            return redirect(url_for('home', message='updated', name=request.form["first_name"]))
        elif request.form["email"] in USER_DB.keys():
            flash(f'User with this email address already exists!')
        else:
            if(re.search(email_validation_regex,request.form["email"])): 
                USER_DB[request.form["email"]] = {'first_name':request.form["first_name"], 'last_name':request.form["last_name"]}
                del USER_DB[old_email_data]
                return redirect(url_for('home', message='updated', name=request.form["first_name"]))
            else:
                flash(f'Email address is invalid!')
   return render_template('update_user.html', title='Update User Details', data=[form, form.first_name.data, form.last_name.data, form.email.data])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port='2827', debug=True)