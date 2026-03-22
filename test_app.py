import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200

def test_home_has_status(client):
    response = client.get('/')
    data = json.loads(response.data)
    assert data['status'] == 'running'

def test_health_endpoint(client):
    response = client.get('/health')
    data = json.loads(response.data)
    assert data['healthy'] == True

def test_info_has_tech_stack(client):
    response = client.get('/info')
    data = json.loads(response.data)
    assert 'Docker' in data['tech_stack']