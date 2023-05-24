from flask_mysqldb import MySQL
from flask import Flask, redirect, url_for, render_template, request, flash, json, session
# from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import date, datetime
from flask_session import Session
from helper import login_required, apology
import datetime
import requests
import uuid
import json
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
        # print(Username,password)
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


@app.route("/Follow/<string:community_name>")
@login_required
def FollowInshowByCategory(community_name):
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
        return redirect(request.referrer)

    else:
        cur.execute("DELETE FROM Communities_Joined WHERE user_id = %s AND community_id = %s", (user[0][0], community_id[0]))
        mysql.connection.commit()
        cur.close() 
        return redirect(request.referrer)




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
    # print(communities)
    return render_template("TopCommunities.html",name = user[0][2], categories=categories,communities = communities, category_name = "Top Communities" )



@app.route("/search_by_post")
@login_required
def search_by_post():
    a = request.args.get("s")
    a = a.lower()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
    user = cur.fetchall()
    cur.execute("SELECT * FROM Posts WHERE title LIKE %s LIMIT 50", ("%"+a+"%",))
    posts = cur.fetchall()
    post = []
    for i in range(len(posts)):
        cur.execute("SELECT Username FROM Users WHERE id = %s", (posts[i][5],))
        name = cur.fetchall()
        cur.execute("SELECT Name FROM Communities WHERE id = %s", (posts[i][6],))
        communityn = cur.fetchall()
        cur.execute("SELECT Name FROM Categories WHERE category_id = %s", (posts[i][7],))
        categoryn = cur.fetchall()
        post.append([name[0][0],communityn[0][0],categoryn[0][0],posts[i]])
    cur.close()
    return render_template("searchpost.html",posts = post, name = user[0][2],s=a)

@app.route("/search_by_posts/<string:a>")
@login_required
def search_by_posts(a):
    if (a==None):
        return redirect("/")
    a = a.lower()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
    user = cur.fetchall()
    cur.execute("SELECT * FROM Posts WHERE title LIKE %s LIMIT 50", ("%"+a+"%",))
    posts = cur.fetchall()
    post = []
    for i in range(len(posts)):
        cur.execute("SELECT Username FROM Users WHERE id = %s", (posts[i][5],))
        name = cur.fetchall()
        cur.execute("SELECT Name FROM Communities WHERE id = %s", (posts[i][6],))
        communityn = cur.fetchall()
        cur.execute("SELECT Name FROM Categories WHERE category_id = %s", (posts[i][7],))
        categoryn = cur.fetchall()
        post.append([name[0][0],communityn[0][0],categoryn[0][0],posts[i]])
    cur.close()
    return render_template("searchpost.html",posts = post, name = user[0][2],s=a)

@app.route("/search_for_author/<string:a>")
@login_required
def search_for_author(a):
    if (a==None):
        return redirect("/")
    a = a.lower()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
    user = cur.fetchall()
    cur.execute("SELECT * FROM Users WHERE Username LIKE %s LIMIT 50", ("%"+a+"%",))
    authors = cur.fetchall()
    
    cur.close()
    return render_template("searchauthor.html",results = authors,name = user[0][2],s=a)

@app.route("/search_for_community/<string:a>")
@login_required
def search_for_community(a):
    if (a==None):
        return redirect("/")
    a = a.lower()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
    user = cur.fetchall()
    cur.execute("SELECT * FROM Communities WHERE Name LIKE %s LIMIT 50", ("%"+a+"%",))
    results = cur.fetchall()
    cur.execute("SELECT community_id FROM Communities_Joined WHERE user_id = %s",(session["user_id"],))
    joined_communities = cur.fetchall()
    l = []
    for i in range(len(results)):
        flag = False
        for x in joined_communities:
            if (x == (results[i][0],)):
                flag = True
                break
        if flag:
            l.append((results[i],True))
        else:
            l.append((results[i],False))
    cur.close()
    print()
    print()
    print(l)
    return render_template("searchpagecommunity.html",results = l,name = user[0][2],s=a)




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

@app.route("/Vote/<int:post_id>/<int:response>")
@login_required
def Vote(post_id,response):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Post_Vote WHERE post_id = %s", (post_id,))
    votes = cur.fetchall()
    vote = 0
    add = 0
    flag = False
    for x in votes :
        if x[1] == session["user_id"]:
            vote = x[2]
            flag = True
    if vote == 0:
        if response == 1:
            add = 1
        elif response == 0:
            add = -1
    elif vote == 1:
        if response == 1:
            add = 0
        elif response == 0:
            add = -1
    elif vote == -1:
        if response == 1:
            add = 1
        elif response == 0:
            add = 0
    vote = vote + add
    if flag:
        cur.execute("UPDATE Post_Vote SET vote = %s WHERE (post_id,user_id) = (%s,%s) ", (vote,post_id,session["user_id"],))
    else:
        cur.execute("INSERT into Post_Vote (post_id,user_id,vote) VALUES (%s,%s,%s)", (post_id,session["user_id"],vote))
    
    cur.execute("SELECT * FROM Posts WHERE id = %s", (post_id,))
    post = cur.fetchall()
    old_vote = post[0][4]
    new_vote = old_vote + add
    cur.execute("UPDATE Posts SET Votes = %s WHERE id = %s ", (new_vote,post_id,))
    cur.execute("SELECT * FROM Users WHERE id = %s", (session["user_id"],))
    users = cur.fetchall()
    old_karma = users[0][4]
    new_karma = old_karma + add
    cur.execute("UPDATE Users SET Karma = %s WHERE id = %s ", (new_karma,session["user_id"],))
    mysql.connection.commit()
    cur.close()
    return redirect(request.referrer)

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
    post = []
    for i in range(len(posts)):
        cur.execute("SELECT Username FROM Users WHERE id = %s", (posts[i][5],))
        name = cur.fetchall()
        cur.execute("SELECT Name FROM Communities WHERE id = %s", (posts[i][6],))
        communityn = cur.fetchall()
        cur.execute("SELECT Name FROM Categories WHERE category_id = %s", (posts[i][7],))
        categoryn = cur.fetchall()
        post.append([name[0][0],communityn[0][0],categoryn[0][0],posts[i]])
    cur.close() 
    # print()
    # print()
    # print()
    # print(post)
    return render_template("category-page-top-posts.html", name = user[0][2], categories=categories,posts = post, category_name=category_name )

    

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
    cur.execute("SELECT USERNAME FROM Users WHERE id = %s",(community[0][6],))
    creator=cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM Communities_Joined WHERE community_id = %s",(community_id,))
    members=cur.fetchall()
    cur.execute("SELECT * FROM Posts WHERE community_id = %s", (community_id,))
    posts = cur.fetchall()
    post = []
    cur.execute("SELECT community_id FROM Communities_Joined WHERE user_id = %s",(session["user_id"],))
    joined_communities = cur.fetchall()
    flag = False
    for x in joined_communities:
        if (x == (community_id,)):
            flag = True
            break
    for i in range(len(posts)):
        cur.execute("SELECT Username FROM Users WHERE id = %s", (posts[i][5],))
        name = cur.fetchall()
        cur.execute("SELECT Name FROM Communities WHERE id = %s", (posts[i][6],))
        communityn = cur.fetchall()
        cur.execute("SELECT Name FROM Categories WHERE category_id = %s", (posts[i][7],))
        categoryn = cur.fetchall()
        post.append([name[0][0],communityn[0][0],categoryn[0][0],posts[i]])
    cur.close() 
    return render_template("community-page.html", name = user[0][2],flag = flag, posts= post, community = community[0],date=community[0][5].date(), creator=creator[0][0], members=members[0][0])


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
    post = []
    for i in range(len(posts)):
        cur.execute("SELECT Username FROM Users WHERE id = %s", (posts[i][5],))
        name = cur.fetchall()
        cur.execute("SELECT Name FROM Communities WHERE id = %s", (posts[i][6],))
        communityn = cur.fetchall()
        cur.execute("SELECT Name FROM Categories WHERE category_id = %s", (posts[i][7],))
        categoryn = cur.fetchall()
        post.append([name[0][0],communityn[0][0],categoryn[0][0],posts[i]])
    cur.execute("SELECT * FROM Communities_Joined WHERE user_id = %s ",(creator_id,))
    follows = cur.fetchall()
    Following = len(follows)
    cur.close()
    return render_template("profile.html", name = user[0][2], posts= post, users= users,Following=Following)


@app.route("/post/<int:post_id>",methods=['GET','POST'])
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
    img=details[0][8]
    vote = details[0][4]

    cur.execute("SELECT Username FROM Users WHERE id = %s", (creator_id,))
    creators = cur.fetchall()
    creator = creators[0]
    cur.execute("SELECT Name FROM Communities WHERE id = %s", (community_id,))
    communities = cur.fetchall()
    community = communities[0]
    cur.close()
    if request.method == 'GET':
        return render_template("post-page.html" ,name = user[0][2],time = time.time(),date=time.date(), title = title, content = content,vote=vote, creator = creator, community = community,post_id=post_id,img=img, selected_lang = 'en')
    # else:                                                                              
    #     text = content
    #     to_lang = request.form.get("target_language")
    #     subscription_key = ''                                                                                 This whole part of ML API will now not work beacuse I removed Subscription Key from here.
    #     endpoint = 'https://api.cognitive.microsofttranslator.com/translate'
    #     location = 'southeastasia'

    #     headers = {
    #         'Ocp-Apim-Subscription-Key': subscription_key,
    #         'Ocp-Apim-Subscription-Region': location,
    #         'Content-type': 'application/json',
    #         'X-ClientTraceId': str(uuid.uuid4())
    #     }
    #     params = {
    #         'api-version': '3.0',
    #         'from': 'en',
    #         'to': to_lang
    #     }
    #     body = [{
    #         'text': text
    #     }]
    #     response = requests.post(endpoint, headers=headers, params=params, json=body)
    #     # print(response)
    #     response.raise_for_status()
    #     content = response.content
    #     # try:
    #     #     json_content = json.loads(content)
    #     #     print("Response content is valid JSON")
    #     # except ValueError:
    #     #     print("Response content is not valid JSON")
    #     translated_text = response.json()[0]['translations'][0]['text']
    #     return render_template("post-page.html" ,name = user[0][2],time = time.time(),date=time.date(), title = title, content = translated_text,vote=vote, creator = creator,img =img ,community = community ,post_id=post_id,selected_lang=to_lang)
    
# @app.route("/post_translate/<int:post_id>",methods=['POST'])
# @login_required
# def post_page_translate(post_id):
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
#     user = cur.fetchall()
#     cur.execute("SELECT * FROM Posts WHERE id = %s", (post_id,))
#     details = cur.fetchall()
#     if details is None :
#         cur.close()
#         return apology("No Such Posts ", 404)
#     time = details[0][1]
#     title = details[0][2]
#     content = details[0][3]
#     creator_id = details[0][5]
#     community_id = details[0][6]
#     cur.execute("SELECT Username FROM Users WHERE id = %s", (creator_id,))
#     creators = cur.fetchall()
#     creator = creators[0]
#     cur.execute("SELECT Name FROM Communities WHERE id = %s", (community_id,))
#     communities = cur.fetchall()
#     community = communities[0]
#     cur.close()
#     return render_template("post-page.html" ,name = user[0][2],time = time.time(),date=time.date(), title = title, content = content, creator = creator, community = community )
    

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
        pic = request.form.get("url")
        if not Post_title:
            return apology("must provide Post_title", 400)
        elif not Post_body:
            return apology("must provide Post_body", 400)
        elif not category:
            return apology("must provide category",400)
        elif not community:
            return apology("must provide community",400)

        if pic=="":
            pic = None
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
        cur.execute("INSERT INTO Posts (Title, Content, Creator_id, Community_id ,Category_id,img) VALUES (%s,%s,%s,%s,%s,%s)", (Post_title, Post_body, (session["user_id"]), community_id[0], category_id[0],pic))
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
        cur.execute("INSERT INTO Communities (Name, ABOUT, category_id,Points,creator_id) VALUES (%s,%s,%s,%s,%s)", (community_name, community_description, category_id[0],1,session["user_id"]))
        mysql.connection.commit()
        cur.close() 
        return render_template("index.html",name = user[0][2])

@app.route("/profilesettings", methods = ["GET","POST"])
def update_profile():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
    user = cur.fetchall()
    if request.method == "GET":
        return render_template("profile-settings.html",name = user[0][2])
    if request.method == "POST":
        Username = request.form.get("change_username")
        password = request.form.get("change_password")
        
        confirmation = request.form.get("confirm_password")
        img = request.form.get("url")
        about = request.form.get("change_about")
        # print(Username=="")
        # print(password=="")
        # print(confirmation=="")
        # print(img=="")
        # print(about=="")
        # print(about)

        # if not Username:
        #     return apology("must provide username", 400)
        # elif not request.form.get("password"):
        #     return apology("must provide password", 400)
        # elif not request.form.get("confirmation"):
        #     return apology("must confirm password",400)
        # elif request.form.get("password")!=request.form.get("confirmation"):
        #     return apology("password is not same as Confirm Password",400)

        if password!="":
            if password!=confirmation:
                return apology("password is not same as Confirm Password",400)




        if Username != "":
            cur.execute("SELECT * FROM Users WHERE Username = %s", (Username,))
            rows = cur.fetchall()
            if (len(rows)!=0):
                cur.close()
                return apology("Username is taken",400)
            cur.execute("UPDATE Users SET Username = %s where id = %s",(Username,session["user_id"]))
        if password != "":
            cur.execute("UPDATE Users SET Password = %s where id = %s",(generate_password_hash(password),session["user_id"]))
        if img != "":
            cur.execute("UPDATE Users SET img = %s where id = %s",(img,session["user_id"]))
        if about != "":
            cur.execute("UPDATE Users SET About = %s where id = %s",(about,session["user_id"]))

        # cur.execute("INSERT INTO Users (Username, Password, About, Created) VALUES (%s,%s,'I am using Maskit',NOW())", (Username, generate_password_hash(password)))
        cur.execute("SELECT * FROM Users")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.execute("SELECT * FROM Users WHERE id = %s",(session["user_id"],))
        user = cur.fetchall()
        session["user_id"] = data[0][0]
        cur.close()
        return render_template("index.html",name = user[0][2])
