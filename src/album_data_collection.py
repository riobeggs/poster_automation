import calendar
import csv
import os
import urllib.request

import spotipy
from colorthief import ColorThief
from PIL import Image

from .credentials import client_credentials_manager

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class AlbumData:
    def __init__(self) -> None:
        self._album_object = None
        self._artist_object = None

        self._album_id = None
        self._album_name = None
        self._artist_id = None
        self._artist_name = None
        self._artist_genre = None
        self._track_names = None
        self._release_date = None
        self._record_company = None
        self._album_cover_image_url = None
        self._album_cover_path = None
        self._colour_palette = []
        self._colour_1 = None
        self._colour_2 = None
        self._colour_3 = None
        self._colour_4 = None
        self._colour_5 = None

    def get_album_id(self) -> None:
        """
        Locates an albums id from the album URL given by the user.
        """
        album_url = input("\nAlbum link: ")

        # Remove after testing ---------------------------------------------------------------------->
        # album_url = "https://open.spotify.com/album/2mpzeA7pHNIDAPii4EEKsB?si=7rnnAkzuT1mbT3AyJgSkCQ"
        # ------------------------------------------------------------------------------------------->
        self._album_id = album_url.split("/")[-1].split("?")[0]

    def create_album_object(self) -> None:
        """
        Creates album obejct for querying.
        """
        self._album_object = spotify.album(self._album_id)

    def create_artist_object(self) -> None:
        """
        Creates artist object for querying.
        """
        self._artist_object = spotify.artist(self._artist_id)

    def get_album_name(self) -> None:
        """
        Queries album for albums name and stores it as a string.
        """
        self._album_name = self._album_object["name"].upper()

    def get_artist_id(self) -> None:
        """
        Queries album for albums name and stores it as a string.
        """
        artist = self._album_object["artists"][0]

        self._artist_id = artist["id"]

    def get_artist_name(self) -> None:
        """
        Queries album for artists name and stores it as a string.
        """
        self._artist_name = self._artist_object["name"].upper()

    def get_artist_genre(self) -> None:
        """
        Queries artist for genres and stores main genre as a string.
        """
        genres = self._artist_object["genres"]
        genre = genres[0]

        self._artist_genre = genre.title()

    def get_track_names(self) -> None:
        """
        Creates a string with ordered track names separated by "/n"
        """
        tracks = spotify.album_tracks(self._album_id)["items"]
        track_names = []
        track_number = 0

        for track in tracks:

            track_number += 1
            track_name = track["name"].upper()

            track = f"{track_number}. {track_name}"

            track_names.append(track)

        self._track_names = "\n".join(track_names)

    def get_release_date(self) -> None:
        """
        Queries album for release date and stores it as a string.
        """
        date = self._album_object["release_date"]

        if self._album_object["release_date_precision"] != "year":

            date = date.split("-")
            date[1] = calendar.month_name[int(date[1])]
            date = f"{date[2]} {date[1]} {date[0]}"

            self._release_date = date.upper()

        else:

            self._release_date = date

    def get_record_company(self) -> None:
        """
        Queries album for record company and stores it as a string.
        """
        record_company = self._album_object["copyrights"][0]

        self._record_company = record_company["text"]

    def get_album_cover_path(self) -> None:
        """
        Queries album for album covers URL,
        downloads the image and stores the file path as a string.
        """
        images = self._album_object["images"][0]

        self._album_cover_image_url = images["url"]
        self._album_cover_path = f"covers/album_cover.jpg"

        self.download_album_cover()

        self._full_album_cover_path = os.path.abspath(self._album_cover_path)

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

            hex_colour = f"#{colour[0]:02x}{colour[1]:02x}{colour[2]:02x}"

            self._colour_palette.append(hex_colour)

    def download_colour_palette_images(self) -> None:
        """
        Downloads hexcode colours as images as stores their file paths as strings.
        """
        if not os.path.exists("colour_palette_img"):
            os.mkdir("colour_palette_img")

        colour_number = 0
        paths = []

        for colour in self._colour_palette:

            colour_number += 1

            image_path = f"colour_palette_img/colour_{colour_number}.jpg"

            image = Image.new("RGB", (100, 100), colour)
            image.save(image_path)

            paths.append(os.path.abspath(image_path))

        (
            self._colour_1,
            self._colour_2,
            self._colour_3,
            self._colour_4,
            self._colour_5,
        ) = (paths[0], paths[1], paths[2], paths[3], paths[4])

    def create_csv(self) -> None:
        """
        Creates a csv file containing relative data about the album.
        """
        if not os.path.exists("csv_files"):
            os.mkdir("csv_files")
        columns = [
            "album_name",
            "artist_name",
            "tracks",
            "genre",
            "date",
            "record_company",
            "album_cover",
            "colour_1",
            "colour_2",
            "colour_3",
            "colour_4",
            "colour_5",
        ]

        data = [
            self._album_name,
            self._artist_name,
            self._track_names,
            self._artist_genre,
            self._release_date,
            self._record_company,
            self._full_album_cover_path,
            self._colour_1,
            self._colour_2,
            self._colour_3,
            self._colour_4,
            self._colour_5,
        ]

        with open(f"csv_files/album_data.csv", "w", encoding="UTF8", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(columns)
            writer.writerow(data)

    def display(self) -> None:
        """
        Displays data collected (used for testing)
        """
        print()
        print(f"Album ID: {self._album_id}")
        print(f"Album name: {self._album_name}")
        # print(f"Artist ID: {self._artist_id}")
        print(f"Artist name: {self._artist_name}")
        print(f"Artist genre: {self._artist_genre}")
        print(f"Album track names: {self._track_names}")
        print(f"Album release date: {self._release_date}")
        print(f"Record company: {self._record_company}")
        # print(f"Album cover url: {self._album_cover_image_url}")
        print(f"Full album cover file path: {self._full_album_cover_path}")
        print(f"Colour palette: {self._colour_palette}")
        print()

    def run(self) -> None:
        """
        Runs methods for retrieving relative data.
        """
        self.get_album_id()
        self.create_album_object()
        self.get_artist_id()
        self.create_artist_object()
        self.get_album_name()
        self.get_artist_name()
        self.get_artist_genre()
        self.get_track_names()
        self.get_release_date()
        self.get_record_company()
        self.get_album_cover_path()
        self.get_colours_from_album_cover()
        self.download_colour_palette_images()
        self.create_csv()

        # self.display()


def main():
    data = AlbumData()

    data.get_album_id()
    data.create_album_object()
    data.get_artist_id()
    data.create_artist_object()
    data.get_album_name()
    data.get_artist_name()
    data.get_artist_genre()
    data.get_track_names()
    data.get_release_date()
    data.get_record_company()
    data.get_album_cover_path()
    data.get_colours_from_album_cover()
    data.download_colour_palette_images()
    data.create_csv()

    # data.display()


if __name__ == "__main__":
    main()
