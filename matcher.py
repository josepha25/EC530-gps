"""
matcher.py

Given two arrays of GPS locations, match each point in the first array
to the closest point in the second array.

A GPS location is a tuple: (latitude, longitude)
"""

import logging
import math

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def distance_km(point1, point2):
    """Return the distance in km between two GPS points using Haversine.

    Args:
        point1: (latitude, longitude) in decimal degrees
        point2: (latitude, longitude) in decimal degrees

    Returns:
        Distance in kilometres as a float.

    Raises:
        ValueError: if coordinates are out of range.
        TypeError: if inputs are not tuples/lists of two numbers.
    """
    try:
        lat1, lon1 = float(point1[0]), float(point1[1])
        lat2, lon2 = float(point2[0]), float(point2[1])
    except (TypeError, IndexError, ValueError):
        raise TypeError("Each point must be a (latitude, longitude) pair of numbers.")

    for name, val, lo, hi in [
        ("lat1", lat1, -90, 90),
        ("lon1", lon1, -180, 180),
        ("lat2", lat2, -90, 90),
        ("lon2", lon2, -180, 180),
    ]:
        if not (lo <= val <= hi):
            raise ValueError(f"{name}={val} is out of range [{lo}, {hi}].")

    R = 6371.0  # Earth radius in km

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def find_closest(point, array):
    """Find the closest point in array to the given point.

    Args:
        point: (latitude, longitude)
        array: list of (latitude, longitude) tuples

    Returns:
        (closest_point, distance_km) tuple.

    Raises:
        ValueError: if array is empty.
    """
    if not array:
        raise ValueError("array must not be empty.")

    best = None
    best_dist = float("inf")

    for candidate in array:
        d = distance_km(point, candidate)
        if d < best_dist:
            best_dist = d
            best = candidate

    logger.debug("Closest to %s is %s (%.2f km)", point, best, best_dist)
    return best, best_dist


def match_arrays(array1, array2):
    """Match each point in array1 to the closest point in array2.

    Args:
        array1: list of (latitude, longitude) tuples — the points to match
        array2: list of (latitude, longitude) tuples — the pool to match against

    Returns:
        A list of dicts, one per point in array1:
        [
            {
                "point":   (lat, lon),       # original point from array1
                "closest": (lat, lon),       # nearest point from array2
                "distance_km": float         # distance between them
            },
            ...
        ]

    Raises:
        ValueError: if either array is empty.
    """
    if not array1:
        raise ValueError("array1 must not be empty.")
    if not array2:
        raise ValueError("array2 must not be empty.")

    logger.info(
        "Matching %d points in array1 to %d points in array2.",
        len(array1), len(array2),
    )

    results = []
    for point in array1:
        closest, dist = find_closest(point, array2)
        results.append({
            "point": point,
            "closest": closest,
            "distance_km": dist,
        })

    logger.info("Done. Matched %d points.", len(results))
    return results
