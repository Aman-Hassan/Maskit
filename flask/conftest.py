import pytest
from flask_mysqldb import MySQL
from flask import Flask, session
from werkzeug.security import generate_password_hash
from app import app

# Configure app
app.config["TESTING"] = True
app.config["SECRET_KEY"] = "test_secret_key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'test_user'
app.config['MYSQL_PASSWORD'] = 'test_password'
app.config['MYSQL_DB'] = 'test_database'
mysql = MySQL(app)


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("DROP TABLE IF EXISTS Users")
            cur.execute("CREATE TABLE Users (id INT PRIMARY KEY AUTO_INCREMENT, Username VARCHAR(50) NOT NULL UNIQUE, Password VARCHAR(100) NOT NULL, About VARCHAR(255) NOT NULL, Created DATETIME NOT NULL)")
            cur.execute("INSERT INTO Users (Username, Password, About, Created) VALUES ('test_user', %s, 'I am using Maskit', NOW())", (generate_password_hash('test_password'),))
            mysql.connection.commit()
            cur.close()
        yield client
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("DROP TABLE IF EXISTS Users")
            mysql.connection.commit()
            cur.close()
        session.clear()
