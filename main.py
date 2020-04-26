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





# class GiveMePatientRequest(BaseModel):
# 	name: str
# 	surename: str

# class GiveMePatientResponse(BaseModel):
# 	id: int
# 	patient: dict

# @app.post("/patient", response_model=GiveMePatientResponse)
# def receive_patient(rq: GiveMePatientRequest):
# 	app.counter += 1
# 	patient=rq.dict()
# 	app.patients[app.counter] = patient
# 	return GiveMePatientResponse(id = app.counter, patient = patient)




# @app.get("/patient/{pk}", status_code = 200)
# def read_patient_pk(pk: int, response: Response):
# 	if app.counter < pk or pk < 0: 
# 		response.status_code = 204
# 		return 204
# 	else:
# 		return app.patients[pk]






# ------------------------ Lecture 3  ------------------------ #


from hashlib import sha256
from fastapi import Cookie, HTTPException





# ----- Zadanie 1 

@app.get("/")
def root():
	return "Hello!"


# @app.get("/welcome")
# def get_welcome():
# 	return "Hello!"








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
    # print(f"{credentials.username}")
    # print(f"{credentials.password}")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # detail="Incorrect email or password",
            # headers={"WWW-Authenticate": "Basic"},
        )

    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
    app.tokens_list.append(session_token)

    return session_token





@app.post("/login")
def login(
        response: Response, 
        session_token: str = Depends(get_current_username)):
    

    response = RedirectResponse(url='/welcome')
    response.status_code = status.HTTP_302_FOUND
    response.set_cookie(key="session_token", value=session_token)
    
    return response


# @app.get('/welcome')
# def get_welcome():
#     return "Hello!"



# ----- Zadanie 3
@app.post("/logout")
def logout(response: Response):
    response = RedirectResponse(url="/")
    response.status_code = status.HTTP_302_FOUND
    response.delete_cookie("session_token")
    return response




# # ----- Zadanie 4

from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

@app.get("/welcome")
def get_welcome(
    request: Request 
    # session_token = Depends(get_current_username)
    ):
    return templates.TemplateResponse("item.html", {"request": request, "user": credentials_user})






# # ----- Zadanie 5

# @app.post("/patient")
# def receive_patient(
#         name: str, surname: str, 
#         response: Response,
#         credentials_user = Depends(get_current_username)
#     ):

#     app.counter += 1
#     patient={"name": name, "surname": surname}
#     app.patients[app.counter] = patient

#     response.status_code = status.HTTP_302_FOUND
#     response.headers["Location"] = f"/patient/{app.counter}"
#     return patient

# @app.get("/patient")
# def all_patients(credentials_user = Depends(get_current_username)):
#     return app.patients




# @app.get("/patient/{pk}", status_code = 200)
# def read_patient_pk(pk: int, response: Response, credentials_user = Depends(get_current_username)):
#     if app.counter < pk or pk < 0: 
#         response.status_code = 204
#         return 204
#     else:
#         return app.patients[pk]

# @app.delete("/patient/{pk}")
# def delete_patient_pk(pk: int, credentials_user = Depends(get_current_username)):
#     try:
#         del app.patients[pk]
#         print(f'Patient {pk} removed')
#     except KeyError:
#         print(f"Key {pk} not found")


# # "trudnY"
# # "PaC13Nt"
