"""
Scene 1 - Introduction to the Bisection Method.

A ~25 second opening for the M3 project video:
title reveal -> function + graph -> bracket/root highlight + guiding question
-> fade-and-divider transition into the next scene.

Render:
    manim -qh scenes/scene1_intro.py BisectionIntro

LaTeX is optional: MathTex is used only when a TeX toolchain is installed,
otherwise plain Text (Pango) renders the same labels.
"""

import shutil

import numpy as np
from manim import *

# ---------------------------------------------------------------------------
# Palette and typography
# ---------------------------------------------------------------------------
NAVY = "#0A1633"
PANEL = "#0F2247"
PANEL_SHADOW = "#030A18"
GRID_DOT = "#1B3562"
AXIS = "#5A76B4"
CYAN = "#22D3EE"
BLUE = "#3B82F6"
WHITE = "#F4F7FC"
MUTED = "#9DB2D6"

# Helvetica Neue lays out cleanly in Manim (Avenir Next produces gaps after
# certain glyph pairs such as "t").
FONT = "Helvetica Neue"

# MathTex needs both `latex` and `dvisvgm`; fall back to Text if either is absent.
LATEX_AVAILABLE = bool(shutil.which("latex") and shutil.which("dvisvgm"))

config.background_color = NAVY


# ---------------------------------------------------------------------------
# Math helpers
# ---------------------------------------------------------------------------
def f(x):
    """The cubic whose root the bisection method will approximate."""
    return x**3 - x - 2


def bisection_root(a, b, tol=1e-12):
    """
    Locate the root precisely so the on-screen intersection marker is accurate.
    The numeric value itself is intentionally not shown in this intro scene.
    """
    fa = f(a)
    while b - a > tol:
        mid = (a + b) / 2
        fm = f(mid)
        if fa * fm <= 0:
            b = mid
        else:
            a, fa = mid, fm
    return (a + b) / 2


ROOT = bisection_root(1.0, 2.0)  # f(1) = -2, f(2) = 4  ->  root in (1, 2)


def math_label(tex_string, plain_string, font_size, color=WHITE):
    """Use real TeX when available, otherwise a Unicode Text stand-in."""
    if LATEX_AVAILABLE:
        return MathTex(tex_string, font_size=font_size, color=color)
    return Text(plain_string, font=FONT, font_size=font_size, color=color)


# ---------------------------------------------------------------------------
# Reusable visuals
# ---------------------------------------------------------------------------
def make_card(width, height, corner_radius=0.16):
    """
    Rounded dark panel with a small offset shadow.
    The shadow is the only "3D" cue used, keeping the deck uncluttered.
    """
    shadow = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=corner_radius,
        stroke_width=0,
        fill_color=PANEL_SHADOW,
        fill_opacity=0.85,
    ).shift([0.07, -0.09, 0])
    face = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=corner_radius,
        stroke_color=BLUE,
        stroke_width=1.2,
        stroke_opacity=0.5,
        fill_color=PANEL,
        fill_opacity=0.92,
    )
    return VGroup(shadow, face), face


def make_dot_grid(spacing=1.0, radius=0.016):
    """Very faint dot grid; adds depth without competing with the graph."""
    dots = VGroup()
    for x in np.arange(-6.5, 7.0, spacing):
        for y in np.arange(-3.5, 4.0, spacing):
            dots.add(
                Dot(
                    [x, y, 0],
                    radius=radius,
                    color=GRID_DOT,
                    fill_opacity=0.5,
                )
            )
    return dots


# ---------------------------------------------------------------------------
# Scene
# ---------------------------------------------------------------------------
class BisectionIntro(Scene):
    def construct(self):
        self.camera.background_color = NAVY

        # ===================================================================
        # 1. Title card
        # ===================================================================
        dot_grid = make_dot_grid()
        self.play(FadeIn(dot_grid), run_time=0.8)

        title = Text(
            "THE BISECTION METHOD",
            font=FONT,
            weight=BOLD,
            font_size=62,
            color=WHITE,
            t2c={"BISECTION": CYAN},
        )
        # Offset duplicate acts as a subtle extruded 3D shadow.
        title_depth = (
            title.copy()
            .set_color("#123A72")
            .set_opacity(0.55)
            .shift([0.035, -0.05, 0])
        )
        title.move_to([0, 0.8, 0])
        title_depth.move_to([0.035, 0.75, 0])

        rule = Line(LEFT * 2.8, RIGHT * 2.8, color=CYAN, stroke_width=2)
        rule.move_to([0, 0.15, 0])

        subtitle = Text(
            "Finding roots through repeated interval halving",
            font=FONT,
            font_size=28,
            color=MUTED,
        ).move_to([0, -0.45, 0])

        self.play(
            FadeIn(title_depth, shift=UP * 0.06),
            AddTextLetterByLetter(title, time_per_char=0.055),
            run_time=1.4,
        )
        self.play(GrowFromCenter(rule), FadeIn(subtitle, shift=UP * 0.12), run_time=0.8)
        self.wait(1.0)

        # ===================================================================
        # 2. Compact the title into a header, then build the coordinate plane
        # ===================================================================
        header = VGroup(title_depth, title)
        self.play(
            header.animate.scale(0.5).move_to([-3.55, 3.42, 0]),
            FadeOut(subtitle, shift=DOWN * 0.2),
            FadeOut(rule),
            run_time=1.2,
        )

        # Domain chosen so the whole visible branch fits inside the axes.
        axes = Axes(
            x_range=[-2, 2.6, 1],
            y_range=[-6, 9, 3],
            x_length=9.4,
            y_length=5.0,
            axis_config={
                "color": AXIS,
                "stroke_width": 2.4,
                "include_ticks": True,
                "tick_size": 0.075,
                "tip_width": 0.18,
                "tip_height": 0.18,
            },
        ).move_to([0.35, 0.0, 0])

        x_axis_label = Text("x", font=FONT, font_size=30, color=WHITE, slant=ITALIC)
        x_axis_label.next_to(axes.x_axis.get_end(), RIGHT, buff=0.18)
        y_axis_label = Text("y", font=FONT, font_size=30, color=WHITE, slant=ITALIC)
        y_axis_label.next_to(axes.y_axis.get_end(), UP, buff=0.18)

        x_numbers = VGroup(
            *[
                Text(f"{v}", font=FONT, font_size=20, color=MUTED).next_to(
                    axes.c2p(v, 0), DOWN, buff=0.16
                )
                for v in (-2, -1, 0, 1, 2)
            ]
        )

        self.play(Create(axes), run_time=1.3)
        self.play(
            FadeIn(x_axis_label),
            FadeIn(y_axis_label),
            FadeIn(x_numbers),
            run_time=0.6,
        )

        # ===================================================================
        # 3. Plot f(x) = x^3 - x - 2
        # ===================================================================
        curve = axes.plot(f, x_range=[-1.7, 2.2], stroke_width=4.5)
        curve.set_color_by_gradient(CYAN, BLUE)
        # Wide translucent stroke behind the curve creates a soft glow.
        curve_glow = axes.plot(f, x_range=[-1.7, 2.2], color=CYAN)
        curve_glow.set_stroke(width=14, opacity=0.12)

        self.play(Create(curve_glow), Create(curve), run_time=2.2, rate_func=smooth)
        self.wait(0.4)

        # ===================================================================
        # 4. Function card
        # ===================================================================
        func_card, func_face = make_card(3.6, 0.86)
        func_card.move_to([4.75, 2.55, 0])
        func_text = math_label(
            r"f(x) = x^{3} - x - 2",
            "f(x) = x³ - x - 2",
            font_size=30,
        ).move_to(func_face)

        self.play(FadeIn(func_card, shift=DOWN * 0.12), run_time=0.9)
        self.play(Write(func_text), run_time=0.9)

        # ===================================================================
        # 5. Highlight the bracketing interval [1, 2] on the x-axis
        # ===================================================================
        a_point = axes.c2p(1, 0)
        b_point = axes.c2p(2, 0)
        root_point = axes.c2p(ROOT, 0)

        interval_glow = Line(a_point, b_point, stroke_width=14, color=CYAN)
        interval_glow.set_stroke(opacity=0.12).shift(DOWN * 0.02)
        interval_line = Line(a_point, b_point, stroke_width=4.5, color=CYAN)
        interval_line.set_stroke(opacity=0.75).shift(DOWN * 0.02)
        end_dots = VGroup(
            Dot(a_point, radius=0.045, color=WHITE),
            Dot(b_point, radius=0.045, color=WHITE),
        )

        a_label = Text("a", font=FONT, font_size=24, color=CYAN, slant=ITALIC)
        a_label.next_to(a_point, UP, buff=0.18)
        b_label = Text("b", font=FONT, font_size=24, color=CYAN, slant=ITALIC)
        b_label.next_to(b_point, UP, buff=0.18)

        self.play(
            Create(interval_glow),
            Create(interval_line),
            FadeIn(end_dots),
            run_time=0.9,
        )
        self.play(FadeIn(a_label, shift=UP * 0.08), FadeIn(b_label, shift=UP * 0.08), run_time=0.6)

        # ===================================================================
        # 6. Root marker at the x-axis intersection
        # ===================================================================
        root_ring = Ellipse(
            width=0.9,
            height=0.5,
            color=CYAN,
            stroke_width=1.4,
            stroke_opacity=0.5,
        ).move_to(root_point)

        # Layered translucent circles fake a soft radial glow (no shaders needed).
        root_halo = VGroup(
            Circle(radius=0.36, stroke_width=0, fill_color=CYAN, fill_opacity=0.07),
            Circle(radius=0.22, stroke_width=0, fill_color=CYAN, fill_opacity=0.13),
            Circle(radius=0.11, stroke_width=0, fill_color=CYAN, fill_opacity=0.25),
        ).move_to(root_point)
        root_core = Dot(root_point, radius=0.06, color=WHITE)

        self.play(
            FadeIn(root_ring, scale=0.7),
            FadeIn(root_halo, scale=0.5),
            FadeIn(root_core, scale=0.3),
            run_time=0.9,
        )
        self.play(
            Flash(
                root_point,
                color=CYAN,
                flash_radius=0.45,
                line_length=0.12,
                num_lines=14,
                time_width=0.35,
            ),
            run_time=0.7,
        )

        # One expanding ring directs the eye to the intersection.
        pulse = Circle(
            radius=0.17, color=CYAN, stroke_width=2.2, stroke_opacity=0.9
        ).move_to(root_point)
        self.play(
            pulse.animate.scale(2.6).set_stroke(opacity=0),
            run_time=1.1,
            rate_func=smooth,
        )

        # ===================================================================
        # 7. "root" callout
        # ===================================================================
        root_card, root_face = make_card(1.5, 0.62, corner_radius=0.12)
        root_card.move_to([1.25, 1.05, 0])
        root_text = Text("root", font=FONT, weight=BOLD, font_size=26, color=WHITE)
        root_text.move_to(root_face)

        leader = Line(
            root_point,
            root_card.get_right(),
            color=CYAN,
            stroke_width=1.3,
            stroke_opacity=0.55,
        )

        self.play(FadeIn(root_card, shift=UP * 0.1), Write(root_text), run_time=0.8)
        self.play(Create(leader), run_time=0.5)

        # ===================================================================
        # 8. The guiding question
        # ===================================================================
        question_card, question_face = make_card(9.4, 1.2, corner_radius=0.16)
        question_card.move_to([0, -3.3, 0])

        # Manim's Text left-aligns multi-line blocks, so build two lines and
        # center them explicitly inside the card.
        question_line1 = Text(
            "How can we find the root",
            font=FONT,
            font_size=28,
            color=WHITE,
        )
        question_line2 = Text(
            "without solving the equation directly?",
            font=FONT,
            font_size=28,
            color=WHITE,
        )
        question_text = VGroup(question_line1, question_line2)
        question_text.arrange(DOWN, buff=0.13, center=True).move_to(question_face)

        accent = Line(
            question_face.get_left() + RIGHT * 0.22 + DOWN * 0.3,
            question_face.get_left() + RIGHT * 0.22 + UP * 0.3,
            color=CYAN,
            stroke_width=4,
            stroke_opacity=0.9,
        )

        self.play(FadeIn(question_card, shift=UP * 0.25), Create(accent), run_time=0.8)
        self.play(
            LaggedStart(
                Write(question_line1),
                Write(question_line2),
                lag_ratio=0.25,
            ),
            run_time=1.6,
        )
        self.wait(3.0)

        # ===================================================================
        # 9. Transition to the next scene
        # ===================================================================
        # Drift everything up and fade to navy...
        self.play(
            FadeOut(Group(*self.mobjects), shift=UP * 0.35),
            run_time=1.3,
        )
        # ...then a single cyan divider line grows and dissolves, acting as a
        # visual cut before the next scene fades in on the same navy background.
        divider = Line(
            LEFT * 3.2, RIGHT * 3.2, color=CYAN, stroke_width=2, stroke_opacity=0.9
        )
        self.play(GrowFromCenter(divider), run_time=0.7)
        self.play(divider.animate.set_opacity(0), run_time=0.5)
