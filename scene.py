from manim import *
import rce_lib as rce
import json
import pandas as pd


def get_data():
    with open('data.json') as f:
        return json.load(f)

def get_neuron_color(expected):
    colors = [BLACK, RED, BLUE]
    return colors[expected]


class RceNetworkCreation(Scene):
    def __init__(self):
        super().__init__()
        self.axes = Axes(x_range=[-3, 8], y_range=[-2, 4], x_length=11, y_length=6).add_coordinates()
        self.origin = self.axes.get_origin()
        self.neuron_radiuses = pd.DataFrame(columns=['x', 'y', 'radius'])

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
        rce_problem.start()
        self.wait()

    def add_points(self, points):
        dots = [Dot(coordinates) for coordinates in points]
        for d in dots:
            self.add(d)

    def add_neuron(self, neuron, expected):
        neuron_color = get_neuron_color(expected)
        # Get poit according to axes coordination
        point = self.axes.coords_to_point(neuron.x, neuron.y)

        # Add point representing middle of a neuron
        dot_point = Dot(point=point, radius=0.12, color=neuron_color)
        self.add(dot_point)

        # Add radius around a neuron
        neuron_radius = Dot(point=point, radius=neuron.radius, stroke_width=1.3, color=neuron_color,
                            fill_color=neuron_color, fill_opacity=0.08)
        neuron_record = {'x': neuron.x, 'y': neuron.y, 'radius': neuron_radius}
        self.neuron_radiuses.loc[len(self.neuron_radiuses)] = neuron_record
        # neuron_radius.set_fill(neuron_color, opacity=0.08)  # set the color and transparency
        self.add(neuron_radius)  # show the circle on screen

    def shrink_neuron_radius(self, neuron, expected):

        pass


animation = RceNetworkCreation()
animation.construct()
