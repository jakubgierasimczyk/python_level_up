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


from hashlib import sha256
from fastapi import Cookie, HTTPException





# ----- Zadanie 1 

@app.get("/")
def root():
	return "Hello!"


@app.get("/welcome")
def get_welcome():
	return "Hello!"








# ----- Zadanie 2

from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends
import secrets


app.secret_key = "very constatn and random secret, best 64 characters"
app.tokens_list = []
security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # detail="Incorrect email or password",
            # headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username



@app.post("/login")
def login(
    user: str, password: str, 
    response: Response, 
    credentials_user = Depends(get_current_username)):
    
    print(f"{user}")
    print(f"{password}")
    print(f"{credentials_user}")

    # correct_username = user == "trudnY"
    # correct_password = password == "PaC13Nt"
    
    # if not (correct_username and correct_password):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         # detail="Incorrect login or password",
    #         # headers={"WWW-Authenticate": "Basic"},
    #     )

    session_token = sha256(bytes(f"{user}{password}{app.secret_key}", encoding='utf8')).hexdigest()
    app.tokens_list.append(session_token)
    
    response.set_cookie(key="session_token", value=session_token)
    
    response = RedirectResponse(url = "/welcome")
    response.status_code = status.HTTP_302_FOUND
    
    return response





