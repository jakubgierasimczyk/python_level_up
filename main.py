from fastapi import FastAPI
from enum import Enum


class MethodName(str, Enum):
    get = "GET"
    post = "POST"
    put = "PUT"
    delete = "DELETE"


app = FastAPI()
 



@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}



@app.get("/method/{method_name}")
async def get_model(method_name: MethodName):
    return {"method_name": method_name.value}
