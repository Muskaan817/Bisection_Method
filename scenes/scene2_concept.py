"""
Scene 2 — Understanding the Bisection Method (four-phase edition).

Phase 1  A full-screen graph introduces f(x) = x^3 - x - 2, the bracket
         [1, 2] and the root at x ~ 1.52138.
Phase 2  The very same graph scales down and slides to the left; a wide
         explanation panel opens on the right.
Phase 3  The four calculation steps appear one at a time inside the panel.
Phase 4  The graph reacts: the midpoint drop, the sign test and the
         discarded / retained halves.

All typography is Pango Text in Helvetica Neue Bold, so no LaTeX install
is required.

Render:
    manim -ql scenes/scene2_concept.py BisectionConcept
    manim -qh scenes/scene2_concept.py BisectionConcept
"""

import numpy as np
from manim import *

# ---------------------------------------------------------------------------
# Palette / typography
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

# Helvetica Neue Bold lays out cleanly in Manim's Pango renderer.
FONT = "Helvetica Neue"

config.background_color = NAVY


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def f(x):
    return x**3 - x - 2


def txt(string, size, color=WHITE, highlights=None, slant=NORMAL):
    """Bold Pango text with optional colour highlights on exact substrings."""
    return Text(
        string,
        font=FONT,
        weight=BOLD,
        font_size=size,
        color=color,
        t2c=highlights or {},
        slant=slant,
    )


def make_card(width, height, corner_radius=0.18):
    shadow = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=corner_radius,
        stroke_width=0,
        fill_color=PANEL_SHADOW,
        fill_opacity=0.9,
    ).shift([0.08, -0.1, 0])
    face = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=corner_radius,
        stroke_color=PANEL_EDGE,
        stroke_width=1.8,
        stroke_opacity=0.8,
        fill_color=PANEL,
        fill_opacity=0.96,
    )
    return VGroup(shadow, face), face


def make_dot_grid(spacing=1.0, radius=0.014):
    dots = VGroup()
    for x in np.arange(-6.5, 7.0, spacing):
        for y in np.arange(-3.5, 4.0, spacing):
            dots.add(
                Dot([x, y, 0], radius=radius, color=GRID_DOT, fill_opacity=0.45)
            )
    return dots


def glow_dot(point, radius=0.07, halo_radius=0.2):
    halo = Circle(
        radius=halo_radius,
        stroke_width=0,
        fill_color=GLOW,
        fill_opacity=0.22,
    ).move_to(point)
    core = Dot(point, radius=radius, color=WHITE)
    return VGroup(halo, core)


# ---------------------------------------------------------------------------
# Scene
# ---------------------------------------------------------------------------
class BisectionConcept(Scene):
    def construct(self):
        self.camera.background_color = NAVY

        grid = make_dot_grid()
        self.play(FadeIn(grid), run_time=0.6)

        # ===================================================================
        # PHASE 1 — full-screen graph introduction
        # ===================================================================
        title = txt(
            "UNDERSTANDING THE BISECTION METHOD",
            40,
            WHITE,
            {"BISECTION METHOD": CYAN},
        )
        title.move_to([0, 3.35, 0])

        title_shadow = title.copy().set_fill("#12365F", opacity=0.55)
        title_shadow.set_stroke(width=0)
        title_shadow.shift([0.07, -0.09, 0])

        func = txt("f(x) = x³ − x − 2", 30, WHITE, {"x³ − x − 2": CYAN})
        func.move_to([0, 2.62, 0])

        self.play(
            FadeIn(title_shadow),
            AddTextLetterByLetter(title, run_time=1.4),
        )
        self.play(FadeIn(func, shift=DOWN * 0.06), run_time=0.7)
        self.wait(0.5)

        # ---- the graph itself --------------------------------------------
        axes = Axes(
            x_range=[-0.5, 2.5, 0.5],
            y_range=[-2.8, 5.6, 2],
            x_length=8.8,
            y_length=5.0,
            axis_config={
                "color": AXIS,
                "stroke_width": 3,
                "tick_size": 0.08,
                "tip_width": 0.22,
                "tip_height": 0.22,
                "include_numbers": False,
            },
        ).move_to([0, -0.55, 0])

        x_lab = txt("x", 26, WHITE, slant=ITALIC)
        x_lab.next_to(axes.x_axis.get_end(), RIGHT, buff=0.14)
        y_lab = txt("y", 26, WHITE, slant=ITALIC)
        y_lab.next_to(axes.y_axis.get_end(), UP, buff=0.12)

        curve = axes.plot(
            f, x_range=[-0.45, 2.13], stroke_width=5, use_smoothing=True
        )
        curve.set_color_by_gradient(CYAN, BLUE)
        curve_glow = axes.plot(
            f, x_range=[-0.45, 2.13], color=GLOW, use_smoothing=True
        )
        curve_glow.set_stroke(width=14, opacity=0.12)

        self.play(Create(axes), run_time=0.9)
        self.play(FadeIn(VGroup(x_lab, y_lab)), run_time=0.4)
        self.play(
            Create(curve_glow), Create(curve), run_time=1.3, rate_func=smooth
        )

        # ---- bracket [1, 2] on the axis ----------------------------------
        a_pt = axes.c2p(1, 0)
        mid_pt = axes.c2p(1.5, 0)
        b_pt = axes.c2p(2, 0)

        bar_glow_l = Line(a_pt, mid_pt, color=GLOW)
        bar_glow_l.set_stroke(width=24, opacity=0.25)
        bar_glow_r = Line(mid_pt, b_pt, color=GLOW)
        bar_glow_r.set_stroke(width=24, opacity=0.25)
        bar_l = Line(a_pt, mid_pt, color=CYAN, stroke_width=9)
        bar_r = Line(mid_pt, b_pt, color=CYAN, stroke_width=9)
        dot_a = Dot(a_pt, radius=0.06, color=WHITE)
        dot_b = Dot(b_pt, radius=0.06, color=WHITE)

        n1 = txt("1", 24, WHITE)
        n1.move_to(a_pt + DOWN * 0.42 + LEFT * 0.17)
        n2 = txt("2", 24, WHITE)
        n2.move_to(b_pt + DOWN * 0.42 + LEFT * 0.17)

        self.play(
            FadeIn(bar_glow_l),
            FadeIn(bar_glow_r),
            FadeIn(bar_l),
            FadeIn(bar_r),
            FadeIn(dot_a),
            FadeIn(dot_b),
            FadeIn(n1),
            FadeIn(n2),
            run_time=0.8,
        )

        # ---- endpoint evaluations with callout lines ---------------------
        p1 = axes.c2p(1, f(1))
        p2 = axes.c2p(2, f(2))

        guide1 = DashedLine(
            axes.c2p(1, -0.08),
            axes.c2p(1, -1.85),
            dash_length=0.07,
            color=CYAN,
            stroke_width=1.6,
            stroke_opacity=0.45,
        )
        guide2 = DashedLine(
            axes.c2p(2, 0.1),
            axes.c2p(2, 3.8),
            dash_length=0.07,
            color=CYAN,
            stroke_width=1.6,
            stroke_opacity=0.45,
        )
        dot1 = glow_dot(p1, radius=0.075, halo_radius=0.2)
        dot2 = glow_dot(p2, radius=0.075, halo_radius=0.2)

        lab1 = txt("f(1) = −2", 26, WHITE, {"−2": CYAN})
        lab1.move_to([-1.35, -3.45, 0])
        lead1 = Line(
            p1 + DOWN * 0.12,
            lab1.get_right() + UP * 0.02,
            color=CYAN,
            stroke_width=1.3,
        )
        lead1.set_stroke(opacity=0.55)

        lab2 = txt("f(2) = +4", 26, WHITE, {"+4": CYAN})
        lab2.move_to([4.3, 1.33, 0])
        lead2 = Line(
            p2 + RIGHT * 0.12,
            lab2.get_left() + UP * 0.02,
            color=CYAN,
            stroke_width=1.3,
        )
        lead2.set_stroke(opacity=0.55)

        self.play(
            Create(guide1),
            Create(guide2),
            FadeIn(dot1, scale=0.5),
            FadeIn(dot2, scale=0.5),
            run_time=0.7,
        )
        self.play(
            FadeIn(lab1, shift=UP * 0.05),
            FadeIn(lab2, shift=DOWN * 0.05),
            Create(lead1),
            Create(lead2),
            run_time=0.9,
        )

        # ---- the root ----------------------------------------------------
        root_pt = axes.c2p(1.52138, 0)
        root_halo = Circle(
            radius=0.2, stroke_width=0, fill_color=GLOW, fill_opacity=0.28
        ).move_to(root_pt)
        root_ring = Circle(radius=0.11, color=CYAN, stroke_width=2.5)
        root_ring.move_to(root_pt)
        root_lab = txt("root ≈ 1.521", 24, WHITE, {"1.521": CYAN})
        root_lab.move_to([2.45, -2.3, 0])
        root_lead = Line(
            root_pt + DOWN * 0.1 + RIGHT * 0.04,
            [1.9, -2.17, 0],
            color=CYAN,
            stroke_width=1.3,
        )
        root_lead.set_stroke(opacity=0.55)

        self.play(
            FadeIn(root_halo, scale=0.6),
            Create(root_ring),
            FadeIn(root_lab, shift=UP * 0.05),
            Create(root_lead),
            run_time=0.9,
        )
        self.wait(3.2)

        # ===================================================================
        # PHASE 2 — the same graph shrinks and slides left
        # ===================================================================
        header_title = txt(
            "UNDERSTANDING THE BISECTION METHOD",
            26,
            WHITE,
            {"BISECTION METHOD": CYAN},
        )
        header_title.move_to([-6.8, 3.5, 0], aligned_edge=LEFT)

        header_func = txt("f(x) = x³ − x − 2", 24, WHITE, {"x³ − x − 2": CYAN})
        header_func.move_to([6.8, 3.5, 0], aligned_edge=RIGHT)

        header_rule = Line(
            [-6.8, 3.15, 0], [6.8, 3.15, 0], color=CYAN, stroke_width=2
        )
        header_rule.set_stroke(opacity=0.4)

        callouts = VGroup(
            lab1, lead1, lab2, lead2, root_lab, root_lead,
            root_halo, root_ring, n1, n2, guide1, guide2, dot1, dot2,
        )
        self.play(
            FadeOut(callouts),
            FadeOut(title_shadow),
            FadeOut(title, shift=UP * 0.06),
            FadeOut(func, shift=UP * 0.06),
            run_time=0.6,
        )

        graph = Group(
            axes, x_lab, y_lab, curve, curve_glow,
            bar_glow_l, bar_l, bar_glow_r, bar_r, dot_a, dot_b,
        )
        SCALE = 0.72
        graph.generate_target()
        graph.target.scale(SCALE, about_point=[0, -0.55, 0])
        graph.target.shift([-3.6, 0, 0])

        self.play(
            MoveToTarget(graph),
            FadeIn(header_title, shift=DOWN * 0.06),
            FadeIn(header_func, shift=DOWN * 0.06),
            Create(header_rule),
            run_time=1.7,
        )

        # ===================================================================
        # PHASE 3 — sequential explanation panel
        # ===================================================================
        panel, panel_face = make_card(5.9, 4.3, 0.18)
        panel.move_to([3.85, -0.6, 0])

        def step_badge(n):
            return txt(f"STEP {n} OF 4", 20, CYAN).move_to([3.85, 1.24, 0])

        def step_head(name):
            return txt(name, 32, WHITE).move_to([3.85, 0.82, 0])

        def step_body(lines, note):
            block = VGroup(*lines).arrange(DOWN, buff=0.34)
            block.move_to([3.85, -0.72, 0])
            note_t = txt(note, 20, SECONDARY).move_to([3.85, -2.3, 0])
            return block, note_t

        segs = VGroup()
        for _ in range(4):
            segs.add(
                RoundedRectangle(
                    width=1.22,
                    height=0.07,
                    corner_radius=0.035,
                    stroke_width=0,
                    fill_color=PANEL_EDGE,
                    fill_opacity=1.0,
                )
            )
        segs.arrange(RIGHT, buff=0.12).move_to([3.85, 0.44, 0])
        segs[0].set_fill(CYAN)

        divider = Line(
            [1.35, -1.98, 0], [6.35, -1.98, 0], color=PANEL_EDGE, stroke_width=1.2
        )
        divider.set_stroke(opacity=0.7)

        # ---- STEP 1 — initial interval -----------------------------------
        badge = step_badge(1)
        head = step_head("INITIAL INTERVAL")
        block, note = step_body(
            [
                txt("[a, b] = [1, 2]", 38, WHITE, {"[1, 2]": CYAN}),
                txt("f(1) = −2", 32, WHITE, {"−2": CYAN}),
                txt("f(2) = +4", 32, WHITE, {"+4": CYAN}),
            ],
            "Opposite signs: the root is inside.",
        )

        self.play(FadeIn(panel, shift=UP * 0.1), run_time=0.6)
        self.play(
            FadeIn(badge, shift=DOWN * 0.05),
            FadeIn(head, shift=DOWN * 0.05),
            FadeIn(segs),
            FadeIn(divider),
            FadeIn(block, shift=UP * 0.06),
            FadeIn(note),
            run_time=0.8,
        )

        la = txt("a = 1", 22, WHITE, {"1": CYAN})
        la.move_to(axes.c2p(1, 0) + UP * 0.32)
        lb = txt("b = 2", 22, WHITE, {"2": CYAN})
        lb.move_to(axes.c2p(2, 0) + UP * 0.32)
        self.play(
            FadeIn(la, shift=UP * 0.05),
            FadeIn(lb, shift=UP * 0.05),
            run_time=0.6,
        )
        self.wait(2.6)

        # ---- STEP 2 — midpoint --------------------------------------------
        badge2 = step_badge(2)
        head2 = step_head("CALCULATE MIDPOINT")
        block2, note2 = step_body(
            [
                txt("c = (a + b) / 2", 32, WHITE),
                txt("c = (1 + 2) / 2", 28, WHITE),
                txt("c = 1.5", 44, CYAN),
            ],
            "Halfway between the endpoints.",
        )
        self.play(
            FadeOut(badge, shift=UP * 0.05),
            FadeOut(head, shift=UP * 0.05),
            FadeOut(block, shift=UP * 0.05),
            FadeOut(note),
            run_time=0.3,
        )
        self.play(
            FadeIn(badge2, shift=DOWN * 0.05),
            FadeIn(head2, shift=DOWN * 0.05),
            FadeIn(block2, shift=UP * 0.05),
            FadeIn(note2),
            segs[0].animate.set_fill(PANEL_EDGE),
            segs[1].animate.set_fill(CYAN),
            run_time=0.45,
        )

        c_line = DashedLine(
            axes.c2p(1.5, 1.52),
            axes.c2p(1.5, -1.75),
            dash_length=0.08,
            color=CYAN,
            stroke_width=2,
        )
        c_lab = txt("c = 1.5", 24, WHITE, {"1.5": CYAN})
        c_lab.move_to([-2.83, -0.28, 0])
        c_dot = glow_dot(axes.c2p(1.5, f(1.5)), radius=0.06, halo_radius=0.17)

        self.play(
            Create(c_line),
            FadeIn(c_lab, shift=UP * 0.05),
            FadeIn(c_dot, scale=0.5),
            run_time=0.9,
        )
        self.wait(2.4)

        # ---- STEP 3 — midpoint value --------------------------------------
        badge3 = step_badge(3)
        head3 = step_head("EVALUATE MIDPOINT")
        block3, note3 = step_body(
            [
                txt("f(1.5) = 1.5³ − 1.5 − 2", 26, WHITE),
                txt("= 3.375 − 1.5 − 2", 26, WHITE),
                txt("= −0.125", 44, CYAN),
            ],
            "Negative — the root is still ahead.",
        )
        self.play(
            FadeOut(badge2, shift=UP * 0.05),
            FadeOut(head2, shift=UP * 0.05),
            FadeOut(block2, shift=UP * 0.05),
            FadeOut(note2),
            run_time=0.3,
        )
        self.play(
            FadeIn(badge3, shift=DOWN * 0.05),
            FadeIn(head3, shift=DOWN * 0.05),
            FadeIn(block3, shift=UP * 0.05),
            FadeIn(note3),
            segs[1].animate.set_fill(PANEL_EDGE),
            segs[2].animate.set_fill(CYAN),
            run_time=0.45,
        )

        mid_lab = txt("f(1.5) = −0.125", 20, WHITE, {"−0.125": CYAN})
        mid_lab.move_to([-2.05, -2.18, 0])
        self.play(FadeIn(mid_lab, shift=UP * 0.05), run_time=0.7)
        self.wait(2.6)

        # ---- STEP 4 — choose the half -------------------------------------
        badge4 = step_badge(4)
        head4 = step_head("CHOOSE THE INTERVAL")
        block4, note4 = step_body(
            [
                txt(
                    "f(1.5) < 0 and f(2) > 0",
                    28,
                    WHITE,
                    {"< 0": CYAN, "> 0": CYAN},
                ),
                txt("Therefore, the new interval is", 22, WHITE),
                txt("[1.5, 2]", 46, CYAN),
            ],
            "Root ≈ 1.521 remains inside.",
        )
        self.play(
            FadeOut(badge3, shift=UP * 0.05),
            FadeOut(head3, shift=UP * 0.05),
            FadeOut(block3, shift=UP * 0.05),
            FadeOut(note3),
            run_time=0.3,
        )
        self.play(
            FadeIn(badge4, shift=DOWN * 0.05),
            FadeIn(head4, shift=DOWN * 0.05),
            FadeIn(block4, shift=UP * 0.05),
            FadeIn(note4),
            segs[2].animate.set_fill(PANEL_EDGE),
            segs[3].animate.set_fill(CYAN),
            run_time=0.45,
        )

        # ===================================================================
        # PHASE 4 — the graph answers: discard left, retain right
        # ===================================================================
        self.play(
            bar_l.animate.set_color(MUTED).set_stroke(width=7),
            FadeOut(bar_glow_l),
            bar_r.animate.set_stroke(width=13),
            bar_glow_r.animate.set_stroke(width=30, opacity=0.42),
            dot_a.animate.set_fill(MUTED).set_opacity(0.7),
            FadeOut(la, shift=UP * 0.06),
            FadeOut(lb, shift=UP * 0.06),
            run_time=1.2,
        )

        disc_tag = txt("DISCARDED  [1, 1.5]", 18, MUTED)
        disc_tag.move_to([-4.75, -2.72, 0])
        keep_tag = txt("RETAINED  [1.5, 2]", 18, CYAN)
        keep_tag.move_to([-1.75, -2.72, 0])
        self.play(FadeIn(disc_tag), FadeIn(keep_tag), run_time=0.7)

        f2_lab = txt("f(2) = +4", 22, WHITE, {"+4": CYAN})
        f2_lab.move_to([-1.1, -0.62, 0])
        f2_lead = Line(
            [-1.12, -0.47, 0], [-1.46, 0.4, 0], color=CYAN, stroke_width=1.3
        )
        f2_lead.set_stroke(opacity=0.6)
        self.play(
            FadeIn(f2_lab, shift=DOWN * 0.04),
            Create(f2_lead),
            run_time=0.8,
        )
        self.wait(1.2)

        # the root sits just inside the retained half
        root_s = axes.c2p(1.52138, 0)
        pulse = Circle(radius=0.1, color=CYAN, stroke_width=2).move_to(root_s)
        self.play(GrowFromCenter(pulse), run_time=0.4)
        self.play(
            pulse.animate.scale(2.8).set_stroke(opacity=0),
            bar_glow_r.animate.set_stroke(width=36, opacity=0.55),
            run_time=0.8,
        )
        self.play(
            bar_glow_r.animate.set_stroke(width=30, opacity=0.42),
            run_time=0.6,
        )
        self.wait(3.0)

        # ===================================================================
        # Closing statement
        # ===================================================================
        closing = VGroup(
            txt("THE PROCESS REPEATS", 18, CYAN),
            txt("Repeat until the interval", 30, WHITE),
            txt("is sufficiently small.", 30, WHITE),
        ).arrange(DOWN, buff=0.3)
        closing.move_to([3.85, -0.45, 0])
        close_rule = Line(
            [2.25, 0.88, 0], [5.45, 0.88, 0], color=CYAN, stroke_width=3
        )
        close_divider = Line(
            [1.35, -1.65, 0], [6.35, -1.65, 0], color=PANEL_EDGE, stroke_width=1.2
        )
        close_divider.set_stroke(opacity=0.7)
        close_note = txt("Each pass halves the bracket.", 20, SECONDARY)
        close_note.move_to([3.85, -2.1, 0])

        self.play(
            FadeOut(
                VGroup(badge4, head4, block4, note4, segs, divider),
                shift=UP * 0.06,
            ),
            run_time=0.7,
        )
        self.play(Create(close_rule), Create(close_divider), run_time=0.5)
        self.play(
            FadeIn(closing, shift=UP * 0.08),
            FadeIn(close_note),
            run_time=0.9,
        )
        self.wait(6.0)

        self.play(FadeOut(Group(*self.mobjects), shift=UP * 0.3), run_time=1.2)
