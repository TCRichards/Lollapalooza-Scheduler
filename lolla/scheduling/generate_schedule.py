import random
from pathlib import Path

import pandera as pa
import pandas as pd

from lolla.scheduling.constants import (
    STAGES,
    HOURS,
)
from lolla.scheduling.constraints import (
    get_first_schedule_conflict,
    ScheduleConflict,
    Concert,
    check_for_conflicts,
)
from lolla.scheduling import params
from lolla.scheduling.artists import get_random_artist_of_size_and_genre, Genre, ArtistSize, Artist, Genre


class CanNotConvergeError(Exception):
    """Exception raised when the schedule generation algorithm cannot converge to a valid schedule after a set number of iterations.

    This is usually a sign that we're stuck in a local minimum and need to restart the generation process.
    """
    ...


def generate_valid_schedule() -> pd.DataFrame:
    """Top-level function to generate a Lollapalooza schedule with all constraints satisfied."""
    print("=" * 55 + "\nGenerating Lollapalooza Schedule\n" + "=" * 55)
    try:
        schedule_df = generate_initial_schedule()
        print(f"Initial schedule:\n{schedule_df}")
        return fix_schedule_conflicts(schedule_df)
    except CanNotConvergeError:
        return generate_valid_schedule()




def generate_initial_schedule() -> pd.DataFrame:
    """Generate an initial schedule DataFrame with Artist objects assigned to stages and hours."""
    schedule_df = pd.DataFrame(columns=STAGES, index=HOURS, data={})
    schedule_df.index.name = "hour"

    unassigned_artists = generate_artist_pool()
    while unassigned_artists:
        hour = random.choice(HOURS)
        stage = random.choice(STAGES)
        schedule_df.loc[hour, stage] = unassigned_artists.pop()

    schedule_schema = pa.DataFrameSchema(
        index=pa.Index(
            pa.Int, name="hour", checks=pa.Check.in_range(HOURS[0], HOURS[-1])
        ),
        columns={
            **{stage: pa.Column(object, nullable=True) for stage in STAGES},
        },
    )

    print("=" * 55 + "\nSuccessfully Generated Schedule!\n" + "=" * 55)
    return schedule_schema.validate(schedule_df)


def generate_artist_pool() -> list[Artist]:
    """Generates a set of Artists that will be placed on the schedule, satisfying constraints about size and genre."""
    total_slots = len(STAGES) * len(HOURS)
    event_frequency = random.uniform(
        params.MIN_EVENT_FREQUENCY, params.MAX_EVENT_FREQUENCY
    )
    num_small_artists = int(
        total_slots * event_frequency * params.SMALL_ARTIST_FREQUENCY
    )
    num_medium_artists = int(
        total_slots * event_frequency * params.MEDIUM_ARTIST_FREQUENCY
    )
    num_large_artists = int(
        total_slots * event_frequency * params.LARGE_ARTIST_FRQUENCY
    )

    artist_size_to_count = {
        ArtistSize.SMALL: num_small_artists,
        ArtistSize.MEDIUM: num_medium_artists,
        ArtistSize.LARGE: num_large_artists,
    }

    artist_pool = []
    for size in ArtistSize:
        for genre in Genre:
            num_artists_per_size_genre = artist_size_to_count[size] // len(Genre) + 1
            for _ in range(num_artists_per_size_genre):
                artist_pool.append(get_random_artist_of_size_and_genre(size, genre))

    return artist_pool



def fix_schedule_conflicts(schedule_df: pd.DataFrame, max_iterations: int = 1e3) -> pd.DataFrame:
    """Iteratively fix schedule conflicts as they appear by swapping an event with a conflict with another."""
    iterations = 0
    while True:
        conflict = get_first_schedule_conflict(schedule_df)
        if conflict is None:
            break

        potential_schedule = schedule_df.copy()
        swapped_concert = swap_conflict_with_random(potential_schedule, conflict)

        # If the swap doesn't resolve the conflict, take it anyway with 10% probability
        # Eventually, this can correspond be the temperature for simmulated annealing the cools during the algorithm
        conflict_at_swap = check_for_conflicts(
            potential_schedule, swapped_concert.stage, swapped_concert.hour
        )
        conflict_at_original = check_for_conflicts(
            potential_schedule, conflict.concert1.stage, conflict.concert1.hour
        )

        if not (conflict_at_swap or conflict_at_original) or (random.random() < 0.1):
            schedule_df = potential_schedule

        iterations += 1
        if iterations > max_iterations:
            raise CanNotConvergeError(f"Unable to converge after {max_iterations} iterations.  Trying again.")

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
    schedule_df = generate_valid_schedule()
    schedule_path = Path(__file__).parent.parent.parent / "schedules" / "schedule.csv"
    schedule_df.to_csv(schedule_path, index=False)

    print("Schedule generated and saved to:", schedule_path)
    print(schedule_df)
