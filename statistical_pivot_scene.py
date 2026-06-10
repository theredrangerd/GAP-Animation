from manim import *

class StatisticalPivotScene(MovingCameraScene):
    def construct(self):
        # 1. Canvas Styling (Matte Charcoal Background)
        self.camera.background_color = "#151515"

        # 2. Coordinate System Layout
        # Grid settings for 16:9 viewport
        axes = NumberPlane(
            x_range=[-1, 8, 1],
            y_range=[-2, 20, 2],
            x_length=10,
            y_length=6.2,
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.25
            },
            axis_config={
                "stroke_color": WHITE,
                "stroke_width": 1.5,
                "include_ticks": True,
                "include_tip": False,
            }
        )

        # Custom coordinate labels to avoid system LaTeX dependencies
        coord_labels = VGroup()
        for x in range(-1, 9):
            if x == 0:
                continue
            lbl = Text(str(x), font_size=12, color=WHITE)
            lbl.next_to(axes.c2p(x, 0), DOWN, buff=0.15)
            coord_labels.add(lbl)

        for y in range(-2, 22, 2):
            if y == 0:
                continue
            lbl = Text(str(y), font_size=12, color=WHITE)
            lbl.next_to(axes.c2p(0, y), LEFT, buff=0.15)
            coord_labels.add(lbl)

        origin_lbl = Text("0", font_size=12, color=WHITE)
        origin_lbl.next_to(axes.c2p(0, 0), DL, buff=0.1)
        coord_labels.add(origin_lbl)
        axes.add(coord_labels)

        # Axis title labels (Wind vs Coolness)
        x_label = Text("Frequency of Mention as WINDIEST Location (Votes)", font_size=16, color=WHITE).next_to(
            axes.x_axis, DOWN, buff=0.5
        )
        y_label = Text("Frequency of Mention as COOLEST Location (Votes)", font_size=16, color=WHITE).rotate(PI / 2).next_to(
            axes.y_axis, LEFT, buff=0.6
        )

        # 3. Data Points Definition
        base_coords = [
            (3, 2), (0, 3), (2, 1), (2, 1), (0, 2), (0, 2), (1, 1), (2, 0)
        ]
        
        # Soft cream pastel dots for base dataset
        cream_color = "#EFEBE9"
        base_dots = VGroup(*[
            Dot(
                point=axes.c2p(x, y),
                color=cream_color,
                radius=0.08,
                fill_opacity=0.9
            )
            for x, y in base_coords
        ])

        # Outlier (Tent Plaza) setup
        outlier_coords = (6, 17)
        neon_crimson = "#FF3366"
        
        outlier_dot = Dot(
            point=axes.c2p(*outlier_coords),
            color=neon_crimson,
            radius=0.12,
            fill_opacity=1.0
        )
        
        # Pulsing halo glow around the outlier
        halo = Dot(
            point=axes.c2p(*outlier_coords),
            color=neon_crimson,
            radius=0.25,
            fill_opacity=0.25
        )
        
        outlier_label = Text("Tent Plaza\n(Outlier)", font_size=14, color=neon_crimson).next_to(
            outlier_dot, DR, buff=0.15
        )

        # 4. Dynamic Regression Setup
        color_1 = ManimColor("#00FFFF")  # Electric Cyan
        color_2 = ManimColor("#FFBF00")  # Electric Amber/Gold
        
        pivot_tracker = ValueTracker(0.0)
        
        # Regression function interpolator
        def get_regression_y(x, val):
            # Model 1: y = 2.079 * x - 0.474
            # Model 2: y = -0.421 * x + 2.026
            return (1 - val) * (2.079 * x - 0.474) + val * (-0.421 * x + 2.026)

        # Dynamic regression line
        regression_line = always_redraw(
            lambda: axes.plot(
                lambda x: get_regression_y(x, pivot_tracker.get_value()),
                x_range=[-0.5, 7.5],
                color=interpolate_color(color_1, color_2, pivot_tracker.get_value()),
                stroke_width=5
            )
        )



        # Labels for the regression models (positioned at x = 1.5 for visibility inside the zoomed-in frame)
        line_1_label = Text("Slope = +2.08", font_size=12, color=color_1).next_to(
            axes.c2p(1.5, 2.64), UP + RIGHT, buff=0.15
        )
        line_2_label = Text("Slope = -0.42", font_size=12, color=color_2).next_to(
            axes.c2p(1.5, 1.39), UP + RIGHT, buff=0.15
        )

        # Titles for the graphs
        title_1 = Text(
            "Frequency of a place mentioned as coolest on campus vs its frequency mentioned as windiest on campus.",
            font_size=16,
            color=WHITE
        )
        title_1.scale_to_fit_width(12)
        title_1.to_edge(UP, buff=0.15)

        title_zoomed_1 = Text(
            "Zoomed View: Coolest vs Windiest",
            font_size=12,
            color=WHITE
        ).move_to(axes.c2p(1.5, 6.3))

        title_zoomed_2 = Text(
            "Zoomed View: Coolest vs Windiest (Outlier Removed)",
            font_size=12,
            color=WHITE
        ).move_to(axes.c2p(1.5, 6.3))

        # Dynamic R² label that transitions value and font size
        r2_pos = VectorizedPoint(axes.get_top() + UP * 0.25)
        
        def get_r2_text():
            val = pivot_tracker.get_value()
            y_curr = r2_pos.get_center()[1]
            y_init = (axes.get_top() + UP * 0.25)[1]
            y_final = axes.c2p(0, 4.8)[1]
            
            # Interpolate font size from 20 down to 14 as it moves
            if y_init - y_final != 0:
                alpha = max(0.0, min(1.0, (y_init - y_curr) / (y_init - y_final)))
            else:
                alpha = 0.0
            fs = 20 - 6 * alpha
            
            return Text(
                f"R² = {(1 - val) * 0.705 + val * 0.281:.3f}",
                font_size=fs,
                color=interpolate_color(color_1, color_2, val)
            ).move_to(r2_pos.get_center())
            
        r2_text = always_redraw(get_r2_text)

        # --- ANIMATION CHOREOGRAPHY ---

        # Phase 1: Coordinate plane constructs itself
        self.play(Write(axes), run_time=1.5)
        self.play(FadeIn(x_label), FadeIn(y_label), FadeIn(title_1), run_time=0.5)
        self.wait(0.5)

        # Phase 2: Data points scale into existence
        self.play(
            AnimationGroup(*[
                GrowFromCenter(dot) for dot in base_dots
            ], lag_ratio=0.1),
            run_time=1.5
        )
        self.wait(0.5)

        # Phase 3: Outlier and label appear
        self.play(GrowFromCenter(outlier_dot), FadeIn(outlier_label), run_time=0.8)
        self.play(FadeIn(halo), run_time=0.4)
        
        # Halo pulsing effect
        self.play(
            halo.animate.scale(1.6).set_opacity(0.0),
            run_time=1.0,
            rate_func=linear
        )
        self.wait(0.8)

        # Phase 3.5: Show initial regression line and R² label
        self.play(
            FadeIn(regression_line),
            FadeIn(line_1_label),
            FadeIn(r2_text),
            run_time=1.5
        )
        self.wait(2.0)  # Hold to establish initial equilibrium

        # Phase 4: Smooth Camera Zoom-in
        self.play(
            self.camera.frame.animate.move_to(axes.c2p(1.5, 1.5)).set(width=6.0),
            r2_pos.animate.move_to(axes.c2p(1.5, 4.8)),
            x_label.animate.scale(0.65).move_to(axes.c2p(1.5, -1.1)),
            y_label.animate.scale(0.65).move_to(axes.c2p(-0.7, 1.5)),
            ReplacementTransform(title_1, title_zoomed_1),
            run_time=2.5
        )
        self.wait(1.0)

        # Phase 5: Systemic Pivot (inside the zoomed frame)
        self.play(
            FadeOut(outlier_dot),
            FadeOut(halo),
            FadeOut(outlier_label),
            pivot_tracker.animate.set_value(1.0),
            ReplacementTransform(line_1_label, line_2_label),
            ReplacementTransform(title_zoomed_1, title_zoomed_2),
            run_time=3.0
        )
        self.wait(2.0)

        # Phase 6: Outro (Fade out to black)
        self.play(
            FadeOut(axes),
            FadeOut(base_dots),
            FadeOut(regression_line),
            FadeOut(line_2_label),
            FadeOut(r2_text),
            FadeOut(title_zoomed_2),
            run_time=1.5
        )
        self.wait(0.5)
