import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING' : True,
        'DATABASE' : db_path
    })
    
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
    
    yield app
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'# b c'est pour dire une séquence de bytes (0 à 255)
    
class AuthActions(object):
    def __init__(self, client) -> None:
        self._client = client
        
    def login(self,username="test",password="test"):
        return self._client.post(
            '/auth/login', data= {'username' : username, 'password': password}
        )
    def logout(self):
        return self._client.get('/auth/logout')
    
@pytest.fixture
def auth(client):
    return AuthActions(client)