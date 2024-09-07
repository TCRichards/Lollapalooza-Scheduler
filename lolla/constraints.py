import pandas as pd


def is_schedule_valid(schedule_df: pd.DataFrame):
    return not (
        are_stages_double_booked(schedule_df) or
        are_stages_booked_consecutively(schedule_df)
    )

def are_stages_double_booked(schedule_df: pd.DataFrame) -> bool | tuple[tuple[str, int], tuple[str, int]]:
    """Returns: A tuple of idenfitiers for the first cells that were caught to 

    Each identifier is an hour and stage
    """
    return False

def are_stages_booked_consecutively(schule_df) -> bool:
    return True