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



def test_post_patient():
	response = client.post("/patient", json={'name': 'JAKUB', 'surename': 'GIERASIMCZYK'})
	assert response.status_code == 200
	assert response.json() == {"id": 1, "patient": {"name": "JAKUB", "surename": "GIERASIMCZYK"}}

	response = client.post("/patient", json={'name': 'STEFAN', 'surename': 'BANACH'})
	assert response.status_code == 200
	assert response.json() == {"id": 2, "patient": {"name": "STEFAN", "surename": "BANACH"}}


def test_read_patient_pk():
	response = client.get("/patient/1")
	assert response.status_code == 200
	assert response.json() == {"name": "JAKUB", "surename": "GIERASIMCZYK"}

	response = client.get("/patient/3")
	assert response.status_code == 204





# @pytest.mark.parametrize("method_name", ['GET', 'POST', 'PUT', 'DELETE'])
# def test_get_method(method_name):
# 	response = client.get("/method")
# 	assert response.status_code == 200
# 	assert response.json() == {"method_name": f"{method_name}"}


	