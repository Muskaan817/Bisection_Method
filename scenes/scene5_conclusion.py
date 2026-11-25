"""
Scene 5 - the final result.

Root reveal on the graph, then applications, trade-offs, a five-step recap
and the closing credits. New composition: graph panel on the left, a root
card on the right, then tiled and columnar layouts.

Render:
    manim -ql scenes/scene5_conclusion.py BisectionConclusion
"""

import numpy as np
from manim import *

# ---------------------------------------------------------------------------
# Palette and typography (identical to scenes 1-4)
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

config.background_color = NAVY

ROOT = 1.5213797


def f(x):
    return x**3 - x - 2


def txt(string, size, color=WHITE, highlights=None, slant=NORMAL):
    # Pango miscounts glyph advances at small font sizes, so lay out large and
    # scale down; the paths are identical and the spacing stays correct.
    factor = max(1, -(-60 // int(size)))
    t = Text(
        string, font=FONT, weight=BOLD, font_size=size * factor, color=color, slant=slant
    )
    if highlights:
        t.set_color_by_t2c(highlights)
    return t.scale(1 / factor)


def make_dot_grid(spacing=1.0, radius=0.013):
    dots = VGroup()
    for x in np.arange(-6.5, 7.0, spacing):
        for y in np.arange(-3.5, 4.0, spacing):
            dots.add(Dot([x, y, 0], radius=radius, color=GRID_DOT, fill_opacity=0.45))
    return dots


def glow_dot(point, radius=0.06, halo_radius=0.2):
    halo = Circle(
        radius=halo_radius, stroke_width=0, fill_color=GLOW, fill_opacity=0.22
    ).move_to(point)
    core = Dot(point, radius=radius, color=WHITE)
    return VGroup(halo, core)


def panel(width, height, center, fill=PANEL, opacity=0.92, stroke=PANEL_EDGE):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        stroke_color=stroke,
        stroke_width=1.2,
        fill_color=fill,
        fill_opacity=opacity,
    ).move_to(center)


class BisectionConclusion(Scene):
    # -- strip geometry for the interval-narrowing readout ----------------
    S_LEFT, S_RIGHT = 0.75, 5.45
    S_LO, S_HI = 1.49, 1.55

    def sx(self, x):
        return self.S_LEFT + (x - self.S_LO) * (self.S_RIGHT - self.S_LEFT) / (
            self.S_HI - self.S_LO
        )

    def strip_bar(self, a, b, color=CYAN, fill=0.22):
        return RoundedRectangle(
            width=(b - a) * (self.S_RIGHT - self.S_LEFT) / (self.S_HI - self.S_LO),
            height=0.22,
            corner_radius=0.05,
            stroke_color=color,
            stroke_width=1.6,
            fill_color=color,
            fill_opacity=fill,
        ).move_to([self.sx((a + b) / 2), -0.57, 0])

    # -- application tile --------------------------------------------------
    def icon_ruler(self):
        base = Line([-0.5, 0, 0], [0.5, 0, 0], color=CYAN, stroke_width=2.4)
        ticks = VGroup()
        for i in range(7):
            x = -0.45 + 0.15 * i
            h = 0.15 if i % 2 == 0 else 0.08
            ticks.add(
                Line([x, 0.02, 0], [x, h + 0.02, 0], color=CYAN, stroke_width=1.8)
            )
        return VGroup(base, ticks)

    def icon_terminal(self):
        win = RoundedRectangle(
            width=0.98,
            height=0.62,
            corner_radius=0.08,
            stroke_color=CYAN,
            stroke_width=1.8,
            fill_color=NAVY,
            fill_opacity=0.6,
        )
        bar = Line([-0.45, 0.16, 0], [0.45, 0.16, 0], color=CYAN, stroke_width=1.2)
        dots = VGroup(
            *[
                Dot([-0.38 + 0.11 * i, 0.27, 0], radius=0.028, color=CYAN)
                for i in range(3)
            ]
        )
        prompt = Text(">_", font="Menlo", weight=BOLD, font_size=26, color=WHITE)
        prompt.scale(0.55).move_to([-0.24, -0.14, 0])
        return VGroup(win, bar, dots, prompt)

    def icon_equation(self):
        chip = RoundedRectangle(
            width=1.16,
            height=0.5,
            corner_radius=0.25,
            stroke_color=CYAN,
            stroke_width=1.8,
            fill_color=NAVY,
            fill_opacity=0.6,
        )
        eq = txt("f(x) = 0", 15, WHITE, {"0": CYAN}).move_to(chip)
        return VGroup(chip, eq)

    def icon_curve(self):
        base = Line([-0.55, -0.16, 0], [0.55, -0.16, 0], color=CYAN, stroke_width=2)
        wave = ParametricFunction(
            lambda t: np.array([t, 0.22 * np.sin(t * np.pi / 0.37) + 0.03, 0]),
            t_range=[-0.5, 0.5],
            color=CYAN,
            stroke_width=2.4,
        )
        return VGroup(base, wave)

    def tile(self, icon, line1, line2, center):
        box = panel(2.78, 1.78, center, opacity=0.85)
        glow = RoundedRectangle(
            width=2.78,
            height=1.78,
            corner_radius=0.18,
            stroke_color=GLOW,
            stroke_width=12,
            stroke_opacity=0.10,
            fill_opacity=0,
        ).move_to(center)
        icon.move_to([center[0], center[1] + 0.44, 0])
        lab = VGroup(
            txt(line1, 13.5, WHITE),
            txt(line2, 12, SECONDARY),
        ).arrange(DOWN, buff=0.10)
        lab.move_to([center[0], center[1] - 0.47, 0])
        return VGroup(glow, box, icon, lab)

    # -- credits line ------------------------------------------------------
    def construct(self):
        self.camera.background_color = NAVY

        # ===================================================================
        # 1. Header
        # ===================================================================
        grid = make_dot_grid()
        self.play(FadeIn(grid), run_time=0.5)

        head = txt("THE FINAL RESULT", 24, WHITE, {"FINAL RESULT": CYAN})
        head.move_to([-6.35 + head.width / 2, 3.55, 0])
        head_func = txt("f(x) = x³ − x − 2", 22, WHITE, {"x³ − x − 2": CYAN})
        head_func.move_to([6.35 - head_func.width / 2, 3.55, 0])
        rule = Line([-6.35, 3.18, 0], [6.35, 3.18, 0], color=CYAN, stroke_width=2)
        rule.set_stroke(opacity=0.4)
        self.play(
            FadeIn(head, shift=DOWN * 0.05), FadeIn(head_func), Create(rule), run_time=0.8
        )

        # ===================================================================
        # 2. Phase 1 - graph, root, final interval
        # ===================================================================
        shadow = RoundedRectangle(
            width=5.8, height=6.2, corner_radius=0.18,
            stroke_width=0, fill_color=PANEL_SHADOW, fill_opacity=0.9,
        ).move_to([-3.44, -0.34, 0])
        gpanel = panel(5.8, 6.2, [-3.45, -0.3, 0])

        axes = Axes(
            x_range=[1.0, 2.0, 0.5],
            y_range=[-1, 5, 1],
            x_length=4.2,
            y_length=4.6,
            axis_config={
                "color": AXIS,
                "stroke_width": 2.4,
                "tick_size": 0.07,
                "tip_width": 0.16,
                "tip_height": 0.16,
                "include_numbers": False,
            },
        ).move_to([-3.45, -0.45, 0])
        x_lab = txt("x", 20, WHITE, slant=ITALIC).next_to(
            axes.x_axis.get_end(), RIGHT, buff=0.12
        )
        y_lab = txt("f(x)", 18, WHITE, slant=ITALIC).next_to(
            axes.y_axis.get_end(), UP, buff=0.10
        )
        curve = axes.plot(f, x_range=[0.95, 2.05], stroke_width=4.0, use_smoothing=True)
        curve.set_color_by_gradient(CYAN, BLUE)
        curve_glow = axes.plot(f, x_range=[0.95, 2.05], color=GLOW)
        curve_glow.set_stroke(width=12, opacity=0.13)

        # 1.5 sits above the axis (the curve crosses below it near the root),
        # 2.0 below; no 1.0 because it lands on the y-axis corner.
        x_nums = VGroup(
            txt("1.5", 13, MUTED).move_to(
                [axes.c2p(1.5, 0)[0] - 0.16, axes.c2p(1.5, 0)[1] + 0.30, 0]
            ),
            txt("2", 13, MUTED).move_to(
                [axes.c2p(2.0, 0)[0], axes.c2p(2.0, 0)[1] - 0.28, 0]
            ),
        )
        y_nums = VGroup()
        for v in (2, 4):
            p = axes.c2p(1.0, v)
            y_nums.add(txt(f"{v:g}", 13, MUTED).move_to([p[0] - 0.30, p[1], 0]))

        self.play(FadeIn(shadow), FadeIn(gpanel), run_time=0.5)
        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab), run_time=0.8)
        self.play(Create(curve_glow), Create(curve), run_time=1.1)
        self.play(FadeIn(x_nums), FadeIn(y_nums), run_time=0.4)

        root_p = axes.c2p(ROOT, 0)
        root_dot = glow_dot(root_p, 0.07, 0.22)
        root_guide = DashedLine(
            [root_p[0], root_p[1], 0],
            [root_p[0], root_p[1] + 1.55, 0],
            dash_length=0.06,
            dashed_ratio=0.5,
            color=WHITE,
            stroke_width=1.8,
            stroke_opacity=0.55,
        )
        root_tag = txt("root", 14, CYAN).move_to([root_p[0] + 0.42, root_p[1] + 1.72, 0])
        self.play(
            FadeIn(root_dot, scale=0.6), Create(root_guide), FadeIn(root_tag), run_time=0.9
        )

        eyebrow = txt("ROOT OF  f(x) = 0", 14, MUTED).move_to([3.1, 2.2, 0])
        big = txt("x ≈ 1.52138", 42, WHITE, {"1.52138": CYAN}).move_to([3.1, 1.38, 0])
        note = txt("f(1.52138) ≈ 0", 16, SECONDARY, {"≈ 0": CYAN}).move_to([3.1, 0.66, 0])
        self.play(FadeIn(eyebrow, shift=DOWN * 0.05), run_time=0.4)
        self.play(FadeIn(big, shift=DOWN * 0.08), run_time=0.6)
        self.play(FadeIn(note), run_time=0.35)

        strip_axis = Line(
            [self.S_LEFT, -0.68, 0], [self.S_RIGHT, -0.68, 0],
            color=AXIS, stroke_width=2,
        )
        strip_ticks = VGroup()
        for v in (1.50, 1.52, 1.54):
            x = self.sx(v)
            strip_ticks.add(
                Line([x, -0.75, 0], [x, -0.61, 0], color=AXIS, stroke_width=1.4)
            )
            strip_ticks.add(txt(f"{v:g}", 12, MUTED).move_to([x, -1.02, 0]))
        sbar = self.strip_bar(1.5, 1.53125)
        sbar_glow = RoundedRectangle(
            width=(1.53125 - 1.5) * (self.S_RIGHT - self.S_LEFT) / (self.S_HI - self.S_LO),
            height=0.22,
            corner_radius=0.05,
            stroke_color=GLOW,
            stroke_width=12,
            stroke_opacity=0.16,
            fill_opacity=0,
        ).move_to([self.sx(1.515625), -0.57, 0])
        swidth = txt("width  0.03125", 14, SECONDARY, {"0.03125": CYAN}).move_to(
            [3.1, -1.42, 0]
        )
        scaption = txt("each pass halves the error", 13, MUTED).move_to([3.1, -1.95, 0])
        self.play(
            Create(strip_axis), FadeIn(strip_ticks), GrowFromCenter(sbar),
            FadeIn(sbar_glow), FadeIn(swidth), FadeIn(scaption),
            run_time=0.9,
        )

        for a, b, w in (
            (1.515625, 1.53125, "0.015625"),
            (1.51953125, 1.521484375, "0.00195"),
        ):
            new_bar = self.strip_bar(a, b)
            new_glow = RoundedRectangle(
                width=(b - a) * (self.S_RIGHT - self.S_LEFT) / (self.S_HI - self.S_LO),
                height=0.22,
                corner_radius=0.05,
                stroke_color=GLOW,
                stroke_width=12,
                stroke_opacity=0.16,
                fill_opacity=0,
            ).move_to([self.sx((a + b) / 2), -0.57, 0])
            new_w = txt(f"width  {w}", 14, SECONDARY, {w: CYAN}).move_to([3.1, -1.42, 0])
            self.play(
                Transform(sbar, new_bar), Transform(sbar_glow, new_glow),
                FadeOut(swidth), FadeIn(new_w), run_time=0.75,
            )
            swidth = new_w
        self.wait(2.6)

        p1 = Group(
            shadow, gpanel, axes, x_lab, y_lab, curve, curve_glow, x_nums, y_nums,
            root_dot, root_guide, root_tag, eyebrow, big, note, strip_axis,
            strip_ticks, sbar, sbar_glow, swidth, scaption,
        )

        # ===================================================================
        # 3. Phase 2 - where it is used
        # ===================================================================
        p2_head = txt("WHERE IT IS USED", 14, MUTED).move_to([0, 2.3, 0])
        p2_caption = txt(
            "whenever f(x) = 0 must be solved numerically", 14, MUTED, {"0": CYAN}
        ).move_to([0, -2.15, 0])
        tiles = VGroup(
            self.tile(self.icon_ruler(), "ENGINEERING", "calculations", [-4.92, 0.35, 0]),
            self.tile(self.icon_terminal(), "SCIENTIFIC", "computing", [-1.64, 0.35, 0]),
            self.tile(self.icon_equation(), "NUMERICAL", "equation solving", [1.64, 0.35, 0]),
            self.tile(self.icon_curve(), "MATHEMATICAL", "modelling & simulation", [4.92, 0.35, 0]),
        )
        self.play(FadeOut(p1, shift=UP * 0.2), FadeIn(p2_head), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(t, shift=UP * 0.12) for t in tiles], lag_ratio=0.22),
            run_time=1.4,
        )
        self.play(FadeIn(p2_caption), run_time=0.4)
        self.wait(3.6)

        # ===================================================================
        # 4. Phase 3 - advantages and limitations
        # ===================================================================
        cols = VGroup()
        for cx, name, color, rows in (
            (
                -3.35, "ADVANTAGES", CYAN,
                [
                    "Simple to understand and implement.",
                    "Reliable for a continuous f with a sign change.",
                    "Convergence is guaranteed under those conditions.",
                ],
            ),
            (
                3.35, "LIMITATIONS", WHITE,
                [
                    "Convergence is relatively slow.",
                    "Needs an initial interval that brackets a root.",
                    "Not valid for every function or interval.",
                ],
            ),
        ):
            hdr = txt(name, 19, color).move_to([cx, 2.0, 0])
            uline = Line(
                [cx - 1.35, 1.72, 0], [cx + 1.35, 1.72, 0],
                color=color, stroke_width=1.6,
            )
            uline.set_stroke(opacity=0.55)
            block = VGroup(hdr, uline)
            bullet_color = CYAN if color == CYAN else MUTED
            for i, s in enumerate(rows):
                y = 1.05 - 0.75 * i
                bullet = Circle(
                    radius=0.045, stroke_color=bullet_color,
                    stroke_width=1.6, fill_opacity=0,
                ).move_to([cx - 2.85, y, 0])
                line = txt(s, 16, SECONDARY).move_to([0, 0, 0])
                line.move_to([cx - 2.55 + line.width / 2, y, 0])
                block.add(bullet, line)
            cols.add(block)
        divider = Line([0, 2.35, 0], [0, -0.75, 0], color=PANEL_EDGE, stroke_width=1.2)
        divider.set_stroke(opacity=0.8)
        takeaway = txt(
            "Bisection trades speed for certainty.", 16, SECONDARY, {"certainty.": CYAN}
        ).move_to([0, -2.15, 0])

        self.play(
            FadeOut(tiles, shift=UP * 0.15), FadeOut(p2_head),
            FadeOut(p2_caption), run_time=0.6,
        )
        self.play(FadeIn(divider), run_time=0.3)
        self.play(
            LaggedStart(*[FadeIn(b, shift=UP * 0.08) for b in cols], lag_ratio=0.18),
            run_time=1.4,
        )
        self.play(FadeIn(takeaway, shift=UP * 0.06), run_time=0.45)
        self.wait(4.6)

        # ===================================================================
        # 5. Phase 4 - the method in five steps
        # ===================================================================
        steps = [
            ("1", "Start with\nan interval"),
            ("2", "Find the\nmidpoint"),
            ("3", "Check the\nsign"),
            ("4", "Keep the half\nwith the root"),
            ("5", "Repeat until\naccurate"),
        ]
        chips = VGroup()
        for i, (num, label) in enumerate(steps):
            cx = -5.0 + 2.5 * i
            box = panel(2.28, 1.2, [cx, 0.5, 0], opacity=0.9)
            body = VGroup(
                txt(num, 15, CYAN),
                txt(label, 13.5, WHITE),
            ).arrange(DOWN, buff=0.09).move_to([cx, 0.48, 0])
            chips.add(VGroup(box, body))
        p4_head = txt("THE METHOD IN FIVE STEPS", 14, MUTED).move_to([0, 2.05, 0])
        arrows = VGroup()
        for i in range(4):
            arrows.add(
                txt("→", 21, SECONDARY).move_to([-5.0 + 2.5 * i + 1.25, 0.5, 0])
            )
        tagline = txt(
            "Simple.  Reliable.  Mathematically Guaranteed.",
            30,
            WHITE,
            {"Simple.": GLOW, "Guaranteed.": CYAN},
        ).move_to([0, -1.8, 0])

        self.play(
            FadeOut(cols, shift=UP * 0.15), FadeOut(divider),
            FadeOut(takeaway, shift=UP * 0.15), run_time=0.6,
        )
        self.play(FadeIn(p4_head), run_time=0.3)
        self.play(
            LaggedStart(
                *[FadeIn(c, shift=UP * 0.10) for c in chips], lag_ratio=0.16
            ),
            FadeIn(arrows),
            run_time=1.4,
        )
        self.play(FadeIn(tagline, shift=UP * 0.08), run_time=0.8)
        self.wait(4.4)

        # ===================================================================
        # 6. Phase 5 - credits
        # ===================================================================
        self.play(
            FadeOut(chips, shift=UP * 0.12), FadeOut(arrows),
            FadeOut(tagline, shift=UP * 0.12), FadeOut(p4_head),
            FadeOut(head, shift=UP * 0.08), FadeOut(head_func), FadeOut(rule),
            run_time=0.7,
        )

        c_rule = Line([-1.4, 1.55, 0], [1.4, 1.55, 0], color=CYAN, stroke_width=2.4)
        c_rule.set_stroke(opacity=0.75)
        c_title = txt("Bisection Method", 34, WHITE).move_to([0, 0.9, 0])
        c_sub = txt("NUMERICAL ROOT FINDING", 17, CYAN).move_to([0, 0.22, 0])
        c_course = txt("Course:  M3", 17, SECONDARY, {"M3": WHITE}).move_to([0, -0.75, 0])
        c_student = txt(
            "Student:  Muskaan Ram Rakhyani", 19, SECONDARY,
            {"Muskaan Ram Rakhyani": CYAN},
        ).move_to([0, -1.35, 0])
        c_split = DashedLine(
            [-2.1, -2.3, 0], [2.1, -2.3, 0],
            dash_length=0.06, dashed_ratio=0.5, color=MUTED, stroke_width=1.2,
        )
        c_split.set_stroke(opacity=0.6)
        c_team = txt("Team & instructor credits", 13, MUTED).move_to([0, -2.72, 0])
        credits = VGroup(
            c_rule, c_title, c_sub, c_course, c_student, c_split, c_team
        )

        self.play(Create(c_rule), run_time=0.5)
        self.play(FadeIn(c_title, shift=UP * 0.08), run_time=0.6)
        self.play(FadeIn(c_sub), FadeIn(c_course), FadeIn(c_student), run_time=0.6)
        self.play(Create(c_split), FadeIn(c_team), run_time=0.5)
        self.wait(4.2)

        self.play(FadeOut(Group(grid, credits), shift=UP * 0.15), run_time=1.2)
        self.wait(0.5)
