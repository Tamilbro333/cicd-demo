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

def test_home_renders_dashboard_html(client):
    response = client.get('/')
    assert b'Live Deployment Dashboard' in response.data

def test_metadata_endpoint(client):
    response = client.get('/api/metadata')
    data = json.loads(response.data)
    assert 'version' in data
    assert data['app'] == 'My CI/CD Pipeline Project'

def test_stats_endpoint(client):
    response = client.get('/api/stats')
    data = json.loads(response.data)
    assert 'cpu_usage' in data
    assert 'aws_region' in data

def test_github_endpoint(client):
    response = client.get('/api/github')
    data = json.loads(response.data)
    assert 'status' in data

def test_docker_endpoint(client):
    response = client.get('/api/docker')
    data = json.loads(response.data)
    assert 'logs' in data
#comment line

def test_health_endpoint(client):
    response = client.get('/health')
    data = json.loads(response.data)
    assert data['healthy'] == True