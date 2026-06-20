from manim import *

class SpearmanMonotonicityExplanation(MovingCameraScene):
    def construct(self):
        # 1. Canvas Styling (Matte Charcoal Background)
        self.camera.background_color = "#151515"

        # 2. Coordinates Setup
        raw_coords = [
            (3, 2), (0, 3), (2, 1), (2, 1), (0, 2), (0, 2), (1, 1), (2, 0), (6, 17)
        ]
        rank_coords = [
            (8, 6), (2, 8), (6, 3), (6, 3), (2, 6), (2, 6), (4, 3), (6, 1), (9, 9)
        ]

        # Colors
        royal_blue = ManimColor("#4169E1")
        cream_color = ManimColor("#EFEBE9")

        # 3. Helper Function to Create Graphs
        def create_graph(
            x_range, y_range, x_length, y_length, 
            x_label_text, y_label_text, 
            tick_font_size=12, label_font_size=16, 
            tick_step_x=1, tick_step_y=1,
            tick_buff_x=0.15, tick_buff_y=0.15
        ):
            axes = NumberPlane(
                x_range=x_range,
                y_range=y_range,
                x_length=x_length,
                y_length=y_length,
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
            
            labels = VGroup()
            for x in range(int(x_range[0]), int(x_range[1]) + 1, tick_step_x):
                if x == 0:
                    continue
                lbl = Text(str(x), font_size=tick_font_size, color=WHITE)
                lbl.next_to(axes.c2p(x, 0), DOWN, buff=tick_buff_x)
                labels.add(lbl)
                
            for y in range(int(y_range[0]), int(y_range[1]) + 1, tick_step_y):
                if y == 0:
                    continue
                lbl = Text(str(y), font_size=tick_font_size, color=WHITE)
                lbl.next_to(axes.c2p(0, y), LEFT, buff=tick_buff_y)
                labels.add(lbl)
                
            origin_lbl = Text("0", font_size=tick_font_size, color=WHITE)
            origin_lbl.next_to(axes.c2p(0, 0), DL, buff=tick_buff_x * 0.7)
            labels.add(origin_lbl)
            axes.add(labels)
            
            x_lbl = Text(x_label_text, font_size=label_font_size, color=WHITE).next_to(
                axes.x_axis, DOWN, buff=x_length * 0.05
            )
            y_lbl = Text(y_label_text, font_size=label_font_size, color=WHITE).rotate(PI / 2).next_to(
                axes.y_axis, LEFT, buff=y_length * 0.1
            )
            
            return VGroup(axes, x_lbl, y_lbl)

        # 4. Construct Raw Graph
        raw_graph = create_graph(
            x_range=[-1, 8], y_range=[-2, 20], x_length=8.5, y_length=5.2,
            x_label_text="Frequency of Mention as WINDIEST Location (Votes)",
            y_label_text="Frequency of Mention as COOLEST Location (Votes)",
            tick_step_y=2
        )
        raw_graph.shift(UP * 0.3)
        raw_axes, raw_x_label, raw_y_label = raw_graph[0], raw_graph[1], raw_graph[2]

        # 5. Construct Rank Graph
        rank_graph = create_graph(
            x_range=[0, 10], y_range=[0, 10], x_length=8.5, y_length=5.2,
            x_label_text="Rank as WINDIEST Location",
            y_label_text="Rank as COOLEST Location",
            tick_step_y=1
        )
        rank_graph.shift(UP * 0.3)
        rank_axes, rank_x_label, rank_y_label = rank_graph[0], rank_graph[1], rank_graph[2]

        # 6. Data Dots Setup (Initial Royal Blue)
        dots = VGroup(*[
            Dot(
                point=raw_axes.c2p(x, y),
                color=royal_blue,
                radius=0.08,
                fill_opacity=0.9
            )
            for x, y in raw_coords
        ])

        tent_plaza_dot = dots[8]
        tent_plaza_label = Text("Tent Plaza\n(6, 17)", font_size=12, color=WHITE).next_to(
            tent_plaza_dot, DR, buff=0.15
        )

        scene_title = Text("Raw Vote Count", font_size=20, color=WHITE).to_edge(UP, buff=0.15)

        # --- ANIMATION CHOREOGRAPHY ---

        # Phase 1: Draw Raw Space
        self.play(Write(raw_axes), run_time=2.0)
        self.play(FadeIn(raw_x_label), FadeIn(raw_y_label), FadeIn(scene_title), run_time=0.67)
        
        self.play(
            AnimationGroup(*[
                GrowFromCenter(dot) for dot in dots
            ], lag_ratio=0.1),
            run_time=2.0
        )
        self.play(FadeIn(tent_plaza_label), run_time=0.67)
        self.wait(4.0)

        # Phase 2: Morph to Rank Space (Full screen)
        tent_plaza_rank_label = Text("Tent Plaza\nRank (9, 9)", font_size=12, color=cream_color)
        scene_title_rank = Text("Converted to Ranks", font_size=20, color=WHITE).to_edge(UP, buff=0.15)

        dot_animations = []
        for i, dot in enumerate(dots):
            target_point = rank_axes.c2p(*rank_coords[i])
            dot_animations.append(
                dot.animate.move_to(target_point).set_color(cream_color)
            )

        tent_plaza_rank_label.next_to(rank_axes.c2p(*rank_coords[8]), DR, buff=0.15)

        self.play(
            ReplacementTransform(raw_axes, rank_axes),
            ReplacementTransform(raw_x_label, rank_x_label),
            ReplacementTransform(raw_y_label, rank_y_label),
            ReplacementTransform(scene_title, scene_title_rank),
            ReplacementTransform(tent_plaza_label, tent_plaza_rank_label),
            *dot_animations,
            run_time=4.97
        )
        self.wait(4.0)
        
        # Phase 3: Draw the Trend Line and its label directly on the rank graph
        ols_line = rank_axes.plot(
            lambda x: 0.0345 * (x - 5) + 5,
            x_range=[0, 10],
            color=ManimColor("#FFB300"),  # Amber
            stroke_width=4
        )

        ols_label = Text("Trend Line of Sites Ranked", font_size=14, color=ManimColor("#FFB300"))
        ols_label.move_to(rank_axes.c2p(5, 5.6))

        self.play(
            Create(ols_line),
            FadeIn(ols_label),
            run_time=2.0
        )
        self.wait(1.5)

        # Phase 4: Draw the Spearman's Rho value at the bottom of the screen
        rho_label = Text("Spearman's Rank Correlation (Rho) = 0.014", font_size=16, color=WHITE)
        rho_label.to_edge(DOWN, buff=0.3)

        self.play(
            FadeIn(rho_label),
            run_time=1.5
        )
        self.wait(5.0)

        # Phase 5: Outro (Fade out to black)
        self.play(
            FadeOut(rank_graph),
            FadeOut(dots),
            FadeOut(tent_plaza_rank_label),
            FadeOut(scene_title_rank),
            FadeOut(ols_line),
            FadeOut(ols_label),
            FadeOut(rho_label),
            run_time=2.0
        )
        self.wait(1.0)
