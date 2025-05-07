from __future__ import annotations

from lolla.artists import ArtistSize

class Concert:
    def __init__(self, artist: ArtistSize, stage: str, hour: int):
        self.artist = artist
        self.hour = hour
        self.stage = stage

        if not (
            isinstance(artist, ArtistSize)
            or isinstance(stage, str)
            or isinstance(hour, int)
        ):
            raise ValueError(f"Invalid Concert: {self}")

    def __repr__(self) -> str:
        return f"{self.artist} at {self.hour}:00 at {self.stage}"


class ScheduleConflict:
    """A wrapper that represents two concerts that somehow conflict with each other."""

    def __init__(
        self,
        concert1: Concert,
        concert2: Concert,
    ):
        self.concert1 = concert1
        self.concert2 = concert2

    def __str__(self):
        return f"Conflict between {self.concert1} and {self.concert2}"

    def __eq__(self, other: ScheduleConflict) -> bool:
        others = (other.concert1, other.concert2)
        return self.concert1 in others and self.concert2 in others
