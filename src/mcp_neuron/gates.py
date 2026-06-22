"""
mcp_neuron.gates
=================

Canonical threshold-logic constructions corresponding to Theorem II of
McCulloch & Pitts (1943): "Every TPE is realizable by a net of order
zero." That is, for each basic Boolean connective, a single MCP neuron
computes it.

Each helper below adds one neuron to the given Net, wired so that the
neuron's output at time t equals the corresponding Boolean expression of
its inputs at time t-1 (one synaptic delay).
"""
from .network import Net
from .neuron import Neuron


def make_or(net: Net, name: str, a: str, b: str) -> Neuron:
    """output(t) = a(t-1) OR b(t-1).

    A threshold of 1 over two excitatory synapses: either input alone is
    enough to fire.
    """
    return net.add_neuron(Neuron(name, threshold=1, excitatory_inputs=(a, b)))


def make_and(net: Net, name: str, a: str, b: str) -> Neuron:
    """output(t) = a(t-1) AND b(t-1).

    Per the paper: a neuron with two excitatory synapses needs both
    active within the same time step to cross a threshold of 2.
    """
    return net.add_neuron(Neuron(name, threshold=2, excitatory_inputs=(a, b)))


def make_and_not(net: Net, name: str, a: str, b: str) -> Neuron:
    """output(t) = a(t-1) AND NOT b(t-1).

    Uses an absolute inhibitory synapse from `b` (Assumption 4): any
    activity from b vetoes firing outright, regardless of a. This is the
    construction the paper relies on wherever a "but not" condition
    appears (e.g. the heat/cold example).

    Note: a standalone NOT(a), with no other condition, would require a
    constant "tonic" afferent to invert against - the paper does not
    introduce one, so it is not modeled here.
    """
    return net.add_neuron(
        Neuron(name, threshold=1, excitatory_inputs=(a,), inhibitory_inputs=(b,))
    )
