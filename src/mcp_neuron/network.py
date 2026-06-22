"""
mcp_neuron.network
===================

Discrete-time simulation of a McCulloch-Pitts network (a "net" in the
paper's terminology).

Every synapse introduces exactly one unit of delay (Assumption 3), so the
firing pattern of a net at time t is fully determined by which neurons -
internal or peripheral afferents - were active at time t-1.
"""
from typing import Dict, List, Sequence, Set

from .neuron import Neuron


class Net:
    """A directed graph of McCulloch-Pitts neurons, simulated step by step."""

    def __init__(self) -> None:
        self.neurons: Dict[str, Neuron] = {}

    def add_neuron(self, neuron: Neuron) -> Neuron:
        """Register a neuron in this net. Returns the neuron for chaining."""
        if neuron.name in self.neurons:
            raise ValueError(f"Neuron '{neuron.name}' already exists in this net.")
        self.neurons[neuron.name] = neuron
        return neuron

    def add_delay_chain(self, source: str, length: int, prefix: str) -> List[str]:
        """Build a chain of pass-through neurons, each adding exactly one
        synaptic delay, mirroring the delay elements in the paper's
        Figure 1a.

        Returns the names of the chain, in order, so that ``chain[k-1]``
        fires at time t whenever ``source`` fired at time t-k.
        """
        names: List[str] = []
        previous = source
        for i in range(1, length + 1):
            name = f"{prefix}{i}"
            self.add_neuron(Neuron(name, threshold=1, excitatory_inputs=(previous,)))
            names.append(name)
            previous = name
        return names

    def simulate(
        self, steps: int, external: Dict[str, Sequence[bool]]
    ) -> Dict[str, List[bool]]:
        """Run the net for ``steps`` discrete time steps.

        Parameters
        ----------
        steps:
            Number of time steps to simulate (produces steps+1 values per
            neuron, including t=0).
        external:
            Mapping of peripheral-afferent name -> activity sequence (one
            bool per time step, indexed 0..steps-1, representing that
            afferent's activity at each step).

        Returns
        -------
        A mapping of every internal neuron's name to its activity history,
        one bool per time step (t=0 .. t=steps). Internal neurons are
        assumed inactive at t=0.
        """
        history: Dict[str, List[bool]] = {name: [False] for name in self.neurons}

        for t in range(1, steps + 1):
            active_prev: Set[str] = set()
            for name in self.neurons:
                if history[name][t - 1]:
                    active_prev.add(name)
            for name, sequence in external.items():
                if t - 1 < len(sequence) and sequence[t - 1]:
                    active_prev.add(name)

            for name, neuron in self.neurons.items():
                history[name].append(neuron.fires(active_prev))

        return history
