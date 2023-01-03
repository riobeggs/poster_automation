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
        album = spotify.album_tracks(self._album_id)["items"]

        for track in album:

            self._track_names.append(track["name"])

    def display(self) -> None:
        """
        Displays data collected (used for testing)
        """
        print()
        print(f"Album ID: {self._album_id}")
        print(f"Album name: {self._album_name}")
        print(f"Artist ID: {self._artist_id}")
        print(f"Artist name: {self._artist_name}")
        print(f"Album track names: {self._track_names}")
        print()

def main():
    data = AlbumData()
    data.get_album_id()
    data.get_album_name()
    data.get_artist_id()
    data.get_artist_name()
    data.get_track_names()

    data.display()


if __name__ == "__main__":
    main()
