from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel


class MethodName(str, Enum):
    get = "GET"
    post = "POST"
    put = "PUT"
    delete = "DELETE"


app = FastAPI()
app.counter = 0



@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}



@app.get("/method")
async def get_method():
    return {"method": "GET"}


@app.put("/method")
def put_method():
    return {"method": "PUT"}
    

@app.post("/method")
def post_method():
    return {"method": "POST"}





class GiveMePatientRequest(BaseModel):
	name: str
	surename: str

class GiveMePatientResponse(BaseModel):
	id: int
	patient: dict

@app.post("/patient", response_model=GiveMePatientResponse)
def receive_patient(rq: GiveMePatientRequest):
	app.counter += 1
	return GiveMePatientResponse(id = app.counter, patient=rq.dict())


# @app.post("/patient")
# def post_patient():
# 	app.counter += 1
# 	return {"id": app.counter, "patient": {"name": "JAKUB", "surename": "GIERASIMCZYK"}}


# @app.put("/method")
# def put_method(method_name: MethodName):
#     return {"method_name": method_name.value}