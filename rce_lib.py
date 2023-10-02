import numpy as np
from events import Events


class RceNeuron:
    def __init__(self, coordinates, representing_class):
        self.radius = 3
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.coordinates = np.array(coordinates)
        self.representing_class = representing_class

    def contains(self, coords):
        # calculating Euclidean distance
        distance = np.linalg.norm(self.coordinates - np.array(coords))
        return distance < self.radius


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
            if len(self.neurons) == 0:
                self.create_neuron(coordinates, expected)
                continue

            for neuron in self.neurons:
                if neuron.contains(coordinates):
                    if neuron.representing_class == expected:
                        # Neuron is correctly classing examined value
                        pass
                    else:
                        # Neuron does not correctly classify, shrinking needed
                        self.shrink_neuron_radius.on_change(neuron, expected)
                else:
                    # Point is not inside any neuron, new neuron needed
                    self.create_neuron(coordinates, expected)
    def create_neuron(self, coordinates, expected):
        neuron = RceNeuron(coordinates, expected)
        self.neurons.append(neuron)
        self.create_neuron_event.on_change(neuron, expected)
