from src.models.users.user import User
import src.models.users.errors as UserErrors

__author__ = "Nupur Baghel"
from flask import Blueprint, request, session, redirect, url_for, render_template

user_blueprint=Blueprint('users',__name__)

@user_blueprint.route('/login',methods=['GET','POST'])
def login_user():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        try:
            if User.is_login_valid(email,password):
                session['email']=email
                return redirect(url_for('.user_alerts'))
        except UserErrors.UserError as e:
                return e.message

    return render_template("users/login.html")

@user_blueprint.route('/register',methods=['GET','POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for('.user_alerts'))
            else:
                return "Error saving user"
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/register.html")

@user_blueprint.route('/logout')
def logout_user():
    session['email']=None
    return redirect(url_for ('home'))

@user_blueprint.route('/alerts')
def user_alerts():
    user=User.get_by_email(session['email'])
    alerts=user.get_alerts()
    return render_template('users/alerts.html',alerts=alerts)

@user_blueprint.route('/check_alerts/<string:user_id>')
def check_alerts(user_id):
    pass