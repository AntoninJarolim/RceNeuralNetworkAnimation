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
        self.correct_point_appears = Events()
        self.blink_incorrect_neuron = Events()

        # alg initialization
        self.neurons = []

    def start(self):
        modification = True
        while modification:
            modification = False
            for coordinates, expected in zip(self.points, self.expected_values):
                x, y = coordinates[0], coordinates[1]
                if len(self.neurons) == 0:
                    self.create_neuron(coordinates, expected)
                    continue

                point_belongs_somewhere = False
                for neuron in self.neurons:
                    if neuron.contains(coordinates):
                        point_belongs_somewhere = True
                        if neuron.representing_class == expected:
                            # Neuron is correctly classing examined value
                            self.correct_point_appears.on_change(x, y, expected)
                        else:
                            # Neuron does not correctly classify, shrinking needed
                            self.blink_incorrect_neuron.on_change(x, y, expected)
                            neuron.radius = neuron.radius / 2
                            self.shrink_neuron_radius.on_change(neuron)
                            modification = True

                # Point is not inside any neuron, new neuron needed
                if point_belongs_somewhere is False:
                    self.create_neuron(coordinates, expected)
                    modification = True

    def create_neuron(self, coordinates, expected):
        neuron = RceNeuron(coordinates, expected)
        self.neurons.append(neuron)
        self.create_neuron_event.on_change(neuron, expected)
