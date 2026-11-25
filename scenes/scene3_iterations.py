"""
Scene 3 - The power of repetition.

Picks up where Scene 2 leaves off (bracket [1.5, 2]) and runs passes 2-5 with
the same graph on the left, a close-up number line underneath it, and the
calculation panel on the right.

Render:
    manim -ql scenes/scene3_iterations.py BisectionIterations
"""

import numpy as np
from manim import *

# ---------------------------------------------------------------------------
# Palette and typography (identical to scenes 1 and 2)
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
# Geometry: graph on the upper left, close-up number line underneath
# ---------------------------------------------------------------------------
X_MIN, X_MAX = -0.5, 2.5
Y_MIN, Y_MAX = -2.8, 5.6
G_LEFT, G_RIGHT = -6.85, -0.85
G_BOTTOM, G_TOP = -0.25, 2.65
G_XSCALE = (G_RIGHT - G_LEFT) / (X_MAX - X_MIN)  # 2.0 units per x
G_YSCALE = (G_TOP - G_BOTTOM) / (Y_MAX - Y_MIN)
Y_AXIS = G_BOTTOM - Y_MIN * G_YSCALE  # screen y of f(x) = 0: 0.717

NL_Y = -2.15
NL_A, NL_B = 1.45, 2.05
NL_SCALE = 10.0  # screen units per x on the close-up line

ROOT = 1.52138

# bracket before the pass, midpoint, f(midpoint); widths after each pass live in
# WIDTH_HISTORY (index i = width once the bracket has closed i times)
PASSES = [
    dict(k=2, a=1.5, b=2.0, c=1.75, f="1.609375", sign="="),
    dict(k=3, a=1.5, b=1.75, c=1.625, f="0.666016", sign="≈"),
    dict(k=4, a=1.5, b=1.625, c=1.5625, f="0.252197", sign="≈"),
    dict(k=5, a=1.5, b=1.5625, c=1.53125, f="0.059113", sign="≈"),
]

WIDTH_HISTORY = ["0.500", "0.250", "0.125", "0.0625", "0.0313"]
BRACKET_HISTORY = [(1.5, 2.0), (1.5, 1.75), (1.5, 1.625), (1.5, 1.5625), (1.5, 1.53125)]


def f(x):
    return x**3 - x - 2


def g(value):
    return f"{value:g}"


def gx(x):
    return G_LEFT + (x - X_MIN) * G_XSCALE


def gy(value):
    return G_BOTTOM + (value - Y_MIN) * G_YSCALE


def nlx(x):
    return -6.85 + (x - NL_A) * NL_SCALE


# ---------------------------------------------------------------------------
# Reusable visuals
# ---------------------------------------------------------------------------
def txt(string, size, color=WHITE, highlights=None, slant=NORMAL):
    # Manim's Pango layout miscounts glyph advances at small font sizes
    # (e.g. "passes" renders as "p asses" at 15pt), so lay the text out large
    # and scale it down; the paths are identical, the spacing is correct.
    factor = max(1, -(-60 // int(size)))
    t = Text(
        string, font=FONT, weight=BOLD, font_size=size * factor, color=color, slant=slant
    )
    if highlights:
        t.set_color_by_t2c(highlights)
    return t.scale(1 / factor)


def make_card(width, height, corner_radius=0.18):
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
        stroke_color=PANEL_EDGE,
        stroke_width=1.4,
        fill_color=PANEL,
        fill_opacity=0.94,
    )
    return VGroup(shadow, face), face


def make_dot_grid(spacing=1.0, radius=0.013):
    dots = VGroup()
    for x in np.arange(-6.5, 7.0, spacing):
        for y in np.arange(-3.5, 4.0, spacing):
            dots.add(Dot([x, y, 0], radius=radius, color=GRID_DOT, fill_opacity=0.45))
    return dots


def glow_dot(point, radius=0.055, halo_radius=0.16):
    halo = Circle(
        radius=halo_radius, stroke_width=0, fill_color=GLOW, fill_opacity=0.22
    ).move_to(point)
    core = Dot(point, radius=radius, color=WHITE)
    return VGroup(halo, core)


class BisectionIterations(Scene):
    # -- graph-side helpers ------------------------------------------------
    def band(self, a, b):
        return Rectangle(
            width=(b - a) * G_XSCALE,
            height=G_TOP - G_BOTTOM,
            stroke_width=0,
            fill_color=CYAN,
            fill_opacity=0.075,
        ).move_to([gx((a + b) / 2), (G_TOP + G_BOTTOM) / 2, 0])

    def bracket(self, a, b):
        return Line(
            [gx(a), Y_AXIS, 0], [gx(b), Y_AXIS, 0], color=CYAN, stroke_width=8
        )

    def bracket_glow(self, a, b):
        return Line(
            [gx(a), Y_AXIS, 0],
            [gx(b), Y_AXIS, 0],
            color=GLOW,
            stroke_width=20,
            stroke_opacity=0.22,
        )

    def midpoint_marker(self, c):
        x = gx(c)
        top = gy(f(c)) - 0.04
        dash = DashedLine(
            [x, Y_AXIS + 0.04, 0],
            [x, top, 0],
            dash_length=0.05,
            dashed_ratio=0.45,
            color=CYAN,
            stroke_width=2.0,
            stroke_opacity=0.8,
        )
        dot = glow_dot([x, top, 0], 0.05, 0.15)
        tick = Line([x, Y_AXIS - 0.10, 0], [x, Y_AXIS + 0.10, 0], color=WHITE, stroke_width=2)
        return VGroup(dash, dot, tick)

    # -- number-line helper -------------------------------------------------
    def nl_bar(self, a, b, color=CYAN, width=11):
        return Line([nlx(a), NL_Y, 0], [nlx(b), NL_Y, 0], color=color, stroke_width=width)

    # -- panel rows ---------------------------------------------------------
    def pass_block(self, it):
        c = it["c"]
        hdr = txt(f"ITERATION {it['k']} OF 5", 16, CYAN).move_to([4.05, 1.50, 0])
        sub = txt(f"c = ({g(it['a'])} + {g(it['b'])}) / 2", 24, SECONDARY).move_to(
            [4.05, 1.00, 0]
        )
        crow = txt(f"c = {g(c)}", 38, WHITE, {g(c): CYAN}).move_to([4.05, 0.45, 0])
        frow = txt(
            f"f({g(c)}) {it['sign']} {it['f']}  >  0", 22, WHITE, {">  0": CYAN}
        ).move_to([4.05, -0.25, 0])
        note = txt("positive, so the root lies to the left", 17, SECONDARY).move_to(
            [4.05, -0.77, 0]
        )
        split = Line([2.85, -1.17, 0], [5.25, -1.17, 0], color=PANEL_EDGE, stroke_width=1.2)
        lab = txt("NEW INTERVAL", 13, MUTED).move_to([4.05, -1.47, 0])
        interval = txt(f"[{g(it['a'])}, {g(c)}]", 34, CYAN).move_to([4.05, -2.05, 0])
        return VGroup(hdr, sub, crow, frow, note, split, lab, interval)

    def construct(self):
        self.camera.background_color = NAVY

        # ===================================================================
        # 1. Frame: grid, header, graph
        # ===================================================================
        grid = make_dot_grid()
        self.play(FadeIn(grid), run_time=0.55)

        head = txt("THE POWER OF REPETITION", 24, WHITE, {"REPETITION": CYAN})
        head.move_to([G_LEFT + head.width / 2, 3.55, 0])
        head_func = txt("f(x) = x³ − x − 2", 24, WHITE, {"x³ − x − 2": CYAN})
        head_func.move_to([6.85 - head_func.width / 2, 3.55, 0])
        rule = Line([-6.85, 3.18, 0], [6.85, 3.18, 0], color=CYAN, stroke_width=2)
        rule.set_stroke(opacity=0.4)
        self.play(FadeIn(head, shift=DOWN * 0.05), FadeIn(head_func), Create(rule), run_time=0.85)

        axes = Axes(
            x_range=[X_MIN, X_MAX, 0.5],
            y_range=[Y_MIN, Y_MAX, 2],
            x_length=G_RIGHT - G_LEFT,
            y_length=G_TOP - G_BOTTOM,
            axis_config={
                "color": AXIS,
                "stroke_width": 2.6,
                "tick_size": 0.07,
                "tip_width": 0.16,
                "tip_height": 0.16,
                "include_numbers": False,
            },
        ).move_to([(G_LEFT + G_RIGHT) / 2, (G_TOP + G_BOTTOM) / 2, 0])

        x_lab = txt("x", 22, WHITE, slant=ITALIC).next_to(axes.x_axis.get_end(), RIGHT, buff=0.12)
        y_lab = txt("y", 22, WHITE, slant=ITALIC).next_to(axes.y_axis.get_end(), UP, buff=0.10)
        self.play(Create(axes), run_time=0.9)
        self.play(FadeIn(x_lab), FadeIn(y_lab), run_time=0.35)

        curve = axes.plot(f, x_range=[-0.45, 2.05], stroke_width=4.5, use_smoothing=True)
        curve.set_color_by_gradient(CYAN, BLUE)
        curve_glow = axes.plot(f, x_range=[-0.45, 2.05], color=GLOW)
        curve_glow.set_stroke(width=12, opacity=0.13)
        self.play(Create(curve_glow), Create(curve), run_time=1.15)
        self.add(axes, x_lab, y_lab, curve_glow, curve)

        # ===================================================================
        # 2. Current bracket [1.5, 2] on the graph and on the close-up line
        # ===================================================================
        band = self.band(1.5, 2.0)
        gbar_glow = self.bracket_glow(1.5, 2.0)
        gbar = self.bracket(1.5, 2.0)
        dot_a = Dot([gx(1.5), Y_AXIS, 0], radius=0.05, color=WHITE)
        dot_b = Dot([gx(2.0), Y_AXIS, 0], radius=0.05, color=WHITE)
        self.play(FadeIn(band), Create(gbar_glow), Create(gbar), FadeIn(dot_a), FadeIn(dot_b), run_time=0.7)

        nl_axis = Line([nlx(NL_A), NL_Y, 0], [nlx(NL_B), NL_Y, 0], color=AXIS, stroke_width=2.4)
        ticks = VGroup()
        labels = VGroup()
        for i in range(13):
            v = NL_A + 0.05 * i
            major = i % 2 == 1  # labels land on 1.5, 1.6, ... 2.0
            ticks.add(
                Line(
                    [nlx(v), NL_Y - (0.055 if major else 0.035), 0],
                    [nlx(v), NL_Y + (0.055 if major else 0.035), 0],
                    color=AXIS,
                    stroke_width=1.6 if major else 1.1,
                    stroke_opacity=0.9 if major else 0.5,
                )
            )
            if major:
                labels.add(txt(f"{v:g}", 15, MUTED).move_to([nlx(v), NL_Y - 0.27, 0]))

        root_tick = Line(
            [nlx(ROOT), NL_Y - 0.14, 0], [nlx(ROOT), NL_Y - 0.02, 0],
            color=GLOW, stroke_width=2.6,
        )
        caption = txt("CLOSE-UP  ·  THE SEARCH INTERVAL", 14, MUTED).move_to([-3.85, -0.62, 0])

        nl_bar_glow = self.nl_bar(1.5, 2.0, color=GLOW, width=24)
        nl_bar_glow.set_stroke(opacity=0.18)
        nl_bar = self.nl_bar(1.5, 2.0)
        nl_dot_a = Dot([nlx(1.5), NL_Y, 0], radius=0.042, color=WHITE)
        nl_dot_b = Dot([nlx(2.0), NL_Y, 0], radius=0.042, color=WHITE)
        width_label = txt("WIDTH", 18, MUTED).move_to([-4.30, -2.92, 0])
        width_val = txt("0.500", 18, CYAN)
        width_val.next_to(width_label, RIGHT, buff=0.22)

        self.play(
            Create(nl_axis),
            FadeIn(ticks),
            FadeIn(labels),
            FadeIn(root_tick),
            Create(nl_bar_glow),
            Create(nl_bar),
            FadeIn(nl_dot_a),
            FadeIn(nl_dot_b),
            FadeIn(caption),
            FadeIn(width_label),
            FadeIn(width_val),
            run_time=0.8,
        )
        self.wait(0.4)

        # ===================================================================
        # 3. Panel: where we are and the midpoint rule
        # ===================================================================
        card, face = make_card(5.3, 5.05, 0.18)
        card.move_to([4.05, -0.35, 0])

        prelude = VGroup(
            txt("AFTER ONE PASS", 15, MUTED),
            txt("[1.5,  2]", 38, CYAN),
            Line([0, 0, 0], [2.6, 0, 0], color=PANEL_EDGE, stroke_width=1.2),
            txt("NEXT MIDPOINT", 15, CYAN),
            txt("c = (a + b) / 2", 32, WHITE),
            txt("each pass halves the bracket", 17, SECONDARY),
        )
        for row, y in zip(prelude, [1.45, 0.95, 0.35, -0.05, -0.60, -1.55]):
            row.move_to([4.05, y, 0])

        pills = VGroup(
            *[
                RoundedRectangle(
                    width=1.05, height=0.06, corner_radius=0.03,
                    stroke_width=0, fill_color=PANEL_EDGE, fill_opacity=0.75,
                )
                for _ in range(4)
            ]
        ).arrange(RIGHT, buff=0.1).move_to([4.05, 1.93, 0])

        self.play(FadeIn(card, shift=UP * 0.08), FadeIn(pills), run_time=0.7)
        self.play(
            FadeIn(prelude[0]),
            FadeIn(prelude[1], shift=UP * 0.08),
            Create(prelude[2]),
            FadeIn(prelude[3]),
            FadeIn(prelude[4], shift=UP * 0.08),
            FadeIn(prelude[5]),
            run_time=0.9,
        )
        self.wait(0.8)

        # ===================================================================
        # 4. Passes 2-5
        # ===================================================================
        marker = None
        discard = None
        prev_block = None
        for idx, it in enumerate(PASSES):
            block = self.pass_block(it)
            a, b, c = it["a"], it["b"], it["c"]
            new_marker = self.midpoint_marker(c)

            if idx == 0:
                self.play(FadeOut(prelude, shift=UP * 0.05), run_time=0.35)
            else:
                self.play(FadeOut(prev_block, shift=UP * 0.05), run_time=0.35)

            self.play(
                FadeIn(block[0]),
                FadeIn(block[1]),
                pills[idx].animate.set_fill(CYAN),
                run_time=0.45,
            )

            if marker is None:
                self.play(FadeIn(new_marker), FadeIn(block[2]), run_time=0.65)
                marker = new_marker
            else:
                self.play(Transform(marker, new_marker), FadeIn(block[2]), run_time=0.7)

            self.play(FadeIn(block[3]), run_time=0.4)
            self.play(FadeIn(block[4]), run_time=0.35)

            # The discarded right half greys out and the bracket closes.
            new_discard = self.nl_bar(c, 2.0, color="#5D6B85", width=7)
            new_width = txt(WIDTH_HISTORY[idx + 1], 18, CYAN)
            new_width.next_to(width_label, RIGHT, buff=0.22)

            close_anims = [
                Transform(nl_bar, self.nl_bar(a, c)),
                Transform(nl_bar_glow, self.nl_bar(a, c, color=GLOW, width=24)),
                Transform(nl_dot_b, Dot([nlx(c), NL_Y, 0], radius=0.05, color=WHITE)),
                Transform(band, self.band(a, c)),
                Transform(gbar, self.bracket(a, c)),
                Transform(gbar_glow, self.bracket_glow(a, c)),
                Transform(dot_b, Dot([gx(c), Y_AXIS, 0], radius=0.05, color=WHITE)),
                Transform(width_val, new_width),
            ]
            if discard is None:
                discard = new_discard
                close_anims.append(FadeIn(discard))
            else:
                close_anims.append(Transform(discard, new_discard))
            self.play(*close_anims, run_time=0.85)

            self.play(nl_bar_glow.animate.set_stroke(opacity=0.42), run_time=0.25)
            self.play(nl_bar_glow.animate.set_stroke(opacity=0.18), run_time=0.35)

            self.play(FadeIn(block[5]), FadeIn(block[6]), FadeIn(block[7], scale=1.06), run_time=0.45)
            self.wait(2.6)

            prev_block = block

        # ===================================================================
        # 5. Closing: halving widths
        # ===================================================================
        closing = VGroup(
            txt("THE PATTERN", 15, CYAN),
            txt("Each iteration", 30, WHITE),
            txt("halves the interval.", 30, WHITE, {"halves": CYAN}),
            Line([0, 0, 0], [2.4, 0, 0], color=PANEL_EDGE, stroke_width=1.2),
            txt("after 5 passes", 15, MUTED),
            txt("width  0.0313", 32, WHITE, {"0.0313": CYAN}),
            txt("the root, 1.521, is still inside", 16, SECONDARY),
        )
        for row, y in zip(closing, [1.45, 0.92, 0.46, -0.15, -0.75, -1.30, -2.05]):
            row.move_to([4.05, y, 0])

        self.play(FadeOut(prev_block, shift=UP * 0.05), run_time=0.35)
        self.play(
            FadeIn(closing[0]),
            FadeIn(closing[1], shift=UP * 0.06),
            FadeIn(closing[2], shift=UP * 0.06),
            Create(closing[3]),
            FadeIn(closing[4]),
            FadeIn(closing[5], shift=UP * 0.06),
            FadeIn(closing[6]),
            run_time=1.0,
        )

        # The single bracket is replaced by the nested history of brackets.
        chart = VGroup()
        for i, (a, bb) in enumerate(BRACKET_HISTORY):
            y = -0.86 - 0.26 * i
            bar = Line([nlx(a), y, 0], [nlx(bb), y, 0],
                       color=CYAN if i == len(BRACKET_HISTORY) - 1 else BLUE,
                       stroke_width=7)
            end_dot = Dot([nlx(bb), y, 0], radius=0.045, color=CYAN if i == 4 else SECONDARY)
            idx_lab = txt(str(i + 1), 13, MUTED).move_to([nlx(a) - 0.22, y, 0])
            val = txt(WIDTH_HISTORY[i], 13, CYAN if i == 4 else SECONDARY)
            val.move_to([-0.62 - val.width / 2, y, 0])
            chart.add(VGroup(bar, end_dot, idx_lab, val))

        chart_caption = txt("WIDTHS AFTER EACH PASS", 14, MUTED).move_to([-3.85, -0.62, 0])
        self.play(
            FadeOut(nl_bar, shift=UP * 0.05),
            FadeOut(nl_bar_glow),
            FadeOut(nl_dot_b),
            FadeOut(discard),
            FadeOut(width_label),
            FadeOut(width_val),
            FadeOut(caption, shift=UP * 0.10),
            FadeIn(chart_caption, shift=UP * 0.10),
            run_time=0.6,
        )
        self.play(
            LaggedStart(*[FadeIn(row, shift=RIGHT * 0.12) for row in chart], lag_ratio=0.22),
            run_time=2.0,
        )
        self.wait(5.0)

        self.play(FadeOut(Group(*self.mobjects), shift=UP * 0.3), run_time=1.2)
