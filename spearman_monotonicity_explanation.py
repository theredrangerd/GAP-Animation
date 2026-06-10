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
            x_range=[-1, 8], y_range=[-2, 20], x_length=10, y_length=6.2,
            x_label_text="Frequency of Mention as WINDIEST Location (Votes)",
            y_label_text="Frequency of Mention as COOLEST Location (Votes)",
            tick_step_y=2
        )
        raw_axes, raw_x_label, raw_y_label = raw_graph[0], raw_graph[1], raw_graph[2]

        # 5. Construct Rank Graph
        rank_graph = create_graph(
            x_range=[0, 10], y_range=[0, 10], x_length=10, y_length=6.2,
            x_label_text="Rank as WINDIEST Location",
            y_label_text="Rank as COOLEST Location",
            tick_step_y=1
        )
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
        
        # Clean up labels before side-by-side transition
        self.play(
            FadeOut(tent_plaza_rank_label),
            FadeOut(scene_title_rank),
            run_time=0.67
        )
        self.wait(1.0)

        # Phase 3: Scale down first graph to 25% and shift left
        left_graph = VGroup(rank_axes, dots, rank_x_label, rank_y_label)
        left_graph_title = Text("Actual Ranks", font_size=7, color=WHITE)
        left_graph_title.move_to(LEFT * 4.5 + UP * 1.2)

        self.play(
            left_graph.animate.scale(0.25).move_to(LEFT * 4.5),
            FadeIn(left_graph_title),
            run_time=1.0
        )
        self.wait(2.0)

        # Phase 4: Construct Right Graph for Monotonicity (75% size)
        mono_graph = create_graph(
            x_range=[0, 10], y_range=[0, 10], x_length=7.5, y_length=4.65,
            x_label_text="Rank as WINDIEST Location",
            y_label_text="Rank as COOLEST Location",
            tick_font_size=9, label_font_size=12,
            tick_buff_x=0.12, tick_buff_y=0.12,
            tick_step_y=1
        )
        mono_graph.move_to(RIGHT * 2.0)
        mono_axes = mono_graph[0]

        right_graph_title = Text("Hypothetical Perfect Monotonicity", font_size=21, color=WHITE)
        right_graph_title.move_to(RIGHT * 2.0 + UP * 2.8)

        self.play(
            Write(mono_graph),
            FadeIn(right_graph_title),
            run_time=1.0
        )
        self.wait(2.0)

        # Phase 5: Accelerated Diagonal Dot Plotting on the Right Graph
        mono_coords = [(i, i) for i in range(9, 0, -1)]  # (9,9) down to (1,1)
        mono_dots = VGroup(*[
            Dot(
                point=mono_axes.c2p(x, y),
                color=cream_color,
                radius=0.06,  # Matches the 75% scale right graph
                fill_opacity=0.9
            ) for x, y in mono_coords
        ])

        # Plot (9,9)
        tent_plaza_mono_label = Text("Tent Plaza", font_size=12, color=WHITE)
        tent_plaza_mono_label.next_to(mono_dots[0], DR, buff=0.1)

        self.play(
            GrowFromCenter(mono_dots[0]),
            FadeIn(tent_plaza_mono_label),
            run_time=0.4
        )
        self.wait(2.4)
        # Plot (8,8)
        self.play(GrowFromCenter(mono_dots[1]), run_time=0.4)
        self.wait(1.4)
        # Plot (7,7)
        self.play(GrowFromCenter(mono_dots[2]), run_time=0.27)
        self.wait(0.8)
        # Plot (6,6)
        self.play(GrowFromCenter(mono_dots[3]), run_time=0.27)
        self.wait(0.4)
        # Plot (5,5)
        self.play(GrowFromCenter(mono_dots[4]), run_time=0.27)
        self.wait(0.4)
        # Plot (4,4)
        self.play(GrowFromCenter(mono_dots[5]), run_time=0.27)
        self.wait(0.2)
        # Plot (3,3)
        self.play(GrowFromCenter(mono_dots[6]), run_time=0.27)
        self.wait(0.2)
        # Plot (2,2)
        self.play(GrowFromCenter(mono_dots[7]), run_time=0.27)
        self.wait(0.2)
        # Plot (1,1)
        self.play(GrowFromCenter(mono_dots[8]), run_time=0.27)
        self.wait(0.2)

        # Draw the perfect monotonicity line (electric cyan) on the 75% graph
        perfect_line = mono_axes.plot(
            lambda x: x,
            x_range=[0, 10],
            color="#00FFFF",  # Electric Cyan
            stroke_width=3
        )
        self.play(Create(perfect_line), run_time=1.33)
        self.wait(0.5)

        # Phase 6: Transition to 50/50 and Draw Monotonicity Line
        # We group the right graph elements (mono_graph, mono_dots, tent_plaza_mono_label, perfect_line) to scale down to 50%
        right_graph_group = VGroup(mono_graph, mono_dots, tent_plaza_mono_label, perfect_line)
        
        perfect_mono_highlight = Text("Perfect Monotonicity", font_size=14, color="#00FFFF")
        perfect_mono_highlight.move_to(RIGHT * 3.5 + UP * 2.3)

        # 6.1 Animate graphs returning to symmetric 50/50 layouts
        self.play(
            left_graph.animate.scale(2.0).move_to(LEFT * 3.5),
            left_graph_title.animate.scale(2.0).move_to(LEFT * 3.5 + UP * 2.3),
            right_graph_group.animate.scale(2/3).move_to(RIGHT * 3.5),
            ReplacementTransform(right_graph_title, perfect_mono_highlight),
            run_time=2.67
        )
        self.wait(1.0)

        # 6.2 Draw OLS line on the left graph
        ols_line = rank_axes.plot(
            lambda x: 0.0345 * (x - 5) + 5,
            x_range=[0, 10],
            color=ManimColor("#FFB300"),  # Amber
            stroke_width=3
        )

        ols_label = Text("Slope = 0.0345", font_size=10, color=ManimColor("#FFB300"))
        ols_label.next_to(ols_line, UP, buff=0.1)

        self.play(
            Create(ols_line),
            FadeIn(ols_label),
            run_time=2.67
        )
        self.wait(2.0)

        # 6.3 Draw the Spearman's Rho values beneath both graphs
        left_rho_lbl = Text("Spearman's Rho = 0.014", font_size=12, color=WHITE)
        left_rho_lbl.next_to(left_graph, DOWN, buff=0.3)

        right_rho_lbl = Text("Spearman's Rho = 1.0000", font_size=12, color=WHITE)
        right_rho_lbl.next_to(right_graph_group, DOWN, buff=0.3)
        right_rho_lbl.align_to(left_rho_lbl, DOWN)

        self.play(
            FadeIn(left_rho_lbl),
            FadeIn(right_rho_lbl),
            run_time=1.33
        )
        self.wait(5.0)

        # Phase 7: Outro (Fade out to black)
        self.play(
            FadeOut(left_graph),
            FadeOut(left_graph_title),
            FadeOut(mono_graph),
            FadeOut(mono_dots),
            FadeOut(perfect_line),
            FadeOut(perfect_mono_highlight),
            FadeOut(ols_line),
            FadeOut(ols_label),
            FadeOut(tent_plaza_mono_label),
            FadeOut(left_rho_lbl),
            FadeOut(right_rho_lbl),
            run_time=2.0
        )
        self.wait(1.0)
