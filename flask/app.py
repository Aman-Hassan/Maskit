from flask_mysqldb import MySQL
from flask import Flask, redirect, url_for, render_template, request, flash, json, session
# from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import date, datetime
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
app.config['MYSQL_USER'] = 'username'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'mydatabase'
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
        print(Username,password)
        confirmation = request.form.get("confirmation")
        if not Username:
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must confirm password",400)
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
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
    user = cur.fetchall()
    cur.close()
    return render_template ("index.html",name = user[0][2])


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
    if category_id is []:
        cur.close()
        return apology("No Such Category",404) 
    cur.execute("SELECT * FROM Communities WHERE category_id = %s", (category_id[0],))
    communities = cur.fetchall()
    cur.execute("SELECT community_id FROM Communities_Joined WHERE user_id = %s",(session["user_id"],))
    joined_communities = cur.fetchall()
    l = []
    for i in range(len(communities)):
        flag = False
        for x in joined_communities:
            if (x == (communities[i][0],)):
                flag = True
                break
        if flag:
            l.append((communities[i],True))
        else:
            l.append((communities[i],False))

    # print(l)
    cur.close() 
    return render_template("basicpage.html", name = user[0][2], categories=categories,communities = l, category_name=category_name )


@app.route("/Follow/<string:category_name>/<string:community_name>")
@login_required
def FollowInshowByCategory(category_name,community_name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
    user = cur.fetchall()
    cur.execute("SELECT * FROM Categories")
    categories = cur.fetchall()
    cur.execute("SELECT id FROM Communities WHERE Name = %s", (community_name,))
    community_id = cur.fetchall()
    cur.execute("SELECT community_id FROM Communities_Joined WHERE user_id = %s",(user[0][0],))
    isjoined = cur.fetchall()
    if not (community_id[0] in isjoined):
        cur.execute("INSERT into Communities_Joined (user_id,community_id) Values (%s,%s)",(user[0][0],community_id[0]))
        mysql.connection.commit()
        cur.close() 
        return redirect(f"/category/{category_name}")

    else:
        cur.execute("DELETE FROM Communities_Joined WHERE user_id = %s AND community_id = %s", (user[0][0], community_id[0]))
        mysql.connection.commit()
        cur.close() 
        return redirect(f"/category/{category_name}")




@app.route("/Top_Communities")
@login_required
def Top_Communities():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
    user = cur.fetchall()
    cur.execute("SELECT * FROM Communities ORDER BY Points DESC LIMIT 10")
    communities = cur.fetchall()
    cur.execute("SELECT * FROM Categories")
    categories = cur.fetchall()
    cur.close()
    print(communities)
    return render_template("TopCommunities.html",name = user[0][2], categories=categories,communities = communities, category_name = "Top Communities" )



@app.route("/Top_Posts")
@login_required
def Top_Posts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
    user = cur.fetchall()
    cur.execute("SELECT * FROM Posts ORDER BY Votes DESC LIMIT 10")
    posts = cur.fetchall()
    cur.execute("SELECT * FROM Categories")
    categories = cur.fetchall()
    cur.close()
    return render_template("TopPosts.html",name = user[0][2], categories=categories,posts = posts, category_name = "Top Posts" )

@app.route("/Top_Karma")
@login_required
def Top_Karma():
    return redirect("/")


@app.route("/Following")
@login_required
def Following():
    return redirect("/")


@app.route("/Top_Board")
@login_required
def Board():
    return redirect("/")




@app.route("/category_post/<string:category_name>")
@login_required
def show_posts_given_category(category_name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
    user = cur.fetchall()
    cur.execute("SELECT * FROM Categories")
    categories = cur.fetchall()
    cur.execute("SELECT category_id FROM Categories where Name = %s", (category_name,))
    category_id = cur.fetchall()
    if category_id is []:
        cur.close()
        return apology("No Such Category",404) 
    cur.execute("SELECT * FROM Posts WHERE category_id = %s", (category_id[0][0],))
    posts = cur.fetchall()
    cur.close() 
    return render_template("category-page-top-posts.html", name = user[0][2], categories=categories,posts = posts, category_name=category_name )

    

@app.route("/community/<string:community_name>")
@login_required
def show_community(community_name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
    user = cur.fetchall()
    cur.execute("SELECT * FROM Communities where Name = %s", (community_name,))
    community = cur.fetchall()
    if community is None or len(community)!=1:
        cur.close()
        return apology("No Such Community",404) 
    community_id = community[0][0]
    cur.execute("SELECT * FROM Posts WHERE community_id = %s", (community_id,))
    posts = cur.fetchall()
    cur.close() 
    return render_template("community-page.html", name = user[0][2], posts= posts, community = community[0])


@app.route("/uprofile/<string:name>")
@login_required
def user_profile(name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
    user = cur.fetchall()
    cur.execute("SELECT * FROM Users WHERE Username = %s",(name,))
    users = cur.fetchall()
    if users is None:
        cur.close()
        return apology("No Such User",404)
    creator_id = users[0][0]
    cur.execute("SELECT * FROM Posts WHERE creator_id = %s",(creator_id,))
    posts = cur.fetchall()
    cur.close()
    return render_template("profile.html", name = user[0][2], posts= posts, users= users)


@app.route("/post/<int:post_id>")
@login_required
def post_page(post_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
    user = cur.fetchall()
    cur.execute("SELECT * FROM Posts WHERE id = %s", (post_id,))
    details = cur.fetchall()
    if details is None :
        cur.close()
        return apology("No Such Posts ", 404)
    time = details[0][1]
    title = details[0][2]
    content = details[0][3]
    creator_id = details[0][5]
    community_id = details[0][6]
    cur.execute("SELECT Name FROM Users WHERE id = %s", (creator_id))
    creators = cur.fetchall()
    creator = creators[0]
    cur.execute("SELECT Name FROM Community WHERE id = %s", (community_id))
    communities = cur.fetchall()
    community = communities[0]
    cur.close()
    return render_template("post-page.html" ,name = user[0][2],time = time, title = title, content = content, creator = creator, community = community )
    


@app.route("/add_post", methods = ["GET","POST"])
@login_required
def Add_post ():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
        user = cur.fetchall()
        cur.execute("SELECT Name FROM Categories")
        categories = cur.fetchall()
        cur.execute("SELECT Name FROM Communities")
        communities = cur.fetchall()
        cur.close()
        if (user == []):
            return redirect("/login")
        return render_template("create-post.html",name = user[0][2],categories=categories,communities = communities)
    if request.method == "POST":
        Post_title = request.form.get("add_post_title")
        Post_body = request.form.get("add_post_body")
        category = request.form.get("Category")
        community = request.form.get("Community")
        if not Post_title:
            return apology("must provide Post_title", 400)
        elif not Post_body:
            return apology("must provide Post_body", 400)
        elif not category:
            return apology("must provide category",400)
        elif not community:
            return apology("must provide community",400)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
        user = cur.fetchall()
        cur.execute("SELECT category_id FROM Categories where Name = %s", (category,))
        category_id = cur.fetchall()
        if category_id is None:
            cur.close()
            return apology("No Such Category",404) 
        cur.execute("SELECT Name FROM Communities WHERE category_id = %s", (category_id[0],))
        communities = cur.fetchall()
        cur.execute("SELECT id FROM Communities where Name = %s" , (community,))
        community_id = cur.fetchall()
        if community_id is None :
            cur.close()
            return apology("No such Community",404)
        cur.execute("INSERT INTO Posts (Title, Content, Creator_id, Community_id ,Category_id) VALUES (%s,%s,%s,%s,%s)", (Post_title, Post_body, (session["user_id"]), community_id[0], category_id[0]))
        mysql.connection.commit()
        cur.close() 
        return render_template("index.html",name = user[0][2])

@app.route("/create_community", methods = ["GET","POST"])
@login_required
def Create_community ():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
        user = cur.fetchall()
        cur.execute("SELECT Name FROM Categories")
        categories = cur.fetchall()
        cur.close()
        return render_template("create-community.html",name = user[0][2],categories=categories)
    if request.method == "POST":
        community_name = request.form.get("create_community_name")
        community_description = request.form.get("create_community_description")
        category = request.form.get("Category")
        if not community_name :
            return apology("must provide community_name ", 400)
        elif not community_description:
            return apology("must provide community_description ", 400)
        elif not category:
            return apology("must provide category",400)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
        user = cur.fetchall()
        cur.execute("SELECT * FROM Communities where Name = %s", (community_name,))
        rows = cur.fetchall()
        if (len(rows)!=0):
            cur.close()
            return apology("Community username is taken",400)
        cur.execute("SELECT category_id FROM Categories where Name = %s", (category,))
        category_id = cur.fetchall()
        if category_id is None:
            cur.close()
            return apology("No Such Category",404) 
        cur.execute("SELECT Name FROM Communities WHERE category_id = %s", (category_id[0],))
        cur.execute("INSERT INTO Communities (Name, ABOUT, category_id,Points) VALUES (%s,%s,%s,%s)", (community_name, community_description, category_id[0],1))
        mysql.connection.commit()
        cur.close() 
        return render_template("index.html",name = user[0][2])
