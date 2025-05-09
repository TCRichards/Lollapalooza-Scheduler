from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import random


class ArtistSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Genre(Enum):
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
    

# Map each size to a list of artists (10 per genre × size)
size_to_artist_dict: dict[ArtistSize, list[Artist]] = {
    ArtistSize.SMALL: [],
    ArtistSize.MEDIUM: [],
    ArtistSize.LARGE: [],
}

# === Indie Artists ===
size_to_artist_dict[ArtistSize.SMALL].extend(
    [
        Artist("Homescool", ArtistSize.SMALL, Genre.INDIE),
        Artist("Eddie", ArtistSize.SMALL, Genre.INDIE),
        Artist("Courtney Barnett", ArtistSize.SMALL, Genre.INDIE),
        Artist("Parcels", ArtistSize.SMALL, Genre.INDIE),
        Artist("Morgan Wade", ArtistSize.SMALL, Genre.INDIE),
        Artist("Blondshell", ArtistSize.SMALL, Genre.INDIE),
        Artist("Sudan Archives", ArtistSize.SMALL, Genre.INDIE),
        Artist("Beabadoobee", ArtistSize.SMALL, Genre.INDIE),
        Artist("Men I Trust", ArtistSize.SMALL, Genre.INDIE),
        Artist("Sales", ArtistSize.SMALL, Genre.INDIE),
    ]
)
size_to_artist_dict[ArtistSize.MEDIUM].extend(
    [
        Artist("Clairo", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Japanese Breakfast", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Phoebe Bridgers", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("The 1975", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Beach House", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Faye Webster", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Rex Orange County", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Soccer Mommy", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Alvvays", ArtistSize.MEDIUM, Genre.INDIE),
        Artist("Snail Mail", ArtistSize.MEDIUM, Genre.INDIE),
    ]
)
size_to_artist_dict[ArtistSize.LARGE].extend(
    [
        Artist("Arcade Fire", ArtistSize.LARGE, Genre.INDIE),
        Artist("Bon Iver", ArtistSize.LARGE, Genre.INDIE),
        Artist("Cage the Elephant", ArtistSize.LARGE, Genre.INDIE),
        Artist("Foster the People", ArtistSize.LARGE, Genre.INDIE),
        Artist("The Killers", ArtistSize.LARGE, Genre.INDIE),
        Artist("Tame Impala", ArtistSize.LARGE, Genre.INDIE),
        Artist("Florence + The Machine", ArtistSize.LARGE, Genre.INDIE),
        Artist("LCD Soundsystem", ArtistSize.LARGE, Genre.INDIE),
        Artist("MGMT", ArtistSize.LARGE, Genre.INDIE),
        Artist("Sufjan Stevens", ArtistSize.LARGE, Genre.INDIE),
    ]
)

# === Pop Artists ===
size_to_artist_dict[ArtistSize.SMALL].extend(
    [
        Artist("mxmtoon", ArtistSize.SMALL, Genre.POP),
        Artist("Benee", ArtistSize.SMALL, Genre.POP),
        Artist("Ruel", ArtistSize.SMALL, Genre.POP),
        Artist("Benson Boone", ArtistSize.SMALL, Genre.POP),
        Artist("Daya", ArtistSize.SMALL, Genre.POP),
        Artist("Charlotte Lawrence", ArtistSize.SMALL, Genre.POP),
        Artist("Audrey Mika", ArtistSize.SMALL, Genre.POP),
        Artist("CVBZ", ArtistSize.SMALL, Genre.POP),
        Artist("Lauren Spencer-Smith", ArtistSize.SMALL, Genre.POP),
        Artist("Girl in Red", ArtistSize.SMALL, Genre.POP),
    ]
)
size_to_artist_dict[ArtistSize.MEDIUM].extend(
    [
        Artist("Sabrina Carpenter", ArtistSize.MEDIUM, Genre.POP),
        Artist("Victoria Monét", ArtistSize.MEDIUM, Genre.POP),
        Artist("J Balvin", ArtistSize.MEDIUM, Genre.POP),
        Artist("Ice Spice", ArtistSize.MEDIUM, Genre.POP),
        Artist("Omar Apollo", ArtistSize.MEDIUM, Genre.POP),
        Artist("Troye Sivan", ArtistSize.MEDIUM, Genre.POP),
        Artist("Charlie Puth", ArtistSize.MEDIUM, Genre.POP),
        Artist("Julia Michaels", ArtistSize.MEDIUM, Genre.POP),
        Artist("Bazzi", ArtistSize.MEDIUM, Genre.POP),
        Artist("Conan Gray", ArtistSize.MEDIUM, Genre.POP),
    ]
)
size_to_artist_dict[ArtistSize.LARGE].extend(
    [
        Artist("Taylor Swift", ArtistSize.LARGE, Genre.POP),
        Artist("Beyoncé", ArtistSize.LARGE, Genre.POP),
        Artist("Ariana Grande", ArtistSize.LARGE, Genre.POP),
        Artist("Ed Sheeran", ArtistSize.LARGE, Genre.POP),
        Artist("SZA", ArtistSize.LARGE, Genre.POP),
        Artist("Billie Eilish", ArtistSize.LARGE, Genre.POP),
        Artist("The Weeknd", ArtistSize.LARGE, Genre.POP),
        Artist("Harry Styles", ArtistSize.LARGE, Genre.POP),
        Artist("Rihanna", ArtistSize.LARGE, Genre.POP),
        Artist("Bruno Mars", ArtistSize.LARGE, Genre.POP),
    ]
)

# === EDM Artists ===
size_to_artist_dict[ArtistSize.SMALL].extend(
    [
        Artist("Dom Dolla", ArtistSize.SMALL, Genre.EDM),
        Artist("Flux Pavilion", ArtistSize.SMALL, Genre.EDM),
        Artist("Bob Moses", ArtistSize.SMALL, Genre.EDM),
        Artist("SG Lewis", ArtistSize.SMALL, Genre.EDM),
        Artist("DJ Seinfeld", ArtistSize.SMALL, Genre.EDM),
        Artist("Lane 8", ArtistSize.SMALL, Genre.EDM),
        Artist("Mura Masa", ArtistSize.SMALL, Genre.EDM),
        Artist("Louis The Child", ArtistSize.SMALL, Genre.EDM),
        Artist("TOKiMONSTA", ArtistSize.SMALL, Genre.EDM),
        Artist("Shallou", ArtistSize.SMALL, Genre.EDM),
    ]
)
size_to_artist_dict[ArtistSize.MEDIUM].extend(
    [
        Artist("Zedd", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Diplo", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Illenium", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Fisher", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Alison Wonderland", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Kygo", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Marshmello", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Calvin Harris", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Porter Robinson", ArtistSize.MEDIUM, Genre.EDM),
        Artist("Madeon", ArtistSize.MEDIUM, Genre.EDM),
    ]
)
size_to_artist_dict[ArtistSize.LARGE].extend(
    [
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
    ]
)

# === Rap / Hip-Hop Artists ===
size_to_artist_dict[ArtistSize.SMALL].extend(
    [
        Artist("Cordae", ArtistSize.SMALL, Genre.RAP),
        Artist("Joey Bada$$", ArtistSize.SMALL, Genre.RAP),
        Artist("Noname", ArtistSize.SMALL, Genre.RAP),
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
    ]
)
size_to_artist_dict[ArtistSize.LARGE].extend(
    [
        Artist("Drake", ArtistSize.LARGE, Genre.RAP),
        Artist("Kendrick Lamar", ArtistSize.LARGE, Genre.RAP),
        Artist("Jay-Z", ArtistSize.LARGE, Genre.RAP),
        Artist("Eminem", ArtistSize.LARGE, Genre.RAP),
        Artist("Future × Metro Boomin", ArtistSize.LARGE, Genre.RAP),
        Artist("Travis Scott", ArtistSize.LARGE, Genre.RAP),
        Artist("Nicki Minaj", ArtistSize.LARGE, Genre.RAP),
        Artist("Lil Wayne", ArtistSize.LARGE, Genre.RAP),
        Artist("Cardi B", ArtistSize.LARGE, Genre.RAP),
        Artist("Kanye West", ArtistSize.LARGE, Genre.RAP),
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
