from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel


class MethodName(str, Enum):
    get = "GET"
    post = "POST"
    put = "PUT"
    delete = "DELETE"


app = FastAPI()
 



@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}



@app.get("/method")
async def get_method():
    return {"method_name": "GET"}


@app.put("/method")
def put_method():
    return {"method_name": "PUT"}


@app.post("/method")
def post_method():
    return {"method_name": "POST"}


# @app.put("/method")
# def put_method(method_name: MethodName):
#     return {"method_name": method_name.value}