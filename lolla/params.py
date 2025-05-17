"""Various knobs we can turn to impact different parts of the game.

Mostly optimized by playtesting.
"""
# What portion of stage/hour slots are filled
MIN_EVENT_FREQUENCY = 0.55
MAX_EVENT_FREQUENCY = 0.65

# The relative frequency of each size of artist
SMALL_ARTIST_FREQUENCY = 0.45
MEDIUM_ARTIST_FREQUENCY = 0.35
LARGE_ARTIST_FRQUENCY = 1 - SMALL_ARTIST_FREQUENCY - MEDIUM_ARTIST_FREQUENCY

# A given stage must have at least this many performances per day
MIN_ARTISTS_PER_STAGE_PER_DAY = 3

