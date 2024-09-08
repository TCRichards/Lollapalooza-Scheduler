from typing import Optional

import pandas as pd

from lolla.constants import NEIGHBORS
from lolla.wrappers import ScheduleConflict, Concert
from lolla import params


def get_first_schedule_conflict(
    schedule_df: pd.DataFrame,
) -> Optional[ScheduleConflict]:
    for stage in schedule_df.columns:
        for hour in schedule_df.index:
            conflict = check_for_conflicts(schedule_df, stage, hour)
            if conflict is not None:
                return conflict


def check_for_conflicts(
    schedule_df: pd.DataFrame, stage: str, hour: int
) -> Optional[ScheduleConflict]:
    conflict_predicates = (
        is_stage_booked_consecutively,
        is_neighbor_booked_simultaneously,
    )
    for pred in conflict_predicates:
        conflict = pred(schedule_df, stage, hour)
        if conflict is not None:
            return conflict


def is_stage_booked_consecutively(
    schedule_df: pd.DataFrame,
    stage: str,
    hour: int,
) -> Optional[ScheduleConflict]:
    if hour == schedule_df.index[-1]:
        return

    this_hour_artist = schedule_df.loc[hour, stage]
    next_hour_artist = schedule_df.loc[hour + 1, stage]
    if not pd.isna(this_hour_artist) and not pd.isna(next_hour_artist):
        this_concert = Concert(artist=this_hour_artist, stage=stage, hour=hour)
        next_concert = Concert(artist=next_hour_artist, stage=stage, hour=hour + 1)
        return ScheduleConflict(this_concert, next_concert)


def is_neighbor_booked_simultaneously(
    schedule_df: pd.DataFrame, stage: str, hour: int
) -> Optional[ScheduleConflict]:
    """Returns: A tuple of idenfitiers for the first cells that were caught to

    Each identifier is an hour and stage
    """
    this_hour_artist = schedule_df.loc[hour, stage]
    if pd.isna(this_hour_artist) or not NEIGHBORS[stage]:
        return 

    neighboring_artist = schedule_df.loc[hour, NEIGHBORS[stage]]
    if not pd.isna(neighboring_artist):
        return ScheduleConflict(
            concert1=Concert(artist=this_hour_artist, stage=stage, hour=hour),
            concert2=Concert(artist=neighboring_artist, stage=NEIGHBORS[stage], hour=hour),
            )


def is_slot_free_and_not_enough_performances_today(schedule_df: pd.DataFrame,
                                                   stage: str,
                                                   hour: int) -> Optional[ScheduleConflict]:
    """If a stage has less than 3 performances in a day, consider an empty slot a conflict."""
    this_hour_artist = schedule_df.loc[hour, stage]
    if not pd.isna(this_hour_artist):
        return

    this_stage_artist_count = schedule_df[stage].count()
    if this_stage_artist_count < params.MIN_ARTISTS_PER_STAGE_PER_DAY:
        return ScheduleConflict(concert1=Concert(this_hour_artist, stage, hour), concert2=Concert(this_hour_artist, stage, hour))
