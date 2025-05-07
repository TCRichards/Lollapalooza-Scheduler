"""Constraints on the schedule that must be satisfied."""

from typing import Optional

import pandas as pd

from collections import defaultdict
from lolla.wrappers import ScheduleConflict, Concert, ArtistSize
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
        is_slot_free_and_not_enough_performances_today,
        is_size_window_violated,
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
    # Represents stages that can't play at the same time
    NEIGHBORS = defaultdict(lambda: None, {
        "Bud Light": "Tito's",
        "IHG": "T-Mobile",
    })

    # Add the reverse mapping and map stages without neighbords to None
    NEIGHBORS |= {v: k for k, v in NEIGHBORS.items()}

    this_hour_artist = schedule_df.loc[hour, stage]
    if pd.isna(this_hour_artist) or not NEIGHBORS[stage]:
        return

    neighboring_artist = schedule_df.loc[hour, NEIGHBORS[stage]]
    if not pd.isna(neighboring_artist):
        return ScheduleConflict(
            concert1=Concert(artist=this_hour_artist, stage=stage, hour=hour),
            concert2=Concert(
                artist=neighboring_artist, stage=NEIGHBORS[stage], hour=hour
            ),
        )


def is_slot_free_and_not_enough_performances_today(
    schedule_df: pd.DataFrame, stage: str, hour: int
) -> Optional[ScheduleConflict]:
    """If a stage has less than 3 performances in a day, consider an empty slot a conflict."""
    this_hour_artist = schedule_df.loc[hour, stage]
    if not pd.isna(this_hour_artist):
        return

    this_stage_artist_count = schedule_df[stage].count()
    if this_stage_artist_count < params.MIN_ARTISTS_PER_STAGE_PER_DAY:
        return ScheduleConflict(
            concert1=Concert(this_hour_artist, stage, hour),
            concert2=Concert(this_hour_artist, stage, hour),
        )


def is_size_window_violated(
    schedule_df: pd.DataFrame, stage: str, hour: int
) -> Optional[ScheduleConflict]:
    """A basic constraint that checks if the artist size is allowed at this hour.
    
    This is used to enforce that artists gradually get bigger as the day goes on.
    """
    # map hour -> allowed artist sizes
    ALLOWED_SIZES = {
        # 12–2 PM only small
        **{h: {ArtistSize.SMALL} for h in range(12, 14)},
        # 2–5 PM: small or medium
        **{h: {ArtistSize.SMALL, ArtistSize.MEDIUM} for h in range(14, 17)},
        # 5–7 PM: any size
        **{h: {ArtistSize.SMALL, ArtistSize.MEDIUM, ArtistSize.LARGE} for h in range(17, 20)},
        # 7 - 9 PM medium or large
        **{h: {ArtistSize.MEDIUM, ArtistSize.LARGE} for h in range(20, 22)},
        # 9 - 11 PM: large only
        **{h: {ArtistSize.LARGE} for h in range(22, 23)},
    }

    scheduled_artist = schedule_df.loc[hour, stage]
    if pd.isna(scheduled_artist):
        return

    if scheduled_artist.size not in ALLOWED_SIZES[hour]:
        return ScheduleConflict(
            Concert(scheduled_artist, stage, hour),
            Concert(scheduled_artist, stage, hour),
        )
