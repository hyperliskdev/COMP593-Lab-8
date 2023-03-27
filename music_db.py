import sqlite3
import os

# Determine the path of the database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music_library.db')

def main():
    # Create the database and its tables
    create_music_db()

    # Add some data to the DB
    populate_albums()
    populate_songs()
    populate_playlists()

    return

def create_music_db():
    """Creates the music database and all of its tables"""
    # Open a connection to the database. 
    con = sqlite3.connect(db_path) 
    
    # Get a Cursor object that can be used to run SQL queries on the database. 
    cur = con.cursor() 
    
    # Define an SQL query that creates a table named 'albums'. 
    # Each row in this table will hold information about a specific album.
    create_album_table_query = """ 
        CREATE TABLE IF NOT EXISTS albums 
        ( 
            id      INTEGER PRIMARY KEY, 
            title   TEXT NOT NULL, 
            artist  TEXT NOT NULL, 
            year    INTEGER NOT NULL
        ); 
    """ 
    
    # Execute the SQL query to create the 'albums' table. 
    # Database operations like this are called transactions. 
    cur.execute(create_album_table_query)

    # Create the 'songs' table 
    create_songs_table_query = """ 
        CREATE TABLE IF NOT EXISTS songs 
        ( 
            id        INTEGER PRIMARY KEY, 
            title     TEXT NOT NULL, 
            track     INTEGER NOT NULL,
            album_id  TEXT NOT NULL,
            FOREIGN KEY (album_id) REFERENCES albums (id)
        ); 
    """ 
    cur.execute(create_songs_table_query)

    # Create the 'playlists' table 
    create_playlists_table_query = """ 
        CREATE TABLE IF NOT EXISTS playlists 
        ( 
            id     INTEGER PRIMARY KEY, 
            title  TEXT NOT NULL,
            mood   TEXT
        ); 
    """ 
    cur.execute(create_playlists_table_query)

    # Create the 'playlist_songs' table 
    create_playlist_songs_table_query = """ 
        CREATE TABLE IF NOT EXISTS playlist_songs 
        ( 
            id           INTEGER PRIMARY KEY, 
            playlist_id  INTEGER NOT NULL,
            song_id      INTEGER NOT NULL,
            FOREIGN KEY (playlist_id) REFERENCES playlists (id),
            FOREIGN KEY (song_id) REFERENCES songs (id)
        ); 
    """ 
    cur.execute(create_playlist_songs_table_query)    

    # Commit (save) pending transactions to the database. 
    # Transactions must be committed to be persistent. 
    con.commit() 
    
    # Close the database connection. 
    # Pending transactions are not implicitly committed, so any 
    # pending transactions that have not been committed will be lost. 
    con.close() 

def add_album_to_db(title, artist, year):
    """Adds a new album to the DB

    Args:
        title (str): Album title
        artist (str): Album artist
        year (int): Year album was released

    Returns:
        int: Album ID
    """
    # Check whether album is already in the DB
    album_id = get_album_id(title, artist)
    if album_id != 0:
        return album_id 

    con = sqlite3.connect(db_path) 
    cur = con.cursor() 
    
    # SQL query that inserts a row into the albums table. 
    query = """ 
        INSERT INTO albums (title, artist, year) 
        VALUES (?, ?, ?); 
    """ 

    # Tuple of data for new album to insert into albums table 
    new_album = (title, artist, year) 
    
    # Execute query to add new album to albums table 
    cur.execute(query, new_album) 
    con.commit() 
    con.close() 

    # Return the ID of the added record
    return cur.lastrowid

def get_album_id(title, artist):
    """Gets the ID of an album in the DB

    Args:
        title (str): Album title
        artist (str): Artist name

    Returns:
        int: Album ID, if album is present in the DB, 0 if not present
    """
    con = sqlite3.connect(db_path) 
    cur = con.cursor() 

    # Define query to search for album in DB
    query = """ 
        SELECT id FROM albums 
        WHERE title = ? AND artist = ?;
    """ 

    # Define tuple of data for album to search for in albums table 
    # Data values must be in same order as specified in query 
    album_info = (title, artist) 
    
    # Execute query to add new album to albums table 
    cur.execute(query, album_info) 
    query_result = cur.fetchone()
    con.close() 

    # Return the album ID if album is present in the DB
    if query_result is not None:
        return query_result[0]

    # Return 0 if album is not present in the DB 
    return 0

def populate_albums():
    """Populates the DB with some Canadian rock albums."""

    # Add some Tragically Hip albums to the DB
    add_album_to_db('Up To Here', 'The Tragically Hip', 1989)
    add_album_to_db('Fully Completely', 'The Tragically Hip', 1992)
    add_album_to_db('Day For Night', 'The Tragically Hip', 1994)
    add_album_to_db('Trouble at the Henhouse', 'The Tragically Hip', 1996)
    add_album_to_db('Phantom Power', 'The Tragically Hip', 1998)

    # Add some Rush albums to the DB
    add_album_to_db('Presto', 'Rush', 1989)
    add_album_to_db('Roll the Bones', 'Rush', 1991)
    add_album_to_db('Counterparts', 'Rush', 1993)
    add_album_to_db('Test for Echo', 'Rush', 1996)

    # Add some Nickelback albums to the DB
    add_album_to_db('Curb', 'Nickelback', 1996)
    add_album_to_db('The State', 'Nickelback', 2000)
    add_album_to_db('Silver Side Up', 'Nickelback', 2001)    

def add_song_to_db(song_title, track_num, album_title, artist):
    """Adds a new song to the DB

    Args:
        song_title (str): Song title
        track_num (int): Track number
        album_title (str): Album title
        artist (str): Artist name

    Returns:
        int: Song ID
    """
    # Check whether song is already in the DB
    song_id = get_song_id(song_title, artist, album_title)
    if song_id != 0:
        return song_id 
    
    con = sqlite3.connect(db_path) 
    cur = con.cursor() 
    query = """ 
        INSERT INTO songs (title, track, album_id) 
        VALUES (?, ?, (SELECT id FROM albums WHERE title == ? AND artist == ?)); 
    """ 
    new_song = (song_title, track_num, album_title, artist) 
    cur.execute(query, new_song) 
    con.commit() 
    con.close() 

    # Return the ID of the added record
    return cur.lastrowid

def get_song_id(song_title, artist, album_title):
    """Gets the ID of a specified song

    Args:
        song_title (str): Song title
        artist (str): Song artist
        album_title (str): Album title

    Returns:
        int: Album ID, if album is present in the DB, 0 if not present
    """
    # Query the DB for the song
    con = sqlite3.connect(db_path) 
    cur = con.cursor() 
    query = f""" 
        SELECT songs.id FROM songs 
        JOIN albums ON songs.album_id = albums.id
        WHERE songs.title = "{song_title}" AND albums.title = "{album_title}" AND albums.artist = "{artist}";
    """ 
    cur.execute(query) 
    query_result = cur.fetchone()
    con.close() 

    # Return the song ID if song is present in the DB
    if query_result is not None:
        return query_result[0]

    # Return 0 if song is not present in the DB 
    return 0

def populate_songs():
    """Populates the DB with some songs."""

    # Add all songs on the Rush album Counterparts
    artist = 'Rush'
    album = 'Counterparts'
    songs = ('Animate', 'Stick It Out', 'Cut to the Chase', "Nobody's Hero", 'Between Sun & Moon', 'Alien Shore', 
             'The Speed of Love', 'Double Agent', 'Leave That Thing Alone', 'Cold Fire', 'Everyday Glory')
    for i, song in enumerate(songs):
        add_song_to_db(song, i+1, album, artist)

    # Add all songs from The Tragically Hip album Fully Completely
    artist = 'The Tragically Hip'
    album = 'Fully Completely'
    songs = ("Courage (for Hugh MacLennan)", "Looking for a Place to Happen", "At the Hundredth Meridian", 
             "Pigeon Camera", "Lionized", "Locked in the Trunk of a Car", "We'll Go, Too", "Fully Completely", 
             "Fifty Mission Cap", "Wheat Kings", "The Wherewithal", "Eldorado")
    for i, song in enumerate(songs):
        add_song_to_db(song, i+1, album, artist)

    # Add all songs from the Nickelback album Silver Side Up
    artist = 'Nickelback'
    album = 'Silver Side Up'
    songs = ("Never Again", "How You Remind Me", "Woke Up This Morning", "Too Bad", "Just For", 
             "Hollywood", "Money Bought", "Where Do I Hide", "Hangnail", "Good Times Gone")
    for i, song in enumerate(songs):
        add_song_to_db(song, i+1, album, artist)

def add_playlist_to_db(title, mood):
    """Adds a new playlist to the DB

    Args:
        title (str): Playlist title
        mood (str): Playlist mood

    Returns:
        int: Playlist ID
    """
    # Check whether playlist is already in the DB
    playlist_id = get_playlist_id(title)
    if playlist_id != 0:
        return playlist_id 
    
    con = sqlite3.connect(db_path) 
    cur = con.cursor() 
    query = f""" 
        INSERT INTO playlists (title, mood) 
        VALUES ("{title}", "{mood}"); 
    """ 
    cur.execute(query) 
    con.commit() 
    con.close() 

    # Return the ID of the added playlist
    return cur.lastrowid

def get_playlist_id(title):
    """Gets the ID of a specified playlist

    Args:
        title (str): Playlist title

    Returns:
        int: Playlist ID, if playlist is present in the DB, 0 if not present
    """
    # Query the DB for the playlist song
    con = sqlite3.connect(db_path) 
    cur = con.cursor() 
    query = f""" 
        SELECT id FROM playlists 
        WHERE title = "{title}";
    """ 
    cur.execute(query) 
    query_result = cur.fetchone()
    con.close() 

    # Return the playlist ID if present in the DB
    if query_result is not None:
        return query_result[0]

    # Return 0 if playlist is not present in the DB
    return 0

def add_song_to_playlist(playlist_title, song_title, artist):
    """Adds a song to a playlist

    Args:
        playlist_title (str): Playlist title
        song_title (str): Song title
        artist (str): Artist name

    Returns:
        int: Playlist song ID
    """
    # Check whether song is already on playlist
    playlist_song_id = get_playlist_song_id(playlist_title, song_title, artist)
    if playlist_song_id != 0:
        return playlist_song_id 
    
    con = sqlite3.connect(db_path) 
    cur = con.cursor() 
    query = f""" 
        INSERT INTO playlist_songs (playlist_id, song_id) 
        VALUES (
            (SELECT playlists.id FROM playlists WHERE title == "{playlist_title}"),
            (SELECT songs.id FROM songs 
             JOIN albums ON songs.album_id = albums.id
             WHERE songs.title = "{song_title}" AND albums.artist = "{artist}")
        ); 
    """ 
    cur.execute(query) 
    con.commit() 
    con.close() 

    # Return the ID of the added playlist song
    return cur.lastrowid

def get_playlist_song_id(playlist_title, song_title, artist):
    """Gets the ID of a playlist song

    Args:
        playlist_title (str): Playlist title
        song_title (str): Song title
        artist (str): Artist name

    Returns:
        int: Playlist song ID, if song is present on the playlist, 0 if not present
    """
    # Query the DB for the playlist song
    con = sqlite3.connect(db_path) 
    cur = con.cursor() 
    query = f""" 
        SELECT playlist_songs.id FROM playlist_songs 
        JOIN playlists ON playlist_songs.playlist_id = playlists.id
        JOIN songs ON playlist_songs.song_id = songs.id
        JOIN albums ON songs.album_id = albums.id
        WHERE playlists.title = "{playlist_title}" AND songs.title = "{song_title}" AND albums.artist = "{artist}";
    """ 
    cur.execute(query) 
    query_result = cur.fetchone()
    con.close() 

    # Return the playlist song ID if present on the playlist
    if query_result is not None:
        return query_result[0]

    # Return 0 if playlist song is not present on the playlist
    return 0

def populate_playlists():
    """Adds some playlists to the DB"""

    # Add a playlist full of Grace's favs
    title = "Grace's Favourites"
    mood = "Party"
    add_playlist_to_db(title, mood)
    songs = [
        ("Wheat Kings", "The Tragically Hip"),
        ("How You Remind Me", "Nickelback"),
        ("At the Hundredth Meridian", "The Tragically Hip"),
        ("Double Agent", "Rush")
    ]
    for song_title, artist in songs:
        add_song_to_playlist(title, song_title, artist)

    # Add a playlist full of rock songs
    title = "Rawk Musak"
    mood = "Vibin'"
    add_playlist_to_db(title, mood)
    songs = [
        ("Stick It Out", "Rush"),
        ("Fifty Mission Cap", "The Tragically Hip"),
        ("How You Remind Me", "Nickelback"),
        ("At the Hundredth Meridian", "The Tragically Hip"),
        ("Wheat Kings", "The Tragically Hip"),
        ("Double Agent", "Rush"),
        ("Hangnail", "Nickelback")
    ]
    for song_title, artist in songs:
        add_song_to_playlist(title, song_title, artist)

if __name__ == '__main__':
    main()