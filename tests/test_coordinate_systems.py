import unittest

import numpy as np

from manimlib.mobject.coordinate_systems import Axes
from manimlib.mobject.coordinate_systems import CoordinateSystem
from manimlib.utils.simple_functions import binary_search


class StubCoordinateSystem(CoordinateSystem):
    def coords_to_point(self, *coords):
        return np.array([coords[0], coords[1], 0.0])

    def point_to_coords(self, point):
        return tuple(point[:2])

    def get_axes(self):
        return []

    def get_all_ranges(self):
        return []


class LineGraph:
    def quick_point_from_proportion(self, alpha):
        return np.array([2.0 + 4.0 * alpha, 3.0, 0.0])


class CoordinateSystemTests(unittest.TestCase):
    def test_binary_search_returns_input_at_endpoints(self):
        def function(value):
            return 2.0 + 4.0 * value

        self.assertEqual(binary_search(function, 2.0, 0.0, 1.0), 0.0)
        self.assertEqual(binary_search(function, 6.0, 0.0, 1.0), 1.0)

    def test_input_to_graph_point_searches_curve_proportion(self):
        axes = StubCoordinateSystem(x_range=(2.0, 6.0, 1.0), y_range=(0.0, 5.0, 1.0))
        graph = LineGraph()

        np.testing.assert_allclose(
            axes.input_to_graph_point(2.0, graph), [2.0, 3.0, 0.0]
        )
        np.testing.assert_allclose(
            axes.input_to_graph_point(4.0, graph), [4.0, 3.0, 0.0]
        )
        np.testing.assert_allclose(
            axes.input_to_graph_point(6.0, graph), [6.0, 3.0, 0.0]
        )


class BindGraphToFuncTests(unittest.TestCase):
    def get_updated_frames(self, func, get_discontinuities, num_frames):
        axes = Axes(x_range=(-4, 4), y_range=(-1, 4))
        graph = axes.get_graph(func)
        bound = axes.bind_graph_to_func(
            graph, func, get_discontinuities=get_discontinuities
        )
        frames = []
        for _ in range(num_frames):
            bound.update(1 / 30)
            frames.append((axes, bound.get_points().copy()))
        return frames

    def check_x_range_and_point_count_stable(self, func, get_discontinuities):
        frames = self.get_updated_frames(func, get_discontinuities, 30)
        _, first_points = frames[0]
        for axes, points in frames:
            xs = np.array([axes.x_axis.p2n(p) for p in points])
            self.assertEqual(len(points), len(first_points))
            self.assertAlmostEqual(xs.min(), -4.0, places=5)
            self.assertAlmostEqual(xs.max(), 4.0, places=5)
            np.testing.assert_allclose(points, first_points, atol=1e-8)

    def test_x_range_stable_with_discontinuity(self):
        self.check_x_range_and_point_count_stable(
            lambda x: 1.0 / x,
            get_discontinuities=lambda: [0.0],
        )

    def test_x_range_stable_without_discontinuity(self):
        self.check_x_range_and_point_count_stable(
            lambda x: x ** 2,
            get_discontinuities=None,
        )


if __name__ == "__main__":
    unittest.main()
