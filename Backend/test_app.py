import pytest
import base64
import io
from PIL import Image
from app import app, search_count

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_image_base64():
    img = Image.new('RGB', (50, 50), color='blue')
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

def test_health_check(client):
    assert client.get('/health').status_code == 200

def test_analyze_empty_json(client):
    response = client.post('/analyze', json={})
    assert response.status_code == 400
    assert "No JSON data provided" in response.get_json()['error']

def test_analyze_success(client, sample_image_base64):
    response = client.post('/analyze', json={"image": sample_image_base64})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'ai_detection' in data
    assert 'tineye' in data

def test_quota_limit_logic(client, sample_image_base64):
    search_count['count'] = 5000
    response = client.post('/analyze', json={"image": sample_image_base64})
    data = response.get_json()
    assert 'tineye' in data
    assert data['tineye']['error'] == 'Monthly search limit reached'
    search_count['count'] = 0