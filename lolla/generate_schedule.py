"""Constraints:

- Each stage can be used at most once per hour
- (Bud Light and Tito's) & (IHG and T-Mobile) can't be used at the same time
- The same stage cannot be used in consecutive hours
- For each hour, between 2 and 4 stages must be used
- There are 3 categories of artists: small, medium, large.
  Over the course of the day, artists should tend to get larger , but there's a possibility for randomness
  (e.g. the first hour usually only has small, the middle has a combination of all, the end is mostly large)
"""

import numpy as np
import pandas as pd
import pandera as pa

from lolla.constants import ArtistSize, STAGES, HOURS, schedule_schema
from lolla.constraints import is_schedule_valid


def main():
    schedule_df = generate_initial_schedule()
    display_schedule(schedule_df)
    print("Is the schedule valid?", is_schedule_valid(schedule_df))


@pa.check_types
def generate_initial_schedule() -> pd.DataFrame:
    schedule_df = pd.DataFrame(columns=STAGES, index=HOURS, data={})
    schedule_df.index.name = "hour"

    for hour in (
        HOURS
    ):  # # This is super slow if it matters - applymap is a harder to read alternative
        for stage in STAGES:
            rand = np.random.rand()
            if rand < 0.2:
                schedule_df.at[hour, stage] = ArtistSize.SMALL.name
            elif rand < 0.4:
                schedule_df.at[hour, stage] = ArtistSize.MEDIUM.name
            elif rand < 0.6:
                schedule_df.at[hour, stage] = ArtistSize.LARGE.name

    return schedule_schema.validate(schedule_df)


def display_schedule(schedule_df: pd.DataFrame):
    print(schedule_df)


if __name__ == "__main__":
    main()
