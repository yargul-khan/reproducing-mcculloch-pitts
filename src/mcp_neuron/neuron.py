class Neuron:
    """
    A McCulloch-Pitts threshold neuron.

    A neuron has:
      - a threshold: how many excitatory inputs need to be active to fire
      - excitatory_inputs: a list of input names that push it toward firing
      - inhibitory_inputs: a list of input names that block it from firing
    """

    def __init__(self, name, threshold=1, excitatory_inputs=None, inhibitory_inputs=None):
        self.name = name
        self.threshold = threshold
        self.excitatory_inputs = excitatory_inputs or []
        self.inhibitory_inputs = inhibitory_inputs or []

    def fires(self, active_inputs):
        """
        active_inputs is a set of names that are currently active.
        Returns True if this neuron fires, otherwise False.
        """
        # Rule: if any inhibitory input is active, the neuron is blocked,
        # no matter what else is going on.
        for name in self.inhibitory_inputs:
            if name in active_inputs:
                return False

        # Count how many excitatory inputs are active.
        active_count = 0
        for name in self.excitatory_inputs:
            if name in active_inputs:
                active_count = active_count + 1

        # The neuron fires only if enough excitatory inputs were active.
        return active_count >= self.threshold
