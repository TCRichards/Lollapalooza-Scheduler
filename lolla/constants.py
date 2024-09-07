from enum import Enum

import numpy as np
import pandera as pa


STAGES = ["Bud Light", "Tito's", "Bacardi", "BMI", "Perry's", "IHG", "T-Mobile"]
STAGE_TO_ID = {stage: i for i, stage in enumerate(STAGES)}
HOURS = np.arange(12, 23, 1)


class ArtistSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


schedule_schema = pa.DataFrameSchema(
    index=pa.Index(pa.Int, name="hour", checks=pa.Check.in_range(HOURS[0], HOURS[-1])),
    columns={
        **{stage: pa.Column(pa.String, nullable=True) for stage in STAGES},
    }
)