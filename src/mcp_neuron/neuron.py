"""
mcp_neuron.neuron
==================

The McCulloch-Pitts threshold neuron.

Implements the unit described in:
    McCulloch, W.S. & Pitts, W. (1943). "A Logical Calculus of the Ideas
    Immanent in Nervous Activity." Bulletin of Mathematical Biophysics,
    5, 115-133.

This models the five physical assumptions on p.117-118 of the paper:
    1. The activity of the neuron is an "all-or-none" process.
    2. A fixed number of synapses (the threshold) must be excited within
       the period of latent addition to fire the neuron, independent of
       previous activity or position on the neuron.
    3. The only significant delay within the nervous system is synaptic
       delay (here: exactly one discrete time step per synapse).
    4. The activity of any inhibitory synapse absolutely prevents
       excitation of the neuron at that time.
    5. The structure of the net does not change with time.
"""
from dataclasses import dataclass, field
from typing import Set, Tuple


@dataclass
class Neuron:
    """A single McCulloch-Pitts threshold unit.

    Parameters
    ----------
    name:
        Unique identifier for this neuron within a Net.
    threshold:
        Minimum number of distinct active excitatory inputs required,
        within a single time step, to fire (Assumption 2).
    excitatory_inputs:
        Names of neurons (or peripheral afferents) whose firing
        contributes toward the threshold.
    inhibitory_inputs:
        Names of neurons (or peripheral afferents) whose firing
        absolutely blocks this neuron from firing, regardless of
        excitatory input (Assumption 4).
    """

    name: str
    threshold: int = 1
    excitatory_inputs: Tuple[str, ...] = field(default_factory=tuple)
    inhibitory_inputs: Tuple[str, ...] = field(default_factory=tuple)

    def fires(self, active_at_previous_step: Set[str]) -> bool:
        """Decide whether this neuron fires now, given which inputs were
        active exactly one synaptic delay ago.

        Per Assumption 4, a single active inhibitory input is an absolute
        veto, independent of how much excitatory input is present.
        """
        if any(name in active_at_previous_step for name in self.inhibitory_inputs):
            return False
        excited = sum(
            1 for name in self.excitatory_inputs if name in active_at_previous_step
        )
        return excited >= self.threshold
