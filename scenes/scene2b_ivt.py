"""
Scene 2B - the Intermediate Value Theorem behind the bracket.

Focused explanation that sits between Scene 2 (concept) and Scene 3
(iterations): continuous curve, opposite endpoint signs, guaranteed crossing.

Render:
    manim -qh scenes/scene2b_ivt.py IvtTheorem
"""

import numpy as np
from manim import *

# ---------------------------------------------------------------------------
# Palette / typography (identical to scenes 1-5)
# ---------------------------------------------------------------------------
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

ROOT = 1.5213797


def f(x):
    return x**3 - x - 2


def txt(string, size, color=WHITE, highlights=None, slant=NORMAL):
    factor = max(1, -(-60 // int(size)))
    t = Text(
        string,
        font=FONT,
        weight=BOLD,
        font_size=size * factor,
        color=color,
        slant=slant,
        t2c=highlights or {},
    )
    return t.scale(1 / factor)


def make_dot_grid(spacing=1.0, radius=0.013):
    dots = VGroup()
    for x in np.arange(-6.5, 7.0, spacing):
        for y in np.arange(-3.5, 4.0, spacing):
            dots.add(Dot([x, y, 0], radius=radius, color=GRID_DOT, fill_opacity=0.45))
    return dots


def panel(width, height, center, opacity=0.92):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        stroke_color=PANEL_EDGE,
        stroke_width=1.2,
        fill_color=PANEL,
        fill_opacity=opacity,
    ).move_to(center)


def glow_dot(point, radius=0.06, halo_radius=0.2):
    halo = Circle(radius=halo_radius, stroke_width=0, fill_color=GLOW, fill_opacity=0.22)
    core = Dot(point, radius=radius, color=WHITE)
    return VGroup(halo.move_to(point), core.move_to(point))


class IvtTheorem(Scene):
    def construct(self):
        self.camera.background_color = NAVY

        grid = make_dot_grid()
        self.play(FadeIn(grid), run_time=0.5)

        head = txt("THE INTERMEDIATE VALUE THEOREM", 24, WHITE, {"INTERMEDIATE VALUE": CYAN})
        head.move_to([NL_LEFT + head.width / 2, 3.55, 0])
        head_func = txt("f(x) = x³ − x − 2", 22, WHITE, {"x³ − x − 2": CYAN})
        head_func.move_to([NL_RIGHT - head_func.width / 2, 3.55, 0])
        rule = Line([NL_LEFT, 3.18, 0], [NL_RIGHT, 3.18, 0], color=CYAN, stroke_width=2)
        rule.set_stroke(opacity=0.4)
        self.play(FadeIn(head, shift=DOWN * 0.05), FadeIn(head_func), Create(rule), run_time=0.7)

        # ------------------------------------------------------------------
        # Graph panel
        # ------------------------------------------------------------------
        gshadow = RoundedRectangle(
            width=5.8, height=5.9, corner_radius=0.18, stroke_width=0,
            fill_color=PANEL_SHADOW, fill_opacity=0.9,
        ).move_to([-3.38, -0.44, 0])
        gpanel = panel(5.8, 5.9, [-3.45, -0.35, 0])

        axes = Axes(
            x_range=[0.6, 2.4, 0.5],
            y_range=[-3, 5, 2],
            x_length=4.3,
            y_length=4.2,
            axis_config={
                "color": AXIS,
                "stroke_width": 2.4,
                "tick_size": 0.07,
                "tip_width": 0.16,
                "tip_height": 0.16,
                "include_numbers": False,
            },
        ).move_to([-3.45, -0.45, 0])
        x_lab = txt("x", 20, WHITE, slant=ITALIC).next_to(axes.x_axis.get_end(), RIGHT, buff=0.12)
        y_lab = txt("f(x)", 18, WHITE, slant=ITALIC).next_to(axes.y_axis.get_end(), UP, buff=0.10)
        x_nums = VGroup(
            *[
                txt(f"{v}", 13, MUTED).move_to(
                    [axes.c2p(v, 0)[0], axes.c2p(v, 0)[1] - 0.28, 0]
                )
                for v in (1, 2)
            ]
        )

        # Stop just below the top of the y-range so the curve stays in the panel.
        curve = axes.plot(f, x_range=[0.7, 2.08], stroke_width=4.0, use_smoothing=True)
        curve.set_color_by_gradient(CYAN, BLUE)
        curve_glow = axes.plot(f, x_range=[0.7, 2.08], color=GLOW)
        curve_glow.set_stroke(width=12, opacity=0.13)

        # ------------------------------------------------------------------
        # Sign card
        # ------------------------------------------------------------------
        cshadow = RoundedRectangle(
            width=5.6, height=3.4, corner_radius=0.18, stroke_width=0,
            fill_color=PANEL_SHADOW, fill_opacity=0.9,
        ).move_to([3.22, 0.62, 0])
        cpanel = panel(5.6, 3.4, [3.15, 0.55, 0])

        card_title = txt("ENDPOINT SIGNS", 13, MUTED).move_to([3.15, 1.98, 0])

        row1 = VGroup(
            txt("f(1) = −2", 21, WHITE, {"−2": CYAN}),
            txt("below the axis", 12, MUTED),
        ).arrange(DOWN, buff=0.06).move_to([3.15, 1.32, 0])
        divider = Line([1.0, 0.84, 0], [5.3, 0.84, 0], color=PANEL_EDGE, stroke_width=1.2)
        divider.set_stroke(opacity=0.6)
        row2 = VGroup(
            txt("f(2) = 4", 21, WHITE, {"4": CYAN}),
            txt("above the axis", 12, MUTED),
        ).arrange(DOWN, buff=0.06).move_to([3.15, 0.36, 0])

        concl = VGroup(
            txt("f(1) · f(2) < 0", 20, WHITE, {"< 0": CYAN}),
            txt("opposite signs, so a root is inside", 12, MUTED),
        ).arrange(DOWN, buff=0.08).move_to([3.15, -0.58, 0])

        caption = txt("Continuous ⇒ the curve must cross the axis.", 15, SECONDARY).move_to(
            [3.15, -1.9, 0]
        )

        self.play(
            FadeIn(gshadow), FadeIn(gpanel), FadeIn(cshadow), FadeIn(cpanel), run_time=0.5
        )
        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab), FadeIn(x_nums), run_time=0.6)
        self.play(Create(curve_glow), Create(curve), run_time=1.1)

        # ------------------------------------------------------------------
        # Endpoint 1: f(1) = -2, below the axis
        # ------------------------------------------------------------------
        pA = axes.c2p(1, f(1))
        dash1 = DashedLine(
            axes.c2p(1, 0), pA, color=AXIS, stroke_width=1.4,
            dash_length=0.06, dashed_ratio=0.55,
        )
        dotA = glow_dot(pA, radius=0.055)
        valA = txt("−2", 16, CYAN).move_to(pA + LEFT * 0.38)

        self.play(
            FadeIn(card_title), FadeIn(row1), Create(divider),
            Create(dash1), FadeIn(dotA), FadeIn(valA),
            run_time=0.7,
        )
        self.wait(4.0)

        # ------------------------------------------------------------------
        # Endpoint 2: f(2) = 4, above the axis
        # ------------------------------------------------------------------
        pB = axes.c2p(2, f(2))
        dash2 = DashedLine(
            axes.c2p(2, 0), pB, color=AXIS, stroke_width=1.4,
            dash_length=0.06, dashed_ratio=0.55,
        )
        dotB = glow_dot(pB, radius=0.055, halo_radius=0.18)
        valB = txt("4", 16, CYAN).move_to(pB + LEFT * 0.32)

        self.play(FadeIn(row2), Create(dash2), FadeIn(dotB), FadeIn(valB), run_time=0.7)
        self.wait(4.7)

        # ------------------------------------------------------------------
        # The crossing: trace the curve between the two endpoints
        # ------------------------------------------------------------------
        seg_path = axes.plot(f, x_range=[1, 2], use_smoothing=True)
        seg_hi = axes.plot(f, x_range=[1, 2], color=GLOW, use_smoothing=True)
        seg_hi.set_stroke(width=9, opacity=0.45)
        tracer = Dot(axes.c2p(1, f(1)), radius=0.055, color=WHITE)

        self.play(Create(seg_hi), MoveAlongPath(tracer, seg_path), run_time=1.8)
        self.wait(0.9)

        # Root at the crossing.
        rp = axes.c2p(ROOT, 0)
        root_dash = DashedLine(
            rp + DOWN * 0.85, rp + UP * 0.85, color=CYAN, stroke_width=1.6,
            dash_length=0.05, dashed_ratio=0.5,
        )
        root_dash.set_stroke(opacity=0.65)
        root_dot = glow_dot(rp, radius=0.065)
        root_lab = txt("root", 13, CYAN).move_to(rp + DOWN * 0.42 + LEFT * 0.05)
        root_ring = Circle(radius=0.16, color=CYAN, stroke_width=2.0).move_to(rp)

        self.play(
            Create(root_dash), FadeIn(root_dot, scale=0.6), FadeIn(root_lab),
            run_time=0.7,
        )
        self.wait(1.4)

        self.play(FadeIn(concl, shift=UP * 0.06), FadeIn(caption, shift=UP * 0.06), run_time=0.8)
        self.play(
            root_ring.animate.scale(2.2).set_stroke(opacity=0),
            run_time=1.0,
        )
        self.wait(3.4)

        self.play(FadeOut(Group(*self.mobjects), shift=UP * 0.2), run_time=0.9)
        self.wait(0.1)
