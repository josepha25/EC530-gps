"""
test_matcher.py

Unit tests for matcher.py.

Covers:
- Boundary conditions
- API usage (return types, structure)
- Error handling
- Data correctness
"""

import pytest
from matcher import distance_km, find_closest, match_arrays


# ---------------------------------------------------------------------------
# distance_km
# ---------------------------------------------------------------------------

class TestDistanceKm:

    def test_same_point_is_zero(self):
        assert distance_km((0, 0), (0, 0)) == pytest.approx(0.0)

    def test_known_distance_boston_miami(self):
        # ~2100 km
        d = distance_km((42.36, -71.06), (25.80, -80.29))
        assert 2000 < d < 2200

    def test_symmetry(self):
        d1 = distance_km((42.36, -71.06), (25.80, -80.29))
        d2 = distance_km((25.80, -80.29), (42.36, -71.06))
        assert d1 == pytest.approx(d2)

    def test_result_is_float(self):
        assert isinstance(distance_km((0, 0), (1, 1)), float)

    def test_distance_is_non_negative(self):
        assert distance_km((10, 20), (30, 40)) >= 0

    # boundary conditions
    def test_max_lat(self):
        assert distance_km((90, 0), (0, 0)) > 0

    def test_min_lat(self):
        assert distance_km((-90, 0), (0, 0)) > 0

    def test_max_lon(self):
        assert distance_km((0, 180), (0, 0)) > 0

    def test_min_lon(self):
        assert distance_km((0, -180), (0, 0)) > 0

    # error handling
    def test_lat_too_high_raises(self):
        with pytest.raises(ValueError):
            distance_km((91, 0), (0, 0))

    def test_lat_too_low_raises(self):
        with pytest.raises(ValueError):
            distance_km((-91, 0), (0, 0))

    def test_lon_too_high_raises(self):
        with pytest.raises(ValueError):
            distance_km((0, 181), (0, 0))

    def test_lon_too_low_raises(self):
        with pytest.raises(ValueError):
            distance_km((0, -181), (0, 0))

    def test_bad_type_raises(self):
        with pytest.raises(TypeError):
            distance_km("not a point", (0, 0))

    def test_non_numeric_values_raise(self):
        with pytest.raises(TypeError):
            distance_km(("a", "b"), (0, 0))


# ---------------------------------------------------------------------------
# find_closest
# ---------------------------------------------------------------------------

class TestFindClosest:

    def test_returns_tuple(self):
        result = find_closest((0, 0), [(1, 1), (10, 10)])
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_closest_point_correct(self):
        pool = [(0, 1), (0, 50), (0, 100)]
        closest, _ = find_closest((0, 0), pool)
        assert closest == (0, 1)

    def test_distance_returned_is_float(self):
        _, dist = find_closest((0, 0), [(1, 1)])
        assert isinstance(dist, float)

    def test_single_point_pool(self):
        only = [(42.36, -71.06)]
        closest, dist = find_closest((42.36, -71.06), only)
        assert closest == (42.36, -71.06)
        assert dist == pytest.approx(0.0, abs=0.01)

    def test_exact_match_distance_is_zero(self):
        _, dist = find_closest((10, 20), [(10, 20), (30, 40)])
        assert dist == pytest.approx(0.0, abs=0.01)

    # error handling
    def test_empty_array_raises(self):
        with pytest.raises(ValueError):
            find_closest((0, 0), [])


# ---------------------------------------------------------------------------
# match_arrays
# ---------------------------------------------------------------------------

class TestMatchArrays:

    def test_returns_list(self):
        result = match_arrays([(0, 0)], [(1, 1), (10, 10)])
        assert isinstance(result, list)

    def test_output_length_equals_array1(self):
        a1 = [(0, 0), (10, 10), (20, 20)]
        a2 = [(5, 5), (15, 15)]
        result = match_arrays(a1, a2)
        assert len(result) == 3

    def test_each_result_has_required_keys(self):
        result = match_arrays([(0, 0)], [(1, 1)])
        keys = result[0].keys()
        assert "point" in keys
        assert "closest" in keys
        assert "distance_km" in keys

    def test_point_field_matches_array1(self):
        a1 = [(10, 20), (30, 40)]
        a2 = [(11, 21), (29, 39)]
        result = match_arrays(a1, a2)
        assert result[0]["point"] == (10, 20)
        assert result[1]["point"] == (30, 40)

    def test_correct_match_selected(self):
        # (0,0) should match (1,1) not (50,50)
        result = match_arrays([(0, 0)], [(1, 1), (50, 50)])
        assert result[0]["closest"] == (1, 1)

    def test_distance_km_is_float(self):
        result = match_arrays([(0, 0)], [(1, 1)])
        assert isinstance(result[0]["distance_km"], float)

    def test_distance_is_non_negative(self):
        result = match_arrays([(42, -71)], [(43, -72), (10, 10)])
        assert result[0]["distance_km"] >= 0

    def test_each_point_matches_independently(self):
        a1 = [(0, 0), (0, 100)]
        a2 = [(0, 1), (0, 99)]
        result = match_arrays(a1, a2)
        assert result[0]["closest"] == (0, 1)
        assert result[1]["closest"] == (0, 99)

    def test_one_to_one(self):
        # single point in both arrays
        result = match_arrays([(5, 5)], [(5, 5)])
        assert result[0]["distance_km"] == pytest.approx(0.0, abs=0.01)

    # boundary conditions
    def test_many_points_in_array2(self):
        a2 = [(float(i), float(i)) for i in range(50)]
        result = match_arrays([(0, 0)], a2)
        assert result[0]["closest"] == (0.0, 0.0)

    def test_many_points_in_array1(self):
        a1 = [(float(i), 0) for i in range(10)]
        a2 = [(0, 0), (5, 0), (9, 0)]
        result = match_arrays(a1, a2)
        assert len(result) == 10

    # error handling
    def test_empty_array1_raises(self):
        with pytest.raises(ValueError):
            match_arrays([], [(1, 1)])

    def test_empty_array2_raises(self):
        with pytest.raises(ValueError):
            match_arrays([(1, 1)], [])

    def test_both_empty_raises(self):
        with pytest.raises(ValueError):
            match_arrays([], [])
