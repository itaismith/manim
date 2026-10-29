from manimlib import *

class EllipseFit(Scene):
    def construct(self):
        # Requested 4x1 boxes in yellow; the ellipse should just touch each side
        specs = [
            dict(width=4, height=1, start_angle=0.3, arc_center=3 * LEFT + 1.5 * UP),
            dict(width=4, height=1, n_components=5, arc_center=3 * RIGHT + 1.5 * UP),
            dict(width=3, height=3, start_angle=0.2, n_components=6, arc_center=1.5 * DOWN),
        ]
        boxes = VGroup(*(
            Rectangle(s["width"], s["height"], stroke_color=YELLOW, stroke_width=2).move_to(s["arc_center"])
            for s in specs
        ))
        dots = VGroup(*(Dot(s["arc_center"], radius=0.05, color=YELLOW) for s in specs))
        ellipses = VGroup(*(Ellipse(**s, stroke_color=BLUE, stroke_width=4) for s in specs))
        self.add(boxes, dots)
        self.play(*(ShowCreation(e) for e in ellipses), run_time=2)
        self.wait()
        self.play(*(e.animate.scale(2.5, about_point=s["arc_center"]) for e, s in zip(ellipses[:2], specs[:2])),
                  boxes[:2].animate.scale(2.5), run_time=0) if False else None
        self.wait()
