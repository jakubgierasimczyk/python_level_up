import sqlite3
from fastapi import FastAPI, HTTPException, status





app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect('chinook_copy.db')


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




@app.get("/tracks/composers")
async def composers(composer_name: str):
	app.db_connection.row_factory = lambda cursor, x: x[0]
	names = app.db_connection.execute(
    	'''SELECT Name FROM tracks WHERE Composer = :name
    	ORDER BY Name;''', 
    	{'name': composer_name}
    	).fetchall()

	if len(names) == 0:
		msg = {"error": f'No such artist: {composer_name}'}
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = msg)

	return names









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
        '''SELECT max(AlbumId) FROM albums;'''
        ).fetchall()

    return max_id[0]



from pydantic import BaseModel


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
        "albumid": max_id+1,
        "title": title,
        "artistid": artistid}

    print(f'{new_album=}')
    
    cursor = app.db_connection.execute(
        "INSERT INTO albums (AlbumId, Title, ArtistId) VALUES (?, ?, ?)", 
        (new_album['albumid'], new_album['title'], new_album['artistid'], )
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


    # album_dict = album
    album_dict = {
        "AlbumId": album[0][0],
        "Title": album[0][1],
        "ArtistId": album[0][2]}
    
    return album_dict



