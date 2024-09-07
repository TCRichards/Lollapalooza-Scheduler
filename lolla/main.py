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
import pandera as pa

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


@pa.check_types
def generate_initial_schedule() -> pd.DataFrame:
    schedule_df = pd.DataFrame(columns=STAGES, index=HOURS, data={})
    schedule_df.index.name = "hour"

    for hour in (
        HOURS
    ):  # # This is super slow if it matters - applymap is a harder to read alternative
        for stage in STAGES:
            rand = np.random.rand()
            if rand < 0.1:
                schedule_df.at[hour, stage] = ArtistSize.SMALL.name
            elif rand < 0.2:
                schedule_df.at[hour, stage] = ArtistSize.MEDIUM.name
            elif rand < 0.3:
                schedule_df.at[hour, stage] = ArtistSize.LARGE.name

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

    print(f"Swapping {artist1} at {hour1} on {stage1} with {artist2} at {hour2} on {stage2}...")
    schedule_df.at[hour1, stage1] = artist2
    schedule_df.at[hour2, stage2] = artist1

    return schedule_df


def display_schedule(schedule_df: pd.DataFrame):
    print(f"Schedule:\n{schedule_df}")


if __name__ == "__main__":
    main()
