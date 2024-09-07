from typing import Optional

import pandas as pd

from lolla.constants import STAGES, ArtistSize, schedule_schema


class ScheduleConflict:
    """A wrapper around two conflicting artists and their respective stages and hours."""

    def __init__(
        self,
        artist1: ArtistSize,
        hour1: int,
        stage1: str,
        artist2: ArtistSize,
        hour2: int,
        stage2: ArtistSize,
    ):
        self.artist1 = artist1
        self.hour1 = hour1
        self.stage1 = stage1

        self.artist2 = artist2
        self.hour2 = hour2
        self.stage2 = stage2

    def __str__(self):
        return f"Conflict between {self.artist1} at {self.hour1} on {self.stage1} and {self.artist2} at {self.hour2} on {self.stage2}"


def get_schedule_conflict(schedule_df: pd.DataFrame) -> Optional[ScheduleConflict]:
    consecutively = is_any_stage_booked_consecutively(schedule_df)
    simultaneously = are_any_neighbors_simultaneous(schedule_df)

    return consecutively or simultaneously


def is_any_stage_booked_consecutively(
    schedule_df: pd.DataFrame,
) -> Optional[ScheduleConflict]:
    print("Checking if any stages are booked two hours in a row...")
    schedule_schema.validate(schedule_df)
    for stage in STAGES:
        stage_hourly = schedule_df[stage]
        stage_hourly_shifted = stage_hourly.shift(-1)

        consecutive_hour_mask = stage_hourly.notna() & stage_hourly_shifted.notna()
        consecutive_hours = schedule_df[stage].loc[consecutive_hour_mask]
        if not consecutive_hours.empty:
            # Choose the first instance of a conflict (index represents the initial hour)
            hour1 = consecutive_hours.index[0]
            artist1 = consecutive_hours.iloc[0]
            hour2 = hour1 + 1
            artist2 = stage_hourly[hour2]

            conflict = ScheduleConflict(artist1, hour1, stage, artist2, hour2, stage)
            print("Conflict found for stage ", conflict)
            return conflict


def are_any_neighbors_simultaneous(
    schedule_df: pd.DataFrame,
) -> Optional[ScheduleConflict]:
    """Returns: A tuple of idenfitiers for the first cells that were caught to

    Each identifier is an hour and stage
    """
    print("Checking if any neighboring stages are playing at the same time...")
    return None
