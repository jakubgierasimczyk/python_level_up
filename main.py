import secrets
from typing import Dict, Optional

from fastapi import Depends, FastAPI, Response, status, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.security import APIKeyCookie, HTTPBasic, HTTPBasicCredentials
from jose import jwt
from pydantic import BaseModel
from starlette.responses import RedirectResponse



class Patient(BaseModel):
	name: str
	surname: str


class DaftAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter: int = 0
        self.storage: Dict[int, Patient] = {}
        self.security = HTTPBasic(auto_error=False)
        self.secret_key = "kluczyk"
        self.API_KEY = "session"
        self.cookie_sec = APIKeyCookie(name=self.API_KEY, auto_error=False)
        self.templates = Jinja2Templates(directory="templates")


app = DaftAPI()


def is_logged(session: str = Depends(app.cookie_sec), silent: bool = False):
    try:
        payload = jwt.decode(session, app.secret_key)
        return payload.get("magic_key")
    except Exception:
        pass

    if silent:
        return False

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def authethicate(credentials: Optional[HTTPBasicCredentials] = Depends(app.security)):
    if not credentials:
        return False

    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")

    if not (correct_username and correct_password):
        return False
    return True


@app.get("/")
def read_root():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/welcome")
def welcome(request: Request, is_logged: bool = Depends(is_logged)):
    return app.templates.TemplateResponse(
        "welcome.html", {"request": request, "user": "trudnY"}
    )


@app.post("/login")
async def login_basic(auth: bool = Depends(authethicate)):
    if not auth:
        response = Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)
        return response

    response = RedirectResponse(url="/welcome")
    token = jwt.encode({"magic_key": True}, app.secret_key)
    response.set_cookie("session", token)
    return response


@app.post("/logout")
async def logout(is_logged: bool = Depends(is_logged)):
    response = RedirectResponse(url="/")
    response.delete_cookie("session")
    return response


@app.post("/patient")
def add_patient(patient: Patient, is_logged: bool = Depends(is_logged)):
    app.storage[app.counter] = patient
    response = RedirectResponse(url=f"/patient/{app.counter}")
    app.counter += 1
    return response


@app.get("/patient")
def show_patients(is_logged: bool = Depends(is_logged)):
    return app.storage


@app.get("/patient/{pk}")
def show_patient(pk: int, is_logged: bool = Depends(is_logged)):
    if pk in app.storage:
        return app.storage.get(pk)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/patient/{pk}")
def delte_patient(pk: int, is_logged: bool = Depends(is_logged)):
    if pk in app.storage:
        del app.storage[pk]
    return Response(status_code=status.HTTP_204_NO_CONTENT)









# --------------- Lecture 4 --------------- #


# ----- Zadanie 1
import sqlite3

@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect('chinook.db')


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()





@app.get("/tracks")
async def tracks(page: int = 0, per_page: int = 10):
    app.db_connection.row_factory = sqlite3.Row
    tracks = app.db_connection.execute(
    	'''SELECT "TrackId", "Name", "AlbumId", "MediaTypeId", 
    	"GenreId", "Composer", "Milliseconds", "Bytes", "UnitPrice"
    	FROM tracks ORDER BY "TrackId"
    	LIMIT :per_page OFFSET :offset;''',
    	{'offset': per_page*page, 'per_page': per_page}
    	).fetchall()

    return tracks




# ----- Zadanie 2

@app.get("/tracks/composers")
async def composers(composer_name: str):
	app.db_connection.row_factory = lambda cursor, x: x[0]
	names = app.db_connection.execute(
    	'''SELECT Name FROM tracks WHERE Composer = :name
    	ORDER BY Name;''', 
    	{'name': composer_name}
    	).fetchall()

	if len(names) == 0:
		names = {"error": f'No such artist: {composer_name}'}
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = names)

	return names





# ----- Zadanie 3

def test_artist_exists(artistid: int):

    if artistid is None:
        msg = {"error": 'No such artist: None'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = msg)


    app.db_connection.row_factory = lambda cursor, x: x[0]
    artist_in_db = app.db_connection.execute(
        '''SELECT ArtistId FROM artists 
        WHERE ArtistId = :artistid LIMIT 1;''', 
        {'artistid': artistid}
        ).fetchall()
    
    print(f'{artist_in_db=}')

    if len(artist_in_db) == 0:
        msg = {"error": f'No such artist: {artistid}'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = msg)


    return True

def get_max_id():

    app.db_connection.row_factory = lambda cursor, x: x[0]
    max_id = app.db_connection.execute(
        '''SELECT max(ArtistId) FROM albums;'''
        ).fetchall()

    return max_id[0]




class NewArtist(BaseModel):
    title: str
    artist_id: int


@app.post("/albums", status_code = 201)
async def add_album(new_artist: NewArtist):

    title = new_artist.title
    artistid = new_artist.artist_id
    print(f'{title=}, {artistid=}')

    # Sprawdzenie czy w wejsciowym jsonie sa wymagane pola
    if not title and artistid:
        msg = {"error": f'Empty title or artist id: {title=}, {artistid=}'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = msg)


    # Sprawdzenie czy dany artysta wystepuje w bazie danych
    artist_exists = test_artist_exists(artistid)
    print(f'{artist_exists=}')


    # Sprawdzenie maksymalnego albumid
    max_id = get_max_id()
    print(f'{max_id=}')



    new_album = {
        "AlbumId": max_id+1,
        "Title": title,
        "ArtistId": artistid}
    
    cursor = app.db_connection.execute(
        "INSERT INTO albums (AlbumId, Title, ArtistId) VALUES (?)", (new_album.AlbumId, new_album.Title, new_album.ArtistId, )
    )
    app.db_connection.commit()  

    return new_album
    


@app.get("/albums/{albumid}")
async def get_album(albumid: int):
    app.db_connection.row_factory = lambda cursor, x: x[:4]
    album = app.db_connection.execute(
        '''SELECT AlbumId, Title, ArtistId FROM albums WHERE AlbumId = :albumid;''', 
        {'albumid': albumid}
        ).fetchall()

    if len(album) == 0:
        msg = {"error": f'No such artist: {composer_name}'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = msg)


    album_dict = album
    album_dict = {
        "AlbumId": album[0][0],
        "Title": album[0][1],
        "ArtistId": album[0][2]}
    
    return album_dict
