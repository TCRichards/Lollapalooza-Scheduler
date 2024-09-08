import numpy as np


STAGES = ["Bud Light", "Tito's", "Bacardi", "BMI", "Perry's", "IHG", "T-Mobile"]
HOURS = np.arange(12, 23, 1)


# Represents stages that can't play at the same time
NEIGHBORS = {
    "Bud Light": "Tito's",
    "IHG": "T-Mobile",
}

# Add the reverse mapping and map stages without neighbords to None
NEIGHBORS |= {v: k for k, v in NEIGHBORS.items()}
for stage in STAGES:
    if stage not in NEIGHBORS:
        NEIGHBORS[stage] = None
