from flask import redirect, render_template, session
from functools import wraps
from werkzeug.exceptions import HTTPException, InternalServerError

def erro(message, code=400):
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("erro.html", top=code, bottom=escape(message)), code

def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return erro(e.name, e.code)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def not_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id"):
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function