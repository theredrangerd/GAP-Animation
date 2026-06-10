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

        # 4. Regression Lines and Labels
        # Model 1 (With Outlier): y = 2.079 * x - 0.474
        line_1 = axes.plot(
            lambda x: 2.079 * x - 0.474,
            x_range=[-0.5, 7.5],
            color="#00FFFF",  # Electric Cyan
            stroke_width=5
        )
        
        line_1_label = Text("Initial OLS (Slope = +2.08)", font_size=14, color="#00FFFF").next_to(
            axes.c2p(4, 2.079 * 4 - 0.474), UP + LEFT, buff=0.15
        )

        # Model 2 (Corrected): y = -0.421 * x + 2.026
        line_2 = axes.plot(
            lambda x: -0.421 * x + 2.026,
            x_range=[-0.5, 7.5],
            color="#FFBF00",  # Electric Amber/Gold
            stroke_width=5
        )
        
        line_2_label = Text("Corrected OLS (Slope = -0.42)", font_size=14, color="#FFBF00").next_to(
            axes.c2p(1.5, -0.421 * 1.5 + 2.026), UP + RIGHT, buff=0.2
        )

        # Titles for the graphs
        title_1 = Text(
            "Frequency of a place mentioned as coolest on campus vs its frequency mentioned as windiest on campus.",
            font_size=16,
            color=WHITE
        )
        title_1.scale_to_fit_width(12)
        title_1.to_edge(UP, buff=0.15)

        title_2 = Text(
            "Frequency of a place mentioned as coolest on campus vs its frequency mentioned as windiest on campus(nonoutlier)",
            font_size=16,
            color=WHITE
        )
        title_2.scale_to_fit_width(12)
        title_2.to_edge(UP, buff=0.15)

        # R² Correlation Value Labels
        r2_label_1 = Text("R² = 0.705", font_size=20, color="#00FFFF").next_to(axes, UP, buff=0.15)
        r2_label_2 = Text("R² = 0.281", font_size=20, color="#FFBF00").next_to(axes, UP, buff=0.15)

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

        # Phase 4: Initial positive trendline sweeps on-screen
        self.play(Create(line_1), run_time=1.5)
        self.play(FadeIn(line_1_label), FadeIn(r2_label_1), run_time=0.5)
        self.wait(2.0)  # Hold to establish initial equilibrium

        # Phase 5: Systemic Pivot (Simultaneous Outlier Removal & Trendline Transform)
        self.play(
            FadeOut(outlier_dot),
            FadeOut(halo),
            FadeOut(outlier_label),
            ReplacementTransform(line_1, line_2),
            ReplacementTransform(line_1_label, line_2_label),
            ReplacementTransform(r2_label_1, r2_label_2),
            ReplacementTransform(title_1, title_2),
            run_time=3.0
        )
        self.wait(1.0)  # Short hold on corrected model

        # Phase 5.5: Camera Zoom-in
        self.play(
            self.camera.frame.animate.move_to(axes.c2p(1.5, 1.5)).set(width=6.0),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(r2_label_2),
            FadeOut(title_2),
            run_time=2.5
        )
        self.wait(0.5)

        # Phase 5.6: Show R² value above the zoomed-in dots
        r2_label_zoomed = Text("R² = 0.281", font_size=16, color="#FFBF00").move_to(
            axes.c2p(1.5, 4.0)
        )
        self.play(FadeIn(r2_label_zoomed), run_time=0.8)
        self.wait(1.5)

        # Phase 6: Outro (Fade out to black)
        self.play(
            FadeOut(axes),
            FadeOut(base_dots),
            FadeOut(line_2),
            FadeOut(line_2_label),
            FadeOut(r2_label_zoomed),
            run_time=1.5
        )
        self.wait(0.5)
