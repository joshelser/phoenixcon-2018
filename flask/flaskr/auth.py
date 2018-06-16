import functools

from flask import (
            Blueprint, flash, g, redirect, render_template, request, session, url_for
            )
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
	with db.cursor() as c:
	    error = None

	    if not username:
		error = 'Username is required.'
	    elif not password:
		error = 'Password is required.'

	    c.execute('SELECT id FROM user WHERE username = ?', (username,))
	    row = c.fetchone()
	    if row is not None:
		error = 'User {} is already registered.'.format(username)

	    if error is None:
		c.execute(
		    'UPSERT INTO user (id, username, password) VALUES (next value for flaskr_user_seq, ?, ?)',
		    (username, generate_password_hash(password))
		)
		db.commit()
		return redirect(url_for('auth.login'))

	    flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
	with db.cursor() as cursor:
	    cursor.execute('SELECT username, password, id FROM user WHERE username = ?', (username,))
	    user = cursor.fetchone()

	print user
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[1], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[2]
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
    	with get_db().cursor() as c:
    	    c.execute(
		       'SELECT id, username FROM user WHERE id = ?', (user_id,)
    	    )
            g.user = c.fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
