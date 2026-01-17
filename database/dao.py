from database.DB_connect import DBConnect
from model.album import Album

class DAO:
    @staticmethod
    def get_album(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT a.id, a.title, a.artist_id, SUM(t.milliseconds / 60000) as duration
                    FROM album a, track t 
                    WHERE a.id = t.album_id
                    GROUP BY a.id
                    HAVING duration > %s"""

        cursor.execute(query, (durata,))

        for row in cursor:
            album = Album(
                id=row['id'],
                title=row['title'],
                artist_id=row['artist_id'],
                duration=row['duration']
            )

            result.append(album)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_playlist_album():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT p.playlist_id, t.album_id
                    FROM playlist_track p, track t
                    WHERE t.id = p.track_id"""

        cursor.execute(query)

        for row in cursor:
            p_id = row['playlist_id']
            a_id = row['album_id']

            # Se la playlist non è ancora nel dizionario, creiamo un set vuoto
            if p_id not in result:
                result[p_id] = set()

            # Aggiungiamo l'album al set di quella playlist
            result[p_id].add(a_id)

        cursor.close()
        conn.close()
        return result

