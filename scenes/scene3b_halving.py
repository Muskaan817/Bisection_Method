"""
Scene 3B - why the interval halves at every iteration.

Sits between Scene 3 (iterations) and Scene 4 (convergence): the midpoint,
the sign test, the discarded half and the width shrink 1 -> 0.5 -> 0.25.

Render:
    manim -qh scenes/scene3b_halving.py HalvingWhy
"""

import numpy as np
from manim import *

NAVY = "#0A1633"
PANEL = "#0E1E3E"
PANEL_EDGE = "#2C4B8A"
PANEL_SHADOW = "#030A18"
GRID_DOT = "#17305C"
AXIS = "#89A8E0"
CYAN = "#22D3EE"
BLUE = "#4C8DFF"
WHITE = "#F7FAFF"
SECONDARY = "#C6D3EA"
MUTED = "#7E8AA3"
GLOW = "#67E8F9"

FONT = "Helvetica Neue"
NL_LEFT, NL_RIGHT = -6.35, 6.35


def txt(string, size, color=WHITE, highlights=None):
    factor = max(1, -(-60 // int(size)))
    t = Text(
        string, font=FONT, weight=BOLD, font_size=size * factor, color=color,
        t2c=highlights or {},
    )
    return t.scale(1 / factor)


def make_dot_grid(spacing=1.0, radius=0.013):
    dots = VGroup()
    for x in np.arange(-6.5, 7.0, spacing):
        for y in np.arange(-3.5, 4.0, spacing):
            dots.add(Dot([x, y, 0], radius=radius, color=GRID_DOT, fill_opacity=0.45))
    return dots


class HalvingWhy(Scene):
    BAR_Y = 0.55
    X1, X2 = -4.9, 4.9
    XM, X175 = 0.0, 2.45

    def quarter(self, left, right):
        return RoundedRectangle(
            width=right - left - 0.04,
            height=0.42,
            corner_radius=0.07,
            stroke_color=CYAN,
            stroke_width=1.4,
            stroke_opacity=0.85,
            fill_color=CYAN,
            fill_opacity=0.20,
        ).move_to([(left + right) / 2, self.BAR_Y, 0])

    def width_chip(self, n, value, active):
        box = RoundedRectangle(
            width=2.5,
            height=0.82,
            corner_radius=0.14,
            stroke_color=CYAN if active else PANEL_EDGE,
            stroke_width=2.0 if active else 1.2,
            stroke_opacity=0.95 if active else 0.7,
            fill_color=PANEL,
            fill_opacity=0.9 if active else 0.55,
        )
        lab = VGroup(
            txt(f"n = {n}", 11, CYAN if active else MUTED),
            txt(value, 15, WHITE if active else MUTED),
        ).arrange(DOWN, buff=0.04)
        lab.move_to(box)
        return VGroup(box, lab)

    def keep_tag(self, x):
        box = RoundedRectangle(
            width=1.15, height=0.4, corner_radius=0.2,
            stroke_color=CYAN, stroke_width=1.4, stroke_opacity=0.8,
            fill_color=NAVY, fill_opacity=0.85,
        ).move_to([x, 1.02, 0])
        return VGroup(box, txt("keep", 12, CYAN).move_to(box))

    def construct(self):
        self.camera.background_color = NAVY

        grid = make_dot_grid()
        self.play(FadeIn(grid), run_time=0.5)

        head = txt("WHY THE INTERVAL HALVES", 24, WHITE, {"HALVES": CYAN})
        head.move_to([NL_LEFT + head.width / 2, 3.55, 0])
        head_func = txt("f(x) = x³ − x − 2", 22, WHITE, {"x³ − x − 2": CYAN})
        head_func.move_to([NL_RIGHT - head_func.width / 2, 3.55, 0])
        rule = Line([NL_LEFT, 3.18, 0], [NL_RIGHT, 3.18, 0], color=CYAN, stroke_width=2)
        rule.set_stroke(opacity=0.4)
        self.play(FadeIn(head, shift=DOWN * 0.05), FadeIn(head_func), Create(rule), run_time=0.7)

        # ------------------------------------------------------------------
        # Interval bar split into quarters
        # ------------------------------------------------------------------
        q1 = self.quarter(self.X1, -2.45)
        q2 = self.quarter(-2.45, self.XM)
        q3 = self.quarter(self.XM, self.X175)
        q4 = self.quarter(self.X175, self.X2)

        lab1 = txt("1", 14, MUTED).move_to([self.X1, 0.02, 0])
        lab15 = txt("1.5", 14, MUTED).move_to([self.XM, 0.02, 0])
        lab2 = txt("2", 14, MUTED).move_to([self.X2, 0.02, 0])
        lab175 = txt("1.75", 14, MUTED).move_to([self.X175, 0.02, 0])

        tick1 = Line([self.X1, 0.80, 0], [self.X1, 1.48, 0], color=AXIS, stroke_width=1.3)
        tick2 = Line([self.X2, 0.80, 0], [self.X2, 1.48, 0], color=AXIS, stroke_width=1.3)
        tick1.set_stroke(opacity=0.6)
        tick2.set_stroke(opacity=0.6)
        tag1 = txt("f(1) < 0", 14, WHITE, {"< 0": CYAN}).move_to([self.X1, 1.72, 0])
        tag2 = txt("f(2) > 0", 14, WHITE, {"> 0": CYAN}).move_to([self.X2, 1.72, 0])

        self.play(
            FadeIn(VGroup(q1, q2, q3, q4)),
            FadeIn(VGroup(lab1, lab15, lab2)),
            Create(tick1), Create(tick2),
            FadeIn(tag1), FadeIn(tag2),
            run_time=0.8,
        )

        # First midpoint.
        mid1 = Line([self.XM, 0.24, 0], [self.XM, 0.92, 0], color=WHITE, stroke_width=2.2)
        self.play(Create(mid1), run_time=0.5)
        self.wait(1.6)

        chips = VGroup(
            self.width_chip(0, "width 1.000", True),
            self.width_chip(1, "width 0.500", False),
            self.width_chip(2, "width 0.250", False),
        )
        for chip, x in zip(chips, (-4.4, 0.0, 4.4)):
            chip.move_to([x, -1.45, 0])
        self.play(FadeIn(chips, shift=UP * 0.08), run_time=0.6)
        self.wait(1.5)

        # f(1.5) is still negative: discard the left half.
        fc = RoundedRectangle(
            width=2.9, height=0.52, corner_radius=0.12,
            stroke_color=PANEL_EDGE, stroke_width=1.4,
            fill_color=PANEL, fill_opacity=0.95,
        ).move_to([self.XM, 1.52, 0])
        fc_text = txt("f(1.5) = −0.125", 15, WHITE, {"−0.125": CYAN}).move_to(fc)
        fc_chip = VGroup(fc, fc_text)
        self.play(FadeIn(fc_chip, shift=UP * 0.06), run_time=0.6)

        glow1 = RoundedRectangle(
            width=4.9, height=0.54, corner_radius=0.10,
            stroke_color=GLOW, stroke_width=12, stroke_opacity=0.12,
            fill_opacity=0,
        ).move_to([2.45, self.BAR_Y, 0])
        keep1 = self.keep_tag(2.45)

        self.play(
            VGroup(q1, q2).animate.set_opacity(0.15),
            FadeIn(txt("discarded", 11, MUTED).move_to([-2.45, self.BAR_Y, 0])),
            FadeIn(glow1), FadeIn(keep1, shift=UP * 0.05),
            run_time=0.9,
        )
        self.play(Transform(chips[0], self.width_chip(0, "width 1.000", False).move_to([-4.4, -1.45, 0])),
                  Transform(chips[1], self.width_chip(1, "width 0.500", True).move_to([0, -1.45, 0])),
                  run_time=0.5)

        # Only the kept half can contain the root.
        self.play(glow1.animate.set_stroke(opacity=0.26), run_time=1.0)
        self.wait(1.4)

        # Second midpoint: 1.75, positive, so keep the left quarter.
        self.play(FadeOut(fc_chip, shift=UP * 0.05), run_time=0.3)
        mid2 = Line([self.X175, 0.24, 0], [self.X175, 0.92, 0], color=WHITE, stroke_width=2.2)
        fc2 = RoundedRectangle(
            width=2.9, height=0.52, corner_radius=0.12,
            stroke_color=PANEL_EDGE, stroke_width=1.4,
            fill_color=PANEL, fill_opacity=0.95,
        ).move_to([self.X175, 1.52, 0])
        fc2_text = txt("f(1.75) = +1.609", 15, WHITE, {"+1.609": CYAN}).move_to(fc2)
        fc2_chip = VGroup(fc2, fc2_text)
        self.play(Create(mid2), FadeIn(lab175), FadeIn(fc2_chip, shift=UP * 0.06), run_time=0.7)

        glow2 = RoundedRectangle(
            width=2.45, height=0.54, corner_radius=0.10,
            stroke_color=GLOW, stroke_width=12, stroke_opacity=0.12,
            fill_opacity=0,
        ).move_to([1.225, self.BAR_Y, 0])
        keep2 = self.keep_tag(1.225)

        self.play(
            q4.animate.set_opacity(0.15),
            FadeIn(txt("discarded", 11, MUTED).move_to([3.675, self.BAR_Y, 0])),
            Transform(glow1, glow2), Transform(keep1, keep2),
            run_time=0.9,
        )
        self.play(Transform(chips[1], self.width_chip(1, "width 0.500", False).move_to([0, -1.45, 0])),
                  Transform(chips[2], self.width_chip(2, "width 0.250", True).move_to([4.4, -1.45, 0])),
                  run_time=0.5)
        self.wait(1.4)

        formula = txt(
            "width after n steps  =  (b − a) / 2ⁿ", 26, WHITE, {"(b − a) / 2ⁿ": CYAN}
        ).move_to([0, -2.65, 0])
        self.play(FadeIn(formula, shift=UP * 0.08), run_time=0.8)
        self.wait(6.4)

        self.play(FadeOut(Group(*self.mobjects), shift=UP * 0.2), run_time=0.9)
        self.wait(0.1)
