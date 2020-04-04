from fastapi.testclient import TestClient
import pytest

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World during the coronavirus pandemic!"}




def test_get_method():
	response = client.get('/method')
	assert response.json() == {"method": "GET"}

def test_put_method():
	response = client.put('/method')
	assert response.json() == {"method": "PUT"}


def test_post_method():
	response = client.post('/method')
	assert response.json() == {"method": "POST"}


# @pytest.mark.parametrize("method_name", ['GET', 'POST', 'PUT', 'DELETE'])
# def test_get_method(method_name):
# 	response = client.get("/method")
# 	assert response.status_code == 200
# 	assert response.json() == {"method_name": f"{method_name}"}


	