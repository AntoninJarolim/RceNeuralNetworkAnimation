import numpy as np
from events import Events


class RceNeuron:
    def __init__(self, coordinates):
        self.radius = 3
        self.coordinates = np.array(coordinates)


class RceNeuralNetwork:
    def __init__(self, data):
        # data initialization
        self.data = data
        self.points = [point["coordinates"] for point in self.data]
        self.expected_values = [point["expected"] for point in self.data]

        # events initialization
        self.create_neuron_event = Events()
        self.shrink_neuron_radius = Events()

        # alg initialization
        self.neurons = []

    def start(self):
        for coordinates, expected in zip(self.points, self.expected_values):
            neuron = RceNeuron(coordinates)
            self.create_neuron_event.on_change(neuron, expected)
