"""
Scene 4 - Convergence and accuracy.

Picks up the bracket [1.5, 1.53125] from Scene 3 and zooms the number line in
on it: width, error bound, one more bisection pass, and the tolerance test.
No side panel and no graph - the close-up line is the whole picture.

Render:
    manim -ql scenes/scene4_convergence.py BisectionConvergence
"""

import numpy as np
from manim import *

# ---------------------------------------------------------------------------
# Palette and typography (identical to scenes 1-3)
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

# ---------------------------------------------------------------------------
# Geometry: the close-up line is centred on the Scene 3 bracket
# ---------------------------------------------------------------------------
X_VIEW0, X_VIEW1 = 1.493125, 1.538125
NL_LEFT, NL_RIGHT = -6.35, 6.35
NL_SCALE = (NL_RIGHT - NL_LEFT) / (X_VIEW1 - X_VIEW0)  # ~282 screen units / x

AXIS_Y = 0.55
BAR_BOT, BAR_H = 0.57, 0.26

A0, B0 = 1.5, 1.53125
C_EST = 1.515625  # midpoint of A0..B0, and the next bisection midpoint
ROOT = 1.5213797

W0 = B0 - A0  # 0.03125


def xp(x):
    return NL_LEFT + (x - X_VIEW0) * NL_SCALE


# ---------------------------------------------------------------------------
# Reusable visuals
# ---------------------------------------------------------------------------
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


def glow_dot(point, radius=0.055, halo_radius=0.17):
    halo = Circle(
        radius=halo_radius, stroke_width=0, fill_color=GLOW, fill_opacity=0.22
    ).move_to(point)
    core = Dot(point, radius=radius, color=WHITE)
    return VGroup(halo, core)


class BisectionConvergence(Scene):
    # -- pieces ------------------------------------------------------------
    def bar(self, a, b, color=CYAN, fill=0.20):
        return RoundedRectangle(
            width=(b - a) * NL_SCALE,
            height=BAR_H,
            corner_radius=BAR_H * 0.24,
            stroke_color=color,
            stroke_width=1.6,
            fill_color=color,
            fill_opacity=fill,
        ).move_to([xp((a + b) / 2), BAR_BOT + BAR_H / 2, 0])

    def bar_glow(self, a, b):
        return RoundedRectangle(
            width=(b - a) * NL_SCALE,
            height=BAR_H,
            corner_radius=BAR_H * 0.24,
            stroke_color=GLOW,
            stroke_width=16,
            stroke_opacity=0.16,
            fill_opacity=0,
        ).move_to([xp((a + b) / 2), BAR_BOT + BAR_H / 2, 0])

    def tick(self, x):
        post = Line(
            [xp(x), 0.36, 0], [xp(x), 0.90, 0], color=CYAN, stroke_width=3
        )
        dot = Dot([xp(x), AXIS_Y, 0], radius=0.035, color=WHITE)
        return VGroup(post, dot)

    def dim_line(self, a, b):
        line = Line([xp(a), -0.28, 0], [xp(b), -0.28, 0], color=SECONDARY, stroke_width=1.5)
        caps = VGroup(
            *[
                Line([xp(x), -0.37, 0], [xp(x), -0.19, 0], color=SECONDARY, stroke_width=1.5)
                for x in (a, b)
            ]
        )
        return VGroup(line, caps)

    def width_label(self, value, center_x=0.0):
        g = VGroup(
            txt("WIDTH", 14, MUTED),
            txt(value, 18, CYAN),
        ).arrange(RIGHT, buff=0.28)
        g.move_to([center_x, -0.58, 0])
        return g

    def midpoint_marker(self, x_val):
        tri = Triangle(stroke_width=0, fill_color=CYAN, fill_opacity=0.95)
        tri.scale(0.11).rotate(PI).move_to([xp(x_val), 0.95, 0])
        lab = txt(f"midpoint  {x_val:.6f}", 18, SECONDARY).move_to([xp(x_val), 1.20, 0])
        return VGroup(tri, lab)

    def send_msg(self, rows, run_time=0.7):
        new = VGroup(*rows)
        if len(new) == 1:
            new[0].move_to([0, 2.38, 0])
        else:
            new[0].move_to([0, 2.58, 0])
            new[1].move_to([0, 2.12, 0])
        if getattr(self, "_msg", None) is not None:
            self.play(FadeOut(self._msg, shift=UP * 0.05), run_time=run_time * 0.4)
        self.play(FadeIn(new, shift=DOWN * 0.05), run_time=run_time * 0.6)
        self._msg = new

    def clear_msg(self, run_time=0.5):
        if getattr(self, "_msg", None) is not None:
            self.play(FadeOut(self._msg, shift=UP * 0.05), run_time=run_time)
            self._msg = None

    # -- scene -------------------------------------------------------------
    def construct(self):
        self.camera.background_color = NAVY
        self._msg = None

        # ===================================================================
        # 1. Frame and the close-up line
        # ===================================================================
        grid = make_dot_grid()
        self.play(FadeIn(grid), run_time=0.5)

        head = txt("CONVERGENCE & ACCURACY", 24, WHITE, {"ACCURACY": CYAN})
        head.move_to([NL_LEFT + head.width / 2, 3.55, 0])
        head_func = txt("f(x) = x³ − x − 2", 24, WHITE, {"x³ − x − 2": CYAN})
        head_func.move_to([NL_RIGHT - head_func.width / 2, 3.55, 0])
        rule = Line([NL_LEFT, 3.18, 0], [NL_RIGHT, 3.18, 0], color=CYAN, stroke_width=2)
        rule.set_stroke(opacity=0.4)
        self.play(
            FadeIn(head, shift=DOWN * 0.05), FadeIn(head_func), Create(rule), run_time=0.8
        )

        axis = Line([NL_LEFT, AXIS_Y, 0], [NL_RIGHT, AXIS_Y, 0], color=AXIS, stroke_width=2.4)
        ticks = VGroup()
        for i in range(9):
            v = 1.495 + 0.005 * i
            major = i % 2 == 0
            ticks.add(
                Line(
                    [xp(v), AXIS_Y - (0.085 if major else 0.05), 0],
                    [xp(v), AXIS_Y + (0.085 if major else 0.05), 0],
                    color=AXIS,
                    stroke_width=1.8 if major else 1.3,
                    stroke_opacity=0.9 if major else 0.5,
                )
            )
        scale_labs = VGroup(
            *[
                txt(f"{v:g}", 13, MUTED).move_to([xp(v), 0.18, 0])
                for v in (1.50, 1.51, 1.52, 1.53)
            ]
        )
        self.play(Create(axis), FadeIn(ticks), FadeIn(scale_labs), run_time=0.9)
        self.wait(0.3)

        # ===================================================================
        # 2. Phase 1 - the bracket and its halving width
        # ===================================================================
        bar = self.bar(A0, B0)
        bar_glow = self.bar_glow(A0, B0)
        tick_a = self.tick(A0)
        tick_b = self.tick(B0)
        self.play(GrowFromCenter(bar), FadeIn(bar_glow), run_time=0.7)
        self.play(Create(tick_a), Create(tick_b), run_time=0.55)

        lab_a = txt(f"a = {A0:g}", 20, WHITE, {f"{A0:g}": CYAN})
        lab_a.move_to([xp(A0), 1.72, 0])
        lab_b = txt(f"b = {B0:g}", 20, WHITE, {f"{B0:g}": CYAN})
        lab_b.move_to([xp(B0), 1.72, 0])
        self.play(FadeIn(lab_a, shift=DOWN * 0.06), FadeIn(lab_b, shift=DOWN * 0.06), run_time=0.55)

        dim = self.dim_line(A0, B0)
        wlab = self.width_label("0.03125")
        self.play(Create(dim), FadeIn(wlab, shift=UP * 0.06), run_time=0.75)

        self.send_msg(
            [
                txt("EVERY ITERATION HALVES THE WIDTH", 13, MUTED),
                txt(
                    "0.5  →  0.25  →  0.125  →  0.0625  →  0.03125",
                    22,
                    SECONDARY,
                    {"0.03125": CYAN},
                ),
            ]
        )
        self.wait(1.7)

        # ===================================================================
        # 3. Phase 2 - where the error bound comes from
        # ===================================================================
        marker = self.midpoint_marker(C_EST)
        self.play(FadeIn(marker, shift=DOWN * 0.06), run_time=0.8)

        root_dot = glow_dot([xp(ROOT), AXIS_Y, 0], 0.06, 0.20)
        root_dash = DashedLine(
            [xp(ROOT), BAR_BOT + 0.01, 0],
            [xp(ROOT), BAR_BOT + BAR_H - 0.01, 0],
            dash_length=0.045,
            dashed_ratio=0.55,
            color=WHITE,
            stroke_width=2.2,
            stroke_opacity=1.0,
        )
        self.play(FadeIn(root_dot, scale=0.6), Create(root_dash), run_time=0.9)

        self.send_msg(
            [
                txt(
                    "ERROR  ≤  (b − a) / 2  =  0.015625",
                    26,
                    WHITE,
                    {"0.015625": CYAN},
                ),
                txt("the true root lies inside the bracket", 15, SECONDARY),
            ]
        )
        self.wait(2.8)

        # ===================================================================
        # 4. Phase 3 - one more iteration
        # ===================================================================
        marker_lab = txt(f"c = {C_EST:.6f}", 18, CYAN).move_to([xp(C_EST), 1.20, 0])
        self.play(FadeOut(marker[1]), FadeIn(marker_lab, shift=DOWN * 0.05), run_time=0.6)

        self.send_msg(
            [
                txt(
                    "c  =  (1.5 + 1.53125) / 2  =  1.515625",
                    24,
                    WHITE,
                    {"1.515625": CYAN},
                )
            ]
        )
        self.wait(1.4)

        self.send_msg(
            [
                txt("f(1.515625)  ≈  −0.0341  <  0", 26, WHITE, {"−0.0341": CYAN}),
                txt("negative, so the root lies to the right - keep that half", 15, SECONDARY),
            ]
        )
        self.wait(1.6)

        # The discarded left half greys out, then the bracket closes.
        gone = self.bar(A0, C_EST, color=MUTED, fill=0.10)
        gone.set_stroke(color=MUTED, opacity=0.55)
        self.play(FadeIn(gone), run_time=0.4)

        new_mid = (C_EST + B0) / 2
        lab_a2 = txt(f"a = {C_EST:.6f}", 20, WHITE, {f"{C_EST:.6f}": CYAN})
        lab_a2.move_to([xp(C_EST), 1.72, 0])
        wlab2 = self.width_label("0.015625", xp(new_mid))
        self.play(
            Transform(bar, self.bar(C_EST, B0)),
            Transform(bar_glow, self.bar_glow(C_EST, B0)),
            Transform(tick_a, self.tick(C_EST)),
            Transform(dim, self.dim_line(C_EST, B0)),
            FadeOut(gone),
            FadeOut(lab_a, shift=UP * 0.05),
            FadeIn(lab_a2, shift=DOWN * 0.05),
            FadeOut(wlab, shift=UP * 0.05),
            FadeIn(wlab2, shift=UP * 0.05),
            FadeOut(marker, shift=UP * 0.05),
            FadeOut(marker_lab, shift=UP * 0.05),
            run_time=0.9,
        )
        self.wait(2.8)

        # ===================================================================
        # 5. Phase 4 - tolerance and the stopping criterion
        # ===================================================================
        self.send_msg(
            [
                txt(
                    "MAX ERROR  ≤  0.015625 / 2  =  0.0078125",
                    24,
                    WHITE,
                    {"0.0078125": CYAN},
                )
            ]
        )
        self.wait(1.7)

        # Gauge: the error bound and the tolerance on one scale.
        gx0, k = -5.30, 400.0
        err, tol = 0.0078125, 0.01
        cap1 = txt("MAX ERROR  ≤  0.0078125", 14, MUTED)
        cap1.move_to([gx0 + cap1.width / 2, -1.50, 0])
        bar1 = RoundedRectangle(
            width=err * k, height=0.16, corner_radius=0.05,
            stroke_width=0, fill_color=CYAN, fill_opacity=0.85,
        ).move_to([gx0 + err * k / 2, -1.85, 0])
        val1 = txt("0.0078", 14, CYAN).move_to([gx0 + err * k + 0.45, -1.85, 0])
        cap2 = txt("TOLERANCE  ε = 0.01", 14, MUTED)
        cap2.move_to([gx0 + cap2.width / 2, -2.45, 0])
        bar2 = RoundedRectangle(
            width=tol * k, height=0.16, corner_radius=0.05,
            stroke_width=0, fill_color=SECONDARY, fill_opacity=0.55,
        ).move_to([gx0 + tol * k / 2, -2.75, 0])
        val2 = txt("0.01", 14, SECONDARY).move_to([gx0 + tol * k + 0.35, -2.75, 0])
        guide = DashedLine(
            [gx0 + tol * k, -1.55, 0], [gx0 + tol * k, -2.95, 0],
            dash_length=0.06, dashed_ratio=0.45, color=GLOW,
            stroke_width=1.5, stroke_opacity=0.55,
        )
        gauge = VGroup(cap1, cap2, bar1, bar2, val1, val2, guide)
        self.play(
            FadeIn(cap1), GrowFromEdge(bar1, LEFT), FadeIn(val1),
            FadeIn(cap2), GrowFromEdge(bar2, LEFT), FadeIn(val2),
            Create(guide),
            run_time=1.4,
        )
        self.wait(1.5)

        self.send_msg(
            [txt("0.0078125   <   0.01", 30, WHITE, {"0.0078125": CYAN, "0.01": GLOW})]
        )
        self.wait(1.3)

        # The verdict replaces the message strip.
        pill = RoundedRectangle(
            width=9.6, height=0.86, corner_radius=0.43,
            stroke_color=CYAN, stroke_width=2,
            fill_color=PANEL, fill_opacity=0.96,
        ).move_to([0, 2.46, 0])
        pill_glow = RoundedRectangle(
            width=9.6, height=0.86, corner_radius=0.43,
            stroke_color=GLOW, stroke_width=16, stroke_opacity=0.20, fill_opacity=0,
        ).move_to([0, 2.46, 0])
        banner = txt(
            "REQUIRED ACCURACY ACHIEVED", 28, WHITE, {"ACHIEVED": CYAN}
        ).move_to(pill)
        self.clear_msg(run_time=0.45)
        self.play(FadeIn(pill, scale=0.94), FadeIn(pill_glow), FadeIn(banner, scale=0.96), run_time=0.8)
        self.wait(2.3)

        # ===================================================================
        # 6. Phase 5 - keep going, then the closing statement
        # ===================================================================
        cont = txt("IF WE CONTINUED, THE BRACKET KEEPS CLOSING IN", 13, MUTED)
        cont.move_to([0, 2.38, 0])
        self.play(
            FadeOut(pill), FadeOut(pill_glow), FadeOut(banner, shift=UP * 0.05),
            FadeOut(gauge, shift=DOWN * 0.06),
            FadeOut(lab_a2, shift=UP * 0.05), FadeOut(lab_b, shift=UP * 0.05),
            FadeOut(wlab2, shift=UP * 0.05), FadeOut(dim, shift=UP * 0.05),
            run_time=0.6,
        )
        self.play(FadeIn(cont), run_time=0.4)

        # True bisection keeps shrinking toward the root.
        steps = [(C_EST, 1.5234375), (1.51953125, 1.5234375), (1.51953125, 1.521484375)]
        for a, b in steps:
            self.play(
                Transform(bar, self.bar(a, b)),
                Transform(bar_glow, self.bar_glow(a, b)),
                Transform(tick_a, self.tick(a)),
                Transform(tick_b, self.tick(b)),
                run_time=0.75,
            )
        self.play(root_dot.animate.scale(1.25).set_opacity(1), run_time=0.4)
        self.play(FadeOut(cont), run_time=0.4)

        closing = VGroup(
            txt("Smaller interval.", 34, WHITE, {"interval": CYAN}),
            txt("Smaller error.", 34, WHITE, {"error": CYAN}),
            txt("Better accuracy.", 34, WHITE, {"accuracy": CYAN}),
        )
        for row, y in zip(closing, [-1.55, -2.40, -3.25]):
            row.move_to([0, y, 0])
        self.play(
            LaggedStart(*[FadeIn(r, shift=UP * 0.08) for r in closing], lag_ratio=0.45),
            run_time=1.7,
        )
        # Manim's timeline runs ~0.18 s short of the nominal run-time sum, so
        # the tail leaves room for the full 1.1 s fade to land on navy.
        self.wait(5.4)

        self.play(FadeOut(Group(*self.mobjects), shift=UP * 0.3), run_time=1.1)
