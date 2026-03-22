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
    assert b'CI/CD Pipeline Live Workflow Dashboard' in response.data

def test_metadata_has_version(client):
    response = client.get('/api/metadata')
    data = json.loads(response.data)
    assert data['version'] == '1.0.1'

def test_workflow_status_endpoint(client):
    response = client.get('/api/workflow-status')
    data = json.loads(response.data)
    assert data['aws_deploy_ok'] == True

def test_health_endpoint(client):
    response = client.get('/health')
    data = json.loads(response.data)
    assert data['healthy'] == True

def test_info_has_tech_stack(client):
    response = client.get('/info')
    data = json.loads(response.data)
    assert 'Docker' in data['tech_stack']