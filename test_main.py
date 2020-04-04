from fastapi.testclient import TestClient
import pytest

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World during the coronavirus pandemic!"}






# @pytest.mark.parametrize("method_name", ['GET', 'POST', 'PUT', 'DELETE'])
# def test_get_method(method_name):
# 	response = client.get("/method")
# 	assert response.status_code == 200
# 	assert response.json() == {"method_name": f"{method_name}"}


	