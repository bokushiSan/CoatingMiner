import pytest
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)  # TODO: ошибка, надо править

def test_upload():
    with open('tests/test_paper.pdf', 'rb') as f:
        response = client.post(
            '/papers/upload',
            files={'file': ('sample.pdf', f, 'application/pdf')}
        )

    assert response.status_code == 200

    data = response.json()

    assert 'paper_id' in data
    assert data['status'] == 'uploaded'
