import pytest
from ecommerce.application import app  # Pfad angepasst

@pytest.fixture
def mock_db(mocker):
    mock = mocker.MagicMock()
    mock.execute.return_value = [
        {
            "id": 1,
            "samplename": "Test Shirt",
            "price": 29.99,
            "onSalePrice": 19.99,
            "image": "sample0.jpg",
            "typeClothes": "shirt",
            "description": "A test shirt"
        }
    ]
    mocker.patch('ecommerce.application.get_db', return_value=mock)
    return mock

@pytest.fixture
def client(mock_db):
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_home_page(client, mock_db):
    rv = client.get('/')
    assert rv.status_code == 200
    mock_db.execute.assert_called_with("SELECT * FROM shirts ORDER BY onSalePrice")
