from flask import Blueprint, render_template, session, flash, redirect, url_for
from ..database.manager import AuthDbManager
from .. import limiter

website = Blueprint('website', __name__)


@website.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@website.route('/register', methods=['GET'])
def register():
    return render_template("auth/register.html")


@website.route('/login', methods=['GET'])
def login():
    return render_template("auth/login.html")


@ website.route('/reset', methods=['GET'])
@ limiter.exempt
def reset():
    return render_template("auth/reset.html")


@website.route('/reset/<reset_id>', methods=['GET'])
def reset_with_token(reset_id):
    db = AuthDbManager()
    if db.is_allowed_for_resetting(reset_id) and db.is_reset_link_valid(reset_id):
        session["reset_id"] = reset_id
        return render_template("auth/reset_with_token.html")
    else:
        return "", 401


@ website.route('/dashboard', methods=['GET'])
@ limiter.exempt
def dashboard():
    if not session.get("username"):
        flash("Ta akcja wymaga zalogowania!")
        return redirect(url_for('website.login'))
    return render_template('passwords/dashboard.html')


@ website.route('/dashboard_more', methods=['GET'])
@ limiter.exempt
def dashboard_more():
    if not session.get("username"):
        flash("Ta akcja wymaga zalogowania!")
        return redirect(url_for('website.login'))
    return render_template('passwords/dashboard_more.html')


@ website.route('/logout', methods=['GET'])
@ limiter.exempt
def logout():
    session.clear()
    return redirect(url_for('website.home'))
