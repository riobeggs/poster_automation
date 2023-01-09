import calendar
import os
import urllib.request

import spotipy
from colorthief import ColorThief

from .credentials import client_credentials_manager

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class AlbumData:
    def __init__(self) -> None:
        self._album_id = None
        self._album_name = None
        self._artist_id = None
        self._artist_name = None
        self._artist_genre = None
        self._track_names = []
        self._release_date = None
        self._record_company = None
        self._album_cover_image_url = None
        self._album_cover_path = None
        self._colour_palette = []

    def get_album_id(self) -> None:
        """
        Locates an albums id from the album URL given by the user.
        """
        album_url = input("\nAlbum link: ")

        # Remove after testing ---------------------------------------------------------------------->
        # album_url = "https://open.spotify.com/album/2mpzeA7pHNIDAPii4EEKsB?si=7rnnAkzuT1mbT3AyJgSkCQ"
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

    def get_artist_genre(self) -> None:
        """
        Queries artist for genres and stores main genre as a string.
        """
        artist = spotify.artist(self._artist_id)

        genres = artist["genres"]
        genre = genres[0]

        self._artist_genre = genre.capitalize()

    def get_track_names(self) -> None:
        """
        Appends each tracks name from the album to a list of strings
        """
        album = spotify.album_tracks(self._album_id)["items"]

        for track in album:

            self._track_names.append(track["name"])

    def get_release_date(self) -> None:
        """
        Queries album for release date and stores it as a string.
        """
        album = spotify.album(self._album_id)
        date = album["release_date"]

        date = date.split("-")
        date[1] = calendar.month_name[int(date[1])]
        date = f"{date[2]} {date[1]} {date[0]}"

        self._release_date = date

    def get_record_company(self) -> None:
        """
        Queries album for record company and stores it as a string.
        """
        album = spotify.album(self._album_id)
        record_company = album["copyrights"][0]

        self._record_company = record_company["text"]

    def get_album_cover_path(self) -> None:
        """
        Queries album for album covers URL,
        downloads the image and stores the file path as a string.
        """
        album = spotify.album(self._album_id)
        images = album["images"][0]

        self._album_cover_image_url = images["url"]
        self._album_cover_path = f"covers/{self._album_id}.jpg"

        self.download_album_cover()

    def download_album_cover(self) -> None:
        """
        Downloads the album cover image to covers folder.
        Creates covers folder if not already created.
        """
        if not os.path.exists("covers"):
            os.mkdir("covers")

        urllib.request.urlretrieve(self._album_cover_image_url, self._album_cover_path)

    def get_colours_from_album_cover(self) -> None:
        """
        Uses colour thief to generate a 5 colour palette from the album cover.
        Stores the hex values as strings in a list.
        """
        rgb_palette = ColorThief(self._album_cover_path).get_palette(5)

        for colour in rgb_palette:

            hex_colour = f"{colour[0]:02x}{colour[1]:02x}{colour[2]:02x}"

            self._colour_palette.append(hex_colour)

    def display(self) -> None:
        """
        Displays data collected (used for testing)
        """
        print()
        # print(f"Album ID: {self._album_id}")
        print(f"Album name: {self._album_name}")
        # print(f"Artist ID: {self._artist_id}")
        print(f"Artist name: {self._artist_name}")
        print(f"Artist genre: {self._artist_genre}")
        print(f"Album track names: {self._track_names}")
        print(f"Album release date: {self._release_date}")
        print(f"Record company: {self._record_company}")
        # print(f"Album cover url: {self._album_cover_image_url}")
        print(f"Album cover file path: {self._album_cover_path}")
        print(f"Colour palette: {self._colour_palette}")
        print()

    def run(self) -> None:
        """
        Runs methods for retrieving relative data.
        """
        self.get_album_id()
        self.get_album_name()
        self.get_artist_id()
        self.get_artist_name()
        self.get_artist_genre()
        self.get_track_names()
        self.get_release_date()
        self.get_record_company()
        self.get_album_cover_path()
        self.get_colours_from_album_cover()

        self.display()


def main():
    data = AlbumData()

    data.get_album_id()
    data.get_album_name()
    data.get_artist_id()
    data.get_artist_name()
    data.get_artist_genre()
    data.get_track_names()
    data.get_release_date()
    data.get_record_company()
    data.get_album_cover_path()
    data.get_colours_from_album_cover()

    data.display()


if __name__ == "__main__":
    main()
