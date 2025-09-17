import pytest
from ecommerce.application import app

@pytest.fixture
def mock_db(mocker):
    mock = mocker.MagicMock()
    def mock_execute(*args, **kwargs):
        if "SELECT * FROM users WHERE username = :username" in args[0]:
            return []
        return []
    mock.execute.side_effect = mock_execute
    mocker.patch('ecommerce.application.get_db', return_value=mock)
    return mock

@pytest.fixture
def client(mock_db):
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_user_registration_flow(client):
    client.post('/register/')
    rv = client.post('/register/', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword',
        'fname': 'Test',
        'lname': 'User',
        'confirm': 'testpassword'
    })
    assert rv.status_code in [200, 302]
