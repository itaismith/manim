import os

from manimlib import *


class BindGraphDiscontinuity(Scene):
    def construct(self):
        axes = Axes(x_range=(-4, 4), y_range=(-1, 4))
        func = lambda x: 1.0 / x
        graph = axes.get_graph(func, color=YELLOW)
        axes.bind_graph_to_func(graph, func, get_discontinuities=lambda: [0.0])
        self.add(axes, graph)

        label = os.environ.get("CLIP_LABEL")
        if label:
            self.add(Text(label, font_size=36).to_corner(UL))

        self.wait(2)
