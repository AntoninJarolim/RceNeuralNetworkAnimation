from manim import *
import rce_lib as rce
import json
import pandas as pd


def get_data():
    with open('data/data2.json') as f:
        return json.load(f)


def get_neuron_color(expected):
    colors = [BLACK, RED, BLUE, GREEN]
    return colors[expected]


class RceNetworkCreation(Scene):
    def __init__(self):
        super().__init__()
        self.axes = Axes(x_range=[-3, 8], y_range=[-2, 4], x_length=11, y_length=6).add_coordinates()
        self.origin = self.axes.get_origin()
        self.neuron_radiuses = pd.DataFrame(columns=['x', 'y', 'neuron'])
        self.points = []
        # circ = Circle(radius=0.5).move_to([-4, -1.5, 0])

    def construct(self):
        rce_data = get_data()

        self.add(self.axes)

        plane = NumberPlane(
            x_range=(-20, 20, 1),
            y_range=(-20, 20, 1),
        ).move_to(self.origin)
        self.add(plane)

        rce_problem = rce.RceNeuralNetwork(rce_data)
        rce_problem.create_neuron_event.on_change += self.add_neuron
        rce_problem.shrink_neuron_radius.on_change += self.shrink_neuron_radius
        rce_problem.correct_point_appears.on_change += self.correct_point_appears
        rce_problem.blink_incorrect_neuron.on_change += self.blink_incorrect_neuron

        rce_problem.start()

        self.wait(1)

    def add_points(self, points):
        dots = [Dot(coordinates) for coordinates in points]
        for d in dots:
            self.add(d)

    def add_neuron(self, neuron, expected):
        neuron_color = get_neuron_color(expected)
        # Get poit according to axes coordination
        point = self.axes.coords_to_point(neuron.x, neuron.y)

        # Add radius around a neuron
        neuron_dot = Dot(point=point, radius=neuron.radius, stroke_width=1.3, color=neuron_color,
                         fill_color=neuron_color, fill_opacity=0.08)
        neuron_record = {'x': neuron.x, 'y': neuron.y, 'neuron': neuron_dot}
        self.neuron_radiuses.loc[len(self.neuron_radiuses)] = neuron_record
        self.add(neuron_dot)  # show the circle on screen

        # Add point representing middle of a neuron
        dot_point = Dot(point=point, radius=0.12, color=neuron_color)
        self.add(dot_point)
        self.points.append(str(neuron.x) + str(neuron.y))
        self.wait(0.5)

    def shrink_neuron_radius(self, neuron):
        # select correct neuron radius
        row = self.neuron_radiuses[
            (self.neuron_radiuses['x'] == neuron.x) &
            (self.neuron_radiuses['y'] == neuron.y)
            ]
        neuron_dot = row.squeeze()
        neuron_radius = neuron_dot['neuron']

        # Create new neuron using old neuron
        new_radius = neuron_radius.radius / 2
        point = self.axes.coords_to_point(neuron.x, neuron.y)
        new_neuron = Dot(point=point, radius=new_radius, stroke_width=neuron_radius.stroke_width,
                         color=neuron_radius.color, fill_color=neuron_radius.fill_color,
                         fill_opacity=neuron_radius.fill_opacity)

        # Play transformation before removing neuron
        self.play(
            Transform(neuron_radius, new_neuron, replace_mobject_with_target_in_scene=True)
        )

        # Replace old neuron (drop one row, create new row, add new row to df)
        self.neuron_radiuses = self.neuron_radiuses.drop(row.index)
        neuron_record = {'x': neuron.x, 'y': neuron.y, 'neuron': new_neuron}
        self.neuron_radiuses = self.neuron_radiuses._append(neuron_record, ignore_index=True)

        self.wait(0.5)

    def correct_point_appears(self, x, y, expected):
        str_repr = str(x) + str(y)
        for point_str_repr in self.points:
            if point_str_repr == str_repr:
                return
        self.points.append(str_repr)

        neuron_color = get_neuron_color(expected)
        # Get poit according to axes coordination
        point = self.axes.coords_to_point(x, y)
        # Add point representing middle of a neuron
        dot_point = Dot(point=point, radius=0.12, color=neuron_color)
        self.add(dot_point)
        self.wait(duration=0.5)

    def blink_incorrect_neuron(self, x, y, expected):
        neuron_color = get_neuron_color(expected)
        # Get poit according to axes coordination
        point = self.axes.coords_to_point(x, y)
        point[2] = 36
        # Add point representing middle of a neuron

        for _ in range(3):
            dot_point = Dot(point=point, radius=0.16, color=neuron_color)
            self.add(dot_point)
            self.wait(duration=0.15)
            self.remove(dot_point)
            self.wait(duration=0.15)


if __name__ == "__main__":
    animation = RceNetworkCreation()
    animation.construct()
