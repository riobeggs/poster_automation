import spotipy

from credentials import client_credentials_manager

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class AlbumData:
    def __init__(self) -> None:
        self._album = None
        self._artist_name = None
        self._album_name = None
        self._album_cover = None
        self._release_date = None
        self._track_names = []
        self._record_company = None

    def get_album_url(self) -> None:
        """
        Creates an album instance from the album URL given by the user.
        """
        # Test link = "https://open.spotify.com/album/2mpzeA7pHNIDAPii4EEKsB?si=UXtfaj3ORzSSiOREq6a__A"
        album_url = input("Album link: ")

        self._album = spotify.album_tracks(album_url)["items"]

    def get_track_names(self) -> None:
        """
        Appends each tracks name from the album to a list (self.track_names)
        """
        for track in self._album:
            self._track_names.append(track["name"])


def main():
    data = AlbumData()

    data.get_album_url()
    data.get_track_names()


if __name__ == "__main__":
    main()
