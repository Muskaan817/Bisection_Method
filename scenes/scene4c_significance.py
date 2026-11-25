"""
Scene 4C - practical significance and limits.

Sits just before the closing scene: what bisection offers in real software,
what it costs, and how it is used alongside faster methods.

Render:
    manim -qh scenes/scene4c_significance.py InPractice
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

ROWS = [
    ("f", "NO DERIVATIVE", "only f(x) values and a sign change"),
    ("↺", "DEPENDABLE FALLBACK", "safe choice inside larger solvers"),
    ("1 0 1", "ONE BIT PER PASS", "each halving adds one binary digit"),
]


def txt(string, size, color=WHITE, highlights=None):
    factor = max(1, -(-60 // int(size)))
    return Text(
        string,
        font=FONT,
        weight=BOLD,
        font_size=size * factor,
        color=color,
        t2c=highlights or {},
    ).scale(1 / factor)


def make_dot_grid(spacing=1.0, radius=0.013):
    dots = VGroup()
    for x in np.arange(-6.5, 7.0, spacing):
        for y in np.arange(-3.5, 4.0, spacing):
            dots.add(Dot([x, y, 0], radius=radius, color=GRID_DOT, fill_opacity=0.45))
    return dots


class InPractice(Scene):
    def row(self, icon, label, detail, y):
        box = RoundedRectangle(
            width=12.5,
            height=1.16,
            corner_radius=0.15,
            stroke_color=PANEL_EDGE,
            stroke_width=1.2,
            stroke_opacity=0.9,
            fill_color=PANEL,
            fill_opacity=0.7,
        ).move_to([0, y, 0])
        accent = Line([-6.2, y - 0.42, 0], [-6.2, y + 0.42, 0], color=CYAN, stroke_width=3.2)
        accent.set_stroke(opacity=0.85)

        chip = RoundedRectangle(
            width=0.86, height=0.86, corner_radius=0.16,
            stroke_color=CYAN, stroke_width=1.4, stroke_opacity=0.75,
            fill_color=NAVY, fill_opacity=0.65,
        ).move_to([-5.6, y, 0])
        icon_text = txt(icon, 21 if icon != "1 0 1" else 11, CYAN).move_to(chip)

        label_text = txt(label, 20, WHITE).move_to([-4.85, y, 0], aligned_edge=LEFT)
        detail_text = txt(detail, 13, MUTED).move_to([5.9, y, 0], aligned_edge=RIGHT)
        return VGroup(box, accent, chip, icon_text, label_text, detail_text)

    def construct(self):
        self.camera.background_color = NAVY

        grid = make_dot_grid()
        self.play(FadeIn(grid), run_time=0.5)

        head = txt("IN PRACTICE", 24, WHITE, {"PRACTICE": CYAN})
        head.move_to([NL_LEFT + head.width / 2, 3.55, 0])
        head_func = txt("f(x) = x³ − x − 2", 22, WHITE, {"x³ − x − 2": CYAN})
        head_func.move_to([NL_RIGHT - head_func.width / 2, 3.55, 0])
        rule = Line([NL_LEFT, 3.18, 0], [NL_RIGHT, 3.18, 0], color=CYAN, stroke_width=2)
        rule.set_stroke(opacity=0.4)
        self.play(FadeIn(head, shift=DOWN * 0.05), FadeIn(head_func), Create(rule), run_time=0.7)

        question = txt("Where does bisection fit?", 17, SECONDARY).move_to([0, 2.55, 0])
        self.play(FadeIn(question, shift=DOWN * 0.05), run_time=0.5)
        self.wait(2.4)

        rows = [self.row(i, l, d, y) for (i, l, d), y in zip(ROWS, (1.35, 0.0, -1.35))]
        for row, hold in zip(rows, (3.7, 3.7, 3.9)):
            self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.8)
            self.wait(hold)

        takeaway = txt(
            "BISECTION  +  NEWTON   →   certainty, then speed",
            18,
            WHITE,
            {"BISECTION": CYAN, "NEWTON": CYAN, "certainty, then speed": SECONDARY},
        ).move_to([0, -2.68, 0])
        self.play(FadeIn(takeaway, shift=UP * 0.06), run_time=0.8)
        self.wait(4.0)

        self.play(FadeOut(Group(*self.mobjects), shift=UP * 0.2), run_time=0.9)
        self.wait(0.1)
