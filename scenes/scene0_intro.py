"""
Scene 0 - personal introduction before the title sequence.

"Hello everyone!" -> name -> Turing Batch -> film title, then a fade to navy
so Scene 1 opens without a hard cut. Kept to about 12 seconds so the full
film starts promptly.

Render:
    manim -qh scenes/scene0_intro.py BisectionWelcome
"""

import numpy as np
from manim import *

# ---------------------------------------------------------------------------
# Palette and typography (identical to scenes 1-5)
# ---------------------------------------------------------------------------
NAVY = "#0A1633"
GRID_DOT = "#1B3562"
AXIS = "#5A76B4"
CYAN = "#22D3EE"
BLUE = "#3B82F6"
WHITE = "#F4F7FC"
MUTED = "#9DB2D6"
SECONDARY = "#C6D3EA"

FONT = "Helvetica Neue"

config.background_color = NAVY


def txt(string, size, color=WHITE, weight=BOLD):
    # Pango miscounts glyph advances below ~60 pt, so lay out large and scale.
    factor = max(1, -(-60 // int(size)))
    return Text(
        string, font=FONT, weight=weight, font_size=size * factor, color=color
    ).scale(1 / factor)


def make_dot_grid(spacing=1.0, radius=0.016):
    dots = VGroup()
    for x in np.arange(-6.5, 7.0, spacing):
        for y in np.arange(-3.5, 4.0, spacing):
            dots.add(
                Dot([x, y, 0], radius=radius, color=GRID_DOT, fill_opacity=0.5)
            )
    return dots


class BisectionWelcome(Scene):
    def construct(self):
        self.camera.background_color = NAVY

        grid = make_dot_grid()

        eyebrow = txt("M3  ·  NUMERICAL METHODS", 16, MUTED).move_to([0, 3.22, 0])

        # -- greeting ------------------------------------------------------
        hello = Text(
            "HELLO EVERYONE!",
            font=FONT,
            weight=BOLD,
            font_size=44,
            color=WHITE,
            t2c={"HELLO": CYAN},
        )
        hello_depth = (
            hello.copy()
            .set_color("#123A72")
            .set_opacity(0.55)
            .shift([0.03, -0.045, 0])
        )
        hello.move_to([0, 0.62, 0])
        hello_depth.move_to([0.03, 0.575, 0])

        self.play(
            FadeIn(grid, run_time=0.7),
            AddTextLetterByLetter(hello, time_per_char=0.05),
            run_time=0.7,
        )
        # The depth copy arrives after the write so no ghost letters trail it.
        self.play(
            FadeIn(hello_depth, shift=UP * 0.05),
            FadeIn(eyebrow, shift=DOWN * 0.06),
            run_time=0.4,
        )

        # -- name (the greeting becomes a small kicker above it) -----------
        self.play(
            hello.animate.scale(0.66).move_to([0, 2.32, 0]),
            hello_depth.animate.scale(0.66).move_to([0.02, 2.29, 0]),
            run_time=0.75,
        )

        name = Text(
            "MUSKAAN RAMRAKHYANI",
            font=FONT,
            weight=BOLD,
            font_size=64,
            color=WHITE,
        ).move_to([0, 0.86, 0])
        name_depth = (
            name.copy()
            .set_color("#123A72")
            .set_opacity(0.55)
            .shift([0.035, -0.05, 0])
        )

        self.play(AddTextLetterByLetter(name, time_per_char=0.05), run_time=0.95)

        underline = Line(
            LEFT * 3.55, RIGHT * 3.55, color=CYAN, stroke_width=2.2, stroke_opacity=0.85
        ).move_to([0, 0.26, 0])
        # The depth copy arrives after the write so no ghost letters trail it.
        self.play(FadeIn(name_depth, shift=UP * 0.05), GrowFromCenter(underline), run_time=0.5)

        # -- batch ---------------------------------------------------------
        turing = txt("T U R I N G   B A T C H", 24, SECONDARY).move_to([0, -0.42, 0])
        gap, seg = 0.35, 2.1
        rule_left = Line(
            turing.get_left() + LEFT * (gap + seg),
            turing.get_left() + LEFT * gap,
            color=AXIS,
            stroke_width=1.4,
            stroke_opacity=0.9,
        )
        rule_right = Line(
            turing.get_right() + RIGHT * gap,
            turing.get_right() + RIGHT * (gap + seg),
            color=AXIS,
            stroke_width=1.4,
            stroke_opacity=0.9,
        )

        self.play(
            FadeIn(turing, shift=UP * 0.08),
            GrowFromCenter(rule_left),
            GrowFromCenter(rule_right),
            run_time=0.6,
        )

        identity = VGroup(
            hello_depth, hello, name_depth, name, underline, turing, rule_left, rule_right
        )
        # A barely perceptible breath keeps the portrait from feeling frozen.
        self.play(identity.animate.scale(1.012), run_time=2.0, rate_func=smooth)

        # -- title ---------------------------------------------------------
        title = Text(
            "BISECTION METHOD",
            font=FONT,
            weight=BOLD,
            font_size=60,
            color=WHITE,
            t2c={"BISECTION": CYAN},
        ).move_to([0, 0.55, 0])
        title_depth = (
            title.copy()
            .set_color("#123A72")
            .set_opacity(0.55)
            .shift([0.035, -0.05, 0])
        )
        divider = Line(LEFT * 2.3, RIGHT * 2.3, color=CYAN, stroke_width=2).move_to(
            [0, -0.16, 0]
        )
        subtitle = txt("N U M E R I C A L   R O O T   F I N D I N G", 22, CYAN).move_to(
            [0, -0.78, 0]
        )
        title_group = VGroup(title_depth, title, divider, subtitle)

        self.play(
            FadeOut(identity, shift=UP * 0.3),
            run_time=0.75,
        )
        self.play(
            FadeIn(title_depth, shift=UP * 0.06, run_time=0.6),
            AddTextLetterByLetter(title, time_per_char=0.055),
            run_time=0.95,
        )
        self.play(GrowFromCenter(divider), run_time=0.4)
        self.play(FadeIn(subtitle, shift=UP * 0.1), run_time=0.55)

        self.play(title_group.animate.scale(1.018), run_time=2.45, rate_func=smooth)

        # Fade everything back to navy so Scene 1's dot grid continues the
        # same background instead of cutting to it.
        self.play(
            FadeOut(Group(grid, eyebrow, title_group), shift=UP * 0.25),
            run_time=0.85,
        )
        self.wait(0.15)
