"""
That an Ellipse comes out the width and height it was asked for, whatever its start_angle or
n_components, and centered on its arc_center.

Sizing the unit circle by its bounding box shrank the ellipse whenever bezier handles stuck out
past the anchors, which they do unless an anchor sits on each extreme.

    python tests/ellipse_size.py
"""
from __future__ import annotations

import sys

import numpy as np

from manimlib import Ellipse


def curve_points(mobject, samples: int = 200) -> np.ndarray:
    points = mobject.get_points()
    t = np.linspace(0, 1, samples)[:, None]
    return np.vstack([
        (1 - t)**2 * a + 2 * t * (1 - t) * h + t**2 * b
        for a, h, b in zip(points[0::2], points[1::2], points[2::2])
    ])


CASES = [
    ("default", dict(width=4, height=1)),
    ("start_angle=0.3", dict(width=4, height=1, start_angle=0.3)),
    ("n_components=5 off center", dict(width=4, height=1, n_components=5, arc_center=(3, 3, 0))),
]


def main() -> int:
    failures = []
    for name, kwargs in CASES:
        ellipse = Ellipse(**kwargs)
        pts = curve_points(ellipse)
        size = np.ptp(pts[:, :2], axis=0)
        center = (pts.min(0) + pts.max(0))[:2] / 2
        want_size = (kwargs["width"], kwargs["height"])
        want_center = np.array(kwargs.get("arc_center", (0, 0, 0)))[:2]
        # Curve extremes of a coarse quadratic approximation sit within a few percent
        ok = np.allclose(size, want_size, rtol=0.05) and np.allclose(center, want_center, atol=0.05)
        print(f"  {name}: size {np.round(size, 3).tolist()}, center {np.round(center, 3).tolist()}")
        if not ok:
            failures.append(name)
    for failure in failures:
        print(f"  FAIL: {failure}")
    return 1 if failures else 0


sys.exit(main())
