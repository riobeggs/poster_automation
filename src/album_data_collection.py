import spotipy

from credentials import client_credentials_manager

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class AlbumData:
    def __init__(self) -> None:
        self._album_id = None
        self._album_name = None
        self._artist_id = None
        self._artist_name = None
        self._track_names = []
        self._album_cover = None
        self._release_date = None
        self._record_company = None

    def get_album_id(self) -> None:
        """
        Locates an albums id from the album URL given by the user.
        """
        # album_url = input("Album link: ")

        # Remove after testing ---------------------------------------------------------------------->
        album_url = "https://open.spotify.com/album/2mpzeA7pHNIDAPii4EEKsB?si=UXtfaj3ORzSSiOREq6a__A"
        # ------------------------------------------------------------------------------------------->
        self._album_id = album_url.split("/")[-1].split("?")[0]

    def get_album_name(self) -> None:
        """
        Queries album for albums name and stores it as a string.
        """
        album = spotify.album(self._album_id)

        self._album_name = album["name"]

    def get_artist_id(self) -> None:
        """
        Queries album for albums name and stores it as a string.
        """
        album = spotify.album(self._album_id)
        artist = album["artists"][0]

        self._artist_id = artist["id"]

    def get_artist_name(self) -> None:
        """
        Queries album for artists name and stores it as a string.
        """
        album = spotify.album(self._album_id)
        artist = album["artists"][0]

        self._artist_name = artist["name"]

    def get_track_names(self) -> None:
        """
        Appends each tracks name from the album to a list of strings
        """
        for track in self._album:

            self._track_names.append(track["name"])


def main():
    data = AlbumData()

    data.get_album_id()
    data.get_album_name()

    data.get_artist_id()
    data.get_artist_name()


if __name__ == "__main__":
    main()
