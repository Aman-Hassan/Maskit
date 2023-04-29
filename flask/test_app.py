import pytest
from flask import session
from app import app, mydatabase, User

# Set up fixture to create and return a test client for each test
@pytest.fixture(scope="module")
def client():
    # Set up Flask app in testing mode
    app.config['TESTING'] = True

    # Set up a test client using Flask's built-in test client
    with app.test_client() as client:
        # Set up a testing database using SQLAlchemy
        mydatabase.create_all()

        # Set up a session to use in testing
        with client.session_transaction() as sess:
            sess['key'] = 'value'

        yield client

        # Tear down the testing database
        mydatabase.session.remove()
        mydatabase.drop_all()

# Define test functions
def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_login_post_success(client):
    with client:
        # Create a test user
        user = User(username='testuser', password='testpassword')
        mydatabase.session.add(user)
        mydatabase.session.commit()

        # Log in the test user
        response = client.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        assert response.status_code == 200

        # Check that the user is logged in and the session contains their user ID
        with client.session_transaction() as sess:
            assert sess.get('user_id') == user.id

def test_login_post_failure(client):
    with client:
        # Try to log in with invalid credentials
        response = client.post('/login', data=dict(
            username='invaliduser',
            password='invalidpassword'
        ), follow_redirects=True)
        assert response.status_code == 403

        # Check that the session does not contain a user ID
        with client.session_transaction() as sess:
            assert sess.get('user_id') is None
