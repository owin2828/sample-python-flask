import pytest
import redis, json

import sys
sys.path.append(".")
from app.main.board import app

@pytest.fixture
def client():
    client = app.test_client()

    yield client

def test_create_board(client):
    response = client.post('/boards/', data=dict(
        title="test-title",
        content="test-content" 
        ), follow_redirects=True)
    
    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "title": "test-title",
        "content": "test-content"
    }

def test_get_board(client):
    response = client.get('/boards/1')

    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "title": "test-title",
        "content": "test-content"
    }

def test_update_board(client):
    response = client.put('/boards/1', data=dict(
        title="modified-title",
        content="modified-content",
        id="1" 
        ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "title": "modified-title",
        "content": "modified-content"
    }

def test_delete_board(client):
    response = client.delete('/boards/1', data=dict(
        id="1" 
        ), follow_redirects=True)
    
    assert response.status_code == 200