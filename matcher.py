import logging
import math

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def distance_km(p1, p2):
    # get the lat and lon from both points
    try:
        lat1, lon1 = float(p1[0]), float(p1[1])
        lat2, lon2 = float(p2[0]), float(p2[1])
    except (TypeError, IndexError, ValueError):
        raise TypeError("Each point must be (latitude, longitude).")

    # make sure coords are in range
    checks = [
        ("lat1", lat1, -90, 90),
        ("lon1", lon1, -180, 180),
        ("lat2", lat2, -90, 90),
        ("lon2", lon2, -180, 180),
    ]
    for name, val, lo, hi in checks:
        if not (lo <= val <= hi):
            raise ValueError(f"{name}={val} must be between {lo} and {hi}.")

    # haversine formula to get km distance
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def find_closest(point, pool):
    if not pool:
        raise ValueError("pool must not be empty.")

    best = None
    best_dist = float("inf")

    # go through each point and find the nearest one
    for candidate in pool:
        d = distance_km(point, candidate)
        if d < best_dist:
            best_dist = d
            best = candidate

    return best, best_dist


def match_arrays(list1, list2):
    if not list1:
        raise ValueError("list1 must not be empty.")
    if not list2:
        raise ValueError("list2 must not be empty.")

    results = []
    for point in list1:
        closest, dist = find_closest(point, list2)
        results.append({
            "point": point,
            "closest": closest,
            "distance_km": dist,
        })

    return results
