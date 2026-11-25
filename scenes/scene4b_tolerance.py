"""
Scene 4B - tolerance and the stopping criterion.

Sits between Scene 4 (convergence) and the closing section: maximum error per
iteration, the tolerated error epsilon, and the pass that ends the search.

Render:
    manim -qh scenes/scene4b_tolerance.py ToleranceStop
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

X0 = -4.5
SPAN = 8.6
ERR_MAX = 0.035
EPS = 0.01
ROWS = [
    (4, 0.03125),
    (5, 0.015625),
    (6, 0.0078125),
]


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


def px(err):
    return X0 + err / ERR_MAX * SPAN


class ToleranceStop(Scene):
    def bar(self, y, err, highlight=False):
        w = px(err) - X0
        return RoundedRectangle(
            width=w,
            height=0.42,
            corner_radius=0.07,
            stroke_color=CYAN,
            stroke_width=1.6,
            stroke_opacity=1.0 if highlight else 0.85,
            fill_color=CYAN,
            fill_opacity=0.42 if highlight else 0.18,
        ).move_to([X0 + w / 2, y, 0])

    def construct(self):
        self.camera.background_color = NAVY

        grid = make_dot_grid()
        self.play(FadeIn(grid), run_time=0.5)

        head = txt("TOLERANCE & STOPPING CRITERIA", 24, WHITE, {"TOLERANCE": CYAN})
        head.move_to([NL_LEFT + head.width / 2, 3.55, 0])
        head_func = txt("f(x) = x³ − x − 2", 22, WHITE, {"x³ − x − 2": CYAN})
        head_func.move_to([NL_RIGHT - head_func.width / 2, 3.55, 0])
        rule = Line([NL_LEFT, 3.18, 0], [NL_RIGHT, 3.18, 0], color=CYAN, stroke_width=2)
        rule.set_stroke(opacity=0.4)
        self.play(FadeIn(head, shift=DOWN * 0.05), FadeIn(head_func), Create(rule), run_time=0.7)

        caption = txt("maximum error = half the interval width", 15, MUTED).move_to(
            [2.55, 2.62, 0]
        )
        zero = Line([X0, 2.30, 0], [X0, -1.00, 0], color=AXIS, stroke_width=1.4)
        zero.set_stroke(opacity=0.5)
        y_pos = [1.58, 0.58, -0.42]

        self.play(FadeIn(caption, shift=DOWN * 0.05), Create(zero), run_time=0.7)
        self.wait(2.0)

        # Faint hint of the iteration rows while the tolerance is discussed.
        row_labs = VGroup(
            *[
                txt(f"n = {n}", 15, MUTED).move_to([-5.85, y, 0], aligned_edge=LEFT)
                for (n, _), y in zip(ROWS, y_pos)
            ]
        )
        row_labs.set_opacity(0.22)
        self.play(FadeIn(row_labs), run_time=0.6)
        self.wait(2.4)

        # ------------------------------------------------------------------
        # Tolerance threshold
        # ------------------------------------------------------------------
        x_eps = px(EPS)
        thresh = DashedLine(
            [x_eps, 2.24, 0], [x_eps, -0.98, 0],
            color=CYAN, stroke_width=1.8, dash_length=0.07, dashed_ratio=0.55,
        )
        thresh.set_stroke(opacity=0.85)
        eps_tag = VGroup(
            txt("ε = 0.01", 18, CYAN),
            txt("tolerance", 11, MUTED),
        ).arrange(DOWN, buff=0.03).move_to([x_eps, 2.36, 0])
        self.play(Create(thresh), FadeIn(eps_tag, shift=UP * 0.05), run_time=0.8)
        self.wait(2.1)

        stop_rule = txt(
            "STOP when the maximum error ≤ ε", 17, WHITE, {"≤ ε": CYAN}
        ).move_to([-1.3, -1.38, 0])
        stop_chip = VGroup(
            RoundedRectangle(
                width=1.7, height=0.62, corner_radius=0.14,
                stroke_color=CYAN, stroke_width=2.0, stroke_opacity=0.95,
                fill_color=NAVY, fill_opacity=0.7,
            ),
            txt("STOP", 22, CYAN),
        ).move_to([4.95, -1.38, 0])
        stop_chip[1].move_to(stop_chip[0])
        self.play(FadeIn(stop_rule, shift=UP * 0.05), run_time=0.8)

        # ------------------------------------------------------------------
        # Error per iteration
        # ------------------------------------------------------------------
        bars = VGroup()
        vals = VGroup()
        for (n, err), y in zip(ROWS, y_pos):
            bars.add(self.bar(y, err))
            vals.add(
                txt(f"{err:g}", 12, SECONDARY).move_to([4.95, y, 0], aligned_edge=RIGHT)
            )

        for i, (bar, val, lab) in enumerate(zip(bars, vals, row_labs)):
            self.play(
                FadeIn(bar, shift=RIGHT * 0.1),
                FadeIn(val, shift=RIGHT * 0.1),
                lab.animate.set_opacity(1.0),
                run_time=0.55,
            )
        self.wait(1.05)

        # Sixth pass clears the tolerance.
        pass_pill = VGroup(
            RoundedRectangle(
                width=1.25, height=0.46, corner_radius=0.23,
                stroke_color=CYAN, stroke_width=1.6, stroke_opacity=0.9,
                fill_color=NAVY, fill_opacity=0.7,
            ),
            txt("PASS", 14, CYAN),
        ).move_to([-1.15, -0.42, 0])
        pass_pill[1].move_to(pass_pill[0])

        self.play(
            bars[2].animate.set_fill(CYAN, opacity=0.42).set_stroke(opacity=1.0),
            FadeIn(pass_pill, shift=LEFT * 0.05),
            FadeIn(stop_chip, scale=0.9),
            run_time=0.8,
        )
        self.wait(1.6)

        takeaway = txt("smaller ε  ⇒  more iterations", 15, SECONDARY).move_to([0, -2.78, 0])
        self.play(FadeIn(takeaway), run_time=0.6)
        self.wait(1.6)

        self.play(FadeOut(Group(*self.mobjects), shift=UP * 0.2), run_time=0.9)
        self.wait(0.1)
