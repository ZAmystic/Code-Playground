from manim import *
import numpy as np

class Waves(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(x_range=[0, 12], y_range=[-6, 6], z_range=[-6, 6])
        axes.rotate(-90 * DEGREES, axis=RIGHT)
        self.set_camera_orientation(phi=70 * DEGREES, theta=-140 * DEGREES, zoom=0.6)

        x_label = Text("x", font_size=24).move_to(axes.coords_to_point(12, 0, 0) + RIGHT)
        y_label = Text("y", font_size=24).move_to(axes.coords_to_point(0, 6, 0) + OUT)
        z_label = Text("z", font_size=24).move_to(axes.coords_to_point(0, 0, 6) + UP)
        for label in [x_label, y_label, z_label]:
            label.always_face_camera = True

        vt = ValueTracker(0)

        graph = always_redraw(lambda: axes.plot(
            lambda x: (
                np.sin(x)
                + np.cos(x * 0.737)
                + np.sin(x / 2)
                + np.sin(x / 0.69)
                + np.cos(x / 1.2)
                + np.sin(x / 0.335)
                + np.sin(x / 0.913)
                + np.cos(x / 1.3911)
                + np.sin(x / 0.81)
                + np.sin(x / 0.9 + vt.get_value())
            ),
            color=WHITE,
            stroke_width=2
        ))

        gradient_colors = color_gradient([BLUE, PURPLE, RED], 10)

        components = VGroup(*[
            always_redraw(lambda i=i: axes.plot(
                lambda x: np.sin(x / (0.5 + i * 0.1) + vt.get_value()) * (1 + i * 0.2),
                color=gradient_colors[i],
                stroke_width=1.5
            )) for i in range(10)
        ])

        self.add(axes, x_label, y_label, z_label, graph)

        self.play(vt.animate.set_value(-30), run_time=4, rate_func=linear)
        self.wait(0.5)

        self.play(ReplacementTransform(graph, components))
        self.wait(0.5)

        self.play(vt.animate.set_value(-60), run_time=8, rate_func=linear)

        vt.set_value(-60)
        updater = lambda m, dt: m.increment_value(-0.5 * dt)
        vt.add_updater(updater)

        self.move_camera(theta=-100 * DEGREES, run_time=4)

        vt.remove_updater(updater)

        self.wait(3)
