from .neuron import Neuron


def make_or(net, name, a, b):
    """Creates a neuron that fires if 'a' OR 'b' was active."""
    return net.add_neuron(Neuron(name, threshold=1, excitatory_inputs=[a, b]))


def make_and(net, name, a, b):
    """Creates a neuron that fires only if BOTH 'a' AND 'b' were active."""
    return net.add_neuron(Neuron(name, threshold=2, excitatory_inputs=[a, b]))


def make_and_not(net, name, a, b):
    """Creates a neuron that fires if 'a' was active AND 'b' was NOT active."""
    return net.add_neuron(
        Neuron(name, threshold=1, excitatory_inputs=[a], inhibitory_inputs=[b])
    )
