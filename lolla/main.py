import random
from pathlib import Path

import pandera as pa
import pandas as pd

from lolla.constants import (
    STAGES,
    HOURS,
)
from lolla.wrappers import ArtistSize
from lolla.constraints import (
    get_first_schedule_conflict,
    ScheduleConflict,
    Concert,
    check_for_conflicts,
)
from lolla import params
from lolla.visualize import display_schedule
from lolla.artists import get_random_artist_of_size




def generate_valid_schedule() -> pd.DataFrame:
    schedule_df = generate_initial_schedule()
    print(f"Initial schedule:\n{schedule_df}")
    return fix_schedule_conflicts(schedule_df)


def generate_initial_schedule() -> pd.DataFrame:
    """Generate an initial schedule DataFrame with Artist objects assigned to stages and hours."""
    schedule_df = pd.DataFrame(columns=STAGES, index=HOURS, data={})
    schedule_df.index.name = "hour"

    total_slots = len(STAGES) * len(HOURS)
    num_small_artists = int(
        total_slots * params.EVENT_FREQUENCY * params.SMALL_ARTIST_FREQUENCY
    )
    num_medium_artists = int(
        total_slots * params.EVENT_FREQUENCY * params.MEDIUM_ARTIST_FREQUENCY
    )
    num_large_artists = int(
        total_slots * params.EVENT_FREQUENCY * params.LARGE_ARTIST_FRQUENCY
    )
    artist_to_num = {
        ArtistSize.SMALL: num_small_artists,
        ArtistSize.MEDIUM: num_medium_artists,
        ArtistSize.LARGE: num_large_artists,
    }

    for artist_size, artist_count in artist_to_num.items():
        while artist_count > 0:
            hour = random.choice(HOURS)
            stage = random.choice(STAGES)
            schedule_df.loc[hour, stage] = get_random_artist_of_size(artist_size)
            artist_count -= 1

    schedule_schema = pa.DataFrameSchema(
        index=pa.Index(
            pa.Int, name="hour", checks=pa.Check.in_range(HOURS[0], HOURS[-1])
        ),
        columns={
            **{stage: pa.Column(object, nullable=True) for stage in STAGES},
        },
    )

    return schedule_schema.validate(schedule_df)


def fix_schedule_conflicts(schedule_df: pd.DataFrame) -> pd.DataFrame:
    """Iteratively fix schedule conflicts as they appear by swapping an event with a conflict with another."""
    while True:
        conflict = get_first_schedule_conflict(schedule_df)
        if conflict is None:
            break

        potential_schedule = schedule_df.copy()
        swapped_concert = swap_conflict_with_random(potential_schedule, conflict)

        # If the swap doesn't resolve the conflict, take it with 20% probability
        # Eventually, this will be the temperature for simmulated annealing the cools during the algorithm
        conflict_at_swap = check_for_conflicts(
            potential_schedule, swapped_concert.stage, swapped_concert.hour
        )
        conflict_at_original = check_for_conflicts(
            potential_schedule, conflict.concert1.stage, conflict.concert1.hour
        )
        if not (conflict_at_swap or conflict_at_original) or (random.random() < 0.1):
            schedule_df = potential_schedule

    print("No conflicts remaining")
    return schedule_df


def swap_conflict_with_random(schedule_df: pd.DataFrame, conflict: ScheduleConflict):
    """Modifies schedule_df in place by swapping a concert from the conflict with a random"""
    print(f"Swapping slots due to {conflict}")

    concert_to_swap = random.choice((conflict.concert1, conflict.concert2))
    this_artist = concert_to_swap.artist
    this_stage = concert_to_swap.stage
    this_hour = concert_to_swap.hour

    random_hour = random.choice(HOURS)
    random_stage = random.choice(STAGES)
    random_artist = schedule_df.loc[random_hour, random_stage]
    random_concert = Concert(artist=random_artist, stage=random_stage, hour=random_hour)

    print(f"Swapping {conflict.concert1} and {random_concert}")
    schedule_df.loc[this_hour, this_stage] = random_artist
    schedule_df.loc[random_hour, random_stage] = this_artist

    return random_concert


if __name__ == "__main__":
    print("=" * 55 + "\nGenerating Lollapalooza Schedule\n" + "=" * 55)
    schedule_df = generate_valid_schedule()

    schedule_path = Path(__file__).parent.parent / "schedules" / "schedule.csv"
    schedule_df.to_csv(schedule_path, index=False)

    display_schedule(schedule_df)
