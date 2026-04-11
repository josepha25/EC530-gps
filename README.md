# Assignment 1 — GPS Location Matcher

Given two arrays of GPS locations, match each point in the first array
to the closest point in the second array.

---

## How it works

A GPS location is a `(latitude, longitude)` tuple in decimal degrees.

```python
from matcher import match_arrays

array1 = [(42.36, -71.06), (25.80, -80.29)]   # points to match
array2 = [(40.71, -74.01), (34.05, -118.24), (41.88, -87.63)]  # pool

results = match_arrays(array1, array2)

for r in results:
    print(r["point"], "→", r["closest"], f"({r['distance_km']:.1f} km)")
```

Output:
```
(42.36, -71.06) → (40.71, -74.01) (306.7 km)
(25.8, -80.29)  → (40.71, -74.01) (...)
```

---

## Setup

No external dependencies. Standard library only.

```bash
pip install pytest pytest-cov flake8 coverage
```

---

## Run the tests

```bash
pytest
```

## Run with coverage

```bash
coverage run -m pytest
coverage report
```

## Run flake8

```bash
# hard errors (blocks CI)
flake8 . --select=E9,F63,F7,F82 --show-source

# full style check
flake8 . --max-line-length=100 --statistics
```

---

## Files

| File | Purpose |
|---|---|
| `matcher.py` | Core module: `distance_km`, `find_closest`, `match_arrays` |
| `test_matcher.py` | 35 unit tests |
| `.github/workflows/ci.yml` | GitHub Actions: lint + test + coverage |
| `pyproject.toml` | pytest + coverage config |
