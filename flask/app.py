from flask_mysqldb import MySQL
from flask import Flask, redirect, url_for, render_template, request, flash, json, session
# from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
from flask_session import Session
from helper import login_required, apology
import datetime
# import db
# Configure app
app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'Mask'
mysql = MySQL(app)
Session(app)


# To Ensure that Client Always sees the fresh content and there is no cache
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/login", methods = ["GET"])
def login():
    session.clear()
    return render_template("login.html")


@app.route("/login", methods = ["POST"])
def login_post():
    session.clear()
    name = request.form.get("name")
    password = request.form.get("password")
    if not name:
        return apology("must provide username", 400)
    elif not password:
        return apology("must provide password", 400)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE Username = %s", (name,)) 
    rows = cur.fetchall()
    if len(rows) != 1 or not check_password_hash(rows[0][3], password):
        return apology("invalid username and/or password", 403)
    session["user_id"] = rows[0][0]
    cur.close()
    return redirect("/")







@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        Username = request.form.get("name")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not Username:
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must cofirm password",400)
        elif request.form.get("password")!=request.form.get("confirmation"):
            return apology("password is not same as Confirm Password",400)


        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Users WHERE Username = %s", (Username,))
        rows = cur.fetchall()
        if (len(rows)!=0):
            cur.close()
            return apology("Username is taken",400)
        cur.execute("INSERT INTO Users (Username, Password, About, Created) VALUES (%s,%s,'I am using Maskit',NOW())", (Username, generate_password_hash(password)))
        cur.execute("SELECT * FROM Users")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        session["user_id"] = data[0][0]
        return login()



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/")
@login_required
def index():
    return show_communities_given_category("Academics")


@app.route("/category/<string:category_name>")
@login_required
def show_communities_given_category(category_name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
    user = cur.fetchall()
    cur.execute("SELECT * FROM Categories")
    categories = cur.fetchall()
    cur.execute("SELECT category_id FROM Categories where Name = %s", (category_name,))
    category_id = cur.fetchall()
    if category_id is None:
        return apology("No Such Category",404) 
    cur.execute("SELECT * FROM Communities WHERE category_id = %s", (category_id[0]))
    communities = cur.fetchall()
    cur.close() 
    return render_template("index.html", name = user[0][2], categories=categories,communities = communities, category_name=category_name )

@app.route("/community/<string:community_name>")
@login_required
def show_community(community_name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
    user = cur.fetchall()
    cur.execute("SELECT * FROM Categories")
    categories = cur.fetchall()
    cur.execute("SELECT * FROM Communities where Name = %s", (community_name,))
    community = cur.fetchall()
    if community is None or len(community)!=1:
        return apology("No Such Community",404) 
    cur.close() 
    return render_template("community.html", name = user[0][2], categories=categories,community = communtiy[0])


@app.route("/settings")
@login_required
def Settings():
    return render_template("setting.html")

@app.route("/profile")
@login_required
def Profile():
    return render_template("profile.html")
# @app.route("/post")














# @app.route("/")
# def index():
#     cur = mysql.connection.cursor()
#     cur.execute('''SELECT * FROM Categories''')
#     data = cur.fetchall()
#     cur.close()
#     print(data[0][1])
#     return render_template("index.html",categories = data)


# def add_user():
#     cur = mysql.connection.cursor()
#     cur.execute('''INSERT INTO users (created, Username,Password,Karma, About) VALUES (%s, %s,%s,%s,%s)''', ('timw','John','passw','12','dknkde'))
#     mysql.connection.commit()
#     cur.close()
#     print()
#     print()
#     print()
#     print("User Addeed Successfully")
#     print()
#     print()
#     print()
#     return 'User added successfully!'




# def get_post(post_id):
#     conn = get_db_connection()
#     post = conn.execute('SELECT * FROM posts WHERE id = ?',
#                         (post_id,)).fetchone()
#     conn.close()
#     if post is None:
#         abort(404)
#     return post

# @app.route("/")
# def index():
#     cur = mysql.connection.cursor()
#     cur.execute('''SELECT * FROM Users''')
#     data = cur.fetchall()
#     cur.close()
#     return str(data)
# @app.route('/<int:post_id>')
# def post(post_id):
#     post = get_post(post_id)
#     return render_template('post.html', post=post)

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         session["name"] = request.form.get("name")
#         return redirect("/")
#     return render_template("login.html")


# @app.route("/logout")
# def logout():
#     session["name"] = None
#     return redirect("/")