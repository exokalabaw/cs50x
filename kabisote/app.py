from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import escape
import json

from helpers import login_required, is_item_owner, get_next_number
app = Flask(__name__)



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///kabisote.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    if session.get("user_id") is None:
        return render_template("login.html")
    else:
        return redirect("my-quizzes")

@app.route("/leaderboards")
@login_required
def leaderboards():

    return render_template("leaderboards.html")

@app.route("/add-quiz", methods=["GET", "POST"])
@login_required
def add_quiz():
    if request.method == "POST":
        title = request.form.get("title")
        details = request.form.get("desc")
        public = False
        if request.form.get("public"):
            public = True
        newquiz = db.execute("INSERT INTO quiz(user_id, public, name, details, published) VALUES(?,?,?,?,false)", session.get("user_id"), public, escape(title), escape(details))
        print("return is ", newquiz)
        flash("New quiz saved, add questions", "success")
        return redirect(f"/edit-quiz/{newquiz}")
    else:
        return render_template("add-quiz.html", item = None, script="addquiz.js")
@app.route("/delete/<id>")
@login_required
def delete_quiz(id):
    intid = int(id)
    tandid = db.execute("SELECT name FROM quiz WHERE id IS ?", intid)
    if is_item_owner(intid):
        deletedquestions = db.execute("DELETE FROM quiz_item WHERE quiz_id IS ?", intid)
        deleted = db.execute("DELETE FROM quiz WHERE id IS ?", intid)

        flash("Quiz has been deleted")
    else:
        flash("what are you doing?")
    return redirect("/")

# add edit quiz details features here
@app.route("/edit-quiz-details/<id>", methods=["GET", "POST"])
@login_required
def edit_quiz_details(id):
    item = db.execute("SELECT * FROM quiz WHERE id = ?", id)
    if request.method == "POST":
        changedtitle = escape(request.form.get('title'))
        changedbody = escape(request.form.get('desc'))
        changedp = False
        if request.form.get('public'):
            changedp = True
        print(f"changed p {changedp}")
        if item[0]['name'] != changedtitle or item[0]['details'] != changedbody or item[0]['public'] != changedp:
            edited = db.execute("UPDATE quiz SET name = ?, details = ?, public = ? WHERE id = ?", changedtitle,changedbody,changedp,id)
            flash('updated', 'success')
        else:
            flash('nothing changed','error')
        return redirect(f"/edit-quiz/{id}")
    else:
        return render_template("add-quiz.html", item = item, script="addquiz.js")

@app.route("/edit-quiz/<id>")
@login_required
def edit_quiz(id):
    if is_item_owner(id):
        item = db.execute("SELECT * FROM quiz WHERE id = ?", id)
        quit = db.execute("SELECT * FROM quiz_item WHERE quiz_id = ? ORDER BY question_number ASC", id)
        for q in quit:
            al = f"[{q['answer_list']}]"
            al = eval(al)
            q['answer_list'] = al
            q['answer_options']=eval(q['answer_options'])
        return render_template("edit-quiz.html", item=item, questions=quit, name="editquiz", script="editquiz.js")
    else:
        flash("what are you doing?")
        return redirect("/")

@app.route("/add-textbox/<quizid>")
@login_required
def add_textbox(quizid):
    intqid = int(quizid)


    if is_item_owner(intqid):
        return render_template("add-textbox.html", script="addtextbox.js", quizid=intqid)
    else:
        flash("what are you doing?")
        return redirect("/")

@app.route("/add-multi/<quizid>")
@login_required
def add_multi(quizid):
    intqid = int(quizid)

    if is_item_owner(intqid):
        return render_template("add-multi.html", script="addmulti.js", quizid=intqid)
    else:
        flash("what are you doing?")
        return redirect("/")
@app.route("/edit-quiz-item/<itemid>")
@login_required
def edit_quiz_item(itemid):
    qit = db.execute("SELECT * FROM quiz_item WHERE id IS ?", itemid)
    qit = qit[0]
    qid = qit['quiz_id']
    intqid =int(qid)
    if is_item_owner(intqid):
        type = qit["item_type"]
        al = f"[{qit['answer_list']}]"
        al = eval(al)
        qit['answer_list'] = al
        qit['answer_options']=eval(qit['answer_options'])
        if type == "textbox":
            return render_template("edit-textbox.html", script="addtextbox.js", quizid=intqid, details=qit)
        elif type == "multiple_choice":
            return render_template("edit-multi.html", script="addmulti.js", quizid=intqid, details=qit)
        else:
            flash("what is you doenn")
            return redirect("/")
    else:
        flash("what is you doenn")
        return redirect("/")
@app.route("/save-order/<quizid>", methods=["POST"])
@login_required
def save_order(quizid):
    if request.method == "POST":
        d = db.execute("SELECT * FROM quiz_item WHERE quiz_id IS ?", quizid)
        for item in d:
            id = item['id']
            dict = request.form
            submitted_order_number = dict[str(id)]
            if submitted_order_number != item['question_number']:
                savepos = db.execute("UPDATE quiz_item SET question_number=? WHERE id IS ?",int(submitted_order_number), id)
                print("things have changed /n")
            print(f"submitted order number is { submitted_order_number}, original number is {item['question_number']} ")
        flash("arrangement updated", "success")
        return redirect(f'/edit-quiz/{quizid}')




@app.route("/public-quizzes")
def public_quizzes():
    plist = db.execute("SELECT DISTINCT quiz.id, users.username as username, users.id as userid, DATE(quiz.updated) as date, quiz.name, quiz.details FROM quiz INNER JOIN users ON quiz.user_id = users.id WHERE quiz.public = 1 ORDER BY updated DESC")

    return render_template("public-quizzes.html", plist = plist, userid=None)

@app.route("/public-quizzes/<userid>")
def public_quizzes_user(userid):
    plist = db.execute("SELECT DISTINCT quiz.id, users.username as username, users.id as userid, DATE(quiz.updated) as date, quiz.name, quiz.details FROM quiz INNER JOIN users ON quiz.user_id = users.id WHERE users.id = ? AND quiz.public = 1 ORDER BY updated DESC", userid)

    return render_template("public-quizzes.html", plist = plist, userid = userid)

@app.route("/my-quizzes")
@login_required
def my_quizzes():
    mylist = db.execute("SELECT id, DATE(updated) as date, name, details, user_id, public FROM quiz WHERE user_id=? ORDER BY updated DESC", int(session["user_id"]))
    # print("my list ", mylist)
    return render_template("my-quizzes.html", mylist = mylist)

@app.route("/quiz/<id>", methods=["GET", "POST"])
def tests(id):
    print("the id is ", id)
    qi = db.execute("SELECT * FROM quiz WHERE id = ?", id)
    questions = db.execute("SELECT * FROM quiz_item WHERE quiz_id = ? ORDER BY question_number ASC", id)
    public = qi[0]['public']
    userid = qi[0]['user_id']
    userid = int(userid)

    for q in questions:
        q['answer_options'] = eval(q['answer_options'])

    if public:
        return render_template("quiz.html", item = qi, questions = questions, script="quiz.js", name="quiz")
    else:
        if  is_item_owner(id):
            return render_template("quiz.html", item = qi, questions = questions, script="quiz.js", name="quiz")
        else:
            flash("What are you doing?")
            return redirect("/public-quizzes")




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if session.get("user_id") is not None:
        return redirect("/")

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("no username", "error")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("no password", "error")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("wrong credentials", "error")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Successfully logged in", "success")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/signout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("signed out", "success")
    return redirect("/")




@app.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("user_id") is not None:
        return redirect("/")
    """Register user"""
    if request.method == "POST":
        un = request.form.get("username")
        pw = request.form.get("password")
         # Ensure username was submitted
        if not un:
            return apology("must provide username", 400)
            # return print("no username")
        # Ensure password was submitted
        usernamefound = db.execute("SELECT username FROM users WHERE username is ? ", un)
        print("username  part : ", un, usernamefound )
        if usernamefound:
            flash("Username not available", "error")
            return render_template("signup.html")
            # return print("went to usernamefound should make an error")
        elif not pw or not request.form.get("confirmation"):
            flash("No password", "error")
            return render_template("signup.html")
            # return print("should go to no password submitted")
        # Ensure passwords match
        elif pw != request.form.get("confirmation"):
            flash("Passwords don't match", "error")
            return render_template("signup.html")
            # return print("passwords didn't match")
        newpw = generate_password_hash(pw)
        returnedaccount = db.execute("INSERT INTO users(username, hash) VALUES (?,?)", un, newpw)
        # return print("returned account ?", returnedaccount)
        # Remember which user has logged in
        session["user_id"] = returnedaccount
        flash("Sign up successful", "success")
        return redirect("/")


    else:
        return render_template("signup.html")

@app.route("/add-multi/submit", methods=["POST"])
@login_required
def submit_multi():
    dict = request.form
    question = dict['question']
    quiz_id = dict['quizid']
    quiz_id = int(quiz_id)
    answer_options = []
    if is_item_owner(quiz_id):
        i = 0
        # place the id in a variable, check if the id is owner by the current user
        for key in dict:
            if i >= 2:
                if key == 'answer':
                    indexer = i-3
                    print(f"indexer {indexer}")
                    answer_options[indexer]["correct"] = 1
                else:
                    toappend = {"pa":"", "correct":0}
                    toappend["pa"] = dict[key]
                    answer_options.append(toappend)
            print("answer options is updating ?", answer_options )
            i =i+1
            jd = json.dumps(answer_options)
            emptyjson = json.dumps({})
        insert = db.execute("INSERT INTO quiz_item(question, quiz_id, answer_options, is_case_sensitive, question_number, item_type ) VALUES (?,?,?, false, ?, 'multiple_choice')",question,quiz_id,jd, get_next_number(quiz_id))
        flash("new question saved", "success")
        return redirect(f"/edit-quiz/{quiz_id}")
    else:
        flash("what are you doing?","error")
        return redirect("/")
@app.route("/edit-multi/submit", methods=['POST'])
@login_required
def edit_multi_submit():
    dict = request.form
    question = dict['question']
    quiz_id = dict['quizid']
    quiz_id = int(quiz_id)
    item_id = dict['itemid']
    item_id = int(item_id)
    answer_options = []
    if is_item_owner(quiz_id):
        i = 0
        # place the id in a variable, check if the id is owner by the current user
        for key in dict:
            if i >= 3:
                if key == 'answer':
                    indexer = i-4
                    print(f"indexer {indexer}")
                    answer_options[indexer]["correct"] = 1
                else:
                    toappend = {"pa":"", "correct":0}
                    toappend["pa"] = dict[key]
                    answer_options.append(toappend)
            print("answer options is updating ?", answer_options )
            i =i+1
            jd = json.dumps(answer_options)
            emptyjson = json.dumps({})
        insert = db.execute("UPDATE quiz_item SET question=?, answer_options=? WHERE id=?",question, jd,item_id )
        flash("question updated","success")
        return redirect(f"/edit-quiz/{quiz_id}")
    else:
        flash("what are you doing?", "error")
        return redirect("/")

@app.route("/add-textbox/submit", methods=["POST"])
@login_required
def submit_text():
    dict = request.form
    question = dict['question']
    quiz_id = dict['quizid']
    quiz_id = int(quiz_id)
    possible_answers = []
    emptyjson = json.dumps({})
    if is_item_owner(quiz_id):
        i = 0
        for value in dict:
            if i >= 2:
               e = dict[value]
               print("e is", e)
               possible_answers.append(e)
            i = i+1
        print("possible answers", possible_answers)
        paj = json.dumps(possible_answers)
        inserter = db.execute("INSERT INTO quiz_item(question, quiz_id, answer_options , answer_list, is_case_sensitive, question_number, item_type ) VALUES(?,?,?,?,0,?,'textbox')",question,quiz_id,emptyjson,paj, get_next_number(quiz_id))
        print("added : ", inserter)
        flash("new question saved", "success")
        return redirect(f"/edit-quiz/{quiz_id}")
    else:
        flash("what are you doing?", "error")
        return redirect("/")

@app.route("/edit-textbox/submit", methods=['POST'])
@login_required
def edit_textbox_submit():
    dict = request.form
    print(dict)
    question = dict['question']
    quiz_id = dict['quizid']
    quiz_id = int(quiz_id)
    item_id = dict['itemid']
    item_id = int(item_id)
    possible_answers = []
    emptyjson = json.dumps({})
    if is_item_owner(quiz_id):
        i = 0
        for value in dict:
            if i >= 3:
               e = dict[value]
               print("e is", e)
               possible_answers.append(e)
            i = i+1
        print("possible answers", possible_answers)
        paj = json.dumps(possible_answers)
        editer = db.execute("UPDATE quiz_item SET answer_list=?, question=?WHERE id IS ?",paj, question, item_id)
        flash("question updated", "success")
        return redirect(f"/edit-quiz/{quiz_id}")
    else:
        flash("eh?","error")
        return redirect("/")


@app.route("/delete-quiz-item/<itemid>")
@login_required
def delete_quiz_item(itemid):
    itemowner = db.execute("SELECT id FROM quiz WHERE id IS(SELECT quiz_id FROM quiz_item WHERE id IS ?)",itemid)
    io = itemowner[0]['id']
    if is_item_owner(io):
        deleted = db.execute("DELETE FROM quiz_item WHERE id IS ?",itemid)
        flash("item deleted", "success")
        return redirect(f"/edit-quiz/{io}")
    else:
        flash("what are you doing?", "error")
        return redirect("/")

