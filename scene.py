from manim import *
import rce_lib as rce
import json

def get_data():
    with open('data.json') as f:
        return json.load(f)

def something_changed(reason):
    print("prdeeeeeeeeel")

class RceNetworkCreation(Scene):
    def construct(self):
        rce_data = get_data()

        plane = NumberPlane()
        self.add(plane)

        rce_problem = rce.RceNeuralNetwork(rce_data)
        rce_problem.create_neuron_event.on_change += self.add_neuron
        rce_problem.start()

    def add_points(self, points):
        dots = [Dot(coordinates) for coordinates in points]
        for d in dots:
            self.add(d)

    def add_neuron(self, neuron):
        print("sracka")
        circle = Circle().from_three_points(LEFT, LEFT + UP, UP * 2, color=RED)
        circle.set_fill(PINK, opacity=0.8)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen


animation = RceNetworkCreation()
animation.construct()
