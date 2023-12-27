from cs50 import SQL

from flask import redirect, render_template, session
from functools import wraps

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///kabisote.db")

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def is_item_owner(id):
    owner = db.execute("SELECT user_id FROM quiz WHERE id= ?", id)
    isowner = False;
    if owner[0]['user_id'] == session.get("user_id"):
        isowner = True;
    return isowner

def get_next_number(n):
    getlast = db.execute("SELECT question_number FROM quiz_item Where quiz_id=? ORDER BY  question_number DESC LIMIT 1", n);
    next = 0;
    if getlast:
        next = getlast[0]['question_number'] + 1
    else:
        next = 1;



    return next
