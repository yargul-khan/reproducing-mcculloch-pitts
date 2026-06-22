from .neuron import Neuron


class Net:
    """
    A Net is a group of neurons wired together. It runs step by step:
    at each time step, every neuron looks at who was active one step
    before, and decides whether to fire.
    """

    def __init__(self):
        self.neurons = {}

    def add_neuron(self, neuron):
        self.neurons[neuron.name] = neuron
        return neuron

    def add_delay_chain(self, source, length, prefix):
        """
        Builds a chain of "pass-through" neurons. Each one just repeats
        whatever its input did, one step later. Chaining several of
        them creates a longer delay (2 steps, 3 steps, and so on).
        """
        names = []
        previous = source
        for i in range(1, length + 1):
            name = prefix + str(i)
            self.add_neuron(Neuron(name, threshold=1, excitatory_inputs=[previous]))
            names.append(name)
            previous = name
        return names

    def simulate(self, steps, external):
        """
        Runs the net for a number of time steps.

        steps: how many time steps to simulate
        external: a dictionary like {"A": [True, False, True]} giving
                  the activity of any inputs that come from outside
                  the net (not computed by a neuron)

        Returns a dictionary: each neuron's name maps to a list of
        True/False values, one per time step (starting at t=0).
        """
        history = {}
        for name in self.neurons:
            history[name] = [False]  # everything starts off at t=0

        for t in range(1, steps + 1):
            # Build the set of everything that was active at the
            # previous time step.
            active_before = set()

            for name in self.neurons:
                if history[name][t - 1]:
                    active_before.add(name)

            for name in external:
                sequence = external[name]
                if t - 1 < len(sequence) and sequence[t - 1]:
                    active_before.add(name)

            # Now decide who fires at this step, based on who was
            # active a moment ago.
            for name in self.neurons:
                neuron = self.neurons[name]
                fired = neuron.fires(active_before)
                history[name].append(fired)

        return history
