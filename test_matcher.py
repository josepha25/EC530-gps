import pytest
from matcher import distance_km, find_closest


def test_same_point_is_zero():
    assert distance_km((0, 0), (0, 0)) == pytest.approx(0.0)


def test_known_distance():
    # boston to miami is around 2100 km
    d = distance_km((42.36, -71.06), (25.80, -80.29))
    assert 2000 < d < 2200


def test_symmetry():
    # should be same distance both ways
    d1 = distance_km((42.36, -71.06), (25.80, -80.29))
    d2 = distance_km((25.80, -80.29), (42.36, -71.06))
    assert d1 == pytest.approx(d2)


def test_result_is_float():
    assert isinstance(distance_km((0, 0), (1, 1)), float)


def test_distance_is_positive():
    assert distance_km((10, 20), (30, 40)) >= 0


def test_max_lat():
    assert distance_km((90, 0), (0, 0)) > 0


def test_min_lat():
    assert distance_km((-90, 0), (0, 0)) > 0


def test_max_lon():
    assert distance_km((0, 180), (0, 0)) > 0


def test_min_lon():
    assert distance_km((0, -180), (0, 0)) > 0


def test_lat_too_high():
    with pytest.raises(ValueError):
        distance_km((91, 0), (0, 0))


def test_lat_too_low():
    with pytest.raises(ValueError):
        distance_km((-91, 0), (0, 0))


def test_lon_too_high():
    with pytest.raises(ValueError):
        distance_km((0, 181), (0, 0))


def test_lon_too_low():
    with pytest.raises(ValueError):
        distance_km((0, -181), (0, 0))


def test_bad_type():
    with pytest.raises(TypeError):
        distance_km("bad input", (0, 0))


def test_non_numeric():
    with pytest.raises(TypeError):
        distance_km(("a", "b"), (0, 0))


def test_find_returns_tuple():
    result = find_closest((0, 0), [(1, 1), (10, 10)])
    assert isinstance(result, tuple)


def test_find_correct_point():
    closest, _ = find_closest((0, 0), [(0, 1), (0, 50)])
    assert closest == (0, 1)


def test_find_distance_is_float():
    _, dist = find_closest((0, 0), [(1, 1)])
    assert isinstance(dist, float)


def test_find_exact_match_is_zero():
    _, dist = find_closest((10, 20), [(10, 20), (30, 40)])
    assert dist == pytest.approx(0.0, abs=0.01)


def test_find_single_point_in_pool():
    closest, _ = find_closest((42.36, -71.06), [(42.36, -71.06)])
    assert closest == (42.36, -71.06)


def test_find_empty_pool_raises():
    with pytest.raises(ValueError):
        find_closest((0, 0), [])


