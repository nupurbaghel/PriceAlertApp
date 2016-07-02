__author__ = "Nupur Baghel"
import src.config as config
from functools import wraps

from flask import session, flash, redirect, url_for, request


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            flash(u'You need to be signed in for this page.')
            return redirect(url_for('users.login_user', next=request.path))
        return f(*args, **kwargs)

    return decorated_function

def requires_admin_permissions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            flash(u'You need to be signed in for this page.')
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in config.ADMINS:
            flash('You need to be an admin to do desired changes')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)

    return decorated_function