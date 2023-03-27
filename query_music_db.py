import sqlite3
from music_db import db_path

def main():
    # Use a breakpoint to view the query results
    nineties_albums = get_albums_by_year(1990, 1999)
    fully_completely_tracks = get_album_tracks("The Tragically Hip", "Fully Completely")
    rawk_musak_tracks = get_playlist_tracks("Rawk Musak")
    graces_fav_tracks = get_playlist_tracks("Grace's Favourites")
    return

def get_albums_by_year(min_year, max_year):
    con = sqlite3.connect(db_path) 
    cur = con.cursor() 
    query = f""" 
        SELECT title, artist, year FROM albums
        WHERE year >= {min_year} AND year <= {max_year};
    """ 
    cur.execute(query) 
    query_result = cur.fetchall()
    con.close() 
    return query_result

def get_album_tracks(artist, album_title):
    con = sqlite3.connect(db_path) 
    cur = con.cursor() 
    query = f""" 
        SELECT songs.track, songs.title, albums.artist, albums.title FROM songs
        JOIN albums ON songs.album_id = albums.id
        WHERE albums.artist = "{artist}" AND albums.title = "{album_title}"
        ORDER BY songs.track;
    """ 
    # Execute query 
    cur.execute(query) 
    query_result = cur.fetchall()
    con.close() 

    return query_result

def get_playlist_tracks(playlist_title):
    con = sqlite3.connect(db_path) 
    cur = con.cursor() 
    query = f""" 
        SELECT songs.title, albums.artist, albums.title, albums.year FROM playlist_songs
        JOIN playlists ON playlist_songs.playlist_id = playlists.id
        JOIN songs ON playlist_songs.song_id = songs.id
        JOIN albums ON songs.album_id = albums.id
        WHERE playlists.title = "{playlist_title}";
    """ 
    cur.execute(query) 
    query_result = cur.fetchall()
    con.close() 
    return query_result

if __name__ == '__main__':
    main()