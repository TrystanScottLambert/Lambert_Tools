"Functions."


import numpy as np


def hms_to_deg(h, sep=":"):
    """Convert hours, minutes, seconds to degrees."""
    hms = list(map(float, h.split(sep)))
    return (hms[0] + hms[1] / 60 + hms[2] / 3600) * 15  # 15 degrees per hour


def dms_to_deg(d, sep=":"):
    """Convert degrees, minutes, seconds to degrees."""
    dms = list(map(float, d.split(sep)))
    return dms[0] + dms[1] / 60 + dms[2] / 3600


def skyarea(long=[129, 141], lat=[-2, 3], inunit="deg", outunit="deg2", sep=":"):
    """Works out the area of the of a rectangular survey given the coordinates"""
    # Check input units
    valid_inunits = ["deg", "amin", "asec", "rad", "sex"]
    valid_outunits = ["deg2", "amin2", "asec2", "rad2", "sr"]

    if inunit not in valid_inunits:
        raise ValueError("inunit must be one of deg, amin, asec, rad or sex")

    if outunit not in valid_outunits:
        raise ValueError("outunit must be one of deg2, amin2, asec2, rad2 or sr")

    # Expand long and lat if only one value is provided
    if len(long) == 1:
        long = [0, long[0]]
    if len(lat) == 1:
        lat = [0, lat[0]]

    fullsky = 129600 / np.pi  # Full sky area in square degrees

    # Convert units to degrees
    if inunit == "sex":
        long = [hms_to_deg(l, sep) for l in long]
        lat = [dms_to_deg(l, sep) for l in lat]
    elif inunit == "amin":
        long = [l / 60 for l in long]
        lat = [l / 60 for l in lat]
    elif inunit == "asec":
        long = [l / 3600 for l in long]
        lat = [l / 3600 for l in lat]
    elif inunit == "rad":
        long = [l * 180 / np.pi for l in long]
        lat = [l * 180 / np.pi for l in lat]

    # Calculate the area fraction
    areafrac = (
        (np.sin(np.radians(lat[1])) - np.sin(np.radians(lat[0])))
        * (long[1] - long[0])
        / 360
    ) / 2

    if areafrac < 0:
        raise ValueError("Sky area is non-physical (negative)")
    if areafrac > 1:
        raise ValueError("Sky area is non-physical (bigger than the full sky)")

    area = areafrac * fullsky

    # Convert output units
    if outunit == "amin2":
        area *= 3600
    elif outunit == "asec2":
        area *= 12960000
    elif outunit in ["rad2", "sr"]:
        area /= (180 / np.pi) ** 2

    return {"area": area, "areafrac": areafrac}
