import pandas as pd

from lolla.scheduling.constants import HOURS, ArtistSize
from lolla.scheduling.constraints import is_any_stage_booked_consecutively, are_any_neighbors_simultaneous, ScheduleConflict




def test_consecutive_bookings():
    schedule_with_consecutive = pd.DataFrame(data={
        "Test Stage": [pd.NA, pd.NA, ArtistSize.SMALL, ArtistSize.MEDIUM]
    })
    consecutive_conflict = is_any_stage_booked_consecutively(schedule_with_consecutive)
    expected_conflict = ScheduleConflict(ArtistSize.SMALL, 2, "Test Stage", ArtistSize.MEDIUM, 3, "Test Stage")
    assert expected_conflict == consecutive_conflict




