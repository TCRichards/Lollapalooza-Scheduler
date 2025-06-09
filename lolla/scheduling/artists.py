"""Module defining the Artist class, as well as creating a bunch of artists to choose from when generating a schedule."""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import random

import pandas as pd

from pandas._libs.missing import NAType


class ArtistSize(Enum):
    """Artists can be roughly SMALL, MEDIUM, or LARGE.
    
    The default point value in the game is determined by the size of the artist.
    """
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Genre(Enum):
    """Enum representing different music genres.
    
    In the game, a player selects their favorite genre,
    and receive more points for attending concerts of that genre.
    """
    POP = 1
    RAP = 2
    EDM = 3
    INDIE = 4


@dataclass
class Artist:
    name: str
    size: ArtistSize
    genre: Genre

    def __repr__(self) -> str:
        return f"{self.name}<br>Size: {self.size.name.title()}<br>Genre: {self.genre.name.title()}"
    
    @classmethod
    def from_str(cls, artist_str: str | NAType) -> Artist | NAType:
        """Create an Artist instance from a string representation."""
        if pd.isna(artist_str):
            return pd.NA

        name, size_str, genre_str = artist_str.split("<br>")
        size = ArtistSize[size_str.split(": ")[1].upper()]
        genre = Genre[genre_str.split(": ")[1].upper()]
        return cls(name=name, size=size, genre=genre)
    
    def to_dict(self) -> dict:
        """Convert Artist to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "size": self.size.name,
            "genre": self.genre.name,
            "_type": "Artist"
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Artist":
        """Create Artist from dictionary."""
        if data is None or not isinstance(data, dict) or data.get("_type") != "Artist":
            return None
        return cls(
            name=data["name"],
            size=ArtistSize[data["size"]],
            genre=Genre[data["genre"]]
        )
    
    def to_display(self) -> str:
        ICONS = {
            Genre.INDIE: "🎸",
            Genre.POP: "🎤",
            Genre.EDM: "🎛🔊️",
            Genre.RAP: "🔥",
        }

        return f"{ICONS[self.genre]} {self.name}<br>{self.size.name.title()}<br>{self.genre.name.title()}"

# Map each size to a list of artists (10 per genre × size)
size_to_artist_dict: dict[ArtistSize, list[Artist]] = {
    ArtistSize.SMALL: [],
    ArtistSize.MEDIUM: [],
    ArtistSize.LARGE: [],
}

# === Indie Artists ===
size_to_artist_dict[ArtistSize.SMALL].extend(
    [
        Artist("Eddie", ArtistSize.SMALL, Genre.INDIE),
        Artist("Eggy", ArtistSize.SMALL, Genre.INDIE),
        Artist("Courtney Barnett", ArtistSize.SMALL, Genre.INDIE),
        Artist("Parcels", ArtistSize.SMALL, Genre.INDIE),
        Artist("Morgan Wade", ArtistSize.SMALL, Genre.INDIE),
        Artist("Sincere Engineer", ArtistSize.SMALL, Genre.INDIE),
        Artist("Blondshell", ArtistSize.SMALL, Genre.INDIE),
        Artist("Men I Trust", ArtistSize.SMALL, Genre.INDIE),
        Artist("Sales", ArtistSize.SMALL, Genre.INDIE),
    ]
)
size_to_artist_dict[ArtistSize.MEDIUM].extend(
    [
        Artist("Couch", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Lawrence", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Beabadoobee", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Clairo", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Japanese Breakfast", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Phoebe Bridgers", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("The 1975", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Madison Cunningham", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Beach House", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Faye Webster", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Rex Orange County", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Lizzy McAlpine", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("The Marias", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Unknown Mortal Orchestra", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Peach Pitt", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Flipturn", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Mt. Joy", ArtistSize.MEDIUM, Genre.INDIE),
    ]
)
size_to_artist_dict[ArtistSize.LARGE].extend(
    [
        Artist("Bon Iver", ArtistSize.LARGE, Genre.INDIE),
        Artist("Hozier", ArtistSize.LARGE, Genre.INDIE),
        Artist("Noah Kahan", ArtistSize.LARGE, Genre.INDIE),
        Artist("Cage the Elephant", ArtistSize.LARGE, Genre.INDIE),
        Artist("Foster the People", ArtistSize.LARGE, Genre.INDIE),
        Artist("The Killers", ArtistSize.LARGE, Genre.INDIE),
        Artist("Tame Impala", ArtistSize.LARGE, Genre.INDIE),
        Artist("Florence + The Machine", ArtistSize.LARGE, Genre.INDIE),
        Artist("LCD Soundsystem", ArtistSize.LARGE, Genre.INDIE),
        Artist("MGMT", ArtistSize.LARGE, Genre.INDIE),
        Artist("Hippo Campus", ArtistSize.LARGE, Genre.INDIE),
    ]
)

# === Pop Artists ===
size_to_artist_dict[ArtistSize.SMALL].extend(
    [
        Artist("Daya", ArtistSize.SMALL, Genre.POP),
        Artist("Charlotte Lawrence", ArtistSize.SMALL, Genre.POP),
        Artist("Audrey Mika", ArtistSize.SMALL, Genre.POP),
        Artist("CVBZ", ArtistSize.SMALL, Genre.POP),
        Artist("Lauren Spencer-Smith", ArtistSize.SMALL, Genre.POP),
        Artist("Sam Fischer", ArtistSize.SMALL, Genre.POP),
        Artist("Lyn Lapid", ArtistSize.SMALL, Genre.POP),
        Artist("JP Cooper", ArtistSize.SMALL, Genre.POP),
    ]
)
size_to_artist_dict[ArtistSize.MEDIUM].extend(
    [
        Artist("Benee", ArtistSize.MEDIUM, Genre.POP),
        Artist("Ruel", ArtistSize.MEDIUM, Genre.POP),
        Artist("mxmtoon", ArtistSize.MEDIUM, Genre.POP),
        Artist("Victoria Monét", ArtistSize.MEDIUM, Genre.POP),
        Artist("J Balvin", ArtistSize.MEDIUM, Genre.POP),
        Artist("Ice Spice", ArtistSize.MEDIUM, Genre.POP),
        Artist("Omar Apollo", ArtistSize.MEDIUM, Genre.POP),
        Artist("Troye Sivan", ArtistSize.MEDIUM, Genre.POP),
        Artist("Charlie Puth", ArtistSize.MEDIUM, Genre.POP),
        Artist("Julia Michaels", ArtistSize.MEDIUM, Genre.POP),
        Artist("Bazzi", ArtistSize.MEDIUM, Genre.POP),
        Artist("Conan Gray", ArtistSize.MEDIUM, Genre.POP),
        Artist("Girl in Red", ArtistSize.MEDIUM, Genre.POP),
        Artist("RAYE", ArtistSize.MEDIUM, Genre.POP),
        Artist("dodie", ArtistSize.MEDIUM, Genre.POP),
        Artist("Teddy Swims", ArtistSize.MEDIUM, Genre.POP),
    ]
)
size_to_artist_dict[ArtistSize.LARGE].extend(
    [
        Artist("Sabrina Carpenter", ArtistSize.LARGE, Genre.POP),
        Artist("Taylor Swift", ArtistSize.LARGE, Genre.POP),
        Artist("Beyoncé", ArtistSize.LARGE, Genre.POP),
        Artist("Ariana Grande", ArtistSize.LARGE, Genre.POP),
        Artist("Ed Sheeran", ArtistSize.LARGE, Genre.POP),
        Artist("Billie Eilish", ArtistSize.LARGE, Genre.POP),
        Artist("The Weeknd", ArtistSize.LARGE, Genre.POP),
        Artist("Harry Styles", ArtistSize.LARGE, Genre.POP),
        Artist("Rihanna", ArtistSize.LARGE, Genre.POP),
        Artist("Bruno Mars", ArtistSize.LARGE, Genre.POP),
        Artist("Benson Boone", ArtistSize.LARGE, Genre.POP),
        Artist("Olivia Rodrigo", ArtistSize.LARGE, Genre.POP),
    ]
)

# === EDM Artists ===
size_to_artist_dict[ArtistSize.SMALL].extend(
    [
        Artist("Flux Pavilion", ArtistSize.SMALL, Genre.EDM),
        Artist("Bob Moses", ArtistSize.SMALL, Genre.EDM),
        Artist("SG Lewis", ArtistSize.SMALL, Genre.EDM),
        Artist("DJ Seinfeld", ArtistSize.SMALL, Genre.EDM),
        Artist("Lane 8", ArtistSize.SMALL, Genre.EDM),
        Artist("Mura Masa", ArtistSize.SMALL, Genre.EDM),
        Artist("TOKiMONSTA", ArtistSize.SMALL, Genre.EDM),
        Artist("Shallou", ArtistSize.SMALL, Genre.EDM),
    ]
)
size_to_artist_dict[ArtistSize.MEDIUM].extend(
    [
        Artist("Dom Dolla", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Louis The Child", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Diplo", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Illenium", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Fisher", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Alison Wonderland", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Kygo", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Marshmello", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Calvin Harris", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Porter Robinson", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Madeon", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Gesaffelstein", ArtistSize.MEDIUM, Genre.EDM),
    ]
)
size_to_artist_dict[ArtistSize.LARGE].extend(
    [
        Artist("Zedd", ArtistSize.LARGE, Genre.EDM),
        Artist("Martin Garrix", ArtistSize.LARGE, Genre.EDM),
        Artist("Tiësto", ArtistSize.LARGE, Genre.EDM),
        Artist("David Guetta", ArtistSize.LARGE, Genre.EDM),
        Artist("Swedish House Mafia", ArtistSize.LARGE, Genre.EDM),
        Artist("Armin van Buuren", ArtistSize.LARGE, Genre.EDM),
        Artist("Skrillex", ArtistSize.LARGE, Genre.EDM),
        Artist("Deadmau5", ArtistSize.LARGE, Genre.EDM),
        Artist("Avicii", ArtistSize.LARGE, Genre.EDM),
        Artist("Steve Aoki", ArtistSize.LARGE, Genre.EDM),
        Artist("Eric Prydz", ArtistSize.LARGE, Genre.EDM),
        Artist("ODESZA", ArtistSize.LARGE, Genre.EDM),
    ]
)

# === Rap / Hip-Hop Artists ===
size_to_artist_dict[ArtistSize.SMALL].extend(
    [
        Artist("Cordae", ArtistSize.SMALL, Genre.RAP),
        Artist("EarthGang", ArtistSize.SMALL, Genre.RAP),
        Artist("Saba", ArtistSize.SMALL, Genre.RAP),
        Artist("Denzel Curry", ArtistSize.SMALL, Genre.RAP),
        Artist("IDK", ArtistSize.SMALL, Genre.RAP),
        Artist("Rapsody", ArtistSize.SMALL, Genre.RAP),
        Artist("GoldLink", ArtistSize.SMALL, Genre.RAP),
        Artist("Mick Jenkins", ArtistSize.SMALL, Genre.RAP),
    ]
)
size_to_artist_dict[ArtistSize.MEDIUM].extend(
    [
        Artist("Doja Cat", ArtistSize.MEDIUM, Genre.RAP),
        Artist("Lil Baby", ArtistSize.MEDIUM, Genre.RAP),
        Artist("Roddy Ricch", ArtistSize.MEDIUM, Genre.RAP),
        Artist("Lil Tjay", ArtistSize.MEDIUM, Genre.RAP),
        Artist("DaBaby", ArtistSize.MEDIUM, Genre.RAP),
        Artist("Post Malone", ArtistSize.MEDIUM, Genre.RAP),
        Artist("21 Savage", ArtistSize.MEDIUM, Genre.RAP),
        Artist("Saweetie", ArtistSize.MEDIUM, Genre.RAP),
        Artist("Gunna", ArtistSize.MEDIUM, Genre.RAP),
        Artist("Jack Harlow", ArtistSize.MEDIUM, Genre.RAP),
        Artist("Joey Bada$$", ArtistSize.MEDIUM, Genre.RAP),
        Artist("Noname", ArtistSize.MEDIUM, Genre.RAP),
    ]
)
size_to_artist_dict[ArtistSize.LARGE].extend(
    [
        Artist("Kendrick Lamar", ArtistSize.LARGE, Genre.RAP),
        Artist("SZA", ArtistSize.LARGE, Genre.POP),
        Artist("Doechii", ArtistSize.LARGE, Genre.POP),
        Artist("Jay-Z", ArtistSize.LARGE, Genre.RAP),
        Artist("Future x Metro Boomin", ArtistSize.LARGE, Genre.RAP),
        Artist("J Cole", ArtistSize.LARGE, Genre.RAP),
        Artist("Tyler, The Creator", ArtistSize.LARGE, Genre.RAP),
        Artist("Travis Scott", ArtistSize.LARGE, Genre.RAP),
        Artist("Nicki Minaj", ArtistSize.LARGE, Genre.RAP),
        Artist("Lil Wayne", ArtistSize.LARGE, Genre.RAP),
        Artist("Cardi B", ArtistSize.LARGE, Genre.RAP),
    ]
)


def get_random_artist_of_size(size: ArtistSize) -> Artist:
    """Return a random Artist instance matching the given size."""
    return random.choice(size_to_artist_dict[size])


if __name__ == "__main__":
    # Test the function
    for size in ArtistSize:
        artist = get_random_artist_of_size(size)
        print(f"Random {size.name.title()} Artist: {artist}")
