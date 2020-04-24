from fastapi import FastAPI, Response, status
from enum import Enum
from pydantic import BaseModel


class MethodName(str, Enum):
    get = "GET"
    post = "POST"
    put = "PUT"
    delete = "DELETE"


app = FastAPI()
app.counter = -1
app.patients = {}



# @app.get("/")
# def root():
# 	return {"message": "Hello World during the coronavirus pandemic!"}



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
	patient=rq.dict()
	app.patients[app.counter] = patient
	return GiveMePatientResponse(id = app.counter, patient = patient)




@app.get("/patient/{pk}", status_code = 200)
def read_patient_pk(pk: int, response: Response):
	if app.counter < pk or pk < 0: 
		response.status_code = 204
		return 204
	else:
		return app.patients[pk]






# ------------------------ Lecture 3  ------------------------ #


# ----- Zadanie 1 

@app.get("/")
def root():
	return "Hello!"


@app.get("/welcome")
def get_welcome():
	return "Hello!"




