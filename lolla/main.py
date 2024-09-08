"""Constraints:

- Each stage can be used at most once per hour
- (Bud Light and Tito's) & (IHG and T-Mobile) can't be used at the same time
- The same stage cannot be used in consecutive hours
- For each hour, between 2 and 4 stages must be used
- There are 3 categories of artists: small, medium, large.
  Over the course of the day, artists should tend to get larger , but there's a possibility for randomness
  (e.g. the first hour usually only has small, the middle has a combination of all, the end is mostly large)
"""

import random

import numpy as np
import pandas as pd

from lolla.constants import ArtistSize, STAGES, HOURS, schedule_schema
from lolla.constraints import get_schedule_conflict, ScheduleConflict


def main():
    print("=" * 55 + "\nGenerating Lollapalooza Schedule\n" + "=" * 55)
    schedule_df = generate_valid_schedule()
    print(f"Valid Schedule:\n{schedule_df}")


def generate_valid_schedule() -> pd.DataFrame:
    schedule_df = generate_initial_schedule()
    print(f"Initial schedule:\n{schedule_df}")
    return fix_schedule_conflicts(schedule_df)


def generate_initial_schedule() -> pd.DataFrame:
    schedule_df = pd.DataFrame(columns=STAGES, index=HOURS, data={})
    schedule_df.index.name = "hour"

    # This decision can significantly impact the game, so make it tunable
    total_slots = len(STAGES) * len(HOURS)

    EVENT_FREQUENCY = 0.4  # What stage/hour slots are filled
    SMALL_ARTIST_FREQUENCY = 0.45
    MEDIUM_ARTIST_FREQUENCY = 0.35
    LARGE_ARTIST_FRQUENCY = 0.2 
    assert (
         SMALL_ARTIST_FREQUENCY + LARGE_ARTIST_FRQUENCY + MEDIUM_ARTIST_FREQUENCY == 1
    ), "Artist frequencies must sum to 1"

    num_small_artists = total_slots * EVENT_FREQUENCY * SMALL_ARTIST_FREQUENCY
    num_medium_artists = total_slots * EVENT_FREQUENCY * MEDIUM_ARTIST_FREQUENCY
    num_large_artists = total_slots * EVENT_FREQUENCY * LARGE_ARTIST_FRQUENCY
    artist_to_num = {
        ArtistSize.SMALL: num_small_artists,
        ArtistSize.MEDIUM: num_medium_artists,
        ArtistSize.LARGE: num_large_artists
    }

    for artist_size, artist_count in artist_to_num.items():
        while artist_count > 0:
            hour = random.choice(HOURS)
            stage = random.choice(STAGES)
            schedule_df.at[hour, stage] = artist_size.name
            artist_count -= 1

    return schedule_schema.validate(schedule_df)


def fix_schedule_conflicts(schedule_df: pd.DataFrame) -> pd.DataFrame:
    conflict = get_schedule_conflict(schedule_df)
    while conflict is not None:
        schedule_df = swap_slots(schedule_df, conflict)
        conflict = get_schedule_conflict(schedule_df)

    print("No conflicts remaining")
    return schedule_df


def swap_slots(schedule_df: pd.DataFrame, conflict: ScheduleConflict):
    print(f"Swapping slots due to {conflict}")
    # Swap one of the conflicting artists with a random slot
    stage1 = conflict.stage1
    artist1 = conflict.artist1
    hour1 = conflict.hour1

    stage2 = random.choice(STAGES)
    hour2 = random.choice(HOURS)
    artist2 = schedule_df.at[hour2, stage2]

    print(
        f"Swapping {artist1} at {hour1} on {stage1} with {artist2} at {hour2} on {stage2}..."
    )
    schedule_df.at[hour1, stage1] = artist2
    schedule_df.at[hour2, stage2] = artist1

    return schedule_df


def display_schedule(schedule_df: pd.DataFrame):
    print(f"Schedule:\n{schedule_df}")


if __name__ == "__main__":
    main()
